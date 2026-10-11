# IZ2 repeat audit

**Date:** 11 October 2026, Asia/Qyzylorda.
**Baseline:** `2bafde3e84e96223e2fa301e083ccbb381037412` — Ground AI explanations, refine UI and document IZ2.
The working tree was clean at entry (426 tracked files). This report also covers
the bounded changes listed below. Git was used read-only; no commit or push ran.

**Verdict:** suitable for a rehearsed, supervised relationship-evidence thesis
demonstration and local review with known limits. It is not ready for unattended
public operation or a claim of validated coordinated-bidding detection. Passing
regressions and a working Docker image do not close the reproduced defects.

The [previous final audit](archive/2026-10-11/FINAL_AUDIT.md) is preserved
byte-for-byte, including its dated follow-ups. The [initial audit](archive/2026-10-11/AUDIT.md)
and [repository audit](archive/2026-10-11/REPOSITORY_AUDIT.md) remain distinct
historical records. Old counts and findings were not reused as fresh proof.

## 1. System, scope and evidence

Django/DRF serves the React/Vite workspace, saved JSON projections, API reference
and compatibility pages. PostgreSQL retains facts, observations and immutable
histories. Redis supports jobs and shared account quotas; Celery runs independent
Docker ingestion and explanation queues. Parsers normalise, ingestion services
persist, graph services publish snapshots, deterministic rules calculate priority,
and optional Qwen selects prepared explanation statements.

Entry points are manage.py, config/urls.py, config/wsgi.py, config/asgi.py,
config/celery.py, Dockerfile/docker-compose.yml, frontend/src/main.tsx and the
operator scripts. /app/, /api/v1/, /api/v1/docs/, /legacy/, /clusters/, /companies/,
/owners/, /analysis/ and /health/ remain intentional interfaces. Existing app
models/migrations and management discovery were retained. Locked Python packages
were scanned by exact version (61 registry packages); npm reported 258 entries.
The stack and module boundaries are detailed in [ARCHITECTURE.md](ARCHITECTURE.md).

The thesis title concerns dynamic graph analysis, OSINT and machine learning.
The implemented research contribution is narrower: source/evidence modelling,
versioned relationship maintenance and constrained model-assisted presentation.
Group versioning is not temporal graph learning. Review priority is not a fitted
or calibrated probability. Complete tender participants/bids/lots/outcomes and
independent detection/readability evaluations are absent.

| Intended use | Readiness and conditions |
| --- | --- |
| Defence | Rehearse a fixed, labelled dataset; explain incomplete sources and the real ML role. Use templates or reviewed grounded saved texts. |
| Local review/development | Useful, with backups, explicit dates and the unresolved collection/name/status limitations below. |
| Unattended pilot | Blocked by recovery/correctness, runtime and publication-policy work. |
| Public service | Additionally requires patched dependencies, real-host TLS/proxy/cookie and privacy/source-term review, monitoring and off-host recovery. |

This audit used code inspection, isolated regression tests, synthetic defect
probes, a read-only PostgreSQL aggregate, fresh empty Compose startup and Chromium.
No live parser, source request, working write/migration/refresh, model inference
or paid generation was run. User services were not stopped. Only explicitly owned
test containers, databases and previews were created and removed.

## 2. Reassessment of AUD-001–AUD-020

Status refers to the original finding, with the scope stated explicitly.
**Fixed: 6; partially fixed: 3; open: 11.** None is closed solely by an old report.

