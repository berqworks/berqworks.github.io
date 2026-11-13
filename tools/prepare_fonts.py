#!/usr/bin/env python3
"""One-off: subset site/fonts-src/ into woff2 under site/assets/fonts/.

Run with the tools venv (fonttools + brotli):
    python3 -m venv .venv-tools && .venv-tools/bin/pip install fonttools brotli
    .venv-tools/bin/python tools/prepare_fonts.py
"""

import shutil
from pathlib import Path

from fontTools import subset

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "site" / "fonts-src"
OUT = ROOT / "site" / "assets" / "fonts"

# output name -> (source file, license file)
FONTS = {
    "fraunces": ("Fraunces.ttf", "Fraunces-OFL.txt"),
    "instrument-sans": ("InstrumentSans.ttf", "InstrumentSans-OFL.txt"),
    "nunito": ("Nunito.ttf", "Nunito-OFL.txt"),
    "baloo2-semibold": ("Baloo2-SemiBold.ttf", "Baloo2-LICENSE.txt"),
    "aileron-regular": ("Aileron-Regular.otf", "Aileron-LICENSE.txt"),
    "aileron-bold": ("Aileron-Bold.otf", "Aileron-LICENSE.txt"),
}

# Basic Latin, Latin-1, Latin Extended-A/B (covers Turkish), punctuation, € → ™
UNICODES = "U+0000-024F,U+2010-2027,U+2030-203A,U+20AC,U+2192,U+2122"


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    for name, (font, lic) in FONTS.items():
        subset.main([
            str(SRC / font),
            f"--unicodes={UNICODES}",
            "--layout-features=*",
            "--flavor=woff2",
            f"--output-file={OUT / (name + '.woff2')}",
        ])
        family = name.split("-")[0]
        shutil.copy(SRC / lic, OUT / f"{family}-LICENSE.txt")
    total = sum(f.stat().st_size for f in OUT.iterdir())
    print(f"fonts: {total / 1024:.0f} KB")


if __name__ == "__main__":
    main()
