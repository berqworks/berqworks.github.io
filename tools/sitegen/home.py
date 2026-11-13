"""Home page: studio intro, then the games stacked with icons alternating sides."""

from html import escape

from . import urls
from .data import t
from .layout import HEADING_FONTS, page


def _game_row(site: dict, game: dict, lang: str, side: str) -> str:
    labels = site["studio"]["labels"]
    theme = game["theme"]
    style = (f"--bg:{theme['bg']};--bg2:{theme['bg2'] or theme['bg']};--fg:{theme['fg']};"
             f"--accent:{theme['accent']};--heading-font:{HEADING_FONTS[game['heading_font']]}")
    meta = t(labels["coming_soon_row"], lang)
    if game.get("age_row"):
        meta += " · " + t(game["age_row"], lang)
    icon = f"/assets/media/{game['id']}/{game['media']['icon']}"
    return f"""<a class="game-row game-row--{side}" href="{urls.game_path(lang, game['id'])}" data-game="{game['id']}" style="{escape(style)}">
<img class="game-icon" src="{icon}" width="256" height="256" alt="" loading="lazy">
<div class="game-text">
<h2 class="game-name">{escape(t(game['name'], lang))}</h2>
<p class="game-card">{escape(t(game['card'], lang))}</p>
<p class="game-meta">{escape(meta)}</p>
<span class="game-cta">{escape(t(labels['meet'], lang))}</span>
</div>
</a>"""


def render_home(site: dict, lang: str) -> str:
    intro = site["studio"]["intro"][lang]
    rows = "\n".join(_game_row(site, g, lang, "left" if i % 2 == 0 else "right")
                     for i, g in enumerate(site["games"]))
    body = f"""<section class="studio">
<h1 class="studio-mark">BerqWorks</h1>
<div class="studio-text">
<p class="studio-lede">{escape(intro[0])}</p>
<p class="studio-aside">{escape(intro[1])}</p>
</div>
</section>
<section class="games" id="games" aria-label="{escape(t(site['studio']['nav']['games'], lang))}">
{rows}
</section>"""
    path = urls.home_path(lang)
    return page(site=site, lang=lang, title="BerqWorks", description=intro[0].split(". ")[0] + ".",
                path=path, alt_path=urls.home_path(urls.other(lang)), body=body, body_class="home")
