"""Run the offline Django suite against a disposable Docker PostgreSQL instance.

Usage: uv run --frozen python scripts/test_postgresql.py
No .env, existing database, Redis server, source credentials or model is used.
Docker must run Linux containers. The owned container uses tmpfs, a loopback port
and no persistent volumes; it is removed even when a test fails.
"""

import argparse
import importlib
import os
from pathlib import Path
import secrets
import subprocess
import sys
import time
import uuid


ROOT = Path(__file__).resolve().parents[1]
IMAGE = "postgres:17-alpine"


def docker(*arguments, **kwargs):
    return subprocess.run(
        ["docker", *arguments], check=True, text=True, capture_output=True,
        timeout=kwargs.pop("timeout", 30), **kwargs,
    ).stdout.strip()


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    os.chdir(ROOT)
    sys.path.insert(0, str(ROOT))
    token = uuid.uuid4().hex
    container = "iz2-tests-" + token
    password = secrets.token_urlsafe(32)
    # Docker reads this value from the child environment, not a command argument.
    environment = {**os.environ, "POSTGRES_PASSWORD": password}
    created = False
    try:
        docker(
            "run", "--detach", "--name", container,
            "--label", "iz2.test-run=" + token,
            "--tmpfs", "/var/lib/postgresql/data:rw,nosuid,size=1024m",
            "--publish", "127.0.0.1::5432", "--env", "POSTGRES_PASSWORD",
            IMAGE, env=environment, timeout=180,
        )
        created = True
        endpoint = docker("port", container, "5432/tcp")
        if not endpoint.startswith("127.0.0.1:") or "\n" in endpoint:
            raise RuntimeError("The test database must have one loopback-only port.")
        port = int(endpoint.rsplit(":", 1)[1])
        deadline = time.monotonic() + 60
        while True:
            try:
                docker("exec", container, "pg_isready", "-h", "127.0.0.1", "-U", "postgres", timeout=5)
                break
            except subprocess.CalledProcessError:
                if time.monotonic() >= deadline:
                    raise RuntimeError("The disposable test database did not become ready.")
                time.sleep(0.5)

        # Importing test_settings clears runtime configuration while importing
        # settings, disables dotenv, and replaces brokers and logging locally.
        os.environ["DJANGO_SETTINGS_MODULE"] = "config.test_settings"
        module = importlib.import_module("config.test_settings")
        module.DATABASES = {"default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "postgres", "USER": "postgres", "PASSWORD": password,
            "HOST": "127.0.0.1", "PORT": port,
            "CONN_MAX_AGE": 0, "OPTIONS": {"connect_timeout": 10},
            "TEST": {"NAME": "test_iz2_" + token},
        }}
        import django
        django.setup()
        from django.test.runner import DiscoverRunner

        print("Running apps and tests on an empty, disposable PostgreSQL 17 instance.", flush=True)
        return DiscoverRunner(interactive=False, verbosity=1).run_tests(["apps", "tests"])
    finally:
        if created:
            # Never remove a container unless this run's unique label matches.
            actual = docker("inspect", "--format", '{{index .Config.Labels "iz2.test-run"}}', container)
            if actual != token:
                raise RuntimeError("Test-container ownership changed; refusing removal.")
            docker("rm", "--force", "--volumes", container)
            print("Removed the owned test container; no persistent volume was used.", flush=True)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, RuntimeError, subprocess.SubprocessError) as error:
        # Do not print subprocess environments or database credentials.
        print(f"PostgreSQL test runner failed: {type(error).__name__}: {error}", file=sys.stderr)
        sys.exit(1)
