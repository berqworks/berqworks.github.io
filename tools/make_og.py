#!/usr/bin/env python3
"""One-off: render the 1200x630 share images with local Chrome.

    python3 tools/make_og.py
Writes site/assets/brand/og.png and og-<game id>.png.
"""

import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "site" / "assets"
OUT = ASSETS / "brand"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FONTS = {"nunito": ("Nunito", "nunito.woff2", 800), "baloo": ("Baloo 2", "baloo2-semibold.woff2", 600),
         "aileron": ("Aileron", "aileron-bold.woff2", 700)}


def font_face(family: str, file: str) -> str:
    return f'@font-face{{font-family:"{family}";src:url({(ASSETS / "fonts" / file).as_uri()});font-weight:100 1000}}'


def studio_html(games: list) -> str:
    icons = "".join(
        f'<img src="{(ASSETS / "media" / g["id"] / g["media"]["icon_large"]).as_uri()}" '
        f'style="transform:rotate({r}deg)">' for g, r in zip(games, (-4, 3, -2)))
    return f"""<!doctype html><style>{font_face("Fraunces", "fraunces.woff2")}
body{{margin:0;width:1200px;height:630px;background:#f3efe6;color:#191714;font-family:Fraunces;position:relative;overflow:hidden}}
h1{{position:absolute;left:72px;top:96px;margin:0;font-size:178px;font-weight:760;letter-spacing:-.045em;line-height:.9;
font-variation-settings:"SOFT" 60,"WONK" 1,"opsz" 144}}
.rule{{position:absolute;left:72px;right:72px;top:330px;border-top:3px solid #191714}}
.icons{{position:absolute;left:72px;bottom:64px;display:flex;gap:28px}}
.icons img{{width:168px;height:168px;border-radius:38px;box-shadow:0 18px 30px -14px rgba(0,0,0,.55)}}
</style><h1>BerqWorks</h1><div class="rule"></div><div class="icons">{icons}</div>"""


def game_html(game: dict) -> str:
    family, file, weight = FONTS[game["heading_font"]]
    th = game["theme"]
    icon = (ASSETS / "media" / game["id"] / game["media"]["icon_large"]).as_uri()
    return f"""<!doctype html><style>{font_face(family, file)}{font_face("Fraunces", "fraunces.woff2")}
body{{margin:0;width:1200px;height:630px;background:linear-gradient(160deg,{th['bg']},{th['bg2'] or th['bg']});
color:{th['fg']};display:flex;align-items:center;gap:64px;padding:0 88px;box-sizing:border-box}}
img{{width:300px;height:300px;border-radius:66px;transform:rotate(-3deg);box-shadow:0 30px 50px -20px rgba(0,0,0,.6)}}
h1{{font-family:"{family}";font-weight:{weight};font-size:76px;line-height:1.02;margin:0 0 22px;letter-spacing:-.015em}}
p{{font:600 30px Fraunces;margin:0;opacity:.75}}
</style><img src="{icon}"><div><h1>{game['name']['en']}</h1><p>BerqWorks</p></div>"""


def shoot(html: str, out: Path) -> None:
    with tempfile.TemporaryDirectory() as d:
        page = Path(d) / "og.html"
        page.write_text(html, encoding="utf-8")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                        "--virtual-time-budget=2000", "--window-size=1200,630", f"--screenshot={out}", page.as_uri()],
                       check=True, capture_output=True)


def main() -> None:
    games = json.loads((ROOT / "site" / "data" / "games.json").read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    shoot(studio_html(games), OUT / "og.png")
    for g in games:
        shoot(game_html(g), OUT / f"og-{g['id']}.png")
    print("\n".join(f"{p.name}: {p.stat().st_size // 1024} KB" for p in sorted(OUT.glob("og*.png"))))


if __name__ == "__main__":
    main()
