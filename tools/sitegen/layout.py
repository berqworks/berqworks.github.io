"""Shared page shell: head, top bar, footer."""

import re
from html import escape

from . import urls
from .data import t

HEAD_RUNNER = (
    'var s=null;try{s=localStorage.getItem("bw-lang")}catch(e){}'
    'var d=document.documentElement;'
    'var r=decide({pathname:location.pathname,hash:location.hash,referrer:document.referrer,'
    'origin:location.origin,stored:s,navLang:navigator.language||"",legal:d.hasAttribute("data-legal")});'
    'if(r.redirect){location.replace(r.redirect+location.hash)}else if(r.lang){d.dataset.lang=r.lang;d.lang=r.lang}'
)


def head_script(root) -> str:
    """lang.js core (pickLang, shouldRedirect, decide) as a classic inline script."""
    src = (root / "site" / "js" / "lang.js").read_text(encoding="utf-8")
    core = src.split("// core:start", 1)[1].split("// core:end", 1)[0]
    core = re.sub(r"^export ", "", core, flags=re.M)
    core = "\n".join(line for line in core.splitlines() if line.strip() and not line.strip().startswith("//"))
    return "<script>(function(){" + core + "\n" + HEAD_RUNNER + "})();</script>"


HEADING_FONTS = {"nunito": "'Nunito'", "baloo": "'Baloo 2'", "aileron": "'Aileron'"}


def _theme_style(theme: dict | None, heading_font: str | None) -> str:
    parts = []
    if theme:
        parts += [f"--bg:{theme['bg']}", f"--bg2:{theme['bg2'] or theme['bg']}",
                  f"--fg:{theme['fg']}", f"--accent:{theme['accent']}"]
    if heading_font:
        parts.append(f"--heading-font:{HEADING_FONTS[heading_font]}")
    return ";".join(parts)


def page(*, site: dict, lang: str, title: str, description: str, path: str, alt_path: str | None,
         body: str, theme: dict | None = None, game_id: str | None = None, heading_font: str | None = None,
         og_image: str = "/assets/brand/og.png", canonical: str | None = None, legal: bool = False,
         body_class: str = "") -> str:
    studio = site["studio"]
    other = urls.other(lang)
    canon = urls.absolute(canonical or path)

    alternates = ""
    if alt_path is not None:
        pair = {lang: path, other: alt_path}
        alternates = "".join(
            f'<link rel="alternate" hreflang="{code}" href="{urls.absolute(pair[code])}">' for code in ("en", "tr"))
        alternates += f'<link rel="alternate" hreflang="x-default" href="{urls.absolute(pair["en"])}">'

    style = _theme_style(theme, heading_font)
    body_attrs = f' class="{escape(body_class)}"' if body_class else ""
    if game_id:
        body_attrs += f' data-game="{game_id}"'
    if style:
        body_attrs += f' style="{escape(style)}"'

    home = urls.home_path(lang)
    switch = ""
    if alt_path is not None:
        switch = (f'<a class="lang-switch" href="{alt_path}" hreflang="{other}" lang="{other}" '
                  f'data-lang-switch="{other}">{other.upper()}</a>')

    nav = t(studio["nav"]["games"], lang), t(studio["nav"]["contact"], lang)
    nav_html = (f'<a href="{home}#games">{escape(nav[0])}</a><a href="#contact">{escape(nav[1])}</a>{switch}')
    if legal:
        # Bilingual page: both label sets, CSS shows the one matching html[data-lang].
        nav_html = "".join(
            f'<a class="legal-{code}" lang="{code}" href="{urls.home_path(code)}#games">'
            f'{escape(t(studio["nav"]["games"], code))}</a>' for code in ("tr", "en"))
        nav_html += '<a href="#contact">' + '<span class="legal-sep" aria-hidden="true"> / </span>'.join(
            f'<span class="legal-{code}" lang="{code}">{escape(t(studio["nav"]["contact"], code))}</span>'
            for code in ("tr", "en")) + "</a>"
    html_attrs = f'lang="{lang}"' + (" data-legal" if legal else "")

    return f"""<!doctype html>
<html {html_attrs}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{head_script(site["root"])}
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<link rel="canonical" href="{canon}">
{alternates}
<meta property="og:type" content="website">
<meta property="og:site_name" content="BerqWorks">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{urls.absolute(og_image)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/brand/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/assets/fonts/fraunces.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/instrument-sans.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/site.css">
<script type="module" src="/js/lang.js"></script>
</head>
<body{body_attrs}>
<header class="top">
<a class="wordmark" href="{home}">BerqWorks</a>
<nav class="top-nav">{nav_html}</nav>
</header>
<main>
{body}
</main>
<footer class="foot" id="contact">
<a class="foot-mail" href="mailto:{studio['email']}">{studio['email']}</a>
<span class="foot-note">© 2026 BerqWorks</span>
</footer>
</body>
</html>
"""
