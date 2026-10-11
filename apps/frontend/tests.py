"""SPA integration checks without working data or a frontend development server."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from django.test import SimpleTestCase, override_settings


class FrontendServingTests(SimpleTestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.manifest = self.base / 'static/frontend/vite-manifest.json'
        self.manifest.parent.mkdir(parents=True)
        (self.base / 'collected').mkdir()
        self.override = override_settings(BASE_DIR=self.base, STATIC_ROOT=self.base / 'collected')
        self.override.enable()
        self.addCleanup(self.override.disable)

    def write_manifest(self, value):
        self.manifest.write_text(json.dumps(value), encoding='utf-8')

    def test_home_redirects_to_react_and_legacy_dashboard_is_retained(self):
        self.assertRedirects(self.client.get('/'), '/app/', fetch_redirect_response=False)
        from django.urls import reverse
        self.assertTrue(reverse('dashboard:index').startswith('/legacy/'))

    def test_missing_build_has_actionable_service_unavailable_response(self):
        response = self.client.get('/app/companies/42')
        self.assertEqual(response.status_code, 503)
        self.assertContains(response, 'collectstatic', status_code=503)

    def test_compiled_entry_is_served_on_deep_routes_without_bootstrap(self):
        self.write_manifest({'index.html': {'file': 'assets/main-abcd.js', 'css': ['assets/main-abcd.css']}})
        response = self.client.get('/app/companies/42')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '/static/frontend/assets/main-abcd.js')
        self.assertContains(response, '/static/frontend/assets/main-abcd.css')
        self.assertContains(response, 'id="root"')
        self.assertNotContains(response, 'bootstrap')
        self.assertEqual(response['Cache-Control'], 'no-cache')

    def test_corrupt_or_traversing_manifest_fails_closed(self):
        for entry in [None, {'file': '../private.js'}, {'file': '/assets/evil.js'}, {'file': 'assets/../../evil.js'}, {'file': 17}]:
            with self.subTest(entry=entry):
                self.write_manifest({'index.html': entry})
                self.assertEqual(self.client.get('/app/').status_code, 503)
        self.manifest.write_text('{invalid', encoding='utf-8')
        self.assertEqual(self.client.get('/app/').status_code, 503)

    def test_collected_manifest_takes_precedence_over_source_build(self):
        self.write_manifest({'index.html': {'file': 'assets/source.js'}})
        collected = self.base / 'collected/frontend/vite-manifest.json'
        collected.parent.mkdir(parents=True)
        collected.write_text(json.dumps({'index.html': {'file': 'assets/collected.js'}}), encoding='utf-8')
        response = self.client.get('/app/')
        self.assertContains(response, 'assets/collected.js')
        self.assertNotContains(response, 'assets/source.js')

    def test_entry_urls_keep_vite_hashes_under_manifest_storage(self):
        self.write_manifest({
            'index.html': {
                'file': 'assets/index-ABC123.js', 'css': ['assets/index-ABC123.css'],
                'imports': ['_heading.js'],
            },
            '_heading.js': {'file': 'assets/heading-DEF456.js', 'css': ['assets/heading-DEF456.css']},
        })
        mappings = {'frontend/assets/index-ABC123.js':'frontend/assets/index-ABC123.abcdef123456.js', 'frontend/assets/index-ABC123.css':'frontend/assets/index-ABC123.abcdef123456.css', 'frontend/assets/heading-DEF456.css':'frontend/assets/heading-DEF456.abcdef123456.css', 'frontend/favicon.svg':'frontend/favicon.abcdef123456.svg'}
        (self.base / 'collected/staticfiles.json').write_text(json.dumps({'version':'1.1','paths':mappings,'hash':'test'}),encoding='utf-8')
        with override_settings(STORAGES={'default':{'BACKEND':'django.core.files.storage.InMemoryStorage'},'staticfiles':{'BACKEND':'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'}}):
            response=self.client.get('/app/')
            self.assertContains(response, 'src="/static/frontend/assets/index-ABC123.js"')
            self.assertContains(response, 'href="/static/frontend/assets/index-ABC123.css"')
            self.assertContains(response, 'href="/static/frontend/assets/heading-DEF456.css"')
            self.assertNotContains(response, 'index-ABC123.abcdef123456')
            self.assertNotContains(response, 'heading-DEF456.abcdef123456')

    def test_static_chunk_styles_precede_entry_and_are_deduplicated(self):
        self.write_manifest({
            'index.html': {
                'file': 'assets/index.js',
                'imports': ['_heading.js', '_navigation.js', '_heading.js'],
                'css': ['assets/shared.css', 'assets/index.css'],
                'dynamicImports': ['missing-lazy-page.tsx'],
            },
            '_heading.js': {
                'file': 'assets/heading.js',
                'imports': ['_base.js'],
                'css': ['assets/heading.css'],
            },
            '_navigation.js': {
                'file': 'assets/navigation.js',
                'imports': ['_base.js'],
                'css': ['assets/shared.css', 'assets/navigation.css'],
            },
            '_base.js': {'file': 'assets/base.js', 'css': ['assets/shared.css']},
        })
        response = self.client.get('/app/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['entry_styles'], [
            '/static/frontend/assets/shared.css',
            '/static/frontend/assets/heading.css',
            '/static/frontend/assets/navigation.css',
            '/static/frontend/assets/index.css',
        ])
        self.assertContains(response, 'href="/static/frontend/assets/shared.css"', count=1)
        self.assertNotContains(response, 'missing-lazy-page')

    def test_static_chunk_cycles_finish_with_each_stylesheet_once(self):
        self.write_manifest({
            'index.html': {
                'file': 'assets/index.js', 'imports': ['_shared.js'],
                'css': ['assets/index.css'],
            },
            '_shared.js': {
                'file': 'assets/shared.js', 'imports': ['index.html', '_shared.js'],
                'css': ['assets/shared.css', 'assets/shared.css'],
            },
        })
        response = self.client.get('/app/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['entry_styles'], [
            '/static/frontend/assets/shared.css', '/static/frontend/assets/index.css',
        ])

    def test_missing_malformed_or_traversing_static_dependencies_fail_closed(self):
        invalid_chunks = [
            None, [], {}, {'file': 12}, {'file': '../private.js'},
            {'file': 'assets/%2e%2e/private.js'}, {'file': 'assets\\private.js'},
            {'file': 'assets/chunk.js', 'imports': '_nested.js'},
            {'file': 'assets/chunk.js', 'imports': [None]},
            {'file': 'assets/chunk.js', 'imports': [{}]},
            {'file': 'assets/chunk.js', 'imports': ['../private.js']},
            {'file': 'assets/chunk.js', 'css': 'assets/chunk.css'},
            {'file': 'assets/chunk.js', 'css': [None]},
            {'file': 'assets/chunk.js', 'css': ['assets/../../private.css']},
        ]
        for chunk in invalid_chunks:
            with self.subTest(chunk=chunk):
                self.write_manifest({
                    'index.html': {'file': 'assets/index.js', 'imports': ['_chunk.js']},
                    '_chunk.js': chunk,
                })
                self.assertEqual(self.client.get('/app/').status_code, 503)
        self.write_manifest({
            'index.html': {'file': 'assets/index.js', 'imports': ['_missing.js']},
        })
        self.assertEqual(self.client.get('/app/').status_code, 503)

    def test_static_dependency_walk_has_explicit_work_limits(self):
        self.write_manifest({
            'index.html': {'file': 'assets/index.js', 'imports': ['_shared.js']},
            '_shared.js': {'file': 'assets/shared.js', 'css': ['assets/shared.css']},
        })
        for limit in ('MAX_STATIC_CHUNKS', 'MAX_STATIC_IMPORTS', 'MAX_STATIC_STYLES'):
            with self.subTest(limit=limit), patch(f'apps.frontend.views.{limit}', 0):
                self.assertEqual(self.client.get('/app/').status_code, 503)
