# Data readiness and directory visibility

This document describes the current selection and collection rules. The latest
bounded catalogue counts and unresolved defects belong in
[FINAL_AUDIT.md](FINAL_AUDIT.md), not in a second changing status table. The
[9 October checkpoint](archive/2026-10-11/DATA_READINESS.md) preserves the original
implementation checks and their limits.

## What appears in directories

| Surface | Default selection | What it establishes |
| --- | --- | --- |
| Companies | Source-checked profiles | The displayed name and BIN match accepted registry or Adata profile evidence for that exact company. |
| People | Verified identities with an observed current role | An identifier-confirmed saved identity has a role marked current in the observations. This is not proof of the legal appointment period. |
| Company directorships | Current observed records | Current and historical episodes are presented separately; identity evidence and legal dates remain separate properties. |
| Overview counts | Shared directory scopes | Totals describe the corresponding default listings, rather than every legacy row in the database. |

Company checking requires a selected name fact with a successful supported-source
observation, the same supplier, the exact `company:<BIN>` subject, and matching
normalised BIN and displayed name. This is a provenance rule, not a completeness,
freshness or good-standing certificate. A profile can pass it while other fields
or KGD checks are missing.

Pending/all-company and unverified/historical-person choices remain available.
Filtering precedes pagination. Direct links, contract participants and saved graph
history remain readable. The API's optional `profile_status`, `is_verified` and
`has_current_role` filters do not silently restrict compatibility clients that omit
them. Visibility filters are not access control.

A page reload reads committed data and applies the active filters again. A newly
accepted profile can appear then, subject to its search, ordering and page. GET
never collects a source, rebuilds a graph or generates an explanation. A later
failed source request does not erase the last accepted evidence.

## Names, roles and provenance

The same name can belong to different people or to several source-scoped historical
records. Exact verified identifiers permit identity reuse; names alone create
matching candidates. They do not merge people or connect companies in the graph.
A directory row is a saved identity, not a guarantee of a unique physical person.

Source retrieval time, observed current status and legal start/end dates are
separate. Unknown legal dates stay unknown; supplied intervals use an exclusive
end date. Current graph construction filters currently observed roles by the chosen
date. It does not reconstruct all historical appointments. Legacy observation dates
record migration provenance, not a new external check.

Current adapters collect directorship evidence. Founder markup or a director name
does not establish current ownership; empty ownership presentation is hidden.
Court, bankruptcy and restricted-participant integrations are not implemented.
Company arrears are never assigned to a director or owner.

The open corrected-name projection issue is tracked as AUD-006: newer verified
source evidence can coexist with an older People display name. That requires a
source-aware name/alias policy, not name-based deduplication.

## Collection and freshness

Parsers fetch and normalise; ingestion services own persistence and orchestration.
The collector has independent bounded contract, company-profile, KGD-registration
and KGD-debt stages. It rotates stages, limits HTTP attempts, reserves capacity for
previously attempted companies, observes source-specific due times and stops a
host on challenges, denial or repeated transport failures. Successful observations
from older parser versions become eligible for refresh; failed attempts still
respect their retry delay.

Contracts use separate head, archive-history and repair streams. Unfinished page
slices and retry rows preserve progress across restarts. Registry HTML pagination
can change between requests, so repeated reconciliation is necessary and does not
prove national completeness. Discovery pauses when the profile-attempt backlog
reaches its configured high-water limit. An attempted profile is not necessarily
a successfully checked one.

Accepted changes feed saved graph/analysis/template versions through the collection
service. Repeated unchanged evidence does not create new graph versions. Optional
model jobs are separate and deduplicated. New Docker environments leave collection
and automatic model jobs disabled; enabling them is an explicit operational step
in [DEPLOY.md](../DEPLOY.md#collection-and-qwen).

Open audit items remain relevant to operations: the older manual contract-import
path cannot repair some quarantined rows (AUD-005); an expired worker can alter a
replacement run's status (AUD-007); profile/KGD stage record counters under-report
work (AUD-008). These limits are not resolved by the newer crawler's passing fixture
tests. Use source/run outcomes alongside stage counters until those fixes pass
independent recovery tests.

## KGD states

| State | Meaning |
| --- | --- |
| Registration success | The source returned the requested identifier and supported subject type. It says nothing about arrears. |
| Debt success with zero amounts | The separate debt service returned a complete, validated zero result for that company and its reporting dates. |
| Debt success with positive amounts | Saved company-level arrears for the returned dates; not a finding about a person or coordinated bidding. |
| Not checked | No usable check was requested/saved, or prerequisites were not met. The result is unknown. |
| Unavailable or invalid | A source/response problem prevented a confirmed result. This does not mean absence of debt. |
| Retained success after failure | The earlier result remains visible with its original date and the later failed-attempt status. |

Registration and debt have separate clocks and retained successes. Debt requests
require a configured credential for the exact company and supported legal-entity
scope. Entrepreneur registration is supported where explicitly confirmed; current
entrepreneur debt scope remains unverified. A registration token does not authorise
every company's debt check. Fresh retrieval alone also does not establish that the
source's underlying record is complete or current.

## How to assess readiness

`audit_data_quality` reads saved coverage, identity/role consistency, provenance and
safe configuration counts. `ingestion_status` reads saved stage outcomes, backlog,
retry counts and due times. Neither command contacts sources or starts collection.
Actual procedures and commands belong in [DEPLOY.md](../DEPLOY.md).

Before relying on unattended collection, check source-specific attempted,
accepted and fresh denominators; explain unsupported/missing fields; and rehearse
bounded head/history/repair interruption and restart. Source permission and KGD
entitlement need separate confirmation. A completed synthetic cycle, a healthy
worker or a hidden pending row is not evidence of complete coverage.

A reviewed, frozen subset can support a local demonstration with these limits
visible. Pilot/public readiness also requires the remaining
[audit acceptance criteria](FINAL_AUDIT.md) and publication policy. Preserve
original observations, history and failed attempts while improving coverage.
