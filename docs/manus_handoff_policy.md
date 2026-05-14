# P8 Manus Handoff Policy

## Purpose

This policy defines what KEIJI may prepare **before** any Manus-assisted work. It is a local-only handoff policy. It does not connect to Manus, open a browser, call an external API, log in, add to cart, check out, purchase, pay, or list products.

## Allowed Manus-Side Work

Manus may only help a human operator understand local review information:

- Organize product-page information for a human to inspect.
- Summarize price, shipping fee, stock status, model number, JAN, ASIN, and condition for human review.
- Generate or reformat human-visible checklists.
- Organize pre-purchase confirmation items.
- Read a local handoff packet created by KEIJI.
- Create local reports for human review.

## Forbidden Manus-Side Work

Manus must not perform or assist with execution of:

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
- saving authentication information
- collecting Cookie or session information
- any external operation without explicit human approval

## Information Allowed in a Local Handoff Packet

- Candidate ID
- Product name
- JAN / ASIN / model number
- Local source/sales references
- P4 product identity result
- P3 profit result
- P5 market data summary
- P6 score and recommendation
- P7 review status
- Human checklist
- Budget and SKU-cap impact
- Allowed and forbidden action lists

## Information Not Allowed in a Local Handoff Packet

- Passwords
- API keys
- Tokens
- Credit-card information
- Payment information
- Login credentials
- Cookies
- Session information
- Personal information
- Any executable data required for automatic purchase

## Required Human Approval

Human approval remains required for any purchase-related decision. `BUY_CANDIDATE` means “candidate for human review”; it is not permission for KEIJI or Manus to buy anything.
