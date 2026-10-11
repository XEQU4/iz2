# IZ2 v0.1.0 — Initial Release

IZ2 is a thesis prototype for exploring relationships in Kazakhstan public procurement. It connects saved company, person and contract records with their supporting evidence so researchers and reviewers can decide what needs further checking.

## Included

- Search company, person and contract directories and inspect source records and dates.
- Explore relationship groups and interactive graphs with filters, node selection and an evidence panel.
- Review saved graph snapshots, group lineage, analysis histories and evidence-bound explanations.
- Use deterministic review priorities and labelled templates, with optional validated local Qwen statement selection.
- Save personal graph layouts through workspace accounts; use the English/Russian interface and English Swagger API reference.
- Browse the shared cosmic background with responsive layouts, cursor-reactive borders and controllable motion, including reduced-motion support.

## Get started

Follow the [README quick start](https://github.com/XEQU4/iz2/blob/v0.1.0/README.md#quick-start) for a new Docker Compose installation. Template mode requires no model download. The database starts empty; collection and automatic AI jobs are disabled. Existing data requires the documented transfer and recovery procedure.

## Known limitations

- Relationships and indicators require human review and do not, by themselves, prove collusion or wrongdoing. Review priority is not a calibrated probability or independently validated ML detector.
- Source coverage and legal-date information are incomplete. Unavailable checks do not establish a clean finding; current-role filtering is not historical reconstruction.
- This is a supervised research prototype, not a production-ready or unattended public service. Open audit items include dependency remediation, collection recovery, database-restart and failed-page-download recovery, AI runtime bounds and large-graph performance. See the [current audit](https://github.com/XEQU4/iz2/blob/v0.1.0/docs/FINAL_AUDIT.md).

## Release verification

Release preparation passed 151 frontend tests, the production frontend build and offline SQLite checks (682 tests, six PostgreSQL-specific skips). The full offline suite then passed on disposable PostgreSQL 17: **682 tests, no failures, errors or skips**.

A fresh, isolated Docker Compose installation passed `up --build -d --wait` in template mode: migrations exited successfully and all six persistent services became healthy. All 18 checked HTTP routes and 18 referenced local static resources returned 200; readiness confirmed PostgreSQL and Redis, and the four catalogues remained empty. Overview, directories, About and Swagger loaded in the browser; directory/About/API navigation produced no page errors or failed requests. Collection and model inference stayed disabled. These checks establish local prototype startup, not production readiness or resolution of the open audit findings.

Documentation screenshots use fictional demonstration data. Original code and documentation use MIT; third-party terms remain separate, including MIT + Commons Clause for React Bits adaptations. See [third-party notices](https://github.com/XEQU4/iz2/blob/v0.1.0/THIRD_PARTY_NOTICES.md).
