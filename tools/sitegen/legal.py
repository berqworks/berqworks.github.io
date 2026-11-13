"""Legal pages: TR and EN bodies on one page, language picked from #tr / #en."""

import re
from html import escape

from . import urls
from .data import t

LANG_ORDER = ("tr", "en")
RELATIVE_HTML = re.compile(r'href="([a-z0-9-]+\.html(?:#[^"]*)?)"')


def _fragment(site: dict, game_id: str, doc: str, lang: str) -> str:
    path = site["root"] / "site" / "legal" / game_id / f"{doc}.{lang}.html"
    return path.read_text(encoding="utf-8")


def render_legal(site: dict, game: dict, doc: str, *, legacy: bool = False) -> str:
    from .layout import page

    studio = site["studio"]
    gid = game["id"]
    version = game.get("legal_version")

    sections = []
    for lang in LANG_ORDER:
        meta = f"{t(studio['labels']['last_updated'], lang)}: {t(studio['legal_date'], lang)}"
        if version:
            meta += f" · {t(studio['labels']['version'], lang)} {version}"
        body = _fragment(site, gid, doc, lang)
        if legacy:
            body = RELATIVE_HTML.sub(lambda m: f'href="/games/{gid}/{m.group(1)}"', body)
        sections.append(f"""<section id="{lang}" lang="{lang}" class="legal-{lang}">
<p class="legal-game"><a href="{urls.game_path(lang, gid)}">{escape(t(game['name'], lang))}</a></p>
<h1>{escape(t(studio['legal_titles'][doc], lang))}</h1>
<p class="legal-meta">{escape(meta)}</p>
{body}
</section>""")

    switch = " ".join(f'<a href="#{lang}" data-legal-lang="{lang}" hreflang="{lang}">{lang.upper()}</a>'
                      for lang in LANG_ORDER)
    body = f"""<div class="legal-strip"><nav class="legal-switch" aria-label="Language / Dil">{switch}</nav></div>
<article class="legal">
{sections[0]}
{sections[1]}
</article>"""
    canonical = urls.legal_path(gid, doc)
    title = (f"{t(studio['legal_titles'][doc], 'en')} · {t(studio['legal_titles'][doc], 'tr')} · "
             f"{t(game['name'], 'en')}")
    return page(site=site, lang="en", title=title, description=title, path=canonical, alt_path=None,
                body=body, theme=game["theme"], game_id=gid, canonical=canonical, legal=True,
                body_class="legal-page")
