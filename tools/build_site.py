"""BerqWorks sitesini üretir: oyun bilgileri (GAMES) + ortak düzen → index.html ve games/<oyun>/index.html.
Stil assets/site.css, betik assets/site.js, görseller assets/games/<oyun>/.
Kullanım (depo kökünden): python3 tools/build_site.py
Yeni oyun: GAMES'e bir kayıt ekle, görsellerini assets/games/<id>/ altına koy, betiği çalıştır.
Belge adresleri (gizlilik, koşullar) Play Console'da kayıtlıdır; değiştirme.
"""
import html
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SITE = "https://berqworks.github.io"


def t(tr, en=None):
    """İki dilli metin; en verilmezse iki dilde aynı."""
    if en is None:
        return html.escape(tr)
    return '<span data-l="tr">%s</span><span data-l="en">%s</span>' % (html.escape(tr), html.escape(en))


def plain(text_html, lang="en"):
    """t() çıktısından tek dilin düz metni (meta etiketleri için)."""
    import re
    m = re.search(r'<span data-l="%s">(.*?)</span>' % lang, text_html)
    return html.unescape(m.group(1) if m else re.sub(r"<[^>]+>", "", text_html))


GAMES = [
    {
        "id": "tile-swap-puzzle",
        "name": t("Tile Swap: Kids Puzzle Games"),
        "band": "linear-gradient(135deg, #1b1740, #332b70)",
        "accent": "#ffa94d", "accent_ink": "#2a1a00", "tint": "#9b87ec",
        "icon": "/assets/games/tile-swap-puzzle/icon.png",
        "card": t("Küçük çocukların parçaların yerini değiştirerek renkli resimleri tamamladığı, süresiz bir yapboz oyunu.",
                  "A no-timer puzzle game where young children swap tiles to complete colorful pictures."),
        "lead": t("Tile Swap, küçük çocuklar için bir resim yapbozu. Resim karelere bölünüp karıştırılır; çocuk iki parçaya dokunarak ya da sürükleyerek yerlerini değiştirir, doğru yere gelen parça yerine oturur. Süre ve baskı yok: 2×2 ile başlar, kendi hızında büyür.",
                  "Tile Swap is a picture puzzle for young children. The picture is cut into squares and shuffled; your child taps or drags two pieces to swap them, and each piece clicks into place when it lands in the right spot. No timer, no pressure: it starts at 2×2 and grows at your child's own pace."),
        "feature_img": "/assets/games/tile-swap-puzzle/feature.jpg",
        "features": [
            ("⏱", t("Süre yok", "No timer"), t("Hiçbir tahtada sayaç yok, her yapbozu kendi hızında çöz.", "There is no countdown on any board; every puzzle is solved at your own pace.")),
            ("2×2", t("Kolaydan zora", "From easy to hard"), t("2×2'den 4×4'e üç zorluk; büyükler için Ayarlar'dan 5×5 ve 6×6 uzman seviyeleri.", "Three levels from 2×2 to 4×4, plus 5×5 and 6×6 expert grids in Settings for older kids.")),
            ("180", t("18 kategori, 180 resim", "18 categories, 180 pictures"), t("Hayvanlar, deniz, taşıtlar ve oyuncaklar ücretsiz; uzay, dinozorlar, masallar, çiftlik ve özel günler gibi 14 kategori daha açılabilir.", "Animals, sea, vehicles and toys are free; 14 more categories such as space, dinosaurs, fairy tales, farm and holidays can be unlocked.")),
            ("★", t("Çıkartma albümü", "Sticker album"), t("Biten her yapboz albüme bir çıkartma olarak eklenir.", "Every finished puzzle is added to the album as a sticker.")),
            ("7", t("Haftanın Yapbozu", "Puzzle of the Week"), t("Her pazartesi kilitli bir kategoriden bir yapboz ücretsiz oynanır.", "Every Monday, one puzzle from a locked category is free to play.")),
            ("🔒", t("Ebeveyn kapısı", "Parental gate"), t("Satın almalar ve dış bağlantılar yalnızca bir yetişkin doğrulamasından sonra açılır.", "Purchases and outside links open only after an adult check.")),
        ],
        "shots": "landscape",
        "gallery": {
            "en": [("en_1-ana_menu", "Main menu"), ("en_2-kategoriler", "18 categories"), ("en_3-yapbozlar", "Puzzles in a category"), ("en_4-oyun", "Solving a puzzle"), ("en_5-tebrikler", "A finished picture"), ("en_6-album", "Sticker album")],
            "tr": [("tr_1-oyun", "Yapboz sırasında"), ("tr_2-kategoriler", "18 kategori"), ("tr_3-yapbozlar", "Bir kategorideki yapbozlar"), ("tr_4-tebrikler", "Tamamlanan resim"), ("tr_5-album", "Çıkartma albümü"), ("tr_6-ana_menu", "Ana menü")],
        },
        "gallery_dir": "tile-swap-puzzle",
        "play": None,
        "docs": [
            (t("Gizlilik Politikası", "Privacy Policy"), "https://berqworks.github.io/tile-swap-puzzle/privacy-policy.html", "/tile-swap-puzzle/privacy-policy.html", "update"),
            (t("Kullanım Koşulları", "Terms of Use"), "https://berqworks.github.io/tile-swap-puzzle/terms-of-use.html", "/tile-swap-puzzle/terms-of-use.html", "live"),
        ],
        "facts": [
            (t("Platform", "Platform"), t("Android, telefon ve tablet (yatay)", "Android, phone and tablet (landscape)")),
            (t("Yaş", "Ages"), t("Okul öncesi (3–6)", "Preschool (3–6)")),
            (t("Diller", "Languages"), t("10 dil: Türkçe, İngilizce, Almanca, Fransızca, İspanyolca, Portekizce, İtalyanca, Rusça, Çince, Japonca", "10 languages: English, Turkish, German, French, Spanish, Portuguese, Italian, Russian, Chinese, Japanese")),
            (t("Fiyat", "Price"), t("İndirmesi ücretsiz; reklam içerir, uygulama içi satın alma", "Free to download; contains ads, in-app purchases")),
            (t("Paket", "Package"), t("com.berqworks.tileswappuzzle")),
        ],
    },
    {
        "id": "mahjong-caravan",
        "name": t("Mahjong Caravan: Tile Journey"),
        "band": "linear-gradient(135deg, #14422e, #1f5a40)",
        "accent": "#d8a54a", "accent_ink": "#2b1d00", "tint": "#2f7d5b",
        "icon": "/assets/games/mahjong-caravan/icon.png",
        "card": t("Acele etmeden oynanan, her tahtası çözülebilir sakin bir mahjong solitaire.",
                  "A calm mahjong solitaire you can play at your own pace, where every board can be solved."),
        "lead": t("Mahjong Caravan, açık iki eş taşı eşleştirip tahtayı temizlediğin tek kişilik bir mahjong solitaire oyunu. Süre sınırı ve ceza yok; geri alma sınırsız, her tahta çözülebilir olarak kurulur. 400 seviyelik bir macera ya da 46 yerleşimle serbest oyun seni bekliyor.",
                  "Mahjong Caravan is a single-player mahjong solitaire game: match pairs of free tiles and clear the board. There is no time limit and no penalty, undo is unlimited, and every board is built to be solvable. Play a 400-level journey, or pick any of 46 layouts in free play."),
        "feature_img": None,
        "features": [
            ("✓", t("Her tahta çözülebilir", "Every board can be solved"), t("Tahtalar çözümü garanti edecek biçimde kurulur; kilitlenirsen karıştır, yine çözülebilir kalır.", "Boards are built so a solution always exists; if you get stuck, shuffle and it stays solvable.")),
            ("⏱", t("Süre sınırı yok", "No time limit"), t("Saat yalnızca yıldız için tutulur; hiçbir tahta süre dolduğu için bitmez.", "The clock only counts toward stars; no board ever ends because time ran out.")),
            ("↶", t("Sınırsız geri al", "Unlimited undo"), t("Yanlış hamleyi ceza almadan geri al, istediğin kadar dene.", "Take back any move without a penalty and try as often as you like.")),
            ("400", t("400 seviye, 46 yerleşim", "400 levels, 46 layouts"), t("Kaplumbağadan pagodaya, kolaydan zora ilerleyen bir macera ve dilediğin yerleşimi seçtiğin serbest oyun.", "A journey from turtle to pagoda that grows from easy to hard, plus free play on any layout you choose.")),
            ("★", t("Yıldızla açılan temalar", "Themes unlocked with stars"), t("9 taş teması, 4 arka plan, aydınlık ve koyu görünüm.", "9 tile themes, 4 backgrounds, light and dark looks.")),
            ("Aa", t("Gözü yormayan tasarım", "Easy on the eyes"), t("Büyük taşlar ve yazılar, yüksek kontrast teması, solak modu, serbest taş vurgusu, animasyonları azaltma.", "Large tiles and text, a high-contrast theme, left-handed mode, free-tile highlighting and reduced motion.")),
        ],
        "shots": "landscape",
        "gallery": {
            "en": [("en_menu", "Main menu"), ("en_mid", "Mid-game"), ("en_mid_dark", "Dark look"), ("en_levels", "400 levels"), ("en_layouts", "46 layouts"), ("en_themes", "Themes")],
            "tr": [("tr_menu", "Ana menü"), ("tr_mid", "Bir tahtanın ortasında"), ("tr_mid_dark", "Koyu görünüm"), ("tr_levels", "400 seviye"), ("tr_layouts", "46 yerleşim"), ("tr_themes", "Temalar")],
        },
        "gallery_dir": "mahjong-caravan",
        "play": None,
        "docs": [
            (t("Gizlilik Politikası", "Privacy Policy"), "https://berqworks.github.io/mahjong-caravan/privacy-policy.html", "/mahjong-caravan/privacy-policy.html", "live"),
            (t("Kullanım Koşulları", "Terms of Use"), "https://berqworks.github.io/mahjong-caravan/terms-of-use.html", "/mahjong-caravan/terms-of-use.html", "live"),
        ],
        "facts": [
            (t("Platform", "Platform"), t("Android (yatay)", "Android (landscape)")),
            (t("Yaş", "Ages"), t("Herkes (PEGI 3)", "Everyone (PEGI 3)")),
            (t("Diller", "Languages"), t("Türkçe, İngilizce", "English, Turkish")),
            (t("Fiyat", "Price"), t("Ücretsiz; reklam içerir, isteğe bağlı satın alma", "Free; contains ads, optional purchase")),
            (t("Paket", "Package"), t("com.berqworks.mahjongcaravan")),
        ],
    },
    {
        "id": "water-sort",
        "name": t("Water Sort: Renk Atlası", "Water Sort: Color Atlas"),
        "band": "linear-gradient(135deg, #0f1424, #1d2645)",
        "accent": "#ffc94d", "accent_ink": "#12192e", "tint": "#3b6fd6",
        "icon": "/assets/games/water-sort/icon.svg",
        "card": t("Renkleri kaplarına ayır; her seviyede solmuş bir sahne yeniden renklensin.",
                  "Sort the colors into their own vessels and bring a faded scene back to color, level by level."),
        "lead": t("Renkli sıvıları kaplar arasında dökerek her rengi kendi kabında topla. Renkleri ayırdıkça Atlas'ın solmuş sahneleri parça parça yeniden renklenir; 20 seviyede bir sahne baştan sona canlanır.",
                  "Pour colored liquids between vessels until every color sits in its own. As you sort, the faded scenes of the Atlas come back to color piece by piece, and every 20 levels a whole scene comes alive."),
        "feature_img": None,
        "features": [
            ("50", t("Renk Atlası", "The Color Atlas"), t("50 sayfa, 1.000 seviye. Her seviye sahnede bir bölgeyi renklendirir.", "50 pages, 1,000 levels. Each level brings color back to one area of a scene.")),
            ("◇", t("Her seviyede başka bir merkez kap", "A new center vessel every level"), t("Ortadaki büyük kap 8 birim alır ve biçimi renklenecek nesneyi çağrıştırır: deniz feneri, balina, çan…", "The large center vessel holds 8 units and takes the shape of what you are about to color: a lighthouse, a whale, a bell…")),
            ("✓", t("Her seviye çözülebilir", "Every level is solvable"), t("Seviyeler yayından önce çözücüyle doğrulanır. İpucu gerçek bir çözümden gelir; çıkmaza girdiysen bunu açıkça söyler.", "Levels are checked by a solver before release. Hints come from a real solution and tell you plainly when you are stuck.")),
            ("★", t("Renk yardımı", "Color aid"), t("Her rengin kendi sembolü ve deseni var; renkleri ayırt etmekte zorlananlar için 12 sembol.", "Every color has its own symbol and pattern: 12 symbols for players who find colors hard to tell apart.")),
            ("7", t("Günlük bulmaca", "Daily puzzle"), t("Her gün herkese aynı yeni bulmaca; seriyi sürdürdükçe 3. ve 7. günde ek Pigment.", "A new puzzle every day, the same for everyone; keep your streak for bonus Pigment on days 3 and 7.")),
            ("30", t("Şişeler ve arka planlar", "Bottles and backgrounds"), t("Oyun içi Pigment ile 30 şişe, 33 arka plan (12'si hareketli) ve sıvı efektleri.", "Collect 30 bottles, 33 backgrounds (12 animated) and liquid effects with in-game Pigment.")),
        ],
        "shots": "portrait",
        "gallery": {
            "en": [("en_page_complete", "Page complete: Harbor Town"), ("en_level", "Level 20"), ("en_very_hard", "A Very Hard level"), ("en_shop", "Shop: bottles"), ("en_daily_puzzle", "Daily puzzle"), ("en_daily_streak", "Daily streak")],
            "tr": [("tr_page_complete", "Tamamlanan sayfa: Liman Kasabası"), ("tr_level", "Seviye 991"), ("tr_color_aid", "Renk yardımı açık"), ("tr_shop", "Mağaza: şişeler"), ("tr_daily_streak", "Günlük seri"), ("tr_level_win", "Seviye tamamlandı")],
        },
        "gallery_dir": "water-sort",
        "play": None,
        "docs": [
            (t("Gizlilik Politikası", "Privacy Policy"), None, "/games/water-sort/privacy-policy.html", "draft"),
            (t("Kullanım Koşulları", "Terms of Use"), None, "/games/water-sort/terms-of-use.html", "draft"),
            (t("KVKK Aydınlatma Metni", "KVKK Notice (Turkey)"), None, "/games/water-sort/kvkk.html", "draft"),
        ],
        "facts": [
            (t("Platform", "Platform"), t("Android, telefon ve tablet", "Android, phone and tablet")),
            (t("Yaş", "Ages"), t("13+")),
            (t("Diller", "Languages"), t("Türkçe, İngilizce", "English, Turkish")),
            (t("Fiyat", "Price"), t("Ücretsiz; reklam içerir, uygulama içi satın alma", "Free; contains ads, in-app purchases")),
            (t("Paket", "Package"), t("com.berqworks.watersort")),
        ],
    },
]


