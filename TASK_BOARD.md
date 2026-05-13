# KEIJI Task Board

## Now

- Treat PR #4 as the main candidate.
- Keep PR #1〜#3 marked as duplicate/no-merge candidates because their scope is included in PR #4.
- Keep test commands runnable locally and through GitHub Actions.

## Next

1. Add more P4 local fixtures for model-number, capacity, set-count, and edition extraction edge cases.
2. Expand P4 extraction rules only when covered by deterministic local tests.
3. Split P3 shipping assumptions into a dedicated `shipping_estimator.py` module.
4. Split P3 risk penalties into a dedicated `risk_adjuster.py` module.
5. Add status/report tests for any new P3 output fields.

## Later

- Add explicit approval records and documentation before any real external API adapter is activated.
- Add richer human review packet exports for non-engineer operations.
- Add CI artifacts only if they do not expose sensitive data and do not require external services beyond GitHub Actions itself.

## Done

- P4 before P3 offline MVP foundation.
- Versioned local configs and dependency-free config loader.
- SQLite persistence and audit records.
- Offline CLI scripts and smoke workflow.
- Local review/status/audit exports.
- Unit, integration, and contract tests.
- `STATUS.md` for PR #4 duplicate-candidate handling.
- GitHub Actions test workflow.
