# P3 Profit Calculation Engine Specification

## 1. Objective

The P3 Profit Calculation Engine estimates whether a P4-approved product candidate has sufficient resale profit for the MVP. All shipping, fee, and risk values are operational estimates for local purchase-review screening, not tax or accounting advice.

P3 must not run before P4. P3 must not override P4 safety decisions.

## 2. Inputs

P3 accepts:

- Approved P4 decision.
- Canonical product.
- Source offer purchase price.
- Source shipping cost.
- Expected Amazon sale price from local fixture, manual input, or approved adapter.
- Category and fulfillment assumptions.
- Current capital allocation state.

## 3. Decisions

| Decision | Meaning |
|---|---|
| `pass` | Candidate can be sent to human purchase review. |
| `review` | Profit may be acceptable but needs human review. |
| `fail` | Profit threshold is not met. |
| `blocked` | Budget, risk, or policy violation. |
| `skipped` | P4 gate did not allow P3 calculation. |

## 4. Module Structure

```text
p3_profit/
  input_models.py
  price_model.py
  fee_estimator.py
  shipping_estimator.py
  tax_estimator.py
  roi_calculator.py
  risk_adjuster.py
  capital_guard.py
  decision.py
  explain.py
  engine.py
```

## 5. Module Responsibilities

### `input_models.py`

Defines the P3 input, fee breakdown, shipping summary, structured operational risk details, profit result, and final decision contracts. Optional local/manual fields such as price uncertainty and return risk can feed conservative risk adjustment without any live lookup.

### `price_model.py`

Determines the conservative expected sale price. Initial MVP uses local/manual price data only.

### `fee_estimator.py`

Estimates Amazon fees with configurable category fee rates and default fee fallback. Platform fee remains category-rate driven, while fulfillment and packaging/other buffer values can be supplied by the local shipping estimator so existing fee math stays deterministic.

### `shipping_estimator.py`

Reads local `shipping` rules from `config/profit_rules.v1.yaml` and returns inbound shipping, packaging cost, fulfillment fee, and assumptions. Inbound shipping remains local/manual input. The estimator does not look up live shipping rates and does not execute fulfillment, purchase, payment, listing, login, cart, checkout, browser automation, scraping, external agent API, or live external API actions.

### `tax_estimator.py`

Initial MVP treats prices as tax-inclusive for purchase-decision purposes. It must not claim to provide accounting or tax advice.

### `roi_calculator.py`

Calculates:

```text
total_cost = purchase_price + inbound_shipping + platform_fee + fulfillment_fee + storage_fee + other_cost
net_profit = expected_sale_price - total_cost
roi_percent = net_profit / purchase_cost * 100
profit_margin_percent = net_profit / expected_sale_price * 100
break_even_price = total_cost
```

### `risk_adjuster.py`

Applies deterministic local-config operational risk buffers and emits structured risk details. The current MVP covers:

- Price uncertainty.
- Return risk.
- Budget concentration.

Risk adjustment replaces the former reason-count penalty with named details containing a penalty amount, severity, and human-readable explanation. It affects `risk_adjusted_profit_yen`; core pass/fail/review/block decisions remain driven by profit thresholds and capital guardrails unless those policies are explicitly changed in config and tests. These buffers are operational estimates only and are not tax, accounting, or financial advice.

### `capital_guard.py`

Enforces:

- Per-SKU maximum purchase amount: 5,000 JPY.
- Initial total budget: 50,000 JPY.
- Review warning near per-SKU limit.
- Review warning when budget utilization is high.

### `decision.py`

Produces `pass`, `review`, `fail`, `blocked`, or `skipped`.

### `explain.py`

Creates a human-readable profit summary and required approval notes.

### `engine.py`

Runs:

```text
P4 gate -> price selection -> shipping estimate -> fee estimate
-> ROI calculation -> capital guard -> risk adjustment
-> decision -> explanation -> persist/audit
```

## 6. Initial Threshold Policy

Recommended starting thresholds:

- Minimum net profit: 500 JPY.
- Minimum ROI: 20%.
- Review if purchase amount is 4,500 JPY or higher.
- Block if purchase amount is above 5,000 JPY per SKU.
- Block if monthly budget would exceed 50,000 JPY.

## 7. Output / Persistence / Reports

P3 output includes `risk_adjusted_profit_yen` and structured in-memory `risk_details`. Review packets include `risk_details` for human visibility. SQLite persistence and existing review reports keep the current schema and store the primary decision reasons plus numeric risk-adjusted profit, so no schema migration is required for this change.

## 8. Purchase Restriction

P3 may create a purchase candidate, but it must not execute purchase or payment. Every purchase candidate must have `requires_human_approval = true`. P3 must not implement purchase, payment, listing, checkout, login, cart operation, browser automation, scraping, external agent API, or live external API behavior without separate explicit approval.
