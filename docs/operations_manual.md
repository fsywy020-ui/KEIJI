# KEIJI MVP Operations Manual

## 1. Normal Operating Mode

- Internet access remains OFF.
- Use local fixtures, CSV, and JSON files.
- Run P4 before P3.
- Review all purchase candidates manually.

## 2. External API Exception Procedure

External API access may be enabled only for a specific approved task.

Required steps:

1. Document the target API.
2. Document the required endpoint and purpose.
3. Confirm no purchase or payment execution is involved.
4. Add or update a config entry.
5. Record human approval.
6. Use mocks or fixtures in tests.

## 3. Manus Boundary

Manus may assist only before purchase. It must not execute payment, confirm checkout, or complete order placement.

## 4. WAT-VIDEO Boundary

If any WAT-VIDEO reference appears in code, config, docs, fixtures, environment variables, or tests, treat it as a project-boundary violation and remove it.
