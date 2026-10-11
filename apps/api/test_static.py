"""Swagger must work with collected local assets under strict production storage."""
import json
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from unittest.mock import patch

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.management import call_command
from django.test import Client, SimpleTestCase, override_settings
from django.urls import resolve
from whitenoise.storage import CompressedManifestStaticFilesStorage


class SwaggerAssetParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []
        self.inline_scripts = []
        self.anchors = []
        self.ids = set()
        self._inline_script = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if attributes.get("id"):
            self.ids.add(attributes["id"])
        if tag == "a" and attributes.get("href"):
            self.anchors.append(attributes["href"])
        if tag == "script":
            self._inline_script = [] if not attributes.get("src") else None
        if tag == "script" and attributes.get("src"):
            self.urls.append(attributes["src"])
        elif tag == "link" and attributes.get("rel") in {"stylesheet", "icon"}:
            self.urls.append(attributes["href"])

    def handle_data(self, data):
        if self._inline_script is not None:
            self._inline_script.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._inline_script is not None:
            self.inline_scripts.append("".join(self._inline_script))
            self._inline_script = None


class SwaggerManifestTests(SimpleTestCase):
    def setUp(self):
        static_root = tempfile.TemporaryDirectory(prefix="iz2-swagger-static-")
        self.addCleanup(static_root.cleanup)
        self.static_root = Path(static_root.name)
        settings = override_settings(
            DEBUG=False,
            STATIC_ROOT=self.static_root,
            WHITENOISE_AUTOREFRESH=False,
            WHITENOISE_USE_FINDERS=False,
            STORAGES={
                "default": {"BACKEND": "django.core.files.storage.InMemoryStorage"},
                "staticfiles": {
                    "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
                },
            },
        )
        settings.enable()
        self.addCleanup(settings.disable)

    def test_missing_sidecar_manifest_is_not_silently_served_from_finders(self):
        self.assertIsInstance(staticfiles_storage, CompressedManifestStaticFilesStorage)
        self.assertTrue(staticfiles_storage.manifest_strict)
        with self.assertRaisesRegex(ValueError, "Missing staticfiles manifest entry.*drf_spectacular_sidecar"):
            staticfiles_storage.url("drf_spectacular_sidecar/swagger-ui-dist/swagger-ui.css")
        response = Client().get("/api/v1/docs/")
        self.assertEqual(response.status_code, 500)

    def test_collected_swagger_schema_and_hashed_local_assets_are_served(self):
        call_command("collectstatic", interactive=False, verbosity=0)
        manifest = json.loads((self.static_root / "staticfiles.json").read_text(encoding="utf-8"))
        client = Client()
        with patch("apps.api.jobs.request_rebuild", side_effect=AssertionError("Docs started graph work")), patch(
            "apps.api.jobs.request_analysis", side_effect=AssertionError("Docs started analysis work")
        ):
            response = client.get("/api/v1/docs/")
        self.assertEqual(response.status_code, 200)
        assets = SwaggerAssetParser()
        assets.feed(response.content.decode())
        expected_paths = {
            "drf_spectacular_sidecar/swagger-ui-dist/swagger-ui.css",
            "drf_spectacular_sidecar/swagger-ui-dist/swagger-ui-bundle.js",
            "drf_spectacular_sidecar/swagger-ui-dist/swagger-ui-standalone-preset.js",
            "css/api-docs.css",
            "css/cosmic-background.css",
            "css/surface-spotlight.css",
            "js/api-docs.js",
            "js/api-atmosphere.js",
            "images/iz2-favicon.svg",
        }
        expected_urls = {"/static/" + manifest["paths"][path] for path in expected_paths}
        self.assertEqual(set(assets.urls), expected_urls)
        self.assertEqual(len(assets.urls), len(expected_urls))
        cosmic_url = "/static/" + manifest["paths"]["js/cosmic-scene.js"]
        self.assertContains(response, f'data-cosmic-module="{cosmic_url}"')
        assets.urls.append(cosmic_url)
        self.assertTemplateUsed(response, "api/docs.html")
        self.assertContains(response, "/static/" + manifest["paths"]["images/iz2-logo.png"])
        self.assertNotContains(response, "images/iz2.svg")
        self.assertTemplateUsed(response, "drf_spectacular/swagger_ui.js")
        bootstrap = "\n".join(assets.inline_scripts)
        self.assertEqual(bootstrap.count("const ui = SwaggerUIBundle("), 1)
        self.assertIn('url: "/api/v1/schema/"', bootstrap)
        self.assertIn('dom_id: "#swagger-ui"', bootstrap)
        self.assertIn("requestInterceptor,", bootstrap)
        self.assertIn("responseInterceptor,", bootstrap)
        self.assertIn('request.credentials === "same-origin"', bootstrap)
        self.assertRegex(bootstrap, r'(?i)request\.headers\["X-CSRFToken"\]')
        swagger_settings = json.loads(bootstrap.split("const swaggerSettings = ", 1)[1].split(";", 1)[0])
        self.assertIs(swagger_settings["filter"], True)
        self.assertIs(swagger_settings["deepLinking"], True)
        self.assertEqual(swagger_settings["docExpansion"], "none")
        self.assertIs(swagger_settings["persistAuthorization"], False)
        for option in ("requestInterceptor", "responseInterceptor", "withCredentials"):
            self.assertNotIn(option, swagger_settings)
        for href in assets.anchors:
            parsed = urlsplit(href)
            if not parsed.scheme and not parsed.netloc:
                if parsed.path:
                    # Validate navigation without loading domain-data API pages.
                    resolve(parsed.path)
                elif parsed.fragment:
                    self.assertIn(parsed.fragment, assets.ids)
        for url in assets.urls:
            parsed = urlsplit(url)
            self.assertEqual((parsed.scheme, parsed.netloc), ("", ""))
            self.assertRegex(parsed.path, r"\.[a-f0-9]{12}\.")
            with self.subTest(asset=url):
                asset = client.get(url)
                self.assertEqual(asset.status_code, 200)
                self.assertIn("immutable", asset["Cache-Control"])
                self.assertTrue(b"".join(asset.streaming_content))
                asset.close()
        schema = client.get("/api/v1/schema/", HTTP_ACCEPT="application/vnd.oai.openapi+json")
        self.assertEqual(schema.status_code, 200)
        self.assertIn("/api/v1/companies/", json.loads(schema.content)["paths"])


class BrandingAssetTests(SimpleTestCase):
    def test_original_png_and_runtime_copies_are_identical(self):
        import struct

        root = Path(settings.BASE_DIR)
        content = (root / "frontend/src/assets/branding/iz2-logo.png").read_bytes()
        self.assertEqual(content[:8], b"\x89PNG\r\n\x1a\n")
        self.assertEqual(struct.unpack(">IIBB", content[16:26]), (1254, 1254, 8, 6))
        for name in ("static/images/iz2-logo.png", "docs/assets/iz2-logo.png"):
            with self.subTest(asset=name):
                self.assertEqual(content, (root / name).read_bytes())
        favicon = (root / "frontend/src/assets/branding/iz2-favicon.svg").read_bytes()
        self.assertEqual(favicon, (root / "frontend/public/favicon.svg").read_bytes())
        self.assertEqual(favicon, (root / "static/images/iz2-favicon.svg").read_bytes())
