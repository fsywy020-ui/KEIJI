# ADR-0001: Separate KEIJI From WAT-VIDEO

## Status

Accepted

## Decision

KEIJI is a dedicated resale / commerce automation MVP and must not share implementation, configuration, or operating assumptions with WAT-VIDEO.

## Consequences

- WAT-VIDEO references are boundary violations.
- Tests should detect accidental WAT-VIDEO references.
- Documentation and configuration must describe KEIJI-specific resale constraints only.