| ID | Status | Current evidence and boundary |
| --- | --- | --- |
| AUD-001 | Fixed | config/settings.py sets Asia/Qyzylorda and shares it with Celery. apps/core/test_business_dates.py passes local/UTC midnight, year/leap-day, freshness and role-boundary cases in the fresh PostgreSQL suite. Old immutable results are not rewritten. |
| AUD-002 | Fixed for new jobs | apps/ai/grounding.py closes free prose; services.validate_saved_explanation and jobs.py check exact rendered output at publication/reuse. Fresh adversarial, poisoned-cache, fallback and provenance tests pass. Legacy prose remains outside this guarantee. |
| AUD-003 | Partially fixed | README/architecture now delimit the claim, and build_clusters --as-of help names current-role filtering. rules.py still marks bidding behaviour not assessable; no detector/evaluation or complete historical reconstruction exists. |
| AUD-004 | Fixed in supported deployment | Redis Lua quotas, fail-closed handling and explicit single-proxy trust replace per-process Docker limits. Independent processes accepted 5+5 then denied request 11; four concurrent processes accepted exactly 10/32. Native local fallback remains process-local. |
| AUD-005 | Open | Fresh SQLite and PostgreSQL probes reproduce consumed manual quarantine without a ContractRetry; resume/repair cannot reach the rejected contract. |
| AUD-006 | Open | Same verified identifier with a corrected name updates evidence/company but leaves PersonIdentity.full_name and role label stale. Reproduced on both databases. |
| AUD-007 | Open | An expired worker can mark a replacement's resumed run failed despite no stale domain write. Deterministic lease interleaving reproduced on both databases. |
| AUD-008 | Open | Enrichment/KGD counters use different keys from collection stage accounting; one successful company produces records=0. Reproduced on both databases. |
| AUD-009 | Open | Fresh read-only coverage remains partial; full archive/backlog convergence and broader debt entitlement are not demonstrated. No new source run was authorised. |
| AUD-010 | Open | Exact locked versions have advisories. Vendor lookup adds an applicable October Django header issue absent from scanner output; bounded synthetic route/sink proof below. |
| AUD-011 | Fixed at header layer | XFrameOptionsMiddleware with DENY; fresh admin, Swagger and session response checks pass. Real public ingress remains unverified. |
| AUD-012 | Open | Owned slow-body server exceeded a 5-second provider budget: 7.642 seconds before rejection. No inference or late publication occurred. |
| AUD-013 | Open | Catalogue-wide graph inputs and conservative mass-contact impact remain. One seed reached all 2,000 synthetic companies despite 1,000 separate pairs. A dead duplicate traversal was removed, not the global algorithm. |
| AUD-014 | Open | GraphExplorer still settles D3 ticks synchronously. CPU benchmark below; earlier dense-fit readability concern is not closed by visual refinement or small-graph checks. |
| AUD-015 | Open | providers.py stores configured AI_MODEL_REVISION, not the resolved weights digest/runtime. Actual identity of weights behind a mutable tag is not attested. |
| AUD-016 | Partially fixed | A tracked disposable PostgreSQL runner and docs checker now make local gates reproducible. Clean frozen image build passed. No committed CI workflow or remote branch gate was verified. |
| AUD-017 | Partially fixed | Compose resource limits and 10 MiB × 3 logs are configured and startup-tested. Native redirected logs have no rollover/retention; native collection still requires model startup. |
| AUD-018 | Fixed for current references | Current docs now match React/Vite, single Compose, EN/RU, grounded AI and current operations; diary/revoked restrictions archived. Local links/anchors and startup recipe were checked. |
| AUD-019 | Fixed | No runtime logs/schedules are tracked. Ignored operational state remains local; old deleted-log claims are not current findings. |
| AUD-020 | Open | Four missing entity APIs correctly return 404 but say “The request was rejected.” Browser company detail repeats this with Try again. |

## 3. Confirmed open issues and acceptance criteria

P1 is a blocker for a stronger product/research claim; P2 is a material correctness,
security, reliability or performance task; P3 is a usability/observability task.
No P0 finding was established. A hypothesis is labelled separately from a reproduction.

