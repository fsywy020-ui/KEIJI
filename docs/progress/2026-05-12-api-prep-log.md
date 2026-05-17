# API-Preparation Progress Log - 2026-05-12

## Operating Boundary

- No API keys, credentials, Amazon API calls, price API calls, scraping, Codex review-assist integration, browser automation, purchase execution, or payment execution were added.
- Work stayed inside local deterministic code, fixtures, docs, and tests.
- The implementation order remains P4 first, then P3, then approval/audit foundations.

## Work Completed Before API Input

### 1. P4 Accuracy Improvements

- Added title token matching for mixed Japanese/English product names.
- Added variant extraction and comparison for attributes such as color, capacity, quantity, edition, and domestic/import wording.
- Added condition matching driven by `config/product_identity_rules.v1.yaml` instead of the earlier hard-coded new/new check.
- Added human-readable P4 explanation generation.
- Integrated title, variant, and condition results into the P4 decision engine.

### 2. P3 Offline Profit Engine Foundation

- Added P3 input/output models.
- Added Amazon fee estimation from local `config/profit_rules.v1.yaml`.
- Added ROI, profit margin, break-even, and net-profit calculations.
- Added capital guardrails for 5,000 JPY per-SKU and 50,000 JPY initial budget.
- Added a minimal `ProfitEngine` that can pass/fail/review/block/skip from local fixtures only.
- Purchase candidates and payment execution remain out of scope; every P3 result still requires human approval.

### 3. Human Review and Audit Foundations

- Added human review packet builder for future review screens or CSV exports.
- Added local JSONL audit-event writer for offline testing and later persistence wiring.

### 4. Tests Added

- P4 variant, condition, title, and explanation tests.
- P3 fee, capital, profit, and fixture-decision tests.
- Human review packet tests.
- JSONL audit writer tests.

## Deferred Until User Returns

The following require explicit user-side API/settings work and were intentionally not done:

- Amazon API credentials/configuration.
- External price API credentials/configuration.
- Live marketplace listing ingestion.
- Live fee API lookup.
- Browser automation.
- Codex-assisted purchase flow.
- Purchase or payment execution.

## Recommended Next Work After Review

1. Review whether P4 variant rules are strict enough for target product categories.
2. Decide whether P3 default Amazon fee assumptions should be adjusted before API data is available.
3. Approve or revise local JSON fixture format for importing real manually collected sample products.
4. After API credentials are entered by the user, add adapter interfaces and mock-first integration tests before live calls.
