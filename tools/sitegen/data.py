"""Loads and validates site/data/*.json."""

import json
from pathlib import Path

LANGS = ("en", "tr")
GAME_TEXT_FIELDS = ("name", "card", "short")
STUDIO_TEXT_FIELDS = ("legal_date",)


def t(value, lang: str) -> str:
    """Pick the lang variant of a {"en","tr"} value; plain strings pass through."""
    return value[lang] if isinstance(value, dict) else value


def load_site(root: Path) -> dict:
    data = root / "site" / "data"
    return {
        "studio": json.loads((data / "studio.json").read_text(encoding="utf-8")),
        "games": json.loads((data / "games.json").read_text(encoding="utf-8")),
        "root": root,
    }


def _check_text(value, where: str, errors: list) -> None:
    if not isinstance(value, dict):
        errors.append(f"{where}: expected {{en, tr}}")
        return
    for lang in LANGS:
        if not isinstance(value.get(lang), str) or not value[lang].strip():
            errors.append(f"{where}: missing {lang}")


def validate(site: dict) -> list[str]:
    errors: list[str] = []
    studio = site["studio"]
    for field in STUDIO_TEXT_FIELDS:
        _check_text(studio.get(field), f"studio.{field}", errors)
    for lang in LANGS:
        if len(studio.get("intro", {}).get(lang, [])) != 2:
            errors.append(f"studio.intro: {lang} needs 2 paragraphs")
    for key, value in studio.get("labels", {}).items():
        _check_text(value, f"studio.labels.{key}", errors)

    for game in site["games"]:
        gid = game.get("id", "?")
        for field in GAME_TEXT_FIELDS:
            _check_text(game.get(field), f"{gid}.{field}", errors)
        if game.get("age_row") is not None:
            _check_text(game["age_row"], f"{gid}.age_row", errors)
        if game.get("orientation") not in ("landscape", "portrait"):
            errors.append(f"{gid}.orientation: invalid")
        for i, feat in enumerate(game.get("features", [])):
            _check_text(feat.get("title"), f"{gid}.features[{i}].title", errors)
            _check_text(feat.get("text"), f"{gid}.features[{i}].text", errors)
        if not 4 <= len(game.get("features", [])) <= 6:
            errors.append(f"{gid}.features: need 4-6")
        for i, row in enumerate(game.get("info", [])):
            _check_text(row[0], f"{gid}.info[{i}].label", errors)
            _check_text(row[1], f"{gid}.info[{i}].value", errors)
        for doc in game.get("legal_docs", []):
            for lang in LANGS:
                src = site["root"] / "site" / "legal" / gid / f"{doc}.{lang}.html" if "root" in site else None
                if src is not None and not src.is_file():
                    errors.append(f"{gid}.legal_docs: missing {src.name}")
        errors += _check_media(site, game)
    return errors


def _check_media(site: dict, game: dict) -> list[str]:
    media = game.get("media") or {}
    if not media or "root" not in site:
        return []
    base = site["root"] / "site" / "assets" / "media" / game["id"]
    files = [media.get("icon"), media.get("icon_large")]
    for key in ("hero_video", "hero_poster"):
        files += list((media.get(key) or {}).values())
    for lang_list in (media.get("screens") or {}).values():
        files += [s["file"] for s in lang_list]
    files += list((media.get("motion") or {}).values())
    errors = []
    for f in files:
        if isinstance(f, list):
            missing = [x for x in f if not (base / x).is_file()]
        else:
            missing = [f] if f and not (base / f).is_file() else []
        errors += [f"{game['id']}.media: missing {m}" for m in missing]
    return errors
