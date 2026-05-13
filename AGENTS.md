# KEIJI Agent Instructions

## Project Boundary

This repository is a resale / commerce automation MVP for KEIJI only.

- Do not mix this project with WAT-VIDEO.
- Do not import, reference, copy, or depend on WAT-VIDEO code, configuration, prompts, assets, data, tests, environment variables, or documentation.
- If any WAT-VIDEO reference is discovered, stop and remove it before continuing.

## Business Goal

Build an MVP for a resale automation system targeting monthly profit of 100,000-300,000 JPY, while prioritizing safety, auditability, and human approval.

## Current Approval Conditions

- Initial purchasing budget: 50,000 JPY.
- Maximum purchase amount per SKU: 5,000 JPY.
- Primary sales channel: Amazon.
- Manus may only assist immediately before purchase.
- Fully automated purchasing is prohibited in the initial MVP.
- Payment and purchase execution require human approval.
- Implement P4 Product Identity before P3 Profit Calculation.

## Implementation Order

1. P4 Product Identity Engine foundation.
2. P4 test fixtures and rule validation.
3. P4 persistence and audit records.
4. P4-to-P3 integration gate.
5. P3 Profit Calculation Engine foundation.
6. Human approval workflow.
7. External API adapters only after explicit permission.

## Internet and External Access Policy

- Internet access is OFF by default for product research, tests, and normal development.
- Use local fixtures, manually prepared CSV/JSON, and versioned YAML rules first.
- External API access is allowed only when explicitly approved for a specific integration and task.
- Browser automation and scraping are not part of the initial MVP.

## Automation Restrictions

Never implement initial-MVP behavior that performs any of the following without human approval:

- Login to a purchasing site.
- Add items to a cart.
- Place an order.
- Execute payment.
- Confirm checkout.
- Automatically purchase through Manus or any browser agent.

## Coding Guidance

- Keep P4 and P3 modular and testable.
- Prefer deterministic local tests over live API calls.
- Store business thresholds in `config/*.yaml`, not hard-coded business logic.
- Every decision that blocks, passes, or requires review must include machine-readable reasons and human-readable explanation.
- Preserve audit logs for identity decisions, profit decisions, approvals, and blocked actions.
