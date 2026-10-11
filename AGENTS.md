# Working on IZ2

IZ2 is a thesis prototype for reviewing relationships in Kazakhstan public
procurement. Read the [roadmap](docs/ROADMAP.md), [architecture](docs/ARCHITECTURE.md)
and [current audit](docs/FINAL_AUDIT.md) before work. Operations belong in
[DEPLOY.md](DEPLOY.md); historical records are indexed in [docs/README.md](docs/README.md).

## Scope and workflow

- Work on the assigned task. Do not automatically start new sources, research
  experiments, deployment or another phase.
- The user runs Git. Read-only diagnostics are authorised for this audit; commits,
  branches, PRs, push, reset, clean and checkout need a separate explicit instruction.
  Preserve unrelated user changes.
- Explain results in Russian to the user. Use English for documentation, code
  comments, CLI messages, prompts, new saved explanations and proposed commits.
  Put necessary user actions and exact commands at the end of the final response
  in execution order; do not require opening a document to finish the task.
- Distinguish implemented behaviour, fresh checks, historical evidence, proposals
  and unverified limits. Never reuse old test counts as new verification.
- Brand/package/repository: IZ2 / iz2. iz2.kz is an intended domain, not a live
  service claim. Preserve database/volume identifiers, GPG compatibility settings
  and the graph-view storage key. next-app was removed by request; React/Vite is
  served by Django.

## Data and operations

- Before schema or saved-data algorithm changes, verify a current backup and
  independent restoration using [recovery rules](docs/RECOVERY.md). Never trial
  restoration against the source database or erase data to make a check pass.
- Tests use isolated databases, queues and containers. Use explicit Django labels
  `apps tests`; root `test.py` contains personal learning exercises.
- Live parsing, full imports, cleanup, working migrations, collector startup,
  working graph/text refresh and paid generation need task-specific authorisation.
  Do not use them to verify refactoring. This audit authorises none of them and
  must not stop user services. Preserve background processes unless the current
  task authorises lifecycle changes.
- Never commit passwords, tokens, .env, dumps or raw personal source responses.
  Private reports, backups and model caches stay under ignored artifacts/.
  Preserve local dependencies, operational files and user data.
- Do not update dependency versions/locks unless explicitly in scope. Triage
  scanner findings for applicability; a clean scan is not a security guarantee.
- Parsers fetch and normalise; ingestion services persist and orchestrate. Views
  and commands delegate. Parse money from strings as Decimal. Keep missing data,
  source failure and confirmed absence distinct.
- Respect exact subject/type binding, source dates, independent freshness, request
  budgets, cooldowns, leases and checkpoints. Retain last successes after failures.
  KGD registration does not imply an arrears check; company-specific entitlement
  must not be reused for another company.

## Domain invariants

- Never merge people by name alone. Names create candidates; verified identifiers
  and source-bound roles determine person links. Director is not owner.
- Relationships need evidence, sources and temporal applicability. Retrieval time
  is not an appointment date. Current-role filtering is not historical reconstruction.
- Company debt belongs to the company. Unavailable court, bankruptcy, restricted
  participant or owner-history checks do not establish a clean finding.
- Graphs, rules and explanations use the same saved evidence. Group membership
  can be transitive; a shared contact does not prove collusion.
- Preserve stable group IDs, immutable snapshots/texts and merge/split histories.
  Unchanged meaningful evidence must not recreate analytical versions.
- Public review priority is deterministic, not a trained probability. Qwen selects
  prepared evidence-bound statements; it does not create facts, identify people,
  add edges or set public scores. Validate exact scope/qualifiers at publication
  and cache reuse. Failures save labelled templates.
- Old prose keeps its original provenance. GET never regenerates or reclassifies
  saved evidence/text. Explicit jobs require deduplication and version/ownership
  fences. Experimental scores remain separate until independent evaluation.

## Interface and verification

- Current direction is restrained graphite/black/white with semantic graph/status
  colours, reduced-motion support and EN/RU website controls. API docs stay English.
  Source identifiers/names and stored text do not translate with the interface.
  Business dates use Asia/Qyzylorda.
- Preserve /legacy/, model/migration boundaries, management discovery, API assets,
  notices and compatibility imports. No ordinary imports is not proof of non-use.
- Preserve Vite entry/chunk hashes and dependency-first CSS ordering. Personal views
  stay separate from evidence and require ownership/revision checks, including deletion.
- Run meaningful tests for identity, imports, dates, concurrency, graphs and AI.
  Syntax alone is insufficient; SQLite skips are not a PostgreSQL gate.
  Reproducible commands are in [development](docs/DEVELOPMENT.md).
- Report changes, actual checks and limits. Distinguish sandbox restrictions from
  application defects. Update current references and archive historical evidence;
  do not append another chronological diary here.
