# P3 Profit Calculation Engine Specification

## 1. Objective

The P3 Profit Calculation Engine estimates whether a P4-approved product candidate has sufficient resale profit for the MVP.

P3 must not run before P4. P3 must not override P4 safety decisions.

## 2. Inputs

P3 accepts:

- Approved P4 decision.
- Canonical product.
- Source offer purchase price.
- Source shipping cost.
- Expected Amazon sale price from local fixture, manual input, or approved adapter.
- Conservative buffer/reserve cost configured as local marketplace assumptions.
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

Defines the P3 input, fee breakdown, profit result, risk flags, and final decision contracts.

### `price_model.py`

Determines the conservative expected sale price. Initial MVP uses local/manual price data only.

### `fee_estimator.py`

Estimates Amazon fees with configurable category fee rates, default fee fallback, fulfillment/storage costs, and configured buffer/reserve cost.

### `shipping_estimator.py`

Estimates inbound shipping, fulfillment, self-shipping, packaging, and buffer costs.

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

Applies conservative penalties for:

- Sale price uncertainty.
- Unknown sales rank.
- High competition.
- Low identity confidence.
- Return risk.
- Fee uncertainty.
- Budget concentration.

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
P4 gate -> price selection -> fee estimate -> shipping estimate
-> ROI calculation -> risk adjustment -> capital guard
-> decision -> explanation -> persist/audit
```

## 6. Initial Threshold Policy

Recommended starting thresholds:

- Minimum net profit: 500 JPY.
- Minimum ROI: 20%.
- Review if purchase amount is 4,500 JPY or higher.
- Block if purchase amount is above 5,000 JPY per SKU.
- Block if monthly budget would exceed 50,000 JPY.

## 7. Purchase Restriction

P3 may create a purchase candidate, but it must not execute purchase or payment. Every purchase candidate must have `requires_human_approval = true`.
