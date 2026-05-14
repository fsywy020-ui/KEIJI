# P8 Manus Handoff Policy

## Purpose

P8 prepares a local safety contract for Manus-assisted, human-led pre-purchase review. It does not integrate with Manus APIs, browser agents, purchasing sites, carts, checkout flows, payment systems, Amazon listing flows, scraping tools, or live external APIs.

## Allowed P8 assistance

Manus may only assist a human immediately before purchase by using a human-provided local packet to:

- summarize the local P7 review packet,
- explain checklist items,
- prepare questions for a human reviewer,
- flag missing manual evidence.

## Forbidden P8 actions

The initial MVP must block and audit requests for:

- login,
- add-to-cart or cart operations,
- checkout or checkout confirmation,
- order placement,
- purchase execution,
- payment execution,
- listing creation,
- browser automation,
- scraping,
- live external API access.

## Human approval requirements

A human must confirm product identity, profit assumptions, budget impact, and per-SKU limit before any external purchase-side action occurs outside KEIJI. KEIJI approval records and P8 packets are audit artifacts only; they are not purchase authorization for automation.

## Audit expectation

Every P8 blocked, passed, or review-only decision must include machine-readable reasons and a human-readable explanation. Blocked action checks should write local JSONL audit records when an audit path is provided.
