# Non-Engineer Review Guide for KEIJI Local Outputs

## Purpose

This guide is for the owner who reviews KEIJI smoke outputs before any real-world operation.

KEIJI outputs are **review aids only**. They do **not** mean "buy this." Even when a file says `BUY_CANDIDATE` or `TEST_BUY_CANDIDATE`, it means **a human should check this candidate carefully**. It is not purchase permission, payment permission, listing permission, or automation permission.

P3 profit output is an **operational estimate** based on local/manual assumptions. It is not tax, accounting, legal, or financial advice.

## Hard Safety Boundary

Do not use KEIJI local outputs to perform any of the following:

- purchase,
- payment,
- listing,
- login,
- cart operation,
- checkout or checkout confirmation,
- browser automation,
- scraping,
- Manus API access,
- live external API access,
- external notification sending such as Slack, Discord, LINE, or email.

All real-world purchase-side actions require separate human decision and are performed outside KEIJI.

## 1. Run Smoke and Open Files in This Order

After running:

```bash
PYTHONPATH=src python scripts/local_smoke.py
```

open these local files in order:

1. `storage/smoke/pending_review.md` — short pending review list from the local database.
2. `storage/smoke/p7_review_packets.md` — detailed P4/P3/P5/P6/P7 review packet for human approval checks.
3. `storage/smoke/p8_manus_handoff_packets.md` — local-only Manus handoff safety contract.
4. `storage/smoke/status.md` — counts and budget/status summary.
5. `storage/smoke/audit_log.md` — local audit trail for decisions.
6. `storage/smoke/p8_blocked_actions_audit.jsonl` — proof that a forbidden P8 action check is blocked and audited locally.

JSON and CSV files are available for machine checking, but non-engineer review should start from the Markdown files above.

## 2. How to Read `pending_review.md`

Use `pending_review.md` as the quick triage screen.

Check each candidate for:

- **Human Approval**: must say human approval is required. Treat the candidate as a review item, not as purchase permission.
- **P4 Product Identity**: compare the source offer and Amazon listing summary.
- **P3 Profit Estimate**: read expected sale price, purchase price, shipping, fees, net profit, risk-adjusted profit, ROI, and reasons.
- **Forbidden Actions**: confirm the report says no purchase, payment, listing, login, cart, checkout, browser automation, scraping, Manus API, live external API, or external notification action occurred.

`pending_review.md` is intentionally shorter than P7. If anything is unclear, open `p7_review_packets.md` next.

## 3. How to Read `p7_review_packets.md`

Use `p7_review_packets.md` as the main owner review packet.

For each candidate, read these sections:

1. **Owner Action Required**
   - Shows the recommendation.
   - Confirms human approval is required.
   - Confirms purchase execution and external sending are disabled.

2. **Product / P4 Identity Summary**
   - Shows JAN / ASIN / model number.
   - Shows P4 decision, confidence, human-review flag, and block reason.
   - Lists owner-visible identity checks.

3. **P3 Profit Summary**
   - Shows net profit, risk-adjusted profit, ROI, profit margin, break-even price, and decision reasons.
   - Remember: this is an operational estimate only.

4. **Shipping / Fulfillment Assumptions**
   - Shows inbound shipping, packaging cost, fulfillment fee, and local assumptions.
   - These values come from local/manual inputs and config, not live carrier or Amazon APIs.

5. **Risk Details**
   - Shows named operational buffers such as price uncertainty, return risk, or budget concentration.
   - `penalty_yen` reduces the risk-adjusted view of profit.
   - `severity` helps the owner decide whether more manual evidence is needed.

6. **P6 Score / Budget**
   - Shows total score, initial budget impact, remaining budget, and whether the 5,000 JPY per-SKU limit is satisfied.

7. **Do Not Purchase Reasons**
   - Machine-readable reasons explaining why the packet itself must not trigger purchase.
   - `human_approval_not_recorded` should remain until a human review decision is explicitly recorded.

8. **Human Approval Checklist**
   - Owner checklist to complete before any real-world action outside KEIJI.

## 4. How to Read `p8_manus_handoff_packets.md`

Use this only if a human wants to copy a bounded local summary into a Manus conversation.

