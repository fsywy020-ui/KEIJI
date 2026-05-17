# Human Approval Policy

## 1. Mandatory Human Approval

Human approval is mandatory for:

- Any purchase execution.
- Any payment execution.
- Any Codex-assisted purchase-adjacent step.
- P4 ambiguous identity decisions.
- P4 identity decisions with missing key identifiers.
- P3 review decisions.
- External API activation.
- Any budget exception request.

## 2. Forbidden Initial-MVP Actions

The system must not automatically:

- Log in to purchasing accounts.
- Add items to carts.
- Confirm checkout.
- Submit payment.
- Place purchase orders.
- Use browser automation for purchase flows.

## 3. Approval Record Requirements

Each approval record must include:

- Target type.
- Target ID.
- Reviewer name.
- Decision.
- Comment or reason.
- Timestamp.

## 4. Purchase Candidate Status

All P3 pass/review items begin as `pending_review`. No candidate is executable until approved by a human outside the automated purchase flow.
