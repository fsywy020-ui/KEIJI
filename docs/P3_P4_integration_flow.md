# P4 to P3 Integration Flow

## 1. Principle

P4 protects identity correctness. P3 protects profit and capital. P3 must never treat uncertain identity as profitable opportunity without an explicit human approval record.

## 2. Flow

```text
1. Receive source offer.
2. Compare with Amazon listing candidate through P4.
3. Persist P4 decision and evidence.
4. Gate by P4 decision:
   - same + high confidence + no review -> P3 eligible.
   - same + review required -> human review before P3 or P3 review mode.
   - ambiguous -> human identity review.
   - different -> stop.
   - blocked -> stop and audit.
5. Run P3 only when eligible.
6. Persist P3 estimate and explanation.
7. Create purchase candidate only for pass/review results.
8. Require human approval before purchase or payment.
```

## 3. Gate Matrix

| P4 Decision | Human Review | P3 Action |
|---|---:|---|
| `same` | false | Run P3. |
| `same` | true | Require review or run P3 in review-only mode. |
| `ambiguous` | false | Skip P3. |
| `ambiguous` | approved | Run P3 in review-only mode. |
| `different` | any | Skip P3. |
| `blocked` | any | Skip P3. |

## 4. Audit Requirements

Every gate decision must log:

- Input IDs.
- Rules versions.
- Decision.
- Scores.
- Reasons.
- Whether human review is required.
- Human approval ID when applicable.

## 5. Minimal Implemented Integration

The minimal integration is implemented by `OfflinePipelineRunner` and the P4-to-P3 gate:

1. Load local CSV/JSON candidate input.
2. Run P4 with local product identity rules.
3. Persist and audit the P4 decision.
4. Evaluate the P4-to-P3 gate before profit calculation.
5. Run P3 only when the identity result is eligible.
6. Persist and audit the P3 decision.
7. Create a purchase candidate only for local human review.

The runner does not call external APIs, scrape pages, open browsers, log in, add to cart, place orders, execute payment, or perform listing operations.
