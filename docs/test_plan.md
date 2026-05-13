# KEIJI MVP Test Plan

## 1. P4 Product Identity Tests

| ID | Case | Expected |
|---|---|---|
| P4-001 | JAN, brand, and model match. | `same` |
| P4-002 | ASIN matches and title has minor differences. | `same` |
| P4-003 | Brand alias normalizes to same brand. | `same` |
| P4-101 | JAN conflicts. | `different` |
| P4-102 | Model differs by critical suffix. | `different` or `ambiguous` |
| P4-103 | Color differs. | `different` or `ambiguous` |
| P4-104 | Capacity differs. | `different` |
| P4-201 | Title similar but no identifiers. | `ambiguous` |
| P4-202 | Brand missing and model missing. | `ambiguous` |
| P4-203 | Weak partial model match only. | `ambiguous` |
| P4-301 | Compatible/non-genuine wording. | `blocked` |
| P4-302 | Junk/broken wording. | `blocked` |
| P4-303 | Used/open-box source for new-sale assumption. | `blocked` |
| P4-304 | Expiration-sensitive item with no expiry data. | `blocked` |

## 2. P3 Profit Tests

| ID | Case | Expected |
|---|---|---|
| P3-001 | P4 same, sufficient profit, within SKU cap. | `pass` |
| P3-002 | High ROI and adequate net profit. | `pass` |
| P3-101 | Fee-adjusted calculation is negative. | `fail` |
| P3-102 | Net profit below minimum. | `fail` |
| P3-103 | ROI below minimum. | `fail` |
| P3-201 | Per-SKU purchase amount is 5,001 JPY. | `blocked` |
| P3-202 | Per-SKU purchase amount is exactly 5,000 JPY. | `review` or `pass` |
| P3-203 | Monthly budget would exceed 50,000 JPY. | `blocked` |
| P3-301 | P4 decision is `different`. | `skipped` |
| P3-302 | P4 decision is `ambiguous`. | `skipped` |
| P3-303 | P4 decision is `blocked`. | `skipped` |

## 3. Approval Tests

| ID | Case | Expected |
|---|---|---|
| APR-001 | P3 pass creates purchase candidate. | `pending_review` |
| APR-002 | Purchase attempted without human approval. | blocked |
| APR-003 | Approval has no reviewer name. | invalid |
| APR-004 | Rejected candidate is reprocessed. | requires new review |
| APR-005 | Approval is recorded in audit log. | pass |

## 4. Boundary Tests

| ID | Case | Expected |
|---|---|---|
| SEC-001 | WAT-VIDEO reference appears. | fail |
| SEC-002 | Network call occurs in default tests. | fail |
| SEC-003 | Browser automation is invoked. | fail |
| SEC-004 | Automatic payment is invoked. | fail |
| SEC-005 | External API is used without explicit approval. | fail |
