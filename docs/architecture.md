# KEIJI MVP Architecture

## 1. Recommended Folder Structure

```text
KEIJI/
  AGENTS.md
  README.md
  docs/
    PRD.md
    architecture.md
    approval_policy.md
    operations_manual.md
    test_plan.md
    P4_product_identity_engine_spec.md
    P3_profit_engine_spec.md
    P3_P4_integration_flow.md
    decisions/
  config/
    product_identity_rules.v1.yaml
    profit_rules.v1.yaml
    risk_policy.v1.yaml
    approval_policy.v1.yaml
    external_access_policy.v1.yaml
  src/
    keiji/
      common/
      db/
      p4_identity/
      p3_profit/
      pipeline/
      approval/
      integrations/
  tests/
    fixtures/
      p4/
      p3/
    unit/
    integration/
    regression/
  data/
    samples/
  storage/
```

The initial implementation should create documentation, configuration, and test fixtures before production code.

## 2. Database Design

The first database can be SQLite for local MVP development, with table and type choices kept compatible with PostgreSQL.

### 2.1 Entity Flow

```text
source_offers
  -> p4_identity_runs
  -> product_identity_decisions
  -> canonical_products
  -> p3_profit_runs
  -> profit_estimates
  -> purchase_candidates
  -> human_approvals
  -> audit_logs
```

### 2.2 Tables

#### `source_offers`

Stores purchase-side source items.

| Column | Purpose |
|---|---|
| `id` | Source offer ID. |
| `source_type` | `manual`, `csv`, `fixture`, or future approved adapter. |
| `source_name` | Store or dataset name. |
| `source_url` | Optional URL. |
| `title` | Raw source title. |
| `brand_raw` | Raw source brand. |
| `model_raw` | Raw source model. |
| `jan_raw` | Raw JAN/EAN/UPC. |
| `asin_raw` | Optional ASIN candidate. |
| `condition_raw` | Raw condition. |
| `purchase_price_yen` | Item purchase price. |
| `domestic_shipping_yen` | Purchase-side shipping. |
| `quantity_available` | Available quantity. |
| `captured_at` | Data capture timestamp. |
| `created_at` | Record creation timestamp. |

#### `market_listings`

Stores Amazon-side listing candidates.

| Column | Purpose |
|---|---|
| `id` | Listing ID. |
| `marketplace` | Initial value: `amazon_jp`. |
| `asin` | Amazon ASIN. |
| `jan` | JAN/EAN/UPC. |
| `title` | Marketplace title. |
| `brand` | Marketplace brand. |
| `model` | Marketplace model. |
| `category` | Marketplace category. |
| `condition_policy` | Sellable condition policy. |
| `sales_rank` | Optional future metric. |
| `buybox_price_yen` | Optional sale price input. |
| `lowest_price_yen` | Optional conservative price input. |
| `captured_at` | Data capture timestamp. |

#### `canonical_products`

Stores normalized products created from safe P4 identity decisions.

| Column | Purpose |
|---|---|
| `id` | Canonical product ID. |
| `primary_marketplace` | Initial value: `amazon_jp`. |
| `primary_asin` | Primary ASIN. |
| `jan` | JAN/EAN/UPC. |
| `brand_normalized` | Normalized brand. |
| `model_normalized` | Normalized model. |
| `title_normalized` | Normalized product title. |
| `variant_key` | Color, size, capacity, quantity, edition key. |
| `created_by_identity_run_id` | P4 run that created this record. |
| `created_at` | Record creation timestamp. |

#### `p4_identity_runs`

Stores each P4 execution.

| Column | Purpose |
|---|---|
| `id` | P4 run ID. |
| `rules_version` | Product identity rules version. |
| `input_offer_id` | Source offer ID. |
| `status` | `completed` or `failed`. |
| `started_at` | Start timestamp. |
| `finished_at` | Finish timestamp. |
| `error_message` | Failure details. |

#### `product_identity_decisions`

Stores P4 decisions and explanations.