DOC_STATE = {
    "live": ("ok", t("Yayında", "Live")),
    "update": ("wait", t("Güncelleniyor", "Being updated")),
    "draft": ("wait", t("Hazırlanıyor", "Coming soon")),
}
SOON = t("Yakında", "Coming soon")
PLAY_SVG = '<svg width="20" height="22" viewBox="0 0 20 22" aria-hidden="true"><path d="M1 1.5v19L19 11z" fill="currentColor"/></svg>'


def mail(id_):
    return ('<div class="mail"><code>berqworks@gmail.com</code><button type="button" data-copy="berqworks@gmail.com" id="%s">%s</button></div>'
            % (id_, t("Kopyala", "Copy")))


def shell(title, description, body, image="/assets/games/water-sort/icon.svg"):
    return f'''<!doctype html>
<html lang="en" data-lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:image" content="{SITE}{image}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=Figtree:wght@400;500;600&display=swap">
<link rel="stylesheet" href="/assets/site.css">
<script src="/assets/site.js" defer></script>
</head>
<body>
<header class="site"><div class="wrap">
  <a class="brand" href="/">Berq<b>Works</b></a>
  <nav class="main">
    <a href="/">{t("Oyunlar", "Games")}</a>
    <a href="/#contact">{t("İletişim", "Contact")}</a>
  </nav>
  <div class="lang" role="group" aria-label="Dil / Language">
    <button type="button" id="lang-tr" data-set-lang="tr">TR</button>
    <button type="button" id="lang-en" data-set-lang="en">EN</button>
  </div>
</div></header>
{body}
<footer class="site"><div class="wrap">
  <span>© 2026 BerqWorks</span>
  <span>berqworks@gmail.com</span>
</div></footer>
</body>
</html>
'''


