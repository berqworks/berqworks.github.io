"""404 page, sitemap.xml and robots.txt."""

from . import urls
from .layout import page


def render_404(site: dict) -> str:
    body = """<section class="studio notfound">
<h1 class="studio-mark">404</h1>
<div class="studio-text">
<p class="studio-lede" lang="en">This page doesn't exist. <a href="/">Back to the home page</a>.</p>
<p class="studio-lede" lang="tr">Bu sayfa yok. <a href="/tr/">Ana sayfaya dön</a>.</p>
</div>
</section>"""
    return page(site=site, lang="en", title="404 · BerqWorks", description="Page not found / Sayfa bulunamadı",
                path="/404.html", alt_path=None, body=body, body_class="home")


def sitemap(site: dict) -> str:
    pairs = [(urls.home_path("en"), urls.home_path("tr"))]
    pairs += [(urls.game_path("en", g["id"]), urls.game_path("tr", g["id"])) for g in site["games"]]
    entries = []
    for en, tr in pairs:
        alts = (f'<xhtml:link rel="alternate" hreflang="en" href="{urls.absolute(en)}"/>'
                f'<xhtml:link rel="alternate" hreflang="tr" href="{urls.absolute(tr)}"/>')
        for path in (en, tr):
            entries.append(f"<url><loc>{urls.absolute(path)}</loc>{alts}</url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(entries) + "\n</urlset>\n")


def robots() -> str:
    return f"User-agent: *\nAllow: /\n\nSitemap: {urls.SITE}/sitemap.xml\n"