Manus may help with:

- summarizing the local review packet,
- explaining checklist items,
- preparing questions for the human reviewer,
- flagging missing manual evidence.

Manus must not help with:

- logging in,
- adding to cart,
- checkout,
- ordering,
- purchase execution,
- payment,
- listing,
- browser automation,
- scraping,
- Manus API automation,
- live external APIs.

If Manus is used, tell Manus: **summarize and challenge this local packet only; do not operate websites or execute purchase-side actions.**

## 5. How to Read `status.md` and `audit_log.md`

### `status.md`

Use this for the overall run summary:

- candidate counts,
- P4/P3 decision distribution,
- pending/approved/rejected status distribution,
- budget usage.

If counts look wrong, stop and inspect inputs before considering any candidate.

### `audit_log.md`

Use this to confirm decisions were recorded locally and explainably.

Look for:

- P4 identity decision events,
- P3 profit decision events,
- purchase candidate review state events,
- blocked action events.

Audit logs are evidence for review. They are not purchase approval.

## 6. Recommendation Meanings

| Recommendation | Meaning | Owner action |
|---|---|---|
| `BUY_CANDIDATE` | Stronger human-review candidate. | Review manually; not purchase permission. |
| `TEST_BUY_CANDIDATE` | Candidate that may be worth a small manual test after review. | Review manually; not purchase permission. |
| `WATCH_ONLY` | Monitor only. | Do not purchase. Gather more local evidence if needed. |
| `BLOCKED` | Fails a safety, identity, profit, or budget constraint. | Do not purchase. Read reasons. |
| `NEEDS_HUMAN_REVIEW` | KEIJI cannot safely decide from local evidence. | Human must inspect identity/profit/market assumptions. |

## 7. P4 Product Identity Checks

Before trusting any profit estimate, confirm the product is the same item:

- JAN is the same or explainably absent.
- ASIN points to the intended Amazon listing.
- Model number matches exactly or has a documented harmless notation difference.
- Brand is the same, including Japanese/English naming differences.
- Title does not hide a different capacity, size, generation, color, edition, or set count.
- Condition matches: new, used, unopened, box damage, accessories, and bundle/single differences.
- Domestic/import status is not mixed up.
- Accessories and included items match.

If any point is uncertain, treat the item as `NEEDS_HUMAN_REVIEW` or reject it.

## 8. P3 Profit Checks

P3 is a local operational estimate. Owner should verify:

- expected sale price source and freshness,
- purchase price,
- inbound shipping,
- packaging cost,
- fulfillment fee,
- platform fee,
- storage or other costs,
- net profit,
- risk-adjusted profit,
- ROI,
- break-even price,
- 50,000 JPY initial budget impact,
- 5,000 JPY per-SKU limit.

Do not interpret P3 as tax or accounting advice.

## 9. Shipping and `risk_details`

### Shipping

Shipping fields are local/manual assumptions:

- `inbound_shipping_yen`: shipping cost to acquire the item.
- `packaging_cost_yen`: local config estimate for packing materials.
- `fulfillment_fee_yen`: local config estimate for fulfillment.
- `assumptions`: text labels explaining local assumptions.

### Risk Details

Each risk detail has:

- `name`: the risk buffer name.
- `penalty_yen`: how much profit is buffered down.
- `severity`: low/medium/high style severity.
- `explanation`: human-readable reason.

Risk details help the owner see why risk-adjusted profit is lower than net profit.

## 10. Final Owner Checklist

Before any real-world action outside KEIJI, confirm:

- [ ] I understand this packet is not purchase permission.
- [ ] P4 identity matches the exact product, variant, condition, and accessories.
- [ ] P3 is only an operational estimate, not tax/accounting advice.
- [ ] Shipping, fees, risk details, budget impact, and per-SKU limit were checked.
- [ ] `do_not_purchase_reasons` were read and resolved or accepted as a reason not to act.
- [ ] Manus, if used, is limited to summarizing/challenging the local packet.
- [ ] No purchase, payment, listing, login, cart, checkout, browser automation, scraping, Manus API, live external API, or external notification was triggered by KEIJI.
- [ ] Any real-world purchase-side action will be a separate human decision outside KEIJI.
