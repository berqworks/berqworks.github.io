#!/usr/bin/env python3
"""One-off: turn the source package into web media under site/assets/media/.

Needs ffmpeg (libx264), ffprobe, cwebp and sips. Updates the "media" field of
site/data/games.json and writes site/assets/media/manifest.json.

    python3 tools/prepare_media.py [--source ~/Desktop/site-gerekli-dosyalar]
"""

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "assets" / "media"
GAMES_JSON = ROOT / "site" / "data" / "games.json"

# (source file stem, EN/TR alt text)
GAMES = {
    "mahjong-caravan": {
        "folder": "mahjong",
        "video": {"en": "video/en_win_last-pairs-confetti-stars.mp4", "tr": "video/tr_win_last-pairs-confetti-stars.mp4"},
        "poster": {"en": "screenshots/en/en_mid.png", "tr": "screenshots/tr/tr_mid.png"},
        "screens": {
            "en": [
                ("screenshots/en/en_menu.png", "Main menu with the Play button and the star count"),
                ("screenshots/en/en_levels.png", "Level map with the chapter selector"),
                ("screenshots/en/en_layouts.png", "Free play: choosing one of the 46 layouts"),
                ("screenshots/en/en_themes.png", "Nine tile themes and four table backgrounds"),
                ("screenshots/en/en_mid_dark.png", "A half-played Turtle board in the dark look"),
                ("screenshots/en/en_win.png", "Win panel with three stars"),
            ],
            "tr": [
                ("screenshots/tr/tr_menu.png", "Oyna düğmesi ve yıldız sayısıyla ana menü"),
                ("screenshots/tr/tr_levels.png", "Bölüm seçicili seviye haritası"),
                ("screenshots/tr/tr_layouts.png", "Serbest oyun: 46 yerleşimden birini seçmek"),
                ("screenshots/tr/tr_themes.png", "Dokuz taş teması ve dört masa zemini"),
                ("screenshots/tr/tr_mid_dark.png", "Koyu görünümde yarısı oynanmış Kaplumbağa tahtası"),
                ("screenshots/tr/tr_win.png", "Üç yıldızlı kazanma paneli"),
            ],
        },
        "motion": {
            "body": "art/tiles/bodies/ivory.svg",
            "tiles": ["art/tiles/faces/Chun.svg", "art/tiles/faces/Hatsu.svg", "art/tiles/faces/Pin5.svg",
                      "art/tiles/faces/Sou3.svg", "art/tiles/faces/Man7.svg", "art/tiles/faces/Ton.svg"],
        },
    },
    "tile-swap-puzzle": {
        "folder": "tile-swap-puzzle",
        "video": {"en": "video/intro_jigsaw-assemble.mp4", "tr": "video/intro_jigsaw-assemble.mp4"},
        "poster": {"en": "@last", "tr": "@last"},
        "screens": {
            "en": [
                ("screenshots/en/en_1-ana_menu.png", "Main menu under the night sky"),
                ("screenshots/en/en_2-kategoriler.png", "Choosing a category"),
                ("screenshots/en/en_3-yapbozlar.png", "The ten pictures in a category"),
                ("screenshots/en/en_4-oyun.png", "A puzzle in progress, with pieces locked in place"),
                ("screenshots/en/en_5-tebrikler.png", "The finished picture with its name and stars"),
                ("screenshots/en/en_6-album.png", "Sticker album page"),
            ],
            "tr": [
                ("screenshots/tr/tr_1-oyun.png", "Yerine oturan parçalarla devam eden bir yapboz"),
                ("screenshots/tr/tr_2-kategoriler.png", "Kategori seçimi"),
                ("screenshots/tr/tr_3-yapbozlar.png", "Bir kategorideki on resim"),
                ("screenshots/tr/tr_4-tebrikler.png", "Adı ve yıldızlarıyla tamamlanan resim"),
                ("screenshots/tr/tr_5-album.png", "Çıkartma albümü sayfası"),
                ("screenshots/tr/tr_6-ana_menu.png", "Gece gökyüzü altında ana menü"),
            ],
        },
        "motion": {"image": "art/puzzle-images/animals/fox.png"},
    },
    "water-sort": {
        "folder": "water-sort",
        "video": {"en": "video/en_page-complete_pine-forest_1080x1800.mp4", "tr": "video/tr_page-complete_farm_1080x1800.mp4"},
        "poster": {"en": "@first", "tr": "@first"},
        "screens": {
            "en": [
                ("screenshots/en/en_level.png", "Level 39 with the center vessel"),
                ("screenshots/en/en_very_hard.png", "Level 40, marked Very Hard"),
                ("screenshots/en/en_atlas_page-in-progress.png", "An Atlas scene being colored in"),
                ("screenshots/en/en_page_complete.png", "Page complete: Pine Forest"),
                ("screenshots/en/en_daily_puzzle.png", "Daily puzzle"),
                ("screenshots/en/en_shop_backgrounds.png", "Backgrounds in the shop"),
            ],
            "tr": [
                ("screenshots/tr/tr_level.png", "Merkez kaplı Seviye 21"),
                ("screenshots/tr/tr_color_aid.png", "Renk yardımı: semboller ve desenler"),
                ("screenshots/tr/tr_atlas_page-in-progress.png", "Renklenmekte olan bir Atlas sahnesi"),
                ("screenshots/tr/tr_page_complete.png", "Tamamlanan sayfa: Liman Kasabası"),
                ("screenshots/tr/tr_daily_streak.png", "Günlük seri"),
                ("screenshots/tr/tr_level_win.png", "Seviye tamamlandı"),
            ],
        },
        "motion": {"color": "art/atlas-pages/page_002_pine-forest_color.png",
                   "mask": "art/atlas-pages/page_002_pine-forest_region-mask.png"},
    },
}


