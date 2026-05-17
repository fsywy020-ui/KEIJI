# KEIJI Commerce Automation MVP PRD

## 1. Purpose

KEIJI is a resale / commerce automation MVP designed to help identify safe purchase candidates and estimate profit, with a target monthly profit range of 100,000-300,000 JPY.

The MVP must prioritize product identity correctness, risk control, and human approval over speed or full automation.

## 2. Non-Goals

The initial MVP must not implement:

- Fully automated purchasing.
- Automated payment.
- Browser automation for checkout.
- Codex-assisted purchase completion.
- Live scraping or external API access by default.
- Any non-KEIJI feature, dependency, configuration, or workflow.

## 3. Current Business Constraints

| Constraint | Value |
|---|---:|
| Initial purchasing budget | 50,000 JPY |
| Maximum purchase amount per SKU | 5,000 JPY |
| Primary sales channel | Amazon |
| Purchase execution | Human approval required |
| Initial internet access | OFF |
| External API use | Explicit limited approval only |

## 4. Core Workflow

```text
Source Offer
  -> P4 Product Identity Engine
  -> P4 Decision Gate
  -> P3 Profit Calculation Engine
  -> Purchase Candidate
  -> Human Approval
  -> Manual Purchase / Payment Outside MVP Automation
```

P3 must not run on unsafe identity results. Product identity is the first gate.

## 5. P4 Product Identity Requirements

P4 determines whether a source offer and an Amazon listing refer to the same sellable product.

Required decisions:

- `same`: High-confidence same product.
- `different`: Clearly different product.
- `ambiguous`: Similar or insufficient data; human review required.
- `blocked`: Unsafe or prohibited for the MVP.

P4 must evaluate:

- JAN/EAN/UPC.
- ASIN.
- Brand.
- Model number.
- Title tokens.
- Variant attributes.
- Condition.
- Exclusion keywords and risk categories.

## 6. P3 Profit Calculation Requirements

P3 estimates whether a P4-approved product candidate has sufficient resale profit.

P3 must calculate:

- Expected sale price.
- Purchase price.
- Inbound shipping cost.
- Amazon referral/platform fees.
- Fulfillment or shipping cost.
- Other buffer costs.
- Net profit.
- ROI.
- Profit margin.
- Break-even price.
- Risk-adjusted profit.

P3 must enforce:

- Per-SKU maximum purchase amount of 5,000 JPY.
- Total initial purchase budget of 50,000 JPY.
- Human approval before purchase.

## 7. Approval Requirements

Human approval is required for:

- Any payment.
- Any purchase execution.
- P4 ambiguous results.
- P4 high-risk results.
- P3 review results.
- Any external API activation.
- Any Codex-assisted purchase-adjacent workflow.

## 8. Acceptance Criteria

The MVP design is acceptable when:

1. Non-KEIJI project artifacts are explicitly excluded.
2. `AGENTS.md` exists at the repository root.
3. P4 is specified before P3.
4. Internet access is OFF by default.
5. External API access is documented as opt-in only.
6. P4 and P3 configs are versioned.
7. Human approval gates are documented.
8. Tests can run from local fixtures without network access.
