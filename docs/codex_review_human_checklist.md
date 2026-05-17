# P8 Codex Human Checklist

Use this checklist before copying any local P8 packet into a human-led Codex conversation.

## Pre-handoff checks

- Confirm the packet was generated locally by `scripts/local_smoke.py` or trusted local code.
- Confirm the P7 review packet is attached in the P8 `source_review_packet` field.
- Confirm `human_approval_required` is `true`.
- Confirm purchase, payment, listing, checkout, login, cart operation, browser automation, scraping, and live external API flags are disabled.
- Confirm the product identity evidence covers JAN, ASIN, model number, title, brand, condition, variant, capacity, color, set count, edition, domestic/import status, and accessories where relevant.
- Confirm the profit estimate uses locally prepared assumptions.
- Confirm total purchase cost fits the 50,000 JPY initial budget and 5,000 JPY per-SKU limit.

## Codex prompt boundary

Tell Codex: summarize and challenge the local review packet only. Do not ask Codex to open sites, log in, add items to carts, confirm checkout, place orders, execute payment, list items, scrape pages, automate a browser, or call live APIs.

## Final human decision

A human must record approval, rejection, or `needs_more_info` in KEIJI before acting outside the system. Any external purchase or payment, if approved, is performed manually by a human outside KEIJI.
