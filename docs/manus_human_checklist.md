# Manus Handoff Human Checklist

Use this checklist before a KEIJI P8 local handoff packet is shown to Manus.

## Product Identity

- [ ] P4 is `same` or otherwise acceptable under owner policy.
- [ ] If P4 is `ambiguous`, the item is not treated as buyable.
- [ ] If P4 is `blocked`, the item is not purchased.
- [ ] JAN, ASIN, model number, color, capacity, size, set count, edition, domestic/import status, condition, bundle/single status, and accessories are visually checked.

## Profit and Budget

- [ ] P3 net profit is visible.
- [ ] P3 ROI is visible.
- [ ] Break-even price is visible.
- [ ] Total source-side cost is at or below the 5,000 JPY per-SKU cap.
- [ ] The effect on the initial 50,000 JPY purchasing budget is understood.
- [ ] If profit is below threshold or uncertain, the candidate remains review/watch only.

## Market Data and Scoring

- [ ] P5 market data is present and matched by real identifiers when used.
- [ ] If P5 market data is missing, the candidate is not treated as ready to buy.
- [ ] P6 `BUY_CANDIDATE` is understood as a human-review candidate only, not purchase permission.
- [ ] Seller count, rank, stock status, condition, and price gap are reviewed.

## Policy and Operations

- [ ] The item is not in a prohibited category.
- [ ] If the item is used, secondhand-goods operation records are understood and preserved.
- [ ] The handoff packet contains only information allowed by `docs/manus_handoff_policy.md`.
- [ ] The handoff packet contains no passwords, API keys, tokens, credit-card details, payment details, login credentials, Cookies, sessions, personal information, or automatic-purchase execution data.
- [ ] Manus is explicitly forbidden from login, cart operation, checkout, purchase, payment, listing, browser automation, scraping, and live external API access.