def card(g):
    return f'''<a class="game" href="/games/{g["id"]}/" style="--g-band: {g["band"]}; --g-accent: {g["accent"]}">
  <div class="band"><img class="icon" alt="" src="{g["icon"]}" width="76" height="76"></div>
  <div class="body">
    <h2>{g["name"]}</h2>
    <p>{g["card"]}</p>
    <div class="foot"><span class="chip wait">{SOON}</span><span class="go">{t("Oyun sayfası →", "Game page →")}</span></div>
  </div>
</a>'''


def home():
    body = f'''<main class="wrap">
  <div class="intro">
    <span class="eyebrow">{t("Bağımsız oyun stüdyosu", "Independent game studio")}</span>
    <h1>{t("Acele etmeden oynanan oyunlar", "Games you can take your time with")}</h1>
    <p>{t("BerqWorks her yaştan oyuncu için sakin mobil oyunlar yapar: süre sınırı yok, can sistemi yok, yalnızca çözülmeyi bekleyen bir tahta.", "BerqWorks makes calm mobile games for players of all ages: no time limits, no energy meters, just a board waiting to be solved.")}</p>
  </div>
  <div class="shelf">
{chr(10).join(card(g) for g in GAMES)}
  </div>
  <div class="about-studio" id="contact">
    <div>
      <h3>{t("Reklam ve satın alma", "Ads and purchases")}</h3>
      <p>{t("Oyunlarımızı indirmek ücretsizdir ve reklam içerir. Reklamlar oyun sırasında değil, bir tahta bittikten sonra çıkar. İsteğe bağlı satın almalar Google Play üzerinden yapılır.", "Our games are free to download and contain ads. Ads appear after a board is finished, never during play. Optional purchases go through Google Play.")}</p>
    </div>
    <div>
      <h3>{t("Gizlilik", "Privacy")}</h3>
      <p>{t("Oyunlarımız hesap açmanı istemez. Her oyunun gizlilik politikası ve kullanım koşulları kendi sayfasındadır.", "Our games never ask you to create an account. Each game's privacy policy and terms of use are on its own page.")}</p>
    </div>
    <div>
      <h3>{t("İletişim", "Contact")}</h3>
      {mail("copy-home")}
    </div>
  </div>
</main>'''
    return shell("BerqWorks", "BerqWorks makes calm mobile games for players of all ages.", body)