| ID / priority | File/function and proof | Impact | Separate change and acceptance |
| --- | --- | --- | --- |
| AUD-003 / P1 conditional | apps/ai/rules.py:154, graph/evidence.py:27 applicable() requires is_current even for past as_of; code-confirmed missing capability | An unqualified detector/ML claim exceeds evidence | Keep scoped defence wording. A stronger claim needs complete bidding inputs, independent labels, baselines, held-out evaluation and measured uncertainty. Historical reconstruction needs its own semantics/tests. |
| AUD-005 / P2 | ingestion/services.py:199 _contracts_stage; crawl.py:116 repair only consumes ContractRetry. Two attempted rows, one invalid party: one saved contract, zero repair work after resume | A rejected manual-import row can become unreachable through repair | Persist repairable rejected IDs through consumed budgets/restarts; repair resolves original issues without rewriting accepted history. |
| AUD-006 / P2 | ingestion/identities.py:65 get_or_create keeps original full_name; two same-IIN observations reproduce stale display | People/search/role text can disagree with accepted source correction | Define source/date-aware current name and aliases; test newer/stale/conflicting corrections and frozen historical labels, with no name-only merge. |
| AUD-007 / P2 | ingestion/services.py:486 final failed update lacks lease-token fence | Old worker can corrupt operational status of replacement run | Fence status/error/finished updates and lease release; PostgreSQL same-run A-expiry/B-resume/A-return must leave B untouched. |
| AUD-008 / P3 | ingestion/collection.py:158 reads checked; services.py uses companies_checked/kgd_company_attempts | Status understates completed work, misleading progress decisions | Common or stage-specific attempted/accepted schema; test success/failure/cache/unchanged and retain correct contract counts. |
| AUD-009 / P2 | background due logic, collection backlog gate and KGD entitlement rules; current aggregate below | Saved catalogue is incomplete; success/registration is not full profile/debt coverage | Authorised bounded head/history/repair reconciliation with restart and freshness denominators; no national claim without authoritative target. |
| AUD-010 / P2 public | uv.lock, Django parser/admin renderer and provider streaming; vendor and bounded sink proof | Reachable header parsing work and conditional admin/provider attack surface | Separately update compatible locks, re-scan vendors/advisories, regress headers/admin/provider transport and rerun PG/frontend/image gates. |
| AUD-012 / P2 | ai/providers.py:195–207 checks elapsed time only after iter_content yields; 5s → 7.642s | Configured budget is not a hard service deadline | Bound slow headers, stalled/dripping bodies and repair within documented tolerance; cancellation cannot publish late; preserve fallback. |
| AUD-013 / P2 | graph/services.py load/analysis_fingerprint/impact_boundary; evidence.py components excludes mass contacts while closure includes them | Small evidence changes can do catalogue-wide work | Measure representative PostgreSQL query/memory/latency budgets; narrow dirty work only with threshold-crossing, old/new closure and lineage equivalence checks. |
| AUD-014 / P2 | GraphExplorer.tsx:1052,1211 synchronous 100/160 settling ticks | Large graph opening/reset can block UI; labels need scalable navigation | Choose density/readability/performance budgets; worker/progressive layout or detail strategy must retain keyboard selection, filters, pins and saved views. |
| AUD-015 / P2 | ai/providers.py:76,274 configured revision in keys/metadata | Same tag can conceal changed weights; failures lack complete timing/token accounting | Resolve actual digest/runtime and define cache policy; two digests under one tag remain distinguishable; no raw sensitive prompts in reports. |
| AUD-016 / P2 | No CI workflow; new scripts/test_postgresql.py is runnable locally | Future commits are not automatically gated | Clean frozen CI invokes PG, schema/drift, frontend/build, docs and synthetic smoke; failures block the chosen release path. |
| AUD-017 / P2 | background.ps1:65,74 and local_ai.ps1:62; unbounded redirected logs, model-first native startup | Disk growth; native ingestion unavailable when model startup fails | Rotate/retain native logs, make native AI optional, simulate model absence, disk limits and shutdown/recovery. |
| AUD-020 / P3 | api/common.py:47–55; frontend EntityState/detail routes; real browser/API 404 | User gets a useless retry instead of navigation | Dedicated missing-record state and directory link; preserve private 403 and retryable network/503 handling. |

### Additional reproduced defects

