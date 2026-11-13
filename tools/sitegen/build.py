"""Builds public/ from site/ and guards the URLs shipped apps depend on."""

import re
import shutil
from pathlib import Path

from . import urls

REQUIRED_PATHS = (
    "games/water-sort/privacy-policy.html",
    "games/water-sort/terms-of-use.html",
    "games/water-sort/kvkk.html",
    "games/mahjong-caravan/privacy-policy.html",
    "games/mahjong-caravan/terms-of-use.html",
    "games/mahjong-caravan/kvkk.html",
    "games/tile-swap-puzzle/privacy-policy.html",
    "games/tile-swap-puzzle/terms-of-use.html",
    "mahjong-caravan/privacy-policy.html",
    "mahjong-caravan/terms-of-use.html",
    "tile-swap-puzzle/privacy-policy.html",
    "tile-swap-puzzle/terms-of-use.html",
    "games/water-sort/config.json",
    "app-ads.txt",
    "index.html",
)

TEXT_SUFFIXES = {".html", ".css", ".js", ".mjs", ".json", ".txt", ".xml", ".svg"}
FORBIDDEN = re.compile(r"\bBerk\b")


def write(out: Path, rel: str, text: str) -> None:
    target = out / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def missing_required(out: Path) -> list[str]:
    return [p for p in REQUIRED_PATHS if not (out / p).is_file()]


def forbidden_hits(out: Path) -> list[str]:
    hits = []
    for f in sorted(out.rglob("*")):
        if f.is_file() and f.suffix in TEXT_SUFFIXES:
            if FORBIDDEN.search(f.read_text(encoding="utf-8", errors="ignore")):
                hits.append(f.relative_to(out).as_posix())
    return hits


def total_size(out: Path) -> int:
    return sum(f.stat().st_size for f in out.rglob("*") if f.is_file())


def build(root: Path, out: Path) -> None:
    from .data import load_site, validate

    errors = validate(load_site(root))
    if errors:
        print("\n".join(errors))
        raise SystemExit(1)
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(root / "site" / "root", out)
    for folder in ("css", "js", "assets"):
        shutil.copytree(root / "site" / folder, out / folder,
                        ignore=shutil.ignore_patterns("manifest.json", ".DS_Store"))
    _render_pages(root, out)
    problems = [f"missing: {p}" for p in missing_required(out)]
    problems += [f"forbidden name in: {p}" for p in forbidden_hits(out)]
    if problems:
        print("\n".join(problems))
        raise SystemExit(1)


LEGACY_DOCS = {
    "mahjong-caravan": ("privacy-policy", "terms-of-use"),
    "tile-swap-puzzle": ("privacy-policy", "terms-of-use"),
}


def _render_pages(root: Path, out: Path) -> None:
    from .data import load_site
    from .game import render_game
    from .home import render_home
    from .legal import render_legal
    from .extras import render_404, robots, sitemap

    site = load_site(root)
    write(out, "404.html", render_404(site))
    write(out, "sitemap.xml", sitemap(site))
    write(out, "robots.txt", robots())
    write(out, "index.html", render_home(site, "en"))
    write(out, "tr/index.html", render_home(site, "tr"))

    for game in site["games"]:
        for lang in ("en", "tr"):
            rel = urls.game_path(lang, game["id"]).lstrip("/") + "index.html"
            write(out, rel, render_game(site, game, lang))
        for doc in game["legal_docs"]:
            write(out, urls.legal_path(game["id"], doc).lstrip("/"), render_legal(site, game, doc))
        for doc in LEGACY_DOCS.get(game["id"], ()):
            write(out, f"{game['id']}/{doc}.html", render_legal(site, game, doc, legacy=True))