def run(*cmd: str) -> str:
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def size_of(path: Path) -> tuple[int, int]:
    out = run("sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path))
    vals = [int(line.split()[-1]) for line in out.splitlines() if "pixel" in line]
    return vals[0], vals[1]


def webp(src: Path, dst: Path, width: int | None = None, height: int | None = None) -> tuple[int, int]:
    dst.parent.mkdir(parents=True, exist_ok=True)
    args = ["cwebp", "-quiet", "-q", "78"]
    if width or height:
        args += ["-resize", str(width or 0), str(height or 0)]
    run(*args, str(src), "-o", str(dst))
    return size_of_webp(dst)


def size_of_webp(path: Path) -> tuple[int, int]:
    out = run("ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
              "stream=width,height", "-of", "csv=p=0", str(path))
    w, h = out.strip().split(",")[:2]
    return int(w), int(h)


def video(src: Path, dst: Path, portrait: bool) -> None:
    scale = "scale=-2:900" if portrait else "scale=960:-2"
    run("ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-an", "-vf", scale, "-c:v", "libx264",
        "-crf", "28", "-preset", "slow", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(dst))


def frame(src: Path, dst: Path, last: bool, portrait: bool) -> None:
    with tempfile.TemporaryDirectory() as d:
        png = Path(d) / "f.png"
        pre = ["-sseof", "-0.6"] if last else []
        run("ffmpeg", "-y", "-loglevel", "error", *pre, "-i", str(src), "-frames:v", "1", str(png))
        webp(png, dst, None if portrait else 960, 900 if portrait else None)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default=str(Path.home() / "Desktop" / "site-gerekli-dosyalar"))
    source = Path(ap.parse_args().source).expanduser()

    needed = []
    for cfg in GAMES.values():
        base = source / cfg["folder"]
        needed += [base / "icon" / "icon_512.png"]
        needed += [base / v for v in cfg["video"].values()]
        needed += [base / p for p in cfg["poster"].values() if not p.startswith("@")]
        needed += [base / s for lang in cfg["screens"].values() for s, _ in lang]
        for v in cfg["motion"].values():
            needed += [base / x for x in (v if isinstance(v, list) else [v])]
    missing = [str(p) for p in needed if not p.is_file()]
    if missing:
        print("missing source files:\n" + "\n".join(missing))
        sys.exit(1)

    if OUT.exists():
        shutil.rmtree(OUT)
    manifest: dict[str, str] = {}
    games = json.loads(GAMES_JSON.read_text(encoding="utf-8"))

    for game in games:
        gid = game["id"]
        cfg = GAMES[gid]
        base = source / cfg["folder"]
        out = OUT / gid
        out.mkdir(parents=True)
        portrait = game["orientation"] == "portrait"

        def note(name: str, src: Path) -> str:
            manifest[f"{gid}/{name}"] = str(src.relative_to(source))
            return name

        media: dict = {}
        icon_src = base / "icon" / "icon_512.png"
        webp(icon_src, out / "icon-256.webp", 256, 256)
        webp(icon_src, out / "icon-512.webp")
        media["icon"] = note("icon-256.webp", icon_src)
        media["icon_large"] = note("icon-512.webp", icon_src)

        media["hero_video"], media["hero_poster"] = {}, {}
        for lang, rel in cfg["video"].items():
            src = base / rel
            name = f"hero-{lang}.mp4"
            if lang == "tr" and cfg["video"]["tr"] == cfg["video"]["en"]:
                name = "hero-en.mp4"
            else:
                video(src, out / name, portrait)
            media["hero_video"][lang] = note(name, src)
            poster = cfg["poster"][lang]
            pname = f"poster-{lang}.webp"
            if poster.startswith("@"):
                frame(out / name, out / pname, poster == "@last", portrait)
                media["hero_poster"][lang] = note(pname, src)
            else:
                webp(base / poster, out / pname, None if portrait else 960, 900 if portrait else None)
                media["hero_poster"][lang] = note(pname, base / poster)
            media["hero_size"] = list(size_of_webp(out / name))  # ffprobe reads mp4 too

        media["screens"] = {}
        for lang, shots in cfg["screens"].items():
            media["screens"][lang] = []
            for i, (rel, alt) in enumerate(shots, 1):
                name = f"screen-{lang}-{i}.webp"
                w, h = webp(base / rel, out / name, 600 if portrait else 1200, None)
                media["screens"][lang].append({"file": note(name, base / rel), "alt": alt, "w": w, "h": h})

        motion: dict = {}
        mcfg = cfg["motion"]
        if gid == "mahjong-caravan":
            shutil.copy(base / mcfg["body"], out / "tile-body.svg")
            motion["body"] = note("tile-body.svg", base / mcfg["body"])
            motion["tiles"] = []
            for rel in mcfg["tiles"]:
                name = "tile-" + Path(rel).stem.lower() + ".svg"
                shutil.copy(base / rel, out / name)
                motion["tiles"].append(note(name, base / rel))
        elif gid == "tile-swap-puzzle":
            webp(base / mcfg["image"], out / "swap.webp", 600, 600)
            motion["image"] = note("swap.webp", base / mcfg["image"])
        else:
            webp(base / mcfg["color"], out / "scene.webp", 540, 960)
            motion["color"] = note("scene.webp", base / mcfg["color"])
            run("ffmpeg", "-y", "-loglevel", "error", "-i", str(base / mcfg["mask"]), "-vf",
                "scale=540:960:flags=neighbor,format=gray", str(out / "mask.png"))
            motion["mask"] = note("mask.png", base / mcfg["mask"])
        media["motion"] = motion
        game["media"] = media

    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    GAMES_JSON.write_text(json.dumps(games, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    total = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())
    print(f"media: {total / 1024 / 1024:.1f} MB")


if __name__ == "__main__":
    main()
