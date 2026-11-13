"""Site paths. All paths are root-relative and end with '/' for pages."""

SITE = "https://berqworks.com"
LANGS = ("en", "tr")


def home_path(lang: str) -> str:
    return "/" if lang == "en" else "/tr/"


def game_path(lang: str, game_id: str) -> str:
    return f"{home_path(lang)}games/{game_id}/"


def legal_path(game_id: str, doc: str) -> str:
    return f"/games/{game_id}/{doc}.html"


def absolute(path: str) -> str:
    return SITE + path


def other(lang: str) -> str:
    return "tr" if lang == "en" else "en"
