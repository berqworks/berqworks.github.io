"""BerqWorks sitesini üretir: oyun bilgileri (GAMES) + ortak düzen → index.html ve games/<oyun>/index.html.
Stil assets/site.css, betik assets/site.js, görseller assets/games/<oyun>/, paylaşım görselleri assets/og/.
Kullanım (depo kökünden):
  python3 tools/make_images.py   # yeni/değişen ekran görüntüsü varsa (.jpg → .webp, paylaşım görselleri); Pillow gerekir
  python3 tools/build_site.py    # HTML sayfaları; ek paket gerekmez
Yeni oyun: GAMES'e bir kayıt ekle, görsellerini assets/games/<id>/ altına .jpg olarak koy, iki betiği de çalıştır.
Belge adresleri (gizlilik, koşullar) Play Console'da kayıtlıdır; değiştirme.
"""
import html
import os
import re
import struct

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SITE = "https://berqworks.github.io"
EMAIL = "berqworks@gmail.com"


def t(tr, en=None):
    """İki dilli metin; en verilmezse iki dilde aynı."""
    if en is None:
        return html.escape(tr)
    return '<span data-l="tr">%s</span><span data-l="en">%s</span>' % (html.escape(tr), html.escape(en))


def plain(text_html, lang="en"):
    """t() çıktısından tek dilin düz metni (meta etiketleri ve alt metinler için)."""
    m = re.search(r'<span data-l="%s">(.*?)</span>' % lang, text_html)
    return html.unescape(m.group(1) if m else re.sub(r"<[^>]+>", "", text_html))


