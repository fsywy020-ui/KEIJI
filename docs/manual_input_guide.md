# Manual Input Guide

This guide explains how to prepare local candidate files before any live API integration.

## Safety Rules

- Do not add API keys to CSV files.
- Do not include passwords, account IDs, or checkout data.
- The offline batch only evaluates identity/profit and creates review records.
- Purchase and payment must remain manual and outside this MVP automation.

## CSV Template

Copy the template before editing:

```bash
cp data/samples/offline_candidates.template.csv storage/my_candidates.csv
```

Required columns:

```text
source_id,source_title,source_brand,source_model,source_jan,source_asin,source_condition,purchase_price_yen,domestic_shipping_yen,listing_id,marketplace,listing_title,listing_brand,listing_model,listing_jan,listing_asin,listing_condition,expected_sale_price_yen,category,allocated_budget_yen
```

## Field Notes

- `source_*`: purchase-side item information.
- `listing_*`: Amazon-side listing snapshot entered manually.
- `purchase_price_yen`: item purchase amount in JPY.
- `domestic_shipping_yen`: source-side shipping cost in JPY.
- `expected_sale_price_yen`: conservative expected Amazon sale price.
- `allocated_budget_yen`: already allocated purchase budget in the current period.

## Example Run

```bash
PYTHONPATH=src python scripts/run_offline_batch.py \
  --input data/samples/offline_candidates.example.csv \
  --db storage/keiji.sqlite3 \
  --review-csv storage/pending_review.csv
```

Then export reports:

```bash
PYTHONPATH=src python scripts/export_review_report.py \
  --db storage/keiji.sqlite3 \
  --html storage/pending_review.html \
  --markdown storage/pending_review.md
```
