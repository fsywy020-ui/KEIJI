#!/usr/bin/env python3
"""Validate local candidate JSON/CSV before offline processing."""

from __future__ import annotations

import argparse

from keiji.io.candidate_validation import validate_candidate_file


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate local KEIJI candidate input")
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    result = validate_candidate_file(args.input)
    print(result.format_text())
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
