#!/usr/bin/env python3
"""Build the site: python3 tools/build.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sitegen.build import build, total_size  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

if __name__ == "__main__":
    out = ROOT / "public"
    build(ROOT, out)
    print(f"public/: {total_size(out) / 1024 / 1024:.1f} MB")