**AUD-021 — P2, transient API failure after PostgreSQL restart.** In the isolated
fresh Compose deployment, three database restart cycles produced two HTTP 500
responses among 18 Overview requests; the remaining 18 readiness requests and
16 Overview requests returned 200 after database health was restored.
This is an observed recovery failure, not evidence of data loss.
config/settings.py:137 uses CONN_MAX_AGE=60 without CONN_HEALTH_CHECKS. Stale
persistent connections are a code/documentation-supported explanation, but no
exception stack was retained, so the exact root cause remains an inference.
[Django documents this restart case](https://docs.djangoproject.com/en/6.0/ref/settings/#conn-health-checks).
Acceptance: capture the exception, apply the smallest connection-policy fix, and
repeatedly restart an owned PostgreSQL across all Gunicorn workers; healthy
recovery requests must succeed while genuine downtime still yields readiness 503.

**AUD-022 — P2, failed lazy page download leaves a blank workspace.**
frontend/src/App.tsx uses lazy/Suspense routes without an error boundary.
In a fresh synthetic browser context, aborting the People JavaScript chunk caused
“Failed to fetch dynamically imported module”; body text became empty and #root
had zero children. This is separate from API-network failure, whose retry worked.
Acceptance: a route/chunk error boundary offers safe reload/navigation without a
reload loop; test offline, stale deployment chunks and subsequent recovery while
retaining account/view state. This audit did not silently implement either fix.

### Dependency applicability, checked 11 October

OSV returned 30 records / 15 distinct GHSA IDs across locked Django 6.0.6,
soupsieve 2.8.4, sqlparse 0.5.5 and urllib3 2.7.0. These are advisory records,
not 30 demonstrated vulnerabilities. npm audit reported zero advisories for the
258 lock entries; this does not certify bundled fonts/assets or the container OS.

The [6 October Django release](https://www.djangoproject.com/weblog/2026/oct/06/security-releases/)
includes CVE-2026-84429, absent from that scanner response. Anonymous
/api/v1/session/ content negotiation reached the affected header parser. Inputs
of 525/1,025/2,025/4,025 characters took median 0.234/0.719/2.379/8.583 ms in a
bounded parser probe. This confirms reachability and superlinear work, not a
public load/exploitation measurement.

The [August Django URLField admin issue](https://www.djangoproject.com/weblog/2026/aug/04/security-releases/)
affects the installed renderer; a synthetic javascript URL became a link.
SourceObservation admin exposes a URLField, but no malicious real record or
end-to-end source-to-admin exploit was established.
Requests streaming makes the urllib3 [chunk-header](https://github.com/urllib3/urllib3/security/advisories/GHSA-vxq7-64xx-v4gw)
and [Deflate](https://github.com/urllib3/urllib3/security/advisories/GHSA-gh4c-6fx4-qh6g)
issues conditionally relevant to a malicious configured provider. Public users
cannot choose that endpoint; source collectors use curl-cffi.

No GIS, variable Soup Sieve selector, public SQL formatter, custom proxy TLS
context, LocaleMiddleware or editable-primary-key formset path was found.
Consequently the [July Django](https://www.djangoproject.com/weblog/2026/jul/07/security-releases/),
[Soup Sieve](https://github.com/facelessuser/soupsieve/security/advisories/GHSA-gjv8-xp57-g29c),
[SQLParse](https://github.com/andialbrecht/sqlparse/security/advisories/GHSA-prg7-hcfm-mfcr)
and [urllib3 proxy TLS](https://github.com/urllib3/urllib3/security/advisories/GHSA-8988-9cw3-xx77)
records require scoped triage rather than a blanket exploitation claim.
Examined vendor patch minima are Django 6.0.9, Soup Sieve 2.9, SQLParse 0.6.0 and
urllib3 2.8.0. They are dated minima, not a tested replacement lock. No dependency
version changed in this task.

## 4. Data, graph and AI boundaries

Fresh read-only repeatable-read aggregate: **11 October, 15:50:58 Asia/Qyzylorda**.
Only aggregate counts/statuses were exported. No personal values or credentials
were included.

| Measure | Saved result / interpretation |
| --- | --- |
| Companies / contracts | 813 / 525; not a national or continuously reconciled archive |
| Source-checked directory / pending | 313 / 500; profile evidence is not complete checks |
| Identity records / default current verified people | 1,198 / 115; different populations, not 1,198 distinct verified humans |
| Current directorships / verified identifier roles | 384 / 116; all 384 lack legal role dates |
| Registry latest success / invalid / unavailable / unattempted | 259 / 63 / 17 / 474 |
| Adata latest success / not found / unavailable / unattempted | 237 / 8 / 22 / 546 |
| KGD saved registration states / success | 235 / 223; 126 UL and 97 IP successes |
| Company arrears | Three saved successful zero results; 810 companies have no debt state; one company-scoped credential configured |
| Selected facts / legacy-unconfirmed | 4,396 / 1,481; no wrong-subject/company or nonlegacy selected-value mismatch found by this aggregate |
| Active groups / all groups / snapshots / lineage | 14 / 23 / 57 / 34 |
| Analyses / immutable explanation rows | 44 / 94; counts do not certify old text correctness |
| First-attempt enrichment backlog | 546, above configured high-water 100 |
| Current cursor/repair evidence | Empty head/history/repair progress maps; two unresolved invalid-party issues and zero retry rows |
| Ownership/court/person-debt/bankruptcy | None saved; absence of integration/check is not a negative finding |

Last nonlegacy source observations were dated 9 October, with no uncached source
observation in the preceding hour. This is not a process-health check or current
source-availability proof. Runtime process overrides can differ from normal
configuration. No collection speed or completion date is inferred.

Inspection and fresh suites support exact identifiers, Decimal parsing,
chronological observations, source-specific due dates, cooldown/request caps,
latest-attempt versus last-success KGD state, and atomic graph publication.
The durable crawler retains page/repair progress; the older manual path has
AUD-005. Status fencing is incomplete even where domain publication is fenced.

People are not merged by name. Current verified role evidence forms graph edges;
retrieval dates do not become legal dates. Shared feature nodes avoid pairwise
cliques; connected components may connect companies transitively. Stable UUID
matching, retirement/reactivation and merge/split lineage retain frozen histories.
No-change evidence hashes avoid unnecessary analytical versions.
GET reads saved graphs/analyses/texts; it does not regenerate them.

New AI output selects IDs/variants from prepared facts. Grammar validation,
server rendering, exact cached-output checks and latest-request fencing passed.
Company/scope/amount/date qualifiers remain tied to frozen inputs; the model
cannot set public scores. Old prose is honestly labelled and immutable. No new
real Qwen run occurred in this audit; the nine previous synthetic runs belong
to the [10 October evaluation](archive/2026-10-11/AI_GROUNDING.md#targeted-evaluation).

Public serializers omit IIN, raw observations and experimental scores; own views
require user ownership and revision checks, including delete tombstones.
Session/CSRF, staff jobs, password checks and account uniqueness have fresh
regressions. BIN/name/contact publication still needs an explicit policy,
especially for individual entrepreneurs. There is no HTTP ingestion-start route.

## 5. Cleanup and documentation decisions

No additional whole application file/directory was proved unused. No artificial
source deletion, model/migration move or broad module merger was performed.
The prior next-app/scaffold/overlay deletions were checked, not repeated.

| Path / purpose | Consumers | Decision and evidence | Post-change check |
| --- | --- | --- | --- |
| graph/services.py rebuild_clusters local director_map | No subsequent read; current EvidenceIndex and fingerprint have their own role inputs | Delete one redundant computation, keep the helper for compatibility callers | Same 100-company fixture: identical 50 snapshots/summary, 14 SQL queries and zero writes before/after; map calls 1→0; 47 PG graph tests |
| GlitchText.period / --glitch-period and App caller | Only App passed it; no CSS consumer after finite hover redesign | Delete unused prop/default/style/type import and caller argument; CSS unchanged | 146 React tests, TS/Vite build and formatting |
| build_clusters --as-of help | Django management discovery/operators | Correct the claim to currently observed roles, not historical reconstruction | Existing command regression and actual help output |
| config/settings.py language comment; .env.example source-doc pointer | Developers/environment helper | Correct stale descriptions only; no setting/value change | Settings/schema/Compose checks; link scan |
| AGENTS.md and ROADMAP.md | Agents and current planning | Merge continuing rules into short active references; move diary/plans to archive | Current decisions, scope and user-authorised exceptions reviewed |
| FINAL_AUDIT.md | Release/readiness decisions | Archive original exact bytes, write this independent repeat audit | Original/archive SHA-256 equality |
| AUDIT, BASELINE, PHASE1–7, LANGUAGE, PARSER_AUDIT, REPOSITORY_AUDIT, DEPLOYMENT_CHECK | Historical evidence and links | Move to dated archive; preserve distinct purposes, rebase navigation | Local links/anchors; dated archive index |
| RECOVERY / DATA_READINESS / AI_GROUNDING | Current operators/developers | Separate current policy from archived measurements/protocols | Source comparison, links and acceptance boundaries |
| ARTICLE_CONTEXT.md | Research article handoff | Keep 5 October checkpoint; add clearly separate current pointers, no invented experiment | Historical prose/counts retained |
| scripts/test_postgresql.py / check_docs.py | Clean-clone verification | Add minimal public gates without private data | Full PG run; five docs-checker boundary tests and repository scan |
| templates/, static/, legacy views | URLConf, template tags, Swagger, CSS assets | Keep: compatibility/API routes remain live | Legacy JS suites, HTTP/asset checks |
| management commands, AppConfig/admin, migrations, graph compatibility exports | Convention discovery, old imports and DB history | Keep: zero ordinary imports is not non-use | Full backend suite and route/config review |
| ingestion/services.py and crawl.py | Distinct manual/continuous paths | Investigate shared acceptance in AUD-005; do not delete either | Resume/repair probes establish why a separate change is needed |
| ai/narrative.py | Live aliases/context plus historical diagnostic tests | Keep: not an unused free-prose publication module | Grounding/import/provenance suites |
| Frontend source/styles | Static and lazy imports and CSS cascade | Keep all 74 reachable non-test modules/styles | Import traversal and Vite build |
| Licences/notices and docs/assets/iz2-mark.svg | Distribution/README | Keep terms and the small intentional icon copy | Links; screenshots/logo unchanged |
| test.py, .env, artifacts, caches, local dependencies, operational files | User learning/private/runtime state | Keep untouched; not repository-cleanup targets | Protected-file hashes and isolated check configuration |

Current docs are indexed in [docs/README.md](README.md). DEPLOY is the command
authority; DEVELOPMENT contains reproducible checks; README introduces the
problem, thesis scope, workflow, real synthetic screenshots and template-first
empty installation. Four PNGs and the mark were retained. MIT applies to original
code/docs, while React Bits Commons Clause and other third-party terms remain
separate. Provenance of the retained legacy Kazakhstan background image was not
established; a complete distribution-rights review is still a release task.

The deployment guide now leads with the same verified template-mode startup,
states the tested host-Python requirement and keeps one quiet-writer backup
sequence; a redundant standalone backup after restarting writers was removed.

The archival folder is dated by preservation, not by original event date.
Relative navigation was rebased without rewriting old outcomes. The original
final audit stays byte-identical. The old agent diary is AGENTS-before.md so it
cannot act as nested current instructions. Archived commands are not current
operational steps.

## 6. Fresh verification and measurements

| Check actually run | Result and scope |
| --- | --- |
| Full offline Django suite on owned PostgreSQL 17 | 676 tests, zero failures/errors/skips; runner exit 0; owned container/database removed |
| After dead graph computation removal | 47 PostgreSQL graph tests, zero skips |
| After unused animation prop removal | 146 React tests in 18 files; TypeScript/Vite build and format pass |
| Known-defect diagnostics | Four isolated SQLite and four PG probes reproduce AUD-005–008; a passing diagnostic is evidence of a bug, not desired behaviour |
| New documentation checker | Five tests cover moved links, encoded/duplicate/linked headings, HTML/Setext, code examples and missing paths |
| Django integration | System checks, migration drift and strict OpenAPI validation pass; normal runtime check in new image passes |
| Compatibility JavaScript | frontend_regressions.cjs and graph_interactions.cjs pass |
| Compose | Existing checker: eight configurations; generated template/CPU/GPU × HTTP/HTTPS: six validate |
| Clean-source quick start | Frozen npm ci/uv sync image built from tracked/proposed files without .env, dependencies or cached assets; empty isolated project up --wait passed |
| Empty install HTTP/assets | 16 routes and 13 local assets return 200; company/person/contract/group counts zero; no screenshot seed |
| Runtime image | UID 10001, no private .env/artifacts/.git/next-app/node_modules, no Node/npm runtime |
| Real Redis quotas | Independent and concurrent process limits passed; owned Redis removed |
| Outage/recovery | Redis: readiness503/live200, restart200. PostgreSQL restart: AUD-021 reproduced; not an unconditional pass |
| Browser empty install | Overview, directories, About, Swagger and missing-company route checked; empty states, no overflow/application exception in ordinary flows |
| Browser synthetic populated UI | Company search/deep-link reload, API failure/retry, guest/account save/reload/delete, profile, EN/RU persistence, API English and reduced/manual motion; actual contract API page 2 returns 10 of 24 records with previous/next links |
| Responsive browser | People/company/contracts/groups at 320/768/1440/1920 px; graph at 390 px; no horizontal overflow in the checked cases |
| Browser failure injection | Aborted first-load People chunk reproduces AUD-022; invalid page remains a rejected request, not a successful pagination result |
| Documentation | 39 Markdown files and 236 local links/images/anchors pass; README rendering at 390/1280 px in light/dark loads all five images without overflow; no remote GitHub rendering claim |

Fresh scale probes were controlled synthetic measurements on this laptop:
2,000-company evidence index/component/impact work took 0.6906 s and exposed
global fan-out. D3 settling medians for 50/200/500/1,000 nodes were
29.4/82.1/266.16/677.72 ms (three samples, 96/380/950/1,900 links).
These exclude database/DOM/paint and are not browser FPS, endpoint p95 or capacity
certification. The dead-map cleanup made output equivalent and avoided one call;
single timings were noisy, so no latency gain is claimed.

Tracked gates are in [DEVELOPMENT.md](DEVELOPMENT.md). Audit-specific probes and
aggregate reports stay privately under artifacts/re-audit-2026-10-11/.
The public PostgreSQL/doc runners do not require that folder or working credentials.
A bounded scan of 442 existing tracked/proposed files found no matches for six
meaningful configured credential values or generic private-key/token patterns.
This excludes Git history and unknown/encoded secrets. All six protected-file
hashes (.env, test.py and four dependency manifests/locks) matched; the archived
final audit matched its original SHA-256. No runtime log, schedule, private env,
dump, key, next-app or Compose overlay entered the proposed file set.
The clean build copy predates the final behaviour-neutral cleanup and documentation;
targeted PG/frontend gates ran again after the code changes.

## 7. Unverified boundaries

- Current live source variants, quotas, entitlement, source throughput, national
  coverage and backlog convergence: no new source calls authorised.
- Real inference on this exact cleanup, resolved weights and independent reader/
  prediction usefulness: no new model run or research experiment.
- Public TLS/ingress, real-domain issuance, GPU execution, remote CI/branch rules
  and target-host capacity: no public deployment or remote configuration audit.
- Fresh working-data restore/off-host recovery: this task ran isolated helper tests;
  the [10 October full transfer proof](RECOVERY.md#recorded-restoration-evidence)
  remains historical, not a current backup certification.
- Representative PostgreSQL workload/p95/RSS, broker crash matrix, native disk-full
  behaviour, multi-engine/touch/screen-reader/exact-contrast review and dense browser
  readability: bounded checks do not cover these.
- Every old explanation, all bundled/container OS advisories, original source-data
  distribution rights and complete third-party asset provenance: not certified.
- Exact database-restart exception cause: AUD-021 reproduces the symptom; the
  connection-policy explanation must be confirmed in its fix task.

## 8. Next implementation tasks

1. Dependency remediation (AUD-010), with compatible locks and fresh vendor,
   parser/admin/provider plus full gate checks.
2. Collection/name/status/accounting fixes (AUD-005–008), preserving histories
   and proving repair/replacement behaviour on PostgreSQL.
3. PostgreSQL restart and lazy-chunk recovery (AUD-021/022), with explicit failure
   injection, useful degraded states and repeatable healthy recovery.
4. Hard AI deadline and resolved model provenance (AUD-012/015); old-text review
   remains separate from new constrained publication.
5. CI/native runtime bounds/model independence (AUD-016/017), then explicitly
   authorised bounded source convergence (AUD-009).
6. Measured graph scaling and missing-record UX (AUD-013/014/020), then defence
   rehearsal and target-host/publication/recovery gates.

Acceptance criteria are in the findings table, not implied by task completion.
This audit changes docs and only proven small dead work; it does not mark the
remaining product fixes implemented.
