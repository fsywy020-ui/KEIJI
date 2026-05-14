# Blocked Actions Policy

## Scope

This policy applies to the P8 Manus handoff safety contract and any request that could move KEIJI from local review into external execution.

## Default stance

Unknown or non-allowlisted Manus actions are blocked by default. P8 only permits local review-assistance tasks listed in the handoff contract.

## Always blocked

P8 always blocks actions that match these categories:

- `login`
- `add_to_cart`
- `cart_operation`
- `checkout`
- `confirm_checkout`
- `place_order`
- `purchase_execution`
- `execute_payment`
- `payment`
- `listing_creation`
- `browser_automation`
- `scraping`
- `live_external_api`

## Required decision record

Each action evaluation must include:

- `allowed`,
- `decision`,
- `machine_readable_reasons`,
- `human_readable_explanation`,
- `requires_human_approval`,
- optional local audit event ID.

## Audit record

When an audit path is provided, blocked actions are appended to local JSONL with event type `blocked_action`. This is a local audit artifact and does not notify or call external systems.
