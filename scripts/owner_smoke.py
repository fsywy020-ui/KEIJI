#!/usr/bin/env python3
"""Owner-friendly entry point for the local KEIJI smoke workflow.

This wrapper makes the smoke workflow runnable from Windows PowerShell,
macOS, or Linux without manually setting PYTHONPATH. It only runs the local
offline smoke workflow; it does not call external APIs, open browsers, send
notifications, or execute purchase-side actions.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from local_smoke import main as run_local_smoke  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(run_local_smoke())
