# KEIJI Status

## PR Handling Policy

- Main candidate: **PR #4**.
- Merge policy: **do not merge to `main` from this task**.
- Duplicate candidates: **PR #1, PR #2, and PR #3**.

## PR #4 Inclusion Check

Based on the current branch contents and the supplied PR #4 diff summary, PR #4 includes the earlier duplicate candidate scopes:

| Candidate | Status | Inclusion evidence in PR #4/current branch | Merge decision |
|---|---|---|---|
| PR #1 | Included in PR #4 | Offline-first P4/P3 MVP package, configs, docs, fixtures, and tests are present. | Duplicate; merge not required. |
| PR #2 | Included in PR #4 | Local smoke workflow, audit export CLI/helpers, review/status exports, and integration coverage are present. | Duplicate; merge not required. |
| PR #3 | Included in PR #4 | P4 attribute extraction, brand matching, hard exclusion rules, scoring split, and backlog progress tracking are present. | Duplicate; merge not required. |

Conclusion: **PR #1〜#3 are duplicate candidates and do not need to be merged because PR #4 contains their functional scope.**

## Current Implementation Status

- P4 product identity runs before P3 profit calculation.
- P4 supports deterministic local normalization, attribute extraction, identifier/brand/title/variant/condition matching, hard exclusions, scoring, and evidence-rich decisions.
- P3 supports deterministic local fee estimation, ROI/net profit/break-even calculation, capital guardrails, and pass/review/fail/blocked/skipped decisions.
- SQLite persistence, audit logs, approval records, review/status/audit exports, and offline CLI workflows are present.
- Purchase, payment, checkout, login, listing execution, browser automation, and live external API access are not implemented.

## Test Readiness

The repository is ready to run either of the following local test commands:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
python -m pytest -q
```

A GitHub Actions workflow has also been added at `.github/workflows/tests.yml` to run unittest, pytest, and the offline smoke workflow on pull requests, pushes to tracked branches, and manual dispatch.

## Latest Local Test Results

- PASS: `PYTHONPATH=src python -m unittest discover -s tests -v` — 42 tests passed.
- PASS: `python -m pytest -q` — 42 tests and 8 subtests passed.
- PASS: `PYTHONPATH=src python scripts/local_smoke.py --out-dir /tmp/keiji-smoke-check` — smoke workflow completed with `smoke_ok=true` and processed 1 sample candidate.

## Unfinished Tasks

- Expand P4 attribute extraction with more local fixtures for category-specific model/capacity/set-count patterns.
- Split P3 shipping and risk adjustment into dedicated local-config-driven modules when the current simple assumptions need more detail.
- Keep external API adapters disabled until explicit approval, credentials, and adapter-specific tasks are provided.
- Keep purchase/payment/listing execution outside MVP automation and under human approval.

## Blockers

- No current blocker for local development and tests.
- External services, API keys, paid services, purchase execution, payment execution, listing execution, and `main` merge remain out of scope for this task.
