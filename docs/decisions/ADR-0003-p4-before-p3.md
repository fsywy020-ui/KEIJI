# ADR-0003: Implement P4 Product Identity Before P3 Profit Calculation

## Status

Accepted

## Decision

The system must implement product identity first. Profit calculation must be gated by identity confidence and human approval state.

## Consequences

- P3 cannot run on ambiguous, different, or blocked identity decisions by default.
- P4 evidence and confidence are required inputs for P3.
- Test fixtures must cover identity risk before profit cases.
