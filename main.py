#!/usr/bin/env python3
"""Backward-compatible entry point.

Historically the framework was launched with ``python main.py``. That still works
and simply delegates to the packaged CLI (:mod:`quadrainspect.cli`). Prefer the
installed ``quadrainspect`` console script or ``python -m quadrainspect``.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Ensure the package is importable when run directly from a source checkout.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from quadrainspect.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
