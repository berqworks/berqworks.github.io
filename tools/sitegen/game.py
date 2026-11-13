"""Game page: hero, how to play, highlights, screens, details, legal."""

from html import escape

from . import urls
from .data import t
from .layout import page


def _media(game: dict, name: str) -> str:
    return f"/assets/media/{game['id']}/{name}"


def motion_attrs(game: dict) -> str:
    """data-* attributes the signature motion (motion.js) reads."""
    m = game["media"]["motion"]
    if "tiles" in m:
        tiles = " ".join(_media(game, f) for f in m["tiles"])
        return f' data-src-body="{_media(game, m["body"])}" data-src-tiles="{tiles}"'
    if "image" in m:
        return f' data-src="{_media(game, m["image"])}"'
    return f' data-src-color="{_media(game, m["color"])}" data-src-mask="{_media(game, m["mask"])}"'


def render_game(site: dict, game: dict, lang: str) -> str:
    labels = site["studio"]["labels"]
    media = game["media"]
    name = t(game["name"], lang)
    portrait = game["orientation"] == "portrait"

    if game.get("play_url"):
        play = f'<a class="play" href="{escape(game["play_url"])}" rel="noopener">{escape(t(labels["get_on_play"], lang))}</a>'
    else:
        play = f'<span class="soon">{escape(t(labels["coming_soon_play"], lang))}</span>'

    hero = f"""<section class="hero{' hero--portrait' if portrait else ''}" id="hero">
<div class="hero-text">
<img class="hero-icon" src="{_media(game, media['icon_large'])}" width="512" height="512" alt="">
<h1>{escape(name)}</h1>
<p class="hero-card">{escape(t(game['card'], lang))}</p>
<div class="play-slot">{play}</div>
</div>
<figure class="hero-media">
<video width="{media['hero_size'][0]}" height="{media['hero_size'][1]}" muted loop playsinline preload="none" data-autoplay poster="{_media(game, media['hero_poster'][lang])}" aria-label="{escape(name)}">
<source src="{_media(game, media['hero_video'][lang])}" type="video/mp4">
</video>
</figure>
</section>"""

    how = f"""<section class="block how" id="how">
<h2>{escape(t(labels['how'], lang))}</h2>
<p class="how-text">{escape(t(game['short'], lang))}</p>
</section>"""

    feats = "\n".join(
        f'<li><h3>{escape(t(f["title"], lang))}</h3><p>{escape(t(f["text"], lang))}</p></li>'
        for f in game["features"])
    highlights = f"""<section class="block highlights" id="highlights">
<h2>{escape(t(labels['highlights'], lang))}</h2>
<div class="highlights-grid">
<div class="motion" data-motion="{game['id']}"{motion_attrs(game)} aria-hidden="true"></div>
<ul class="features">
{feats}
</ul>
</div>
</section>"""

    shots = "\n".join(
        f'<li><img src="{_media(game, s["file"])}" width="{s["w"]}" height="{s["h"]}" alt="{escape(s["alt"])}" loading="lazy"></li>'
        for s in media["screens"][lang])
    screens = f"""<section class="block screens{' screens--portrait' if portrait else ''}" id="screens">
<h2>{escape(t(labels['screens'], lang))}</h2>
<ul class="shots">
{shots}
</ul>
</section>"""

    rows = "\n".join(f"<div><dt>{escape(t(k, lang))}</dt><dd>{escape(t(v, lang))}</dd></div>"
                     for k, v in game["info"])
    details = f"""<section class="block details" id="details">
<h2>{escape(t(labels['details'], lang))}</h2>
<dl class="info">
{rows}
</dl>
</section>"""

    docs = "\n".join(
        f'<li><a href="{urls.legal_path(game["id"], d)}#{lang}">{escape(t(site["studio"]["legal_titles"][d], lang))}</a></li>'
        for d in game["legal_docs"])
    legal = f"""<section class="block legal-links" id="legal">
<h2>{escape(t(labels['legal'], lang))}</h2>
<ul>
{docs}
</ul>
</section>"""

    body = "\n".join([hero, how, highlights, screens, details, legal]) + \
        '\n<script type="module" src="/js/motion.js"></script>'
    return page(site=site, lang=lang, title=f"{name} · BerqWorks", description=t(game["card"], lang),
                path=urls.game_path(lang, game["id"]), alt_path=urls.game_path(urls.other(lang), game["id"]),
                body=body, theme=game["theme"], game_id=game["id"], heading_font=game["heading_font"],
                og_image=f"/assets/brand/og-{game['id']}.png", body_class="game")
