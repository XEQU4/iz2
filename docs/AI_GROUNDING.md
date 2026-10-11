# AI explanation contract

Current reference, reviewed 11 October 2026. IZ2 uses a language model to select
and order prepared statements about saved evidence. It does not let the model
create identities, relationships, financial findings or the public review score.
Template-only operation remains the default.

## Selection and rendering

The provider receives a bounded catalogue of wording choices for supported
findings: shared address, phone, email, director, owner, mixed person roles,
company arrears, dated zero arrears and stored contract totals. Company aliases
replace source names, BINs, IINs and original contact values before inference.

The response contains finding IDs, integer variant indexes and ordering.
Paragraphs and follow-up checks have no free-text field. Every offered finding
must appear once in the fact sections. The highest-priority offered finding
leads the narrative, and each selected paragraph has a corresponding check.
Input limits can reduce the offered catalogue; they do not remove facts from the
saved analysis. An optional blinded model estimate is stored separately and
never replaces the deterministic public review score.

[grounding.py](../apps/ai/grounding.py) validates the closed response grammar.
[presentation.py](../apps/ai/presentation.py) renders wording from frozen facts,
keeping amounts and dates attached to their company. It retains stale, undated
and failed-attempt qualifiers, treats ordinary explanations for shared contacts
as possibilities, and keeps company debt separate from personal liability.
Role periods are start-inclusive and end-exclusive. Unknown dates establish
neither simultaneous roles nor authority over tender decisions. Contract totals
describe recorded activity, not losses or coordinated bidding.

| Component | Current version |
| --- | --- |
| Provider prompt | `evidence-presentation-5.4` |
| Saved document | `readable-explanation-5.3` |
| Template | `explanation-template-5.3` |
| Grounding policy | `prepared-claims-1` |
| Public review rules | `review-rules-5.0` |

## Publication, reuse and fallback

[services.py](../apps/ai/services.py) re-renders current-format selections and
compares both saved text and document before publication or reuse.
[jobs.py](../apps/ai/jobs.py) deduplicates requests and fences publication against
the latest requested job, current graph/input hash and provider configuration.
Malformed cached results remain immutable; a fresh explicit job can publish a
safe fallback. Internal section-only selections remain supported without
claiming model-narrative provenance.

A provider or grammar failure saves a labelled fact template covering the
connection, its meaning, credited points, follow-up checks and missing evidence.
Local Ollama may make one repair attempt using the remaining configured budget;
hosted providers do not retry. Rejected output is not echoed into the repair
prompt or public errors. This budget is not yet a strict wall-clock deadline.

GET reads saved explanations and never starts generation. Older prose remains
readable under its original method and is not retroactively certified by the
current grammar. EN/RU translates interface labels, not immutable saved English
explanations. The legacy regex diagnostics remain outside the publication gate.

## Limits and verification

Prepared wording prevents unsupported provider prose from entering new current-
format explanations. It cannot establish that a source is accurate, resolve a
mistaken identity, supply missing bids or prove coordinated behaviour. No
independent prediction or reader-usefulness benchmark has established a benefit
from model selection over the template.

Two operational gaps remain: streaming reads can exceed the configured total
timeout, and provenance records `AI_MODEL_REVISION` as configured rather than
resolving the actual model digest. Replacing weights behind an unchanged tag
therefore is not automatically reflected in the reuse key. Failed attempts also
lack complete timing/token accounting. See AUD-012 and AUD-015 in the
[current audit](FINAL_AUDIT.md).

Tracked regression tests cover the closed grammar, unsupported claims, exact
company/date/amount binding, fallback, altered caches, stale publication and
legacy provenance: [grounding tests](../apps/ai/test_grounding.py),
[publication tests](../apps/ai/test_publication_grounding.py),
[job tests](../apps/ai/tests.py) and
[API provenance tests](../apps/api/test_document_provenance.py).
The [current audit](FINAL_AUDIT.md) records the checks rerun against this revision.

The [10 October evaluation record](archive/2026-10-11/AI_GROUNDING.md#targeted-evaluation)
contains the historical 20-case adversarial comparison and nine real synthetic
Qwen runs. Those results describe that dated sample, not a current full-system
pass or a population accuracy estimate. Model probes require explicit inference
authorisation; use a separate report name to preserve earlier results. Runtime
setup and deployment choices belong in [DEPLOY.md](../DEPLOY.md).
