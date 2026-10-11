# Constrained AI explanation follow-up

Date: 10 October 2026. Scope: AUD-002 and the user's selected publication policy.
New explanations publish only prepared, evidence-bound statements selected by
the model. This closes the reproduced arbitrary-prose path for new jobs; it does
not certify old saved explanations, source accuracy or bidding-risk predictions.

## Implemented contract

Prompt `evidence-presentation-5.4` supplies a bounded catalogue for nine supported
finding types. The response contains only finding IDs, wording variant indexes,
ordering, and an optional separate blinded estimate. Paragraphs and follow-up
checks have no free-text field. The primary finding must lead the explanation;
every selected paragraph must have a corresponding check. Selected fact sections
cannot omit an offered finding. The model sees aliases rather than source names,
BINs, IINs or original contact values.

`grounding.py` validates the closed grammar and rebuilds wording from frozen
analysis. `presentation.py` binds amounts/dates to the exact company, retains
stale/undated/failed-attempt qualifiers, distinguishes possible ordinary contact
explanations from facts, and never treats company debt as a person's liability.
Role periods use the graph's start-inclusive/end-exclusive dates. Unknown role
periods do not become simultaneous management or authority over tender decisions.
Contract totals describe volume, not losses or bidding coordination.

Documents use `readable-explanation-5.3`, templates use
`explanation-template-5.3`, and model-selected narratives carry
`grounding_policy: prepared-claims-1`. Rules/analysis hashes remain 5.0. New
publication and cached-result reuse compare the exact re-rendered document/text
with the saved selection; malformed cached rows remain immutable and a fresh
explicit job falls back safely. Safe internal section-only selection remains
supported without claiming narrative provenance.

Local Ollama may make one bounded repair, within the original timeout. Rejected
output is not echoed into repair prompts or public error messages. Hosted
providers do not retry. Provider/grammar failures save a readable fact template,
with explicit fallback provenance. The template states the connection, its
meaning, credited points, next checks and missing coverage. GET reads saved text;
it never creates explanations or calls a model. No migration is needed.

EN/RU interface labels distinguish prepared-statement selection, templates,
fallback and older prose generation. Saved explanatory text remains English.

## Targeted evaluation

The same 20 synthetic unsupported-output cases were used before and after the
change. The old validator accepted 16/20; the new provider and document boundaries
reject 20/20. Job tests also submit all 20 poisoned completions and verify saved
fallback, safe errors, repeat-request reuse, unchanged graph/score and retained
immutable history. Cases include indirect accusations, benign invention,
non-English/confusable text, wrong company/amount, zero-to-debt reversal,
unsupported tender authority and checks that presuppose wrongdoing.

Positive controls cover all nine finding types and both wording variants.
Additional tests cover strict index types, unknown/duplicate IDs, exact company
scope, dated/stale/retained/zero checks, incomplete and boundary role dates,
contract-only summaries, dense groups and altered saved documents/caches.
The old regex validator remains a historical diagnostic, outside publication.

Real local Qwen3:4b passed four full synthetic jobs and five additional difficult
catalogue cases: **9/9 accepted, all on the first attempt**, approximately
4.8-8.3 seconds each on this laptop. Full jobs checked saved API/HTML reads,
deduplication and unchanged public scores. Difficult cases covered mixed
director/contact scope, mixed undated roles, stale/retained/zero finance,
contract-only records and 20 companies with six findings. The latter request
fit the default 8,000-character budget. Output review found no unsupported
assertion in these nine cases; financial follow-ups can still be repetitive and
large exact amounts remain long. This is a targeted regression sample, not a
held-out truthfulness, readability or prediction benchmark.

Private reports and synthetic scripts are under ignored `artifacts/ai-grounding/`;
the four-job report is `artifacts/local-ai/grounding-20261010.json`.
Run `scripts/check_local_ai.py` with a separate `--report-name` to avoid replacing
the user's last demo. Working data, source collection and paid inference are
outside this evaluation. Existing histories are preserved, not regenerated.

## Regression and integrity checks

- Full isolated PostgreSQL suite: 671 tests, zero failures/errors/skips; its
  temporary database was removed. Ten final publication/date tests also passed
  after the last cache-integrity refinement.
- React: 144 tests, TypeScript/Vite production build and formatting passed.
  OpenAPI validation, migration drift and normal strict collectstatic passed.
- Chromium: 18 scenarios at 1440/390 px covered all four saved Qwen cases,
  EN/RU, evidence disclosure and grounded/legacy/fallback provenance. Historical
  and fallback API variants were mocked only in the browser. No overflow,
  application JavaScript errors, failed responses or non-GET requests occurred
  after collectstatic. Language switching preserved disclosure without API calls.
  Actual desktop/mobile viewport captures were inspected; the browser was closed.
- The verified native recovery manifest matched the pre-change database. Final
  fingerprints matched all 51 tables, schema and 49 sequences. Environment,
  learning and dependency files were unchanged. No working regeneration ran.
- Real inference used a separate owned local server and synthetic data only.
  The server was stopped after evaluation; model cache was retained. Native
  collector workers/beat were already stopped and were not restarted.