GAMES = [
    {
        "id": "tile-swap-puzzle",
        "name": t("Tile Swap: Kids Puzzle Games"),
        # Oyun sayfasında ekran görüntüsünün altındaki düz renk alanı (oyunun kendi rengi).
        "color": "#e9873a",
        "icon": "/assets/games/tile-swap-puzzle/icon.webp",
        "card": t("Küçük çocukların parçaların yerini değiştirerek renkli resimleri tamamladığı, süresiz bir yapboz oyunu.",
                  "A no-timer puzzle game where young children swap tiles to complete colorful pictures."),
        "short": t("3–6 yaş · 180 resim", "Ages 3–6 · 180 pictures"),
        "lead": t("Tile Swap, küçük çocuklar için bir resim yapbozu. Resim karelere bölünüp karıştırılır; çocuk iki parçaya dokunarak ya da sürükleyerek yerlerini değiştirir, doğru yere gelen parça yerine oturur. Süre ve baskı yok: 2×2 ile başlar, kendi hızında büyür.",
                  "Tile Swap is a picture puzzle for young children. The picture is cut into squares and shuffled; your child taps or drags two pieces to swap them, and each piece clicks into place when it lands in the right spot. No timer, no pressure: it starts at 2×2 and grows at your child's own pace."),
        "features": [
            (t("Süre yok", "No timer"), t("Hiçbir tahtada sayaç yok, her yapbozu kendi hızında çöz.", "There is no countdown on any board; every puzzle is solved at your own pace.")),
            (t("Kolaydan zora", "From easy to hard"), t("2×2'den 4×4'e üç zorluk; büyükler için Ayarlar'dan 5×5 ve 6×6 uzman seviyeleri.", "Three levels from 2×2 to 4×4, plus 5×5 and 6×6 expert grids in Settings for older kids.")),
            (t("18 kategori, 180 resim", "18 categories, 180 pictures"), t("Hayvanlar, deniz, taşıtlar ve oyuncaklar ücretsiz; uzay, dinozorlar, masallar, çiftlik ve özel günler gibi 14 kategori daha açılabilir.", "Animals, sea, vehicles and toys are free; 14 more categories such as space, dinosaurs, fairy tales, farm and holidays can be unlocked.")),
            (t("Çıkartma albümü", "Sticker album"), t("Biten her yapboz albüme bir çıkartma olarak eklenir.", "Every finished puzzle is added to the album as a sticker.")),
            (t("Haftanın Yapbozu", "Puzzle of the Week"), t("Her pazartesi kilitli bir kategoriden bir yapboz ücretsiz oynanır.", "Every Monday, one puzzle from a locked category is free to play.")),
            (t("Ebeveyn kapısı", "Parental gate"), t("Satın almalar ve dış bağlantılar yalnızca bir yetişkin doğrulamasından sonra açılır.", "Purchases and outside links open only after an adult check.")),
        ],
        "shots": "landscape",
        "gallery": {
            "en": [("en_1-ana_menu", "Main menu"), ("en_2-kategoriler", "18 categories"), ("en_3-yapbozlar", "Puzzles in a category"), ("en_4-oyun", "Solving a puzzle"), ("en_5-tebrikler", "A finished picture"), ("en_6-album", "Sticker album")],
            "tr": [("tr_1-oyun", "Yapboz sırasında"), ("tr_2-kategoriler", "18 kategori"), ("tr_3-yapbozlar", "Bir kategorideki yapbozlar"), ("tr_4-tebrikler", "Tamamlanan resim"), ("tr_5-album", "Çıkartma albümü"), ("tr_6-ana_menu", "Ana menü")],
        },
        # Oyun sayfasının başındaki görüntü(ler) ve ana sayfadaki kutunun görüntüsü (gallery'deki adlar).
        "hero": {"en": ["en_4-oyun"], "tr": ["tr_1-oyun"]},
        "home_shot": {"en": "en_4-oyun", "tr": "tr_1-oyun"},
        "docs": [
            (t("Gizlilik Politikası", "Privacy Policy"), "https://berqworks.github.io/tile-swap-puzzle/privacy-policy.html", "live"),
            (t("Kullanım Koşulları", "Terms of Use"), "https://berqworks.github.io/tile-swap-puzzle/terms-of-use.html", "live"),
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
        "color": "#1f5a40",
        "icon": "/assets/games/mahjong-caravan/icon.webp",
        "card": t("Acele etmeden oynanan, her tahtası çözülebilir sakin bir mahjong solitaire.",
                  "A calm mahjong solitaire you can play at your own pace, where every board can be solved."),
        "short": t("400 seviye · 46 yerleşim", "400 levels · 46 layouts"),
        "lead": t("Mahjong Caravan, açık iki eş taşı eşleştirip tahtayı temizlediğin tek kişilik bir mahjong solitaire oyunu. Süre sınırı ve ceza yok; geri alma sınırsız, her tahta çözülebilir olarak kurulur. 400 seviyelik bir macera ya da 46 yerleşimle serbest oyun seni bekliyor.",
                  "Mahjong Caravan is a single-player mahjong solitaire game: match pairs of free tiles and clear the board. There is no time limit and no penalty, undo is unlimited, and every board is built to be solvable. Play a 400-level journey, or pick any of 46 layouts in free play."),
        "features": [
            (t("Her tahta çözülebilir", "Every board can be solved"), t("Tahtalar çözümü garanti edecek biçimde kurulur; kilitlenirsen karıştır, yine çözülebilir kalır.", "Boards are built so a solution always exists; if you get stuck, shuffle and it stays solvable.")),
            (t("Süre sınırı yok", "No time limit"), t("Saat yalnızca yıldız için tutulur; hiçbir tahta süre dolduğu için bitmez.", "The clock only counts toward stars; no board ever ends because time ran out.")),
            (t("Sınırsız geri al", "Unlimited undo"), t("Yanlış hamleyi ceza almadan geri al, istediğin kadar dene.", "Take back any move without a penalty and try as often as you like.")),
            (t("400 seviye, 46 yerleşim", "400 levels, 46 layouts"), t("Kaplumbağadan pagodaya, kolaydan zora ilerleyen bir macera ve dilediğin yerleşimi seçtiğin serbest oyun.", "A journey from turtle to pagoda that grows from easy to hard, plus free play on any layout you choose.")),
            (t("Yıldızla açılan temalar", "Themes unlocked with stars"), t("9 taş teması, 4 arka plan, aydınlık ve koyu görünüm.", "9 tile themes, 4 backgrounds, light and dark looks.")),
            (t("Gözü yormayan tasarım", "Easy on the eyes"), t("Büyük taşlar ve yazılar, yüksek kontrast teması, solak modu, serbest taş vurgusu, animasyonları azaltma.", "Large tiles and text, a high-contrast theme, left-handed mode, free-tile highlighting and reduced motion.")),
        ],
        "shots": "landscape",
        "gallery": {
            "en": [("en_menu", "Main menu"), ("en_mid", "Mid-game"), ("en_mid_dark", "Dark look"), ("en_levels", "400 levels"), ("en_layouts", "46 layouts"), ("en_themes", "Themes")],
            "tr": [("tr_menu", "Ana menü"), ("tr_mid", "Bir tahtanın ortasında"), ("tr_mid_dark", "Koyu görünüm"), ("tr_levels", "400 seviye"), ("tr_layouts", "46 yerleşim"), ("tr_themes", "Temalar")],
        },
        "hero": {"en": ["en_mid"], "tr": ["tr_mid"]},
        "home_shot": {"en": "en_mid", "tr": "tr_mid"},
        "docs": [
            (t("Gizlilik Politikası", "Privacy Policy"), "https://berqworks.github.io/mahjong-caravan/privacy-policy.html", "live"),
            (t("Kullanım Koşulları", "Terms of Use"), "https://berqworks.github.io/mahjong-caravan/terms-of-use.html", "live"),
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
        "color": "#1d2645",
        "icon": "/assets/games/water-sort/icon.svg",
        "card": t("Renkleri kaplarına ayır; her seviyede solmuş bir sahne yeniden renklensin.",
                  "Sort the colors into their own vessels and bring a faded scene back to color, level by level."),
        "short": t("1.000 seviye · Günlük bulmaca", "1,000 levels · Daily puzzle"),
        "lead": t("Renkli sıvıları kaplar arasında dökerek her rengi kendi kabında topla. Renkleri ayırdıkça Atlas'ın solmuş sahneleri parça parça yeniden renklenir; 20 seviyede bir sahne baştan sona canlanır.",
                  "Pour colored liquids between vessels until every color sits in its own. As you sort, the faded scenes of the Atlas come back to color piece by piece, and every 20 levels a whole scene comes alive."),
        "features": [
            (t("Renk Atlası", "The Color Atlas"), t("50 sayfa, 1.000 seviye. Her seviye sahnede bir bölgeyi renklendirir.", "50 pages, 1,000 levels. Each level brings color back to one area of a scene.")),
            (t("Her seviyede başka bir merkez kap", "A new center vessel every level"), t("Ortadaki büyük kap 8 birim alır ve biçimi renklenecek nesneyi çağrıştırır: deniz feneri, balina, çan…", "The large center vessel holds 8 units and takes the shape of what you are about to color: a lighthouse, a whale, a bell…")),
            (t("Her seviye çözülebilir", "Every level is solvable"), t("Seviyeler yayından önce çözücüyle doğrulanır. İpucu gerçek bir çözümden gelir; çıkmaza girdiysen bunu açıkça söyler.", "Levels are checked by a solver before release. Hints come from a real solution and tell you plainly when you are stuck.")),
            (t("Renk yardımı", "Color aid"), t("Her rengin kendi sembolü ve deseni var; renkleri ayırt etmekte zorlananlar için 12 sembol.", "Every color has its own symbol and pattern: 12 symbols for players who find colors hard to tell apart.")),
            (t("Günlük bulmaca", "Daily puzzle"), t("Her gün herkese aynı yeni bulmaca; seriyi sürdürdükçe 3. ve 7. günde ek Pigment.", "A new puzzle every day, the same for everyone; keep your streak for bonus Pigment on days 3 and 7.")),
            (t("Şişeler ve arka planlar", "Bottles and backgrounds"), t("Oyun içi Pigment ile 30 şişe, 33 arka plan (12'si hareketli) ve sıvı efektleri.", "Collect 30 bottles, 33 backgrounds (12 animated) and liquid effects with in-game Pigment.")),
        ],
        "shots": "portrait",
        "gallery": {
            "en": [("en_page_complete", "Page complete: Harbor Town"), ("en_level", "Level 20"), ("en_very_hard", "A Very Hard level"), ("en_shop", "Shop: bottles"), ("en_daily_puzzle", "Daily puzzle"), ("en_daily_streak", "Daily streak")],
            "tr": [("tr_page_complete", "Tamamlanan sayfa: Liman Kasabası"), ("tr_level", "Seviye 991"), ("tr_color_aid", "Renk yardımı açık"), ("tr_shop", "Mağaza: şişeler"), ("tr_daily_streak", "Günlük seri"), ("tr_level_win", "Seviye tamamlandı")],
        },
        "hero": {"en": ["en_level", "en_page_complete"], "tr": ["tr_level", "tr_page_complete"]},
        "home_shot": {"en": "en_level", "tr": "tr_level"},
        "docs": [
            (t("Gizlilik Politikası", "Privacy Policy"), "/games/water-sort/privacy-policy.html", "live"),
            (t("Kullanım Koşulları", "Terms of Use"), "/games/water-sort/terms-of-use.html", "live"),
            (t("KVKK Aydınlatma Metni", "KVKK Notice (Turkey)"), "/games/water-sort/kvkk.html", "live"),
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
    "live": None,
    "update": t("Güncelleniyor", "Being updated"),
    "draft": t("Hazırlanıyor", "Coming soon"),
}
PLAY_SVG = '<svg width="14" height="16" viewBox="0 0 20 22" aria-hidden="true" focusable="false"><path d="M1 1.5v19L19 11z" fill="currentColor"/></svg>'
SOON = t("Google Play'de yakında", "Coming soon to Google Play")


def webp_size(path):
    """WebP dosyasının (genişlik, yükseklik) değeri; ek paket gerektirmez."""
    with open(path, "rb") as f:
        head = f.read(30)
    kind = head[12:16]
    if kind == b"VP8 ":
        w, h = struct.unpack("<HH", head[26:30])
        return w & 0x3FFF, h & 0x3FFF
    if kind == b"VP8L":
        b = head[21:25]
        w = 1 + (((b[1] & 0x3F) << 8) | b[0])
        h = 1 + (((b[3] & 0xF) << 10) | (b[2] << 2) | ((b[1] & 0xC0) >> 6))
        return w, h
    if kind == b"VP8X":
        return 1 + int.from_bytes(head[24:27], "little"), 1 + int.from_bytes(head[27:30], "little")
    raise ValueError("WebP değil: " + path)


def caption(g, lang, name):
    return dict(g["gallery"][lang])[name]


def shot(g, lang, name, alt=None, lazy=True):
    """Bir ekran görüntüsü; data-l ile yalnızca seçili dilde görünür."""
    src = "/assets/games/%s/%s.webp" % (g["id"], name)
    w, h = webp_size(os.path.join(ROOT, src.lstrip("/")))
    if alt is None:
        alt = "%s: %s" % (plain(g["name"], lang), caption(g, lang, name))
    load = 'loading="lazy" ' if lazy else 'fetchpriority="high" '
    return (f'<img data-l="{lang}" src="{src}" width="{w}" height="{h}" {load}decoding="async" '
            f'alt="{html.escape(alt)}">')


def mail(id_):
    return (f'<div class="mail"><a class="mail-addr" href="mailto:{EMAIL}">{EMAIL}</a>'
            f'<button type="button" class="copy" data-copy="{EMAIL}" id="{id_}">{t("Kopyala", "Copy")}</button></div>')


EARLY_LANG = ('(function(){var d=document.documentElement,l=null,h=location.hash.slice(1);'
              'try{l=localStorage.getItem("bw-lang")}catch(e){}'
              'if(h==="tr"||h==="en")l=h;'
              'if(!l)l=(navigator.language||"en").toLowerCase().indexOf("tr")===0?"tr":"en";'
              'd.setAttribute("data-lang",l);d.lang=l})();')


def shell(title, description, body, path, image="/assets/og/home.jpg", title_tr=None, nav=None):
    def navlink(href, label, key):
        cur = ' aria-current="page"' if key == nav else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    return f'''<!doctype html>
<html lang="en" data-lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="bw-title-en" content="{html.escape(title)}">
<meta name="bw-title-tr" content="{html.escape(title_tr or title)}">
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="BerqWorks">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:image" content="{SITE}{image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#f3ede1" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#131b17" media="(prefers-color-scheme: dark)">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/assets/fonts/fraunces-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/atkinson-next-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/site.css">
<script>{EARLY_LANG}</script>
<script src="/assets/site.js" defer></script>
</head>
<body>
<a class="skip" href="#main">{t("İçeriğe geç", "Skip to content")}</a>
<header class="site">
  <div class="wrap bar">
    <a class="brand" href="/">BerqWorks</a>
    <nav class="main" aria-label="BerqWorks">
      {navlink("/#games", t("Oyunlar", "Games"), "games")}
      {navlink("/#contact", t("İletişim", "Contact"), "contact")}
    </nav>
    <div class="lang" role="group" aria-label="Dil / Language">
      <button type="button" id="lang-tr" data-set-lang="tr" lang="tr" aria-label="Türkçe">TR</button>
      <button type="button" id="lang-en" data-set-lang="en" lang="en" aria-label="English">EN</button>
    </div>
  </div>
</header>
<main id="main" tabindex="-1">
{body}
</main>
<footer class="site">
  <div class="wrap foot">
    <span class="brand-sm">BerqWorks</span>
    <span>{t("Bağımsız oyun stüdyosu", "Independent game studio")} · © 2026</span>
    <a href="mailto:{EMAIL}">{EMAIL}</a>
  </div>
</footer>
</body>
</html>
'''


def tile(g, i):
    """Ana sayfada bir oyun: masaya bırakılmış bir taş."""
    shots = "".join(shot(g, lang, g["home_shot"][lang]) for lang in ("tr", "en"))
    kind = g["shots"]
    extra = " tile--indent" if (kind == "landscape" and i % 2 == 1) else ""
    return f'''<article class="tile tile--{kind}{extra}">
      <div class="frame">{shots}</div>
      <div class="tile-text">
        <img class="icon" src="{g["icon"]}" width="56" height="56" alt="" loading="lazy">
        <div>
          <h3><a href="/games/{g["id"]}/">{g["name"]}</a></h3>
          <p>{g["card"]}</p>
          <p class="meta">{g["short"]}<span class="sep" aria-hidden="true"> · </span><span class="soon">{SOON}</span></p>
        </div>
      </div>
    </article>'''


def home():
    landscape = [g for g in GAMES if g["shots"] == "landscape"]
    tiles = [tile(g, landscape.index(g) if g in landscape else 0) for g in GAMES]
    body = f'''<section class="intro wrap">
  <p class="kicker">{t("Bağımsız oyun stüdyosu", "Independent game studio")}</p>
  <h1>{t("Acele etmeden oynanan oyunlar", "Games you can take your time with")}</h1>
  <p class="lede">{t("BerqWorks her yaştan oyuncu için sakin mobil oyunlar yapar: süre sınırı yok, can sistemi yok, yalnızca çözülmeyi bekleyen bir tahta.", "BerqWorks makes calm mobile games for players of all ages: no time limits, no energy meters, just a board waiting to be solved.")}</p>
</section>

<section class="rack wrap" id="games" aria-labelledby="games-h">
  <h2 class="label" id="games-h">{t("Oyunlar", "Games")}</h2>
  <div class="rack-grid">
    {chr(10).join("    " + x for x in tiles).strip()}
  </div>
</section>

<section class="ledger wrap" aria-labelledby="about-h">
  <h2 class="label" id="about-h">{t("Oyunlarımız hakkında", "About our games")}</h2>
  <div class="ledger-row">
    <h3>{t("Reklam ve satın alma", "Ads and purchases")}</h3>
    <p>{t("Oyunlarımızı indirmek ücretsizdir ve reklam içerir. Reklamlar oyun sırasında değil, bir tahta bittikten sonra çıkar. İsteğe bağlı satın almalar Google Play üzerinden yapılır.", "Our games are free to download and contain ads. Ads appear after a board is finished, never during play. Optional purchases go through Google Play.")}</p>
  </div>
  <div class="ledger-row">
    <h3>{t("Gizlilik", "Privacy")}</h3>
    <p>{t("Oyunlarımız hesap açmanı istemez. Her oyunun gizlilik politikası ve kullanım koşulları kendi sayfasındadır.", "Our games never ask you to create an account. Each game's privacy policy and terms of use are on its own page.")}</p>
  </div>
</section>

<div class="contact-band" id="contact">
<section class="contact wrap" aria-labelledby="contact-h">
  <h2 id="contact-h">{t("İletişim", "Contact")}</h2>
  <p>{t("Bir sorun mu var ya da bir önerin mi? Oyunun sürümünü ve cihazını yazarsan daha hızlı yardımcı oluruz.", "Found a problem or have an idea? Mention the game version and your device so we can help faster.")}</p>
  {mail("copy-home")}
</section>
</div>'''
    return shell("BerqWorks", "BerqWorks makes calm mobile games for players of all ages.", body, "/",
                 "/assets/og/home.jpg", "BerqWorks")


def page(g):
    gid = g["id"]
    hero_shots = "".join(
        '<div class="frame">' + "".join(shot(g, lang, g["hero"][lang][k], lazy=False) for lang in ("tr", "en")) + "</div>"
        for k in range(len(g["hero"]["en"])))
    feats = "\n".join(f'      <li><h3>{title}</h3><p>{desc}</p></li>' for title, desc in g["features"])
    galleries = []
    for lang in ("tr", "en"):
        figs = "".join(f'<figure><div class="frame">{shot(g, lang, name)}</div><figcaption>{html.escape(cap)}</figcaption></figure>'
                       for name, cap in g["gallery"][lang])
        label = "Ekran görüntüleri" if lang == "tr" else "Screenshots"
        galleries.append(f'<div class="shots shots--{g["shots"]}" data-l="{lang}" role="region" aria-label="{label}" tabindex="0">{figs}</div>')
    docs = []
    for title, url, state in g["docs"]:
        note = DOC_STATE[state]
        docs.append(f'<li><a href="{url}">{title}</a>' + (f' <span class="note">{note}</span>' if note else "") + "</li>")
    facts = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in g["facts"])
    body = f'''<div class="game" style="--g: {g["color"]}">
<section class="game-hero wrap game-hero--{g["shots"]}">
  <div class="gh-text">
    <a class="back" href="/#games">{t("← Tüm oyunlar", "← All games")}</a>
    <img class="icon" src="{g["icon"]}" width="72" height="72" alt="">
    <h1>{g["name"]}</h1>
    <p class="lede">{g["lead"]}</p>
    <p class="store">{PLAY_SVG}<span>{SOON}</span></p>
  </div>
  <div class="gh-shots">{hero_shots}</div>
</section>

<section class="features wrap" aria-labelledby="f-h">
  <h2 class="label" id="f-h">{t("Öne çıkanlar", "Highlights")}</h2>
  <ul class="feature-list">
{feats}
  </ul>
</section>

<section class="gallery wrap" aria-labelledby="s-h">
  <h2 class="label" id="s-h">{t("Ekran görüntüleri", "Screenshots")}</h2>
  {"".join(galleries)}
</section>

<section class="info wrap" aria-label="{html.escape(plain(g["name"]))}">
  <div class="info-block">
    <h2>{t("Belgeler", "Documents")}</h2>
    <ul class="docs">{"".join(docs)}</ul>
  </div>
  <div class="info-block">
    <h2>{t("Destek", "Support")}</h2>
    <p>{t("Bir sorun mu var ya da bir önerin mi? Oyunun sürümünü ve cihazını yazarsan daha hızlı yardımcı oluruz.", "Found a problem or have an idea? Mention the game version and your device so we can help faster.")}</p>
    {mail("copy-" + gid)}
  </div>
  <div class="info-block">
    <h2>{t("Bilgiler", "Details")}</h2>
    <dl class="facts">{facts}</dl>
  </div>
</section>
</div>'''
    return shell(plain(g["name"]) + " · BerqWorks", plain(g["card"]), body, f"/games/{gid}/",
                 f"/assets/og/{gid}.jpg", plain(g["name"], "tr") + " · BerqWorks", nav="games")


# Bu sitede barındırılan yasal metinler: oyun → (dosya adı, başlık, sürüm, tarih TR, tarih EN).
# Metinler tools/legal/<oyun>/<dosya>.tr.html ve .en.html; sürüm oyundaki Consent.POLICY_VERSION ile aynı olmalı.
LEGAL = {
    "water-sort": [
        ("privacy-policy", t("Gizlilik Politikası", "Privacy Policy"), 1, "16 Ekim 2026", "16 October 2026"),
        ("terms-of-use", t("Kullanım Koşulları", "Terms of Use"), 1, "16 Ekim 2026", "16 October 2026"),
        ("kvkk", t("KVKK Aydınlatma Metni", "KVKK Notice (Turkey)"), 1, "16 Ekim 2026", "16 October 2026"),
    ],
}


def legal_page(g, slug, title, version, date_tr, date_en):
    gid = g["id"]
    src = os.path.join(ROOT, "tools", "legal", gid, slug)
    body_tr = open(src + ".tr.html", encoding="utf-8").read()
    body_en = open(src + ".en.html", encoding="utf-8").read()
    others = "".join(f'<li><a href="{s}.html"{" aria-current=\"page\"" if s == slug else ""}>{tl}</a></li>'
                     for s, tl, _, _, _ in LEGAL[gid])
    body = f'''<div class="game" style="--g: {g["color"]}">
<header class="legal-head wrap">
  <a class="back" href="/games/{gid}/">← {g["name"]}</a>
  <h1>{title}</h1>
  <p class="doc-meta">{t("Son güncelleme: " + date_tr + " · Sürüm " + str(version), "Last updated: " + date_en + " · Version " + str(version))}</p>
</header>
<div class="legal-layout wrap">
  <article class="legal"><div data-l="tr" lang="tr">{body_tr}</div><div data-l="en" lang="en">{body_en}</div></article>
  <aside class="legal-side">
    <nav aria-label="{html.escape(plain(title))}"><h2>{t("Belgeler", "Documents")}</h2><ul class="doc-nav">{others}</ul></nav>
    <div><h2>{t("İletişim", "Contact")}</h2>{mail("copy-" + gid + "-" + slug)}</div>
  </aside>
</div>
</div>'''
    return shell(plain(title) + " · " + plain(g["name"]), plain(title) + " — " + plain(g["name"]), body,
                 f"/games/{gid}/{slug}.html", f"/assets/og/{gid}.jpg",
                 plain(title, "tr") + " · " + plain(g["name"], "tr"), nav="games")


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("yazıldı:", path)


def main():
    write("index.html", home())
    for g in GAMES:
        write(os.path.join("games", g["id"], "index.html"), page(g))
        for slug, title, version, date_tr, date_en in LEGAL.get(g["id"], []):
            write(os.path.join("games", g["id"], slug + ".html"), legal_page(g, slug, title, version, date_tr, date_en))


if __name__ == "__main__":
    main()
