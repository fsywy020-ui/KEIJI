# KEIJI Progress Log

## 2026-05-13

### Completed in this pass

- Confirmed the P4-first/P3-after workflow remains the implementation order for the MVP.
- Added a dedicated P4 attribute extractor for local title/fixture text:
  - JAN/EAN/UPC candidates.
  - Model-number candidates.
  - Capacity.
  - Color.
  - Set count / pack count.
  - Condition words.
- Connected extracted JAN/model candidates into identifier matching so locally supplied titles can support P4 scoring when explicit fields are missing.
- Connected set-count extraction into variant comparison so pack-count conflicts require human review.
- Updated versioned P4 rules to include `set_count` as a critical variant attribute.
- Added P4 unit tests for attribute extraction, title-extracted JAN matching, and set-count conflict handling.
- Updated P4/P3 specifications to document the implemented extraction and conservative fee/buffer assumptions.

### Remaining backlog / next tasks

- Expand P4 extraction coverage for size, generation, power specification, and included accessories.
- Move hard-rejection rules into a fully isolated policy module if the rule set grows beyond the current decision logic.
- Add more fixture cases for ambiguous model-only matching and missing variant attributes.
- Add richer P3 risk adjustment inputs for price uncertainty, competition, return risk, and fee uncertainty.
- Add status/audit report filters for date range and decision type after the schema stabilizes.

### Blockers

- No current blocker. External APIs, browser automation, purchase execution, payment execution, and live product research remain intentionally out of scope until explicit human approval.

## Continuation prompt for next Codex run

Continue in AI生徒会長モード. Use AGENTS.md and docs/PRD.md as constraints. Do not wait for confirmation unless a listed blocker appears. Next, expand P4 attribute extraction for size/generation/power/accessories, add fixture-driven tests for those attributes, and consider isolating hard-rejection policy into a dedicated module while preserving offline-only deterministic behavior and human approval gates.
