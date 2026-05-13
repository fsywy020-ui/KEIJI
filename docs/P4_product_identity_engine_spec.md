# P4 Product Identity Engine Specification

## 1. Objective

The P4 Product Identity Engine determines whether a source offer and an Amazon listing represent the same product. P4 must run before P3 profit calculation.

## 2. Inputs

P4 accepts local, deterministic input only in the initial MVP:

- Manual records.
- CSV records.
- JSON fixtures.
- Saved Amazon listing snapshots.

Live internet access, scraping, and external APIs are not part of P4 initial execution.

## 3. Decisions

| Decision | Meaning | P3 Eligibility |
|---|---|---|
| `same` | Same product with sufficient confidence. | Eligible if no review required. |
| `different` | Clear mismatch. | Not eligible. |
| `ambiguous` | Insufficient or conflicting evidence. | Not eligible without human approval. |
| `blocked` | Unsafe, prohibited, or outside MVP policy. | Never eligible unless policy changes. |

## 4. Module Structure

```text
p4_identity/
  input_models.py
  normalizer.py
  identifier_matcher.py
  brand_matcher.py
  title_matcher.py
  variant_matcher.py
  condition_matcher.py
  exclusion_rules.py
  scoring.py
  decision.py
  explain.py
  engine.py
```

## 5. Module Responsibilities

### `input_models.py`

Defines the source offer, market listing, normalized record, score, evidence, and final decision data contracts.

### `normalizer.py`

Normalizes text before matching:

- Unicode normalization.
- Full-width to half-width conversion.
- Case normalization.
- Brand alias conversion.
- Unit normalization.
- Noise-token removal.
- Model candidate extraction.

### `identifier_matcher.py`

Compares strong identifiers:

1. JAN/EAN/UPC.
2. ASIN.
3. Manufacturer model number.
4. Normalized model number.
5. Weak partial model candidates.

Identifier conflicts must strongly prefer `different` or `ambiguous` over `same`.

### `brand_matcher.py`

Compares normalized brands and flags dangerous wording such as compatible, non-genuine, parallel import, or brand-for-use phrasing.

### `title_matcher.py`

Tokenizes and compares product title elements:

- Product family.
- Series.
- Model.
- Capacity.
- Size.
- Color.
- Quantity.
- Generation.
- Compatible device.
- Included accessories.

Title similarity alone must not create a `same` decision.

### `variant_matcher.py`

Compares variant-critical attributes:

- Color.
- Size.
- Capacity.
- Quantity / pack count.
- Edition.
- Domestic or overseas version.
- Power specification.
- Included accessories.

Missing or conflicting variant data should produce `ambiguous` or `blocked`.

### `condition_matcher.py`

Checks condition compatibility. Used/open-box/junk source items must not be treated as new products for Amazon sale.

### `exclusion_rules.py`

Applies immediate block rules, including:

- Junk, broken, parts-only, or訳あり.
- Compatible or non-genuine wording.
- Opened item sold as new.
- Unclear expiration-sensitive items.
- High authenticity risk.
- Set contents unknown.
- Per-SKU amount above 5,000 JPY.

### `scoring.py`

Combines component scores:

- `identifier_score`.
- `brand_score`.
- `title_score`.
- `variant_score`.
- `condition_score`.
- `risk_penalty`.

### `decision.py`

Produces one final decision and review flag.

### `explain.py`

Generates both human-readable explanation and machine-readable evidence.

### `engine.py`

Runs the complete P4 pipeline:

```text
input -> normalize -> match identifiers -> match brand -> match title
-> match variants -> match condition -> apply exclusions -> score
-> decide -> explain -> persist/audit
```

## 6. Initial Threshold Policy

- `same`: strong identifier match, no variant conflict, no condition conflict, and confidence >= 0.90.
- `review`: confidence between 0.80 and 0.90 or any missing non-critical attribute.
- `ambiguous`: weak or incomplete identifiers.
- `blocked`: exclusion rule hit or budget policy violation.

## 7. Required Output

```json
{
  "decision": "same",
  "confidence_score": 0.95,
  "requires_human_review": false,
  "scores": {
    "identifier_score": 1.0,
    "brand_score": 1.0,
    "title_score": 0.9,
    "variant_score": 1.0,
    "condition_score": 1.0
  },
  "evidence": [],
  "block_reason": null
}
```

## 8. Confirmed Implementation Plan and Current Status

The implementation plan is fixed for the offline MVP and maps to the existing package as follows:

| Backlog item | Implemented module | Status |
|---|---|---|
| P4 folder structure | `src/keiji/p4_identity/` | Done |
| Rule loading | `keiji.common.config_loader.load_rule_config` with `config/product_identity_rules.v1.yaml` | Done |
| Product-name normalization | `normalizer.py` | Done |
| JAN/model/capacity/color/set-count/condition extraction | `attribute_extractor.py` | Done |
| Identifier/title/variant/condition scoring | `identifier_matcher.py`, `title_matcher.py`, `variant_matcher.py`, `condition_matcher.py`, `decision.py` | Done |
| Hard rejection conditions | `decision.py` plus config-driven exclusion keywords, condition policy, and SKU cap | Done |
| Unit coverage | `tests/unit/p4_identity/` | Done |

The implementation intentionally keeps brand matching inside `decision.py` for the MVP instead of adding a separate `brand_matcher.py`. Exclusion decisions are also centralized in `decision.py` so every blocked/review result emits machine-readable evidence in one place.

## 9. Attribute Extraction Contract

`attribute_extractor.py` extracts only conservative local attributes from normalized text and structured fields:

- JAN/EAN/UPC-like numeric identifiers.
- Manufacturer model candidates.
- Capacity values such as `256gb` or `500ml`.
- Configured color aliases.
- Set/pack count as the `quantity` variant.
- Condition keywords such as new, used, open-box, or junk.

Structured JAN/model fields override title-derived identifiers. Title-derived unsafe condition terms such as used, open-box, or junk can override a default-looking `new` value so the condition gate remains conservative. Missing or uncertain extracted attributes remain empty; P4 then treats the candidate conservatively through variant-missing or identifier-missing review paths rather than inventing a match.
