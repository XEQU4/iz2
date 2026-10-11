# Development and reproducible checks

Use Python 3.13+, uv and Node 22.12+. Docker with Linux containers is needed for
the PostgreSQL gate. Dependencies are locked in uv.lock and frontend/package-lock.json;
do not upgrade them as a side effect of running checks. No private artifacts or
working credentials are required for the commands below.

## Install and verify

From the repository root, install Python dependencies:

```sh
uv sync --frozen
```

Frontend dependencies, tests and production assets:

```sh
cd frontend
npm ci
npm test -- --maxWorkers=2
npm run build
npm run format:check
cd ..
```

On PowerShell, use npm.cmd if npm.ps1 is blocked by execution policy.

Run the full backend gate against disposable PostgreSQL:

```sh
uv run --frozen python scripts/test_postgresql.py
uv run --frozen python manage.py check --settings=config.test_settings
uv run --frozen python manage.py makemigrations --check --dry-run --settings=config.test_settings
uv run --frozen python manage.py spectacular --validate --fail-on-warn --settings=config.test_settings
node tests/frontend_regressions.cjs
node tests/graph_interactions.cjs
uv run --frozen python scripts/check_compose.py
uv run --frozen python scripts/check_docs.py
```

The PostgreSQL runner uses an owned PostgreSQL 17 container with tmpfs, a random
loopback port/password, no persistent volumes and offline settings. It always uses
the explicit labels **apps tests**, removes only its ownership-verified container
and propagates test failure. Docker may download the PostgreSQL image on first use.
It does not load .env, connect to the native database, use Redis or call sources/models.

For a faster check without Docker:

```sh
uv run --frozen python manage.py test apps tests --settings=config.test_settings
```

This uses isolated SQLite and skips PostgreSQL-specific cases; it is not a
replacement for the database gate. Root test.py is a personal learning file and
must not be discovered as an application test. Compose checks use synthetic
configuration and do not start application services. The docs checker verifies
local Markdown/HTML links, images and heading anchors, not remote website availability.

There is currently no committed CI workflow or remote branch-protection proof.
These commands are reproducible locally; automating them remains a release task.
Controlled diagnostic scripts and old reports under artifacts/ are not required
to execute the standard gates. Live collection, real inference and target-host
testing are separate, explicitly authorised activities.

## Native development

Use a separate development PostgreSQL database and prepare a private .env from
[.env.example](../.env.example). Configure only the sources you are authorised
to access; running the web server does not start collection. Verify a current
backup before migrating an existing database.

After installing Python/frontend dependencies:

```sh
uv run --frozen python manage.py migrate
uv run --frozen python manage.py collectstatic --noinput
uv run --frozen python manage.py runserver
```

Open http://127.0.0.1:8000/app/. For frontend hot reload, keep Django on port 8000
and run npm run dev in frontend/; open http://127.0.0.1:5173/. The Vite proxy
forwards /api to Django. Rebuild, collect static and restart Django when checking
the production asset path; strict manifest storage stays enabled.

Redis is required for queued workers and shared account quotas. Native local
fallback quotas are process-local, unlike the supported Docker deployment.
Native background collection is an explicit opt-in; startup/stop commands and
model coupling are documented in [DEPLOY.md](../DEPLOY.md#native-windows-collector).

## Change boundaries

Prefer synthetic fixtures and narrow behavioural assertions. Imports, identity,
date rules, graph histories and AI publication need meaningful regressions. Check
both saved views and domain histories when changing graph interaction. Preserve
CSS ordering and dependency notices. The current [audit](FINAL_AUDIT.md) separates
passing regression gates from known defects; passing tests alone is not a public
release decision.
