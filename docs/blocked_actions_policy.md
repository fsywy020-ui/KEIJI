# Blocked Actions Policy

## Purpose

KEIJI is offline-first and human-approval-first. This policy describes actions that must remain blocked in the MVP and during P8 Manus handoff preparation.

## Blocked Actions

The following actions must not be implemented or executed by KEIJI or Manus in the initial MVP:

- login
- cart operation
- checkout
- purchase
- payment
- listing / 出品実行
- automatic purchase
- automatic bidding
- browser automation
- scraping
- live external API access
- storing authentication information
- collecting Cookie or session information
- external operations without explicit human approval

## Allowed Mentions

Blocked words may appear in policy documents, safety comments, tests, and human-readable warnings. They must not appear as executable code that performs the blocked action.

## Audit Approach

The local test suite includes blocked-action audit tests that parse executable Python code under `src/` and `scripts/` and fail if forbidden automation libraries or execution-style calls are introduced.

The audit also checks that local Manus handoff packets do not contain secret-like fields and that `BUY_CANDIDATE` is not represented as purchase permission.

## Human Approval Rule

Any future change that might involve external access, Manus purchase-adjacent assistance, payment, checkout, login, cart operation, listing, browser automation, scraping, or live external API access requires explicit owner approval before implementation.