def page(g):
    gid = g["id"]
    feats = "\n".join(f'<li><span class="dot">{html.escape(mark)}</span><span><strong>{title}</strong><span class="d">{desc}</span></span></li>'
                      for mark, title, desc in g["features"])
    galleries = []
    for lang in ("tr", "en"):
        figs = "".join(f'<figure><img loading="lazy" alt="{html.escape(cap)}" src="/assets/games/{gid}/{name}.jpg"><figcaption>{html.escape(cap)}</figcaption></figure>'
                       for name, cap in g["gallery"][lang])
        galleries.append(f'<div class="gallery {g["shots"]}" data-l="{lang}">{figs}</div>')
    docs = []
    for title, url, path, state in g["docs"]:
        cls, label = DOC_STATE[state]
        link = (f'<a href="{url}">{title}</a>' if url else f'<span class="doc-title">{title}</span>')
        docs.append(f'<li><span>{link}<span class="path">{path}</span></span><span class="chip {cls}">{label}</span></li>')
    facts = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in g["facts"])
    feature_img = (f'<img class="feature-art" alt="" src="{g["feature_img"]}">' if g["feature_img"] else "")
    body = f'''<main style="--g-band: {g["band"]}; --g-accent: {g["accent"]}; --g-accent-ink: {g["accent_ink"]}">
  <div class="hero"><div class="wrap">
    <img class="icon" alt="" src="{g["icon"]}" width="120" height="120">
    <div class="hero-text">
      <a class="back" href="/">{t("← Tüm oyunlar", "← All games")}</a>
      <h1>{g["name"]}</h1>
      <p>{g["lead"]}</p>
      <div class="actions"><span class="play" aria-disabled="true">{PLAY_SVG}<span><small>{t("Yakında", "Coming soon to")}</small>Google Play</span></span></div>
    </div>
  </div></div>
  <div class="wrap layout">
    <div class="prose">
      {feature_img}
      <span class="eyebrow">{t("Öne çıkanlar", "Highlights")}</span>
      <ul class="feature-list">{feats}</ul>
      <span class="eyebrow">{t("Ekran görüntüleri", "Screenshots")}</span>
      {"".join(galleries)}
    </div>
    <aside class="side">
      <div class="panel"><h2>{t("Belgeler", "Documents")}</h2><ul class="docs">{"".join(docs)}</ul></div>
      <div class="panel"><h2>{t("Destek", "Support")}</h2>
        <p class="muted">{t("Bir sorun mu var ya da bir önerin mi? Oyunun sürümünü ve cihazını yazarsan daha hızlı yardımcı oluruz.", "Found a problem or have an idea? Mention the game version and your device so we can help faster.")}</p>
        {mail("copy-" + gid)}</div>
      <div class="panel"><h2>{t("Bilgiler", "Details")}</h2><dl class="facts">{facts}</dl></div>
    </aside>
  </div>
</main>'''
    return shell(plain(g["name"]) + " · BerqWorks", plain(g["card"]), body, g["icon"])


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)
    print("yazıldı:", path)


def main():
    write("index.html", home())
    for g in GAMES:
        write(os.path.join("games", g["id"], "index.html"), page(g))


if __name__ == "__main__":
    main()
