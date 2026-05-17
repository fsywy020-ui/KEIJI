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
5. `storage/smoke/` outputs after running `python scripts/owner_smoke.py --out-dir storage/smoke` — generated review/status/audit files for manual inspection.

## Owner Review Start Here

For non-engineer owner review, start with `docs/non_engineer_review_guide.md` before reading generated smoke outputs. The recommended review path is:

1. `README.md` — project boundary, safety rules, and local commands.
2. `docs/non_engineer_review_guide.md` — plain-language guide for reading smoke outputs and review packets.
3. `storage/smoke/pending_review.md` — quick pending-review triage after a local smoke run.
4. `storage/smoke/p7_review_packets.md` — detailed P4/P3/P5/P6/P7 human approval packet.
5. `storage/smoke/p8_review_handoff_packets.md` — local-only Codex review-assist safety contract.

`BUY_CANDIDATE` and `TEST_BUY_CANDIDATE` are not purchase approvals. They are human-review candidates. P3 profit output is an operational estimate only and must not be treated as tax or accounting advice.

## Quick Start

Run the local smoke workflow:

```bash
python scripts/owner_smoke.py --out-dir storage/smoke
```

This creates local outputs under `storage/smoke/`:

- `keiji-smoke.sqlite3`
- `owner_review_index.md`
- `pending_review.csv`
- `pending_review.html`
- `pending_review.md`
- `status.json`
- `status.md`
- `audit_log.json`
- `audit_log.md`

For developer-only flows, `scripts/local_smoke.py` still supports direct use with an appropriate Python path. Non-engineer owner review should use `scripts/owner_smoke.py`.

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

## Post-Merge Phase 1: P4〜P7 Offline MVP

Post-Merge Phase 1 adds a local-only flow that a non-engineer can review without connecting to external services:

- **P4 Product Identity** now has stricter edge-case fixtures for capacity, set count, color, edition, domestic/import status, model number conflicts, model notation variations, size, generation, similar-but-different titles, condition differences, bundle/single differences, and accessory differences.
- **P5 Market Monitoring** can import manually prepared local CSV/JSON market observations and expose them through a fake adapter. Live API access remains disabled.
- **P6 Candidate Scoring** combines P4 identity, P3 profit, and P5 market observations into conservative recommendations: `BUY_CANDIDATE`, `TEST_BUY_CANDIDATE`, `WATCH_ONLY`, `BLOCKED`, or `NEEDS_HUMAN_REVIEW`.
- **P7 Human Approval Review Packets** generate local JSON/CSV/Markdown reports that summarize identity, profit, market data, score, budget impact, SKU-limit fit, reasons not to buy, and human checklist items.

Next files to inspect after running the smoke workflow:

1. `data/samples/market_observations.example.csv` — local P5 market observation example.
2. `tests/fixtures/p4/identity_cases.v1.json` — P4 edge-case identity examples.
3. `/tmp/keiji-smoke-p4-p7/p7_review_packets.md` or `storage/smoke/p7_review_packets.md` — P7 human approval review report.
4. `docs/local_offline_operation_guide.md` — local CSV/JSON operation steps.

Safety remains unchanged: KEIJI still does not purchase, pay, list products, log in, use carts, check out, automate browsers, scrape websites, or call live external APIs.

## P8 Codex review-assist Safety Contract

P8 adds a local-only Codex review-assist safety contract. It wraps P7 review packets into `p8_review_handoff_packets.json` and `p8_review_handoff_packets.md` so a human can review a bounded summary with Codex.

P8 does **not** call external agent APIs, open browsers, scrape websites, log in, add items to carts, check out, place orders, execute payments, create listings, or call live external APIs. It also writes `p8_review_handoff_blocked_actions_audit.jsonl` during local smoke runs to demonstrate that forbidden actions are blocked and audited locally.

Additional P8 files to inspect:

1. `docs/codex_review_assist_policy.md` — allowed and forbidden Codex review-assist scope.
2. `docs/codex_review_human_checklist.md` — human checklist before any Codex-assisted review.
3. `docs/blocked_actions_policy.md` — blocked-action categories and audit requirements.
4. `storage/smoke/p8_review_handoff_packets.md` — generated local P8 packet after the smoke workflow.
