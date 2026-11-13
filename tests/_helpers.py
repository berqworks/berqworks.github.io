import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = Path.home() / "Desktop" / "site-gerekli-dosyalar"
sys.path.insert(0, str(ROOT / "tools"))
