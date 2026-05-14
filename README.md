# KEIJI

KEIJI is an offline-first resale automation MVP.

It is designed to evaluate product identity (P4), calculate profit (P3), persist decisions, create human-review purchase candidates, and export local review reports without external API access or automated purchasing.

## Safety Boundaries

- Internet/API access is off by default.
- P4 product identity runs before P3 profit calculation.
- Purchase and payment execution are not implemented.
- Human approval is required for any purchase decision.
- Cross-project artifacts must not be mixed into this repository.


## Non-Engineer Summary of PR #4

PR #4 is the main KEIJI MVP candidate. In plain language, it adds a local-only safety system for resale decisions:

- First, KEIJI checks whether the item being considered is actually the same product as the Amazon listing.
- Only after that identity check passes does KEIJI estimate profit, fees, budget impact, and whether the result should pass, fail, or require human review.
- KEIJI records decisions and audit logs locally so a human can inspect why something passed, failed, or was blocked.
- KEIJI can export review, status, and audit reports for manual operations.
- KEIJI does **not** buy products, pay for products, log in to stores, add items to carts, check out, list products, scrape websites, or call live external APIs in this MVP.
- PR #4 is intended to supersede duplicate PR candidates #1〜#3 because it contains the combined offline MVP, CLI, docs, tests, audit export, smoke workflow, and P4 refinement work.


## First Files for Non-Engineers After Merge

If PR #4 is merged, start with these files in order:

1. `README.md` — quick overview, safety boundaries, and local command examples.
2. `STATUS.md` — merge readiness, PR #1〜#3 duplicate handling, latest test results, blockers, and human-decision items.
3. `TASK_BOARD.md` — who should work on P4, P3, tests/data, and docs next.
4. `docs/local_offline_operation_guide.md` — step-by-step local offline operation flow.
5. `storage/smoke/` outputs after running `PYTHONPATH=src python scripts/local_smoke.py` — generated review/status/audit files for manual inspection.

## Quick Start

Run the local smoke workflow:

```bash
PYTHONPATH=src python scripts/local_smoke.py
```

This creates local outputs under `storage/smoke/`:

- `keiji-smoke.sqlite3`
- `pending_review.csv`
- `pending_review.html`
- `pending_review.md`
- `status.json`
- `status.md`
- `audit_log.json`
- `audit_log.md`

## Manual Candidate Flow

Validate input:

```bash
PYTHONPATH=src python scripts/validate_candidates.py \
  --input data/samples/offline_candidates.example.csv
```

Run offline P4/P3:

```bash
PYTHONPATH=src python scripts/run_offline_batch.py \
  --input data/samples/offline_candidates.example.csv \
  --db storage/keiji.sqlite3 \
  --review-csv storage/pending_review.csv
```

Export review reports:

```bash
PYTHONPATH=src python scripts/export_review_report.py \
  --db storage/keiji.sqlite3 \
  --html storage/pending_review.html \
  --markdown storage/pending_review.md
```

Export status and audit reports:

```bash
PYTHONPATH=src python scripts/export_status_report.py \
  --db storage/keiji.sqlite3 \
  --json storage/status.json \
  --markdown storage/status.md

PYTHONPATH=src python scripts/export_audit_log.py \
  --db storage/keiji.sqlite3 \
  --json storage/audit_log.json \
  --markdown storage/audit_log.md
```

Record a human review decision:

```bash
PYTHONPATH=src python scripts/review_candidate.py \
  --db storage/keiji.sqlite3 \
  --candidate-id <candidate_id> \
  --decision needs_more_info \
  --reviewer "human-reviewer" \
  --comment "manual visual check required"
```

## Tests

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
python -m pytest -q
```
