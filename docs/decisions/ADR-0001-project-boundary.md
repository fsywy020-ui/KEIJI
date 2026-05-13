# ADR-0001: Keep KEIJI Project Artifacts Isolated

## Status

Accepted

## Decision

KEIJI is a dedicated resale / commerce automation MVP and must not share implementation, configuration, or operating assumptions with non-KEIJI projects.

## Consequences

- Non-KEIJI project artifacts are boundary violations.
- Tests should detect accidental non-KEIJI project artifacts.
- Documentation and configuration must describe KEIJI-specific resale constraints only.
