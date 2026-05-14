# Local Offline Operation Guide

## Purpose

Run KEIJI locally without internet access, API credentials, browser automation, Manus integration, purchase execution, or payment execution.

## Workflow

1. Prepare a CSV or JSON candidate file.
2. Run the offline batch.
3. Review generated CSV/HTML/Markdown reports.
4. Record a human review decision if appropriate.
5. Perform any purchase/payment manually outside this system.


## 0. Quick Smoke Test

To verify the local offline workflow end-to-end:

```bash
PYTHONPATH=src python scripts/local_smoke.py
```

This writes review, status, and audit outputs under `storage/smoke/`.

## 1. Prepare Input

Use the sample template:

```bash
cp data/samples/offline_candidates.template.csv storage/my_candidates.csv
```

Fill in source and Amazon listing snapshot fields manually.


## 1.5 Validate Input

Before running a batch, validate the CSV/JSON file:

```bash
PYTHONPATH=src python scripts/validate_candidates.py \
  --input storage/my_candidates.csv
```

Warnings do not stop processing, but errors should be fixed first.

## 2. Run Offline Batch

```bash
PYTHONPATH=src python scripts/run_offline_batch.py \
  --input storage/my_candidates.csv \
  --db storage/keiji.sqlite3 \
  --review-csv storage/pending_review.csv
```

## 3. Export Human Review Reports

```bash
PYTHONPATH=src python scripts/export_review_report.py \
  --db storage/keiji.sqlite3 \
  --html storage/pending_review.html \
  --markdown storage/pending_review.md
```

## 4. Record Human Review

```bash
PYTHONPATH=src python scripts/review_candidate.py \
  --db storage/keiji.sqlite3 \
  --candidate-id <candidate_id> \
  --decision approved \
  --reviewer "human-reviewer" \
  --comment "manual visual check completed"
```

Allowed decisions:

- `approved`
- `rejected`
- `needs_more_info`

## Safety Notes

- Approval changes local review state only.
- Approval does not purchase, pay, log in, open a browser, or call APIs.
- Keep external API access disabled until explicit approval and credentials are ready.


## 5. Export Status Summary

After running batches or recording reviews, export a local status summary:

```bash
PYTHONPATH=src python scripts/export_status_report.py \
  --db storage/keiji.sqlite3 \
  --json storage/status.json \
  --markdown storage/status.md
```

The summary includes counts, P4/P3 decision distribution, candidate statuses, and budget usage.


## 6. Export Audit Log

To inspect the local audit trail:

```bash
PYTHONPATH=src python scripts/export_audit_log.py \
  --db storage/keiji.sqlite3 \
  --json storage/audit_log.json \
  --markdown storage/audit_log.md
```

## 7. P5〜P7 Local Market Data and Review Packet Flow

Post-Merge Phase 1 can also produce a local human approval packet from local market observations.

### 7.1 Prepare local market observations

Use the sample P5 CSV as a template:

```bash
cp data/samples/market_observations.example.csv storage/my_market_observations.csv
```

Fill it manually with observed Amazon/local market facts such as source, observed time, product title, JAN, ASIN, model number, price, shipping fee, rank, category, stock status, seller count, condition, and reference URL or memo.

### 7.2 Run smoke with P5〜P7 outputs

```bash
PYTHONPATH=src python scripts/local_smoke.py \
  --input data/samples/offline_candidates.example.csv \
  --market-input data/samples/market_observations.example.csv \
  --out-dir storage/smoke
```

The smoke workflow now writes the original P4/P3 review/status/audit files plus P7 review packet files:

- `storage/smoke/p7_review_packets.json`
- `storage/smoke/p7_review_packets.csv`
- `storage/smoke/p7_review_packets.md`

### 7.3 Review the P7 packet

Open `p7_review_packets.md` first. It summarizes:

- candidate ID and product name,
- JAN / ASIN / model number,
- P4 product identity decision,
- P3 profit estimate,
- P5 local market observations,
- P6 score and recommendation,
- reasons not to purchase,
- human checklist items,
- impact on the 50,000 JPY initial budget,
- whether the 5,000 JPY per-SKU limit is satisfied.

### 7.4 Safety reminder

P7 packets are local review files only. They do not send Slack, Discord, LINE, or email notifications. They do not purchase, pay, list products, log in, add items to a cart, check out, automate browsers, scrape websites, or call live external APIs.

## 8. P8 Manus Handoff Packet Review

P8 prepares local handoff files that a human may review before any future Manus-assisted workflow. It does not connect to Manus or any external service.

### 8.1 Generate P8 handoff files

Run the local smoke workflow:

```bash
PYTHONPATH=src python scripts/local_smoke.py \
  --input data/samples/offline_candidates.example.csv \
  --market-input data/samples/market_observations.example.csv \
  --out-dir storage/smoke
```

The smoke workflow writes P8 local handoff files:

- `storage/smoke/p8_manus_handoff_packets.json`
- `storage/smoke/p8_manus_handoff_packets.csv`
- `storage/smoke/p8_manus_handoff_packets.md`

### 8.2 Review before Manus handoff

Open `p8_manus_handoff_packets.md` and verify:

- P4 identity result is safe enough for human consideration.
- P3 profit and break-even information are visible.
- P5 market data summary is present or clearly marked missing.
- P6 recommendation is treated as review guidance, not purchase permission.
- P7 review status is pending or explicitly recorded.
- The 5,000 JPY per-SKU cap and 50,000 JPY initial budget impact are visible.
- Forbidden operations and allowed Manus tasks are visible.

### 8.3 Safety reminder

P8 files are local handoff artifacts only. They must not contain passwords, API keys, tokens, credit-card details, payment details, login credentials, Cookies, sessions, personal information, or automatic-purchase execution data.

Manus is still forbidden from login, cart operation, checkout, purchase, payment, listing, browser automation, scraping, live external API access, or external operation without human approval.
