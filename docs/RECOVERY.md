# Backup and recovery

Use a verified backup before changing schema or algorithms that can affect saved
data. A dump file or matching checksum alone does not prove recoverability: restore
into a separate empty target and compare the result. Keep the source database
until the restored application has been checked.

[DEPLOY.md](../DEPLOY.md#transfer-the-native-database-before-starting-the-application)
is the authoritative command sequence for native transfer, Docker backup and
empty-target restore. This document explains the verification scope and the
recorded evidence. The earlier dated recovery diary is preserved in the
[recovery archive](archive/2026-10-11/RECOVERY.md).

## Choose the required verification scope

| Operation | Consistency and comparison | Requirement |
| --- | --- | --- |
| Native backup with `--verify-restore` | Exported read-only repeatable-read snapshot shared by `pg_dump` and table fingerprints; public table columns, row counts, multiset row hashes and migration history | Local PostgreSQL and permission to create/drop the helper's separate verification database |
| Native backup with `--verify-restore --deployment-manifest` | The table comparison above plus schema metadata, defaults, indexes, constraints and sequence definitions/state; writes a portable transfer manifest | Stop all application writers before starting, because sequence state is outside the row snapshot |
| Compose backup and restore | Quiet application containers, before/after manifest equality, dump checksum, then full table/schema/sequence comparison on a separate empty restore target | Explicit private environment/project selection, same PostgreSQL major version and an independent successful restore |

The native dump includes more than the basic table comparison certifies. Without
`--deployment-manifest`, a passed row/column comparison must not be described as
proof that every default, constraint, index, sequence value, role or privilege was
preserved. The exported MVCC snapshot keeps table data coherent while ordinary
writes continue; it does not freeze sequence state.

Full transfer verification needs quiet writers. The native helper does not stop
them. The Compose helper rejects active, paused or restarting web, worker,
AI-worker, beat or migration containers, but the operator must also account for
external database clients. Merely keeping the website unused does not stop jobs.

## Safe recovery sequence

1. Choose and record the source database, target project and private environment.
   Preserve existing database names and Compose namespace/volume identifiers.
   Renaming a project can select empty replacement volumes.
2. For a deployment manifest or transfer, stop every writer using the maintenance
   procedure in [DEPLOY.md](../DEPLOY.md#transfer-the-native-database-before-starting-the-application).
   Keep the database running. Do not interrupt unrelated user services.
3. Create the backup and, for native verification, request an independent restore.
   Retain the dump and companion reports together. Check the verification result,
   rather than relying only on the command's top-level success status.
4. Restore into a separate empty target before running application migrations there.
   Use the recorded checksum and manifest. Never use the working database as a
   trial restore target.
5. Require equal table, migration and intended schema/sequence metadata. Then start
   the target and inspect health, authentication, a saved graph/history and a saved
   explanation with collection and model generation still disabled.
6. Retain the previous database and secured backup until verification and cutover
   are complete. Resuming writers or changing the application's database connection
   is a separate, deliberate operational action.

Native verification creates only a generated `gpg_restore_verify_<UUID>` database
on the local PostgreSQL server. Cleanup validates the exact name, excludes the
source and removes only that database. A failed cleanup reports the remaining
name; do not delete by an approximate name or broad prefix.

Compose restore requires an empty database, verifies the dump format/checksum,
uses a single transaction with `--exit-on-error`, and compares the restored
manifest. It does not clean, drop or replace an existing schema. If comparison
fails after restoration, the target is retained for inspection rather than erased
for another attempt. Do not use `docker compose down --volumes` on data to retain.

## Reports and credentials

| Helper output | How to interpret it |
| --- | --- |
| Native `.dump` and `.json` | Require `status: passed`, `verification.status: passed`, empty table differences, migration verification and successful temporary-database cleanup. |
| Native `.deployment.json` | Portable table/schema/sequence manifest bound to the dump checksum. Check that its restore verification passed; manifest creation alone is not restoration proof. |
| Compose `.dump` and `.json` | The backup report starts with `restore_verification: not_yet_performed`. Pass that JSON to a separate restore rehearsal. |
| Compose `restore_<UUID>.json` | A passed comparison records `data_schema_and_sequence_state_equal: true`; retain it with the backup. |

Outputs stay in ignored `artifacts/`; neither dumps nor private reports belong in
Git or images. Helpers refuse writable output paths outside that directory.
Restrict access and preserve a secured copy outside the machine being protected.

The native helper reads root `.env` and process variables. `PGDATABASE`, `PGUSER`,
`PGPASSWORD`, `PGHOST` and `PGPORT` take precedence over corresponding `DB_*`
settings; process values override file values. Ambiguous libpq routing and
connection-string database names are rejected. Compatible `pg_dump`/`pg_restore`
are discovered locally or selected through `--pg-bin`. Passwords pass through
child-process environment, not command arguments or printed reports.

Compose uses the explicitly supplied environment file and project. Native and
Docker databases are independent copies; they do not synchronise. Keep that
selection consistent with [startup and upgrades](../DEPLOY.md#operations-and-upgrades).
Do not print expanded Compose configuration with private secrets.

## Recorded restoration evidence

The latest recorded full transfer rehearsal is **10 October 2026**: a native
backup was restored independently and into an empty Linux Compose PostgreSQL 17
target. Public tables, migration history, schema metadata and sequence state
matched. A backup of the isolated Compose rehearsal was then restored into a
second empty project. Owned verification resources were removed; the native
source was preserved.

Exact filenames, checksums, comparison scope and dated counts remain in the
[10 October transfer record](archive/2026-10-11/RECOVERY.md#native-to-linux-compose-recovery-10-october-2026).
An earlier [10 October table-only verification](archive/2026-10-11/RECOVERY.md#final-audit-recovery-and-date-policy-follow-up-10-october-2026)
has a narrower scope and must not be substituted for that full transfer proof.
These historical checks do not certify a newer backup or the current contents
of a database that has changed since then. A new data-changing operation needs a
current backup and a restoration check appropriate to its scope.

The repeat audit exercised isolated tests; it did not perform a new working-data
backup, transfer or cutover. Current test results and remaining gates are in
[FINAL_AUDIT.md](FINAL_AUDIT.md).

## Remaining recovery limits

Verified transfer currently requires the same PostgreSQL major version. Do not
attach an old PostgreSQL 16 volume directly to PostgreSQL 17; a cross-major upgrade
needs a separately rehearsed dump/restore procedure. Original ownership and ACLs
are mapped to the target database user. Custom roles, tablespaces, custom schemas
or routines, external media, private environment files and model caches require
separate preservation and validation.

Changing `SECRET_KEY` invalidates existing sessions. Restoring database contents
does not regenerate immutable explanations, collect missing sources or prove
current source availability. Database recovery and external-data completeness
are different checks.

Automated off-host backup scheduling, retention, encryption/key recovery and
restoration on the chosen production server remain operational work. No recovery
point objective or recovery time objective has been measured. Same-disk backups
help recover from bad changes; they do not protect against loss of that disk.