| Column | Purpose |
|---|---|
| `id` | Decision ID. |
| `p4_run_id` | P4 run ID. |
| `source_offer_id` | Source offer ID. |
| `market_listing_id` | Market listing ID. |
| `canonical_product_id` | Canonical product ID when available. |
| `decision` | `same`, `different`, `ambiguous`, or `blocked`. |
| `confidence_score` | 0.0-1.0 confidence. |
| `match_score` | Overall match score. |
| `identifier_score` | Identifier score. |
| `title_score` | Title score. |
| `brand_score` | Brand score. |
| `variant_score` | Variant score. |
| `condition_score` | Condition score. |
| `block_reason` | Block reason if any. |
| `explanation_json` | Machine-readable explanation. |
| `requires_human_review` | Human review flag. |
| `created_at` | Decision timestamp. |

#### `p3_profit_runs`

Stores each P3 execution.

| Column | Purpose |
|---|---|
| `id` | P3 run ID. |
| `rules_version` | Profit rules version. |
| `identity_decision_id` | P4 decision ID. |
| `status` | `completed`, `skipped`, or `failed`. |
| `skip_reason` | Reason P3 did not run. |
| `started_at` | Start timestamp. |
| `finished_at` | Finish timestamp. |

#### `profit_estimates`

Stores P3 calculations.

| Column | Purpose |
|---|---|
| `id` | Profit estimate ID. |
| `p3_run_id` | P3 run ID. |
| `source_offer_id` | Source offer ID. |
| `canonical_product_id` | Canonical product ID. |
| `expected_sale_price_yen` | Expected Amazon sale price. |
| `purchase_price_yen` | Purchase price. |
| `inbound_shipping_yen` | Purchase-side shipping. |
| `platform_fee_yen` | Amazon fee estimate. |
| `fulfillment_fee_yen` | Fulfillment/shipping estimate. |
| `storage_fee_yen` | Storage estimate. |
| `other_cost_yen` | Buffer and miscellaneous costs. |
| `gross_profit_yen` | Gross profit. |
| `net_profit_yen` | Net profit. |
| `roi_percent` | ROI percentage. |
| `profit_margin_percent` | Profit margin percentage. |
| `break_even_price_yen` | Break-even sale price. |
| `risk_adjusted_profit_yen` | Risk-adjusted profit. |
| `decision` | `pass`, `fail`, `review`, `blocked`, or `skipped`. |
| `decision_reason` | Human-readable reason. |
| `created_at` | Calculation timestamp. |

#### `capital_allocations`

Stores budget allocation state.

| Column | Purpose |
|---|---|
| `id` | Allocation ID. |
| `period_key` | Budget period such as `2026-05`. |
| `total_budget_yen` | Initial default: 50,000. |
| `allocated_yen` | Approved allocated amount. |
| `remaining_yen` | Remaining budget. |
| `created_at` | Creation timestamp. |
| `updated_at` | Update timestamp. |

#### `purchase_candidates`

Stores P3-approved purchase candidates. These are not purchase executions.

| Column | Purpose |
|---|---|
| `id` | Candidate ID. |
| `profit_estimate_id` | Profit estimate ID. |
| `source_offer_id` | Source offer ID. |
| `status` | `pending_review`, `approved`, `rejected`, or `expired`. |
| `requested_quantity` | Candidate quantity. |
| `total_purchase_amount_yen` | Candidate total purchase amount. |
| `requires_human_approval` | Always true in initial MVP. |
| `created_at` | Candidate timestamp. |

#### `human_approvals`

Stores human approvals.

| Column | Purpose |
|---|---|
| `id` | Approval ID. |
| `target_type` | `identity`, `profit`, `purchase`, or `external_access`. |
| `target_id` | Approved target ID. |
| `decision` | `approved`, `rejected`, or `needs_more_info`. |
| `reviewer_name` | Human reviewer. |
| `comment` | Review comment. |
| `approved_at` | Review timestamp. |

#### `audit_logs`

Stores irreversible audit events.

| Column | Purpose |
|---|---|
| `id` | Audit ID. |
| `event_type` | Event name. |
| `actor` | `system` or `human:<name>`. |
| `target_type` | Target type. |
| `target_id` | Target ID. |
| `payload_json` | Structured payload. |
| `created_at` | Event timestamp. |

## 3. P4-to-P3 Gate

P3 may run only when one of these is true:

- P4 decision is `same`, confidence is at or above threshold, and human review is not required.
- P4 decision was reviewed and explicitly approved by a human.

P3 must be skipped for `different`, `ambiguous`, and `blocked` unless a documented human approval route exists.
