# berqworks.com Uygulama Planı

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stüdyoyu ve üç oyunu tanıtan, EN/TR, statik berqworks.com sitesini ve oyunların yasal sayfalarını üretmek.

**Architecture:** `site/` altındaki veri (JSON), yasal metin parçaları, CSS/JS ve hazırlanmış medyadan, bağımlılıksız bir Python paketi (`tools/sitegen/`) bütün sayfaları `public/` klasörüne üretir ve korunması gereken adresleri denetler. `public/` repoya girer; Netlify ve GitHub Pages (Actions ile, derlemesiz) onu olduğu gibi yayınlar. Medya ve font hazırlığı ayrı, tek seferlik betiklerle yapılır (ffmpeg, cwebp, fontTools); site üretimi bunlara bağlı değildir.

**Tech Stack:** Python 3.14 standart kütüphanesi (`unittest`, `html`, `json`, `pathlib`, `shutil`), düz HTML/CSS/JS, Node 26 yalnızca `node --test` için. Hazırlık araçları: ffmpeg (libx264), cwebp, `.venv-tools` içinde fonttools + brotli.

**Spec:** `docs/superpowers/specs/2026-11-13-berqworks-site-design.md`

## Global Constraints

- Tek içerik kaynağı `~/Desktop/site-gerekli-dosyalar/{mahjong,tile-swap-puzzle,water-sort}` ve oradaki `brief.md`'ler. `_eski-repo-yedek/` açılmaz. Eski site referans alınmaz.
- "geliştiricinin adı" adı (ve tek başına "Zeynep" kelimesi) `public/` içinde hiçbir yerde geçmez.
- Fiyat rakamı, Play bağlantısı, çıkış tarihi yok. Durum: üç oyun da "Coming soon" / "Yakında".
- Analitik, çerez, üçüncü taraf istek yok; fontlar dahil her şey `public/` içinden yüklenir.
- Bütün CSS'te `font-variant-ligatures: none`; her sayfada doğru `lang` (`en` / `tr`).
- Uzun metin 18 px, `line-height: 1.6`.
- Asıl adres `https://berqworks.com`; `canonical`/`hreflang`/`og:url` bununla mutlak yazılır.
- `public/` toplamı 15 MB'ın altında. Ham PNG'ler repoya girmez.
- Ana sayfa ve stüdyo bölümünde Tile Swap yapboz resimleri ya da kategori kapakları yok; yalnızca Tile Swap sayfasında (ekranlar, video, hareket) var.
- Yasal tarihler: "13 Kasım 2026" / "13 November 2026". Water Sort belgelerinde "Sürüm 1" / "Version 1"; diğerlerinde sürüm yok.
- `prefers-reduced-motion: reduce` iken animasyon ve otomatik video yok.
- Görünüm yapay zekâ işi ya da şablon gibi durmamalı: ortalanmış degrade hero, eş kart ızgarası, hazır ikon seti, emoji, mor-mavi degrade yok.
- Commit serbest; push yalnızca kullanıcı onayıyla.

## Review Focus

1. Yasal bağlantı bir bölüm çapasıyla açılır (`privacy-policy.html#tr-7`): sayfa Türkçe seçilmeli ve o bölüme kaymalı. → Task 4, `pickLang` testi.
2. Eski adres kopyasındaki iç bağlantılar (`kvkk.html#tr`, `terms-of-use.html#en`): eski klasörde KVKK kopyası yok, bağlantı 404 vermemeli. → Task 7, mutlak bağlantı testi.
3. Türkçe tarayıcılı ziyaretçi EN'yi elle seçtiyse `/`'e her gelişinde `/tr/`'ye atılmamalı. → Task 4, `shouldRedirect` testi.
4. JavaScript kapalıyken yasal sayfa iki dili de göstermeli (boş sayfa değil). → Task 7, CSS gizleme kuralının yalnızca `html[data-lang]` altında olduğunu doğrulayan test.
5. 360 px telefon: zikzak tek sütuna inmeli, yatay kaydırma olmamalı. → Task 9, görsel denetim adımı.

---

## Dosya yapısı

```
site/
  data/studio.json            stüdyo metni, menü etiketleri, e-posta (EN/TR)
  data/games.json             üç oyunun içeriği, renkleri, fontları, medya listesi, yasal belge listesi
  legal/<id>/<doc>.<lang>.html  kaynak klasörden kopyalanan yasal gövdeler (8 belge × 2 dil)
  root/app-ads.txt            olduğu gibi public/ köküne
  root/games/water-sort/config.json  bayt bayt aynı
  css/site.css                ortak stil + oyun temaları
  js/lang.js                  dil seçimi/yönlendirme (saf fonksiyonlar + DOM bağlama)
  js/motion.js                üç imza hareketi
  assets/fonts/*.woff2        hazırlanmış fontlar + OFL lisansları
  assets/media/<id>/*         hazırlanmış görsel/video
  assets/brand/               favicon, og görselleri
  fonts-src/                  indirilen Fraunces + Instrument Sans TTF ve OFL.txt
tools/
  build.py                    CLI: python3 tools/build.py → public/
  sitegen/__init__.py
  sitegen/data.py             load_site, validate
  sitegen/urls.py             adres yardımcıları
  sitegen/layout.py           ortak sayfa kabuğu
  sitegen/home.py             ana sayfa
  sitegen/game.py             oyun sayfası
  sitegen/legal.py            yasal sayfa + eski kopyalar
  sitegen/build.py            build(), REQUIRED_PATHS, denetimler
  prepare_media.py            ffmpeg/cwebp ile site/assets/media üretir
  prepare_fonts.py            fontTools ile woff2 üretir
tests/
  test_build.py  test_data.py  test_media.py  test_layout.py  test_home.py  test_game.py  test_legal.py
  js/lang.test.mjs
public/                       üretilmiş site (repoya girer)
netlify.toml
.github/workflows/pages.yml
```

Testler: `python3 -m unittest discover -s tests -v` ve `node --test tests/js/`.

---

### Task 1: İskelet, kaynak dosyalar ve adres koruması

**Files:**
- Create: `tools/build.py`, `tools/sitegen/__init__.py`, `tools/sitegen/build.py`, `tools/sitegen/urls.py`, `site/root/app-ads.txt`, `site/root/games/water-sort/config.json`, `site/legal/<id>/*.html`, `netlify.toml`, `.github/workflows/pages.yml`
- Test: `tests/test_build.py`

**Interfaces:**
- Produces:
  - `sitegen.urls.SITE = "https://berqworks.com"`
  - `sitegen.urls.home_path(lang: str) -> str` → `"/"` ya da `"/tr/"`
  - `sitegen.urls.game_path(lang: str, game_id: str) -> str` → `"/games/<id>/"` ya da `"/tr/games/<id>/"`
  - `sitegen.urls.legal_path(game_id: str, doc: str) -> str` → `"/games/<id>/<doc>.html"`
  - `sitegen.build.REQUIRED_PATHS: tuple[str, ...]` (aşağıdaki 15 yol)
  - `sitegen.build.build(root: Path, out: Path) -> None` (çıktıyı silip yeniden üretir; sonraki görevler render çağrılarını buraya ekler)
  - `sitegen.build.missing_required(out: Path) -> list[str]`
  - `sitegen.build.forbidden_hits(out: Path) -> list[str]` (`\bBerk\b` ya da `Hatipoğlu` içeren metin dosyalarının yolları; `.html .css .js .json .txt .xml`)
  - `sitegen.build.total_size(out: Path) -> int`
  - `build()` sonunda `missing_required` ya da `forbidden_hits` boş değilse `SystemExit(1)` ile durur.

- [ ] **Step 1: Kaynak dosyaları repoya kopyala**

```bash
S=~/Desktop/site-gerekli-dosyalar
mkdir -p site/legal/{mahjong-caravan,tile-swap-puzzle,water-sort} site/root/games/water-sort
cp $S/mahjong/legal/{privacy-policy,terms-of-use,kvkk}.{tr,en}.html site/legal/mahjong-caravan/
cp $S/tile-swap-puzzle/legal/{privacy-policy,terms-of-use}.{tr,en}.html site/legal/tile-swap-puzzle/
cp $S/water-sort/legal/{privacy-policy,terms-of-use,kvkk}.{tr,en}.html site/legal/water-sort/
cp $S/water-sort/config.json site/root/games/water-sort/config.json
printf 'google.com, pub-3762683248469893, DIRECT, f08c47fec0942fa0\n' > site/root/app-ads.txt
```

`*.rendered.html` dosyaları kopyalanmaz.

- [ ] **Step 2: Başarısız testleri yaz** (`tests/test_build.py`)

`REQUIRED_PATHS` tam olarak:

```python
EXPECTED = {
  "games/water-sort/privacy-policy.html", "games/water-sort/terms-of-use.html", "games/water-sort/kvkk.html",
  "games/mahjong-caravan/privacy-policy.html", "games/mahjong-caravan/terms-of-use.html", "games/mahjong-caravan/kvkk.html",
  "games/tile-swap-puzzle/privacy-policy.html", "games/tile-swap-puzzle/terms-of-use.html",
  "mahjong-caravan/privacy-policy.html", "mahjong-caravan/terms-of-use.html",
  "tile-swap-puzzle/privacy-policy.html", "tile-swap-puzzle/terms-of-use.html",
  "games/water-sort/config.json", "app-ads.txt", "index.html",
}
```

Testler:
- `test_required_paths_exact`: `set(REQUIRED_PATHS) == EXPECTED`.
- `test_passthrough_byte_identical`: geçici klasöre `build()` sonra `public/games/water-sort/config.json` baytları `site/root/...` ile ve `~/Desktop/site-gerekli-dosyalar/water-sort/config.json` ile aynı (kaynak yoksa bu ikinci karşılaştırmayı atla); `app-ads.txt` içeriği `pub-3762683248469893` içerir.
- `test_missing_required_lists_absent`: boş klasörde `missing_required` 15 yol döndürür.
- `test_forbidden_hits`: `Merhaba Zeynep` yazan geçici `x.html` yakalanır; `berqworks` yazan dosya yakalanmaz.
- `test_urls`: `game_path("tr","water-sort") == "/tr/games/water-sort/"`, `home_path("en") == "/"`, `legal_path("water-sort","kvkk") == "/games/water-sort/kvkk.html"`.

Bu görevde sayfa üreticileri henüz yok; `build()` şimdilik `site/root/` içeriğini kopyalar ve geçici olarak boş bir `index.html` yazar. Bu yüzden `missing_required` testini build sonrası değil, boş klasörde yap.

- [ ] **Step 3: Testleri çalıştır, başarısız olduklarını gör**

Run: `python3 -m unittest tests.test_build -v` → Expected: `ModuleNotFoundError: sitegen`. Testler `sys.path`'e `tools/` ekler.

- [ ] **Step 4: `urls.py` ve `sitegen/build.py`'yi uygula; `tools/build.py` CLI'si `build(repo_root, repo_root/"public")` çağırır ve sonunda `public/` boyutunu MB olarak yazar.**

- [ ] **Step 5: Testleri çalıştır** → Expected: hepsi PASS.

- [ ] **Step 6: Yayın ayarları**

`netlify.toml`:

```toml
[build]
  publish = "public"
  command = ""
```

`.github/workflows/pages.yml`: `push` (main) ve `workflow_dispatch` tetikleyicili; `permissions: pages: write, id-token: write, contents: read`; adımlar `actions/checkout@v4`, `actions/configure-pages@v5`, `actions/upload-pages-artifact@v3` (`path: public`), `actions/deploy-pages@v4`. Derleme adımı yok.

- [ ] **Step 7: Commit**

```bash
git add site/legal site/root tools tests netlify.toml .github
git commit -m "Add site skeleton, legal sources and URL guard"
```

---

### Task 2: Site verisi

**Files:**
- Create: `site/data/studio.json`, `site/data/games.json`, `tools/sitegen/data.py`
- Test: `tests/test_data.py`

**Interfaces:**
- Consumes: Task 1'deki `urls`.
- Produces:
  - `sitegen.data.load_site(root: Path) -> dict` → `{"studio": {...}, "games": [mahjong, tile-swap, water-sort]}` (sıra dosyadaki sıra).
  - `sitegen.data.validate(site: dict) -> list[str]` hata listesi; `build()` boş değilse durur.
  - Metin alanları her zaman `{"en": str, "tr": str}`; `t(field, lang)` yardımcısı: `sitegen.data.t(value: dict | str, lang: str) -> str`.

`studio.json` alanları: `name` ("BerqWorks"), `email` ("berqworks@gmail.com"), `intro` (aşağıdaki iki paragraf, `en`/`tr` için birer liste), `nav` (`games`: "Games"/"Oyunlar", `contact`: "Contact"/"İletişim"), `labels` (`coming_soon_row`: "Coming soon · Android"/"Yakında · Android", `meet`: "Meet the game →"/"Oyunu tanı →", `coming_soon_play`: "Coming soon to Google Play"/"Yakında Google Play'de", `get_on_play`: "Get it on Google Play"/"Google Play'den indir", `how`: "How to play"/"Nasıl oynanır", `highlights`: "Highlights"/"Öne çıkanlar", `screens`: "Screens"/"Ekranlar", `details`: "Details"/"Bilgiler", `legal`: "Legal"/"Yasal", `last_updated`: "Last updated"/"Son güncelleme", `version`: "Version"/"Sürüm", `back`: "BerqWorks"/"BerqWorks"), `legal_date` ("13 November 2026"/"13 Kasım 2026"), `legal_titles` (`privacy-policy`: "Privacy Policy"/"Gizlilik Politikası", `terms-of-use`: "Terms of Use"/"Kullanım Koşulları", `kvkk`: "KVKK Notice"/"KVKK Aydınlatma Metni").

Stüdyo metni (spec §5, birebir):
- TR p1: "BerqWorks oyun ve uygulama yapan bağımsız bir stüdyo. Fikirden tasarıma, koddan mağazaya kadar her adım aynı masada atılıyor. Şu an üç Android oyunu yayına hazırlanıyor: yetişkinler için sakin bir mahjong, 3–8 yaş arası çocuklar için bir resim yapbozu ve solmuş sahneleri yeniden renklendiren bir sıralama bulmacası." p2: "Bu oyunların hiçbirinde süreye karşı yarışıp kaybetmezsin. Her bulmacanın bir çözümü var. Takıldığında oyun bunu açıkça söylüyor."
- EN p1: "BerqWorks is an independent studio that makes games and apps. Every step, from the first sketch to the store listing, happens at the same desk. Three Android games are on the way: a calm mahjong solitaire for grown-ups, a picture puzzle for children aged 3 to 8, and a sorting puzzle that brings faded scenes back to color." p2: "None of them has a clock you can lose to. Every puzzle has a solution, and when you're stuck, the game tells you so."

`games.json` her oyun için: `id`, `name` (EN/TR; Water Sort "Water Sort: Color Atlas"/"Water Sort: Renk Atlası", Tile Swap ikisinde "Tile Swap", Mahjong ikisinde "Mahjong Caravan"), `card` (brief §2 "Tek cümle"), `short` (brief §2 "Kısa açıklama"), `age_row` (yalnız Tile Swap: "Ages 3–8"/"3–8 yaş", diğerlerinde `null`), `orientation` (`landscape` / `portrait`), `theme` (`bg`, `bg2` ya da `null`, `fg`, `accent`), `heading_font` (`nunito` / `baloo` / `aileron`), `play_url` (`null`), `features` (aşağıdaki seçimler, başlık + açıklama EN/TR brief §4'ten birebir), `info` (sıralı `[label, value]` çiftleri, aşağıda), `legal_docs`, `media` (Task 3'te doldurulur: `icon`, `hero_video`, `hero_poster`, `screens`).

Temalar (spec §5): Mahjong `bg #1f5a3e, bg2 null, fg #f5efe0, accent #e0a63a`; Tile Swap `bg #1B1740, bg2 #332B70, fg #FAEEDA, accent #FFA94D`; Water Sort `bg #0F1424, bg2 null, fg #F4F6FB, accent #FFC857`.

Özellik seçimleri (brief §4 sıra numaraları): Mahjong 1, 2, 3, 4, 7. Tile Swap 1, 2, 3, 5, 6, 9. Water Sort 1, 2, 3, 4, 5, 7. Water Sort ve Tile Swap'ta tablo hücresindeki metin, Mahjong'da EN/TR madde metinleri kullanılır; dosya yolu ve "Kaynak" sütunu alınmaz.

`info` değerleri (label EN/TR → değer EN/TR):

| Oyun | Platform / Platform | Age / Yaş | Languages / Diller | Price / Fiyat | Ads / Reklam | 6. satır |
|---|---|---|---|---|---|---|
| Mahjong | Android · phone and tablet · landscape / Android · telefon ve tablet · yatay | Adults · rated PEGI 3 / Yetişkinler · içerik derecesi PEGI 3 | English, Turkish / Türkçe, İngilizce | Free; contains ads. One-time purchase: Remove ads / Ücretsiz; reklam içerir. Tek seferlik satın alma: Reklamları kaldır | Never during play; only after a won board / Oynarken asla; yalnızca kazanılan tahtadan sonra | Internet / İnternet: Not needed to play / Oynamak için gerekmez |
| Tile Swap | … · landscape / … · yatay | Ages 3–8 / 3–8 yaş | English, Turkish, Chinese, Japanese, German, French, Spanish, Portuguese, Russian, Italian / Türkçe, İngilizce, Çince, Japonca, Almanca, Fransızca, İspanyolca, Portekizce, Rusça, İtalyanca | Free to download; no ads; in-app purchases / İndirmesi ücretsiz; reklam yok, uygulama içi satın alma | None / Yok | For parents / Ebeveynler için: Purchases and outside links open only after a parent check / Satın almalar ve dış bağlantılar ancak ebeveyn doğrulamasından sonra açılır |
| Water Sort | … · portrait / … · dikey | 13+ / 13+ | English, Turkish / Türkçe, İngilizce | Free; contains ads and in-app purchases (No Ads Pack available) / Ücretsiz; reklam ve uygulama içi satın alma içerir (Reklamsız Paket var) | Never during a level; banner only on the Atlas screen / Seviye oynarken asla; banner yalnızca Atlas ekranında | Internet / İnternet: Required; No Ads Pack owners can play offline / Gerekir; Reklamsız Paket sahipleri çevrimdışı da oynar |

`legal_docs`: Mahjong `["privacy-policy","terms-of-use","kvkk"]`, Tile Swap `["privacy-policy","terms-of-use"]`, Water Sort `["privacy-policy","terms-of-use","kvkk"]`. Water Sort'ta ayrıca `legal_version: 1`.

- [ ] **Step 1: Başarısız testleri yaz** (`tests/test_data.py`): `load_site` üç oyunu `["mahjong-caravan","tile-swap-puzzle","water-sort"]` sırasıyla döndürür; `validate(load_site(root)) == []`; bir oyunun `card.tr`'si silinince `validate` o alanı adlandıran bir hata döndürür; hiçbir metin alanında `Zeynep` geçmez; hiçbir metin alanında `₺`, `$` ya da `USD` geçmez; her oyunun `media` alanı Task 3'e kadar boş olabilir (`validate` medya dosyalarının varlığını yalnızca `media` doluysa denetler).
- [ ] **Step 2: Çalıştır, FAIL gör.** `python3 -m unittest tests.test_data -v`
- [ ] **Step 3: JSON dosyalarını ve `data.py`'yi yaz.** Metinler brief'lerden birebir kopyalanır; brief §11'deki düzeltmeler (Mahjong yaşı vb.) yukarıdaki tabloda zaten uygulanmıştır.
- [ ] **Step 4: Çalıştır, PASS gör.**
- [ ] **Step 5: Commit** `git commit -m "Add studio and game data"`

---

### Task 3: Medya ve font hazırlığı

**Files:**
- Create: `tools/prepare_media.py`, `tools/prepare_fonts.py`, `site/fonts-src/`, `site/assets/media/**`, `site/assets/fonts/**`
- Modify: `site/data/games.json` (`media` alanları)
- Test: `tests/test_media.py`

**Interfaces:**
- Consumes: `games.json`.
- Produces: `site/assets/media/manifest.json` (`{"<çıktı yolu>": "<kaynak yolu>"}`, testler kaynağı buradan denetler), `site/assets/media/<id>/` altında dosyalar ve `games.json` → `media`: `{"icon": "icon.webp", "hero_video": {"en": "...mp4","tr": "...mp4"}, "hero_poster": {"en": "...webp","tr": "...webp"}, "screens": {"en": [{"file","alt"}...], "tr": [...]}, "motion": {...}}`. Yollar `site/assets/media/<id>/` köküne görelidir; `build()` `site/assets/` klasörünü `public/assets/` olarak kopyalar.
- Fontlar: `site/assets/fonts/{fraunces,instrument-sans,nunito,baloo2-semibold,aileron-regular,aileron-bold}.woff2` + her biri için OFL/CC0 lisans dosyası.

Seçimler (kaynak yolu `~/Desktop/site-gerekli-dosyalar/` köküne göre):

| Oyun | Video EN / TR | Poster | Ekranlar EN | Ekranlar TR | Hareket |
|---|---|---|---|---|---|
| mahjong-caravan | `mahjong/video/en_win_last-pairs-confetti-stars.mp4` / `tr_…` | `screenshots/{en,tr}/{lang}_mid.png` | `en_menu, en_levels, en_layouts, en_themes, en_mid_dark, en_win` | aynı adların `tr_` hâli | `art/tiles/bodies/ivory.svg` + `art/tiles/faces/{Chun,Hatsu,Pin5,Sou3,Man7,Ton}.svg` (CC0, olduğu gibi kopya) |
| tile-swap-puzzle | `tile-swap-puzzle/video/intro_jigsaw-assemble.mp4` (iki dil) | videonun son karesi | `screenshots/en/en_1…en_6` | `screenshots/tr/tr_1…tr_6` | `art/puzzle-images/animals/fox.png` → 600×600 webp |
| water-sort | `water-sort/video/en_page-complete_pine-forest_1080x1800.mp4` / `tr_page-complete_farm_1080x1800.mp4` | videonun ilk karesi | `en_level, en_very_hard, en_atlas_page-in-progress, en_page_complete, en_daily_puzzle, en_shop_backgrounds` | `tr_level, tr_color_aid, tr_atlas_page-in-progress, tr_page_complete, tr_daily_streak, tr_level_win` | `art/atlas-pages/page_002_pine-forest_color.png` → 540×960 webp, `…_region-mask.png` → 540×960 PNG (yeniden örneklemede en yakın komşu, gri değerler korunur) |

İkonlar: `{mahjong,tile-swap-puzzle,water-sort}/icon/icon_512.png` → 256 ve 512 px webp. `eski-kedi-ikonu/`, `_tablet-*`, `_desktop-preview-*`, `*_test-recording*` kullanılmaz.

Kodlama: video `ffmpeg -an -c:v libx264 -crf 28 -preset slow -pix_fmt yuv420p -movflags +faststart`, yatay için genişlik 960, dikey için yükseklik 900 (çift sayıya yuvarla). Görseller `cwebp -q 78`; yatay ekranlar 1200 px genişlik, dikey ekranlar 600 px genişlik. Her ekran için `alt` metni brief §9 "Ne gösteriyor" sütunundan, sayfanın dilinde, kısa bir cümle.

Fontlar: Fraunces ve Instrument Sans `https://github.com/google/fonts/raw/main/ofl/fraunces/Fraunces%5BSOFT,WONK,opsz,wght%5D.ttf` ve `…/ofl/instrumentsans/InstrumentSans%5Bwdth,wght%5D.ttf` adreslerinden, `OFL.txt` dosyalarıyla birlikte `site/fonts-src/`'a. `prepare_fonts.py`, `.venv-tools/bin/python` ile çalışır (`python3 -m venv .venv-tools && .venv-tools/bin/pip install fonttools brotli`; `.venv-tools/` `.gitignore`'a eklenir) ve `fontTools.subset` ile `U+0000-024F, U+2010-2027, U+2030-203A, U+20AC, U+2192, U+2122` aralığına indirip `woff2` yazar; değişken eksenleri korur.

- [ ] **Step 1: Başarısız testleri yaz** (`tests/test_media.py`): `games.json` içindeki her `media` dosyası `site/assets/media/<id>/` altında var; Tile Swap dışında hiçbir oyunun medyasında `puzzle-images` ya da `category-covers` kaynaklı dosya yok (hazırlık betiği kaynak yolunu `site/assets/media/manifest.json`'a yazar, test oradan okur); her woff2 için Türkçe harfler `çÇğĞıİöÖşŞüÜ` font cmap'inde var (test fonttools yoksa `skipTest`); `site/assets/` toplamı < 13 MB.
- [ ] **Step 2: Çalıştır, FAIL gör.** `python3 -m unittest tests.test_media -v`
- [ ] **Step 3: `prepare_media.py` (`--source` varsayılanı `~/Desktop/site-gerekli-dosyalar`) ve `prepare_fonts.py`'yi yaz, çalıştır.** Betik, kaynak dosyası eksikse adını yazıp `exit 1` verir.
- [ ] **Step 4: Çalıştır, PASS gör.** Ayrıca `du -sh site/assets` çıktısını kaydet.
- [ ] **Step 5: Commit** `git add tools/prepare_*.py site/fonts-src site/assets site/data/games.json tests/test_media.py .gitignore && git commit -m "Prepare web media and fonts"`

---

### Task 4: Ortak sayfa kabuğu, CSS ve dil seçimi

**Files:**
- Create: `tools/sitegen/layout.py`, `site/css/site.css`, `site/js/lang.js`
- Test: `tests/test_layout.py`, `tests/js/lang.test.mjs`

**Interfaces:**
- Consumes: `urls`, `data.t`.
- Produces:
  - `sitegen.layout.page(*, site: dict, lang: str, title: str, description: str, path: str, alt_path: str | None, body: str, theme: dict | None = None, heading_font: str | None = None, og_image: str = "/assets/brand/og.png") -> str`. `path` ve `alt_path` site köküne göre (`/games/x/`); `alt_path` öbür dildeki karşılık. `theme` verilirse `<body>`'ye `style="--bg:…;--bg2:…;--fg:…;--accent:…"` ve `data-game="<id>"` yazılır.
  - Üst menü: solda "BerqWorks" (ana sayfaya), sağda Oyunlar (`#games` çapası ana sayfada), İletişim (`#contact`), dil düğmesi (`alt_path`'e, `data-lang-switch="<öbür dil>"`). Alt bilgi `id="contact"`: e-posta bağlantısı ve "© 2026 BerqWorks".
  - `lang.js` dışa aktarımları (ES modülü, ayrıca `<script type="module">` ile yüklenir):
    - `pickLang(hash: string, stored: string|null, navLang: string) -> "tr"|"en"`: hash `#tr` ya da `#tr-…` → `tr`; `#en` / `#en-…` → `en`; yoksa `stored` (`"tr"`/`"en"`); yoksa `navLang` `tr` ile başlıyorsa `tr`; yoksa `en`.
    - `shouldRedirect(pathname: string, stored: string|null, navLang: string) -> string|null`: yalnızca `stored === null` ve `navLang` `tr` ile başlıyor ve `pathname` `/tr/` ile başlamıyor ve yasal sayfa değilse (`.html` ile bitmiyorsa) `"/tr" + pathname` döner; yoksa `null`.
    - DOM bağlama: dil düğmesine tıklanınca `localStorage["bw-lang"]` yazılır (try/catch); sayfa yüklenince `shouldRedirect` varsa `location.replace`. Yasal sayfada `document.documentElement.dataset.lang = pickLang(...)` ve dil düğmesi `#tr`/`#en` hash'ini değiştirir.
- `heading_font` → CSS ailesi: `nunito` → `"Nunito"`, `baloo` → `"Baloo 2"`, `aileron` → `"Aileron"`; `page()` bunu `--heading-font` değişkeni olarak `<body>`'ye yazar.
- `site.css`: `:root` renk ve ölçü değişkenleri; `body{font:18px/1.6 "Instrument Sans",…}` ; başlıklar Fraunces; `[data-game] h1,[data-game] h2` oyunun fontu (`--heading-font`); `*{font-variant-ligatures:none}`; `@font-face` yalnızca `/assets/fonts/` yollarıyla; `@media (prefers-reduced-motion: reduce)` tüm `animation`/`transition`'ları kapatır.

- [ ] **Step 1: Başarısız testleri yaz.**
  - `tests/js/lang.test.mjs`: `pickLang("#tr-7", "en", "en-US") === "tr"`; `pickLang("", "en", "tr-TR") === "en"`; `pickLang("", null, "tr-TR") === "tr"`; `pickLang("#en", "tr", "tr") === "en"`; `shouldRedirect("/games/water-sort/", null, "tr-TR") === "/tr/games/water-sort/"`; `shouldRedirect("/", "en", "tr-TR") === null`; `shouldRedirect("/tr/", null, "tr") === null`; `shouldRedirect("/games/water-sort/privacy-policy.html", null, "tr") === null`.
  - `tests/test_layout.py`: `page(lang="tr", path="/tr/", alt_path="/", …)` çıktısında `<html lang="tr">`, `<link rel="canonical" href="https://berqworks.com/tr/">`, `hreflang="en" href="https://berqworks.com/"`, `hreflang="tr"`, `hreflang="x-default" href="https://berqworks.com/"`, `href="mailto:berqworks@gmail.com"` var; `googleapis` ve `gstatic` yok. `site.css` metninde `font-variant-ligatures:none` (boşluk yok sayılarak) ve `prefers-reduced-motion` var; `fonts.googleapis` yok.
- [ ] **Step 2: Çalıştır, FAIL gör.** `node --test tests/js/` ve `python3 -m unittest tests.test_layout -v`
- [ ] **Step 3: `layout.py`, `site.css`, `lang.js`'i yaz.** `build()` `site/css`, `site/js`, `site/assets` klasörlerini `public/` altına `css/`, `js/`, `assets/` olarak kopyalar.
- [ ] **Step 4: Çalıştır, PASS gör.**
- [ ] **Step 5: Commit** `git commit -m "Add page shell, styles and language selection"`

---

### Task 5: Ana sayfa

**Files:**
- Create: `tools/sitegen/home.py`
- Modify: `tools/sitegen/build.py` (`public/index.html`, `public/tr/index.html`), `site/css/site.css`
- Test: `tests/test_home.py`

**Interfaces:**
- Consumes: `layout.page`, `data.t`, `urls.game_path`.
- Produces: `sitegen.home.render_home(site: dict, lang: str) -> str`.

Düzen (spec §5): stüdyo bölümü (kâğıt zemin `#f3efe6`, metin `#191714`; "BerqWorks" büyük Fraunces başlık + iki paragraf), ardından `<section id="games">` içinde her oyun için tam genişlikte bir bant: `<a class="game-row game-row--left|right" href="…" style="--bg…">`. Sıra mahjong (left), tile-swap (right), water-sort (left); `left` ikon solda. Bantta ikon (256 webp, `width/height` öznitelikli), `h2` oyun adı, `card` cümlesi, `coming_soon_row` (Tile Swap'ta ayrıca ` · ` + `age_row`), `meet` etiketi. Bant oyunun temasıyla boyanır (Tile Swap'ta `bg → bg2` degrade). 720 px altında ikon üstte, metin altta, hizalama sola.

- [ ] **Step 1: Başarısız testleri yaz** (`tests/test_home.py`): EN çıktısında stüdyo EN p1 ve p2 birebir; TR çıktısında TR p1; oyun bağlantıları sırasıyla `/games/mahjong-caravan/`, `/games/tile-swap-puzzle/`, `/games/water-sort/` (TR'de `/tr/games/…`); sınıflar sırasıyla `game-row--left`, `game-row--right`, `game-row--left`; "Coming soon · Android" üç kez; "Ages 3–8" bir kez; çıktıda `puzzle-images`, `category-covers`, `fox` geçmez; `play.google.com` geçmez.
- [ ] **Step 2: Çalıştır, FAIL gör.**
- [ ] **Step 3: `home.py`'yi ve bant stillerini yaz; `build()`'e iki ana sayfayı ekle (geçici boş `index.html` kaldırılır).**
- [ ] **Step 4: Çalıştır, PASS gör.** `python3 -m unittest discover -s tests -v`
- [ ] **Step 5: Görsel kontrol:** `python3 tools/build.py && python3 -m http.server -d public 8765`; masaüstü (1280 px) ve telefon (360 px) genişliğinde `/` ve `/tr/` aç. Beklenen: üç bant, ikonlar sol-sağ-sol, yatay kaydırma yok, Türkçe harfler doğru.
- [ ] **Step 6: Commit** `git commit -m "Add home page"`

---

### Task 6: Oyun sayfaları

**Files:**
- Create: `tools/sitegen/game.py`
- Modify: `tools/sitegen/build.py` (6 sayfa), `site/css/site.css`
- Test: `tests/test_game.py`

**Interfaces:**
- Consumes: `layout.page` (`theme`, `heading_font` ile), `data.t`, `urls`.
- Produces: `sitegen.game.render_game(site: dict, game: dict, lang: str) -> str`. Bölümler sırasıyla şu `id`'lerle: `hero`, `how`, `highlights` (`data-motion="<id>"`), `screens`, `details`, `legal`.

Ayrıntılar:
- `hero`: ikon (512 webp), `h1` ad, `card`, Play alanı `<div class="play-slot">`: `play_url` `null` ise `coming_soon_play` metni; doluysa `<a class="play" href="{play_url}" rel="noopener">{get_on_play}</a>`. Yanında `<video muted loop playsinline preload="none" data-autoplay poster="…">` (sayfanın dilindeki video; `autoplay` özniteliği yok, oynatmayı Task 8'deki `motion.js` hareket azaltma açık değilse başlatır); `orientation == "portrait"` ise kapsayıcıya `hero--portrait` sınıfı.
- `how`: `short` metni.
- `highlights`: her özellik için `h3` + paragraf; `motion.js` için boş bir `<div class="motion" aria-hidden="true">` ve gereken medya yolları `data-` özniteliklerinde (Task 8).
- `screens`: sayfanın dilindeki ekranlar, `loading="lazy"`, `width/height`, `alt`.
- `details`: `<dl>` ile `info` satırları.
- `legal`: `legal_docs` sırasıyla `/games/<id>/<doc>.html#<lang>` bağlantıları, başlıklar `legal_titles`'tan; e-posta.
- `<title>`: `"{name} · BerqWorks"`; `description`: `card`.

- [ ] **Step 1: Başarısız testleri yaz** (`tests/test_game.py`): her oyun ve dil için bölüm `id`'leri doğru sırada; Mahjong EN'de `kvkk.html#en` bağlantısı var, Tile Swap'ta `kvkk` yok; Water Sort'ta `hero--portrait` var, Mahjong'da yok; Water Sort TR'de `tr_page-complete_farm` kaynaklı video, EN'de `pine-forest`; `play_url = None` iken "Coming soon to Google Play" var ve `play.google.com` yok; testte `play_url` `"https://play.google.com/store/apps/details?id=com.berqworks.watersort"` yapılınca `class="play"` bağlantısı çıkar ve "Coming soon to Google Play" kaybolur; `<body data-game="water-sort"` ve `--bg:#0F1424` var; Mahjong ve Water Sort sayfalarında `puzzle-images` geçmez.
- [ ] **Step 2: Çalıştır, FAIL gör.**
- [ ] **Step 3: `game.py` ve sayfa stillerini yaz; `build()`'e EN/TR × 3 sayfa.** Taslak `.superpowers/brainstorm/*/content/oyun-sayfasi.html` yalnızca bölüm sırası için referanstır; stil ondan kopyalanmaz.
- [ ] **Step 4: Çalıştır, PASS gör.**
- [ ] **Step 5: Görsel kontrol** (Task 5'teki sunucu): üç oyun sayfası, iki dil, 1280 ve 360 px. Beklenen: renk bandı sayfaya yayılmış, başlıklar oyunun fontunda, Water Sort videosu dikey, yatay kaydırma yok.
- [ ] **Step 6: Commit** `git commit -m "Add game pages"`

---

### Task 7: Yasal sayfalar ve eski adres kopyaları

**Files:**
- Create: `tools/sitegen/legal.py`
- Modify: `tools/sitegen/build.py`, `site/css/site.css`
- Test: `tests/test_legal.py`

**Interfaces:**
- Consumes: `layout.page` (`theme` ile, `alt_path=None`), `site/legal/<id>/<doc>.<lang>.html`.
- Produces: `sitegen.legal.render_legal(site: dict, game: dict, doc: str, *, legacy: bool = False) -> str`.

Ayrıntılar:
- Sayfa `lang="en"` ile başlar; `lang.js` `data-lang`'i ayarlar ve `<html lang>`'ı günceller.
- Üstte oyunun renginde ince şerit: oyun adı + belge başlığı. Altta açık zemin, metin rengi `#1d1a16`, en fazla 72ch genişlik.
- Gövde: `<section id="tr" lang="tr" class="legal-tr">` (TR başlık, "Son güncelleme: 13 Kasım 2026", Water Sort'ta " · Sürüm 1", ardından TR parça) ve `<section id="en" lang="en" class="legal-en">` aynı yapıyla.
- Dil düğmesi: `<a href="#tr">TR</a> <a href="#en">EN</a>`.
- CSS: `html[data-lang="tr"] .legal-en, html[data-lang="en"] .legal-tr {display:none}`; `data-lang` yokken (JS kapalı) iki bölüm de görünür.
- Parçalardaki sınıflar (`summary`, `toc`, `note`, `table-wrap`, `stack`, `email`) için okunur stiller.
- `canonical`: her zaman `https://berqworks.com/games/<id>/<doc>.html`.
- `legacy=True`: çıktı `/<id>/<doc>.html` yoluna yazılır; parçalardaki göreli `href="<x>.html…"` bağlantıları `/games/<id>/<x>.html…` mutlak yoluna çevrilir. `legacy=False`'ta göreli bağlantılar olduğu gibi kalır.
- `build()`: her oyun ve `legal_docs` için asıl sayfa; `mahjong-caravan` ve `tile-swap-puzzle` için `privacy-policy` ve `terms-of-use` eski kopyaları.

- [ ] **Step 1: Başarısız testleri yaz** (`tests/test_legal.py`): `render_legal(water-sort, "kvkk")` çıktısında `id="tr"`, `id="en"`, `id="tr-1"`, `id="en-1"`, "Son güncelleme: 13 Kasım 2026", "Last updated: 13 November 2026", "Sürüm 1", "Version 1"; Mahjong gizlilikte "Sürüm" geçmez; mahjong eski kopyasında `href="kvkk.html` geçmez ve `href="/games/mahjong-caravan/kvkk.html` geçer, `canonical` `https://berqworks.com/games/mahjong-caravan/privacy-policy.html`; asıl sayfada göreli `href="kvkk.html#tr"` korunur; `site.css` içinde `.legal-en{display:none}` kuralı yalnızca `html[data-lang="tr"]` seçicisiyle (regex) var; `build()` sonrası `missing_required(out) == []`.
- [ ] **Step 2: Çalıştır, FAIL gör.**
- [ ] **Step 3: `legal.py`'yi ve stilleri yaz; `build()`'e ekle.**
- [ ] **Step 4: Çalıştır, PASS gör.** `python3 -m unittest discover -s tests -v`
- [ ] **Step 5: Elle kontrol:** sunucuda `/games/water-sort/privacy-policy.html#tr`, `#en`, `#tr-7`; `/mahjong-caravan/terms-of-use.html#tr` içinden KVKK bağlantısına tıkla. Beklenen: doğru dil, doğru bölüme kayma, 404 yok.
- [ ] **Step 6: Commit** `git commit -m "Add legal pages and legacy copies"`

---

### Task 8: İmza hareketleri

**Files:**
- Create: `site/js/motion.js`
- Modify: `tools/sitegen/game.py` (`data-` öznitelikleri), `site/css/site.css`
- Test: `tests/test_game.py` (öznitelik testleri), görsel kontrol

**Interfaces:**
- Consumes: `.motion` öğesi ve `data-motion`, `data-src-*` öznitelikleri.
- Produces: `motion.js` sayfada `IntersectionObserver` ile bölüm görünür olunca bir kez oynatır; `matchMedia("(prefers-reduced-motion: reduce)").matches` ise son durumu hareketsiz çizer. Aynı dosya `video[data-autoplay]` öğelerini, hareket azaltma kapalıysa ve video ekrana girince `play()` ile başlatır; açıksa poster kalır.

Hareketler:
- `mahjong-caravan`: 6 taş (fildişi gövde + yüz SVG'si) üç katman hâlinde, katman başına ~200 ms arayla yukarıdan iner ve hafif gölgeyle oturur (toplam ~600 ms, oyundaki gibi).
- `tile-swap-puzzle`: `fox.webp` 3×3 parçaya bölünmüş, karışık başlar; 4 yer değiştirmede (her biri ~350 ms) yerine oturur; oturan parçada küçük ✓. Parçalar CSS `background-position` ile çizilir.
- `water-sort`: `<canvas>`; renkli sahne önce gri tonda çizilir. Maskedeki farklı gri değerler artan sırayla bölge kabul edilir (arka plan dahil en çok 20 bölge + 0 değeri hariç); her ~120 ms'de bir bölge, maskesi o değere eşit pikseller için renkli sahneden boyanır. Mask ve sahne aynı boyutta (540×960).

- [ ] **Step 1: Başarısız testleri ekle** (`tests/test_game.py`): her oyunun `highlights` bölümünde `data-motion="<id>"`; water-sort'ta `data-src-color` ve `data-src-mask` dosyaları `public/assets/media/water-sort/` altında var; tile-swap'ta `data-src` `fox` içeriyor; sayfada `<script type="module" src="/js/motion.js">` var; hiçbir sayfada `autoplay` özniteliği yok, hero videosunda `data-autoplay` var.
- [ ] **Step 2: Çalıştır, FAIL gör.**
- [ ] **Step 3: `motion.js`, öznitelikler ve stilleri yaz.**
- [ ] **Step 4: Çalıştır, PASS gör.**
- [ ] **Step 5: Görsel kontrol:** üç oyun sayfasında Öne çıkanlar'a kaydır, hareketin bir kez oynadığını gör; tarayıcıda "hareketi azalt" açıkken (DevTools → Rendering → prefers-reduced-motion) hareket yok, son durum görünür, video oynamıyor.
- [ ] **Step 6: Commit** `git commit -m "Add signature motions"`

---

### Task 9: Son parçalar, tam üretim ve denetim

**Files:**
- Create: `site/assets/brand/{favicon.svg,og.png}`, `tools/sitegen/extras.py` (404, sitemap, robots)
- Modify: `tools/sitegen/build.py`
- Test: `tests/test_build.py`

**Interfaces:**
- Produces: `public/404.html` (iki dilli kısa metin, ana sayfa bağlantıları), `public/sitemap.xml` (6 sayfa + 2 ana sayfa, `https://berqworks.com` mutlak, `xhtml:link` hreflang çiftleri; yasal sayfalar yok), `public/robots.txt` (`Sitemap: https://berqworks.com/sitemap.xml`), favicon.

Favicon: kodla çizilmiş basit SVG işaret (yollarla çizilmiş geometrik bir "B"; font gerektirmez). Paylaşım görseli `og.png` 1200×630: `tools/og/og.html` (kâğıt zemin `#f3efe6`, Fraunces ile "BerqWorks", altında üç oyunun ikonu) yerel Chrome ile çekilir: `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --hide-scrollbars --window-size=1200,630 --screenshot=site/assets/brand/og.png tools/og/og.html`. Bu bir kerelik adımdır; `og.png` repoya girer. Oyun sayfalarında `og_image` oyunun 512 px ikonu (webp yerine `icon/icon_512.png`'den üretilmiş PNG, çünkü bazı paylaşım önizlemeleri webp okumaz; `public/` içinde izin verilen PNG'ler: `og.png`, üç `og-<id>.png`, water-sort maskesi).

- [ ] **Step 1: Başarısız testleri ekle:** `sitemap.xml` 8 `<loc>` içerir ve `.html` içermez; `robots.txt` sitemap satırını içerir; `404.html` var; `forbidden_hits(out) == []`; `total_size(out) < 15 * 1024 * 1024`; `public/` içindeki `.png` dosyaları tam olarak `og.png`, `og-<id>.png` (3) ve water-sort maskesi.
- [ ] **Step 2: Çalıştır, FAIL gör.**
- [ ] **Step 3: Uygula.**
- [ ] **Step 4: Tüm testler:** `python3 -m unittest discover -s tests -v && node --test tests/js/` → hepsi PASS. `python3 tools/build.py` → "public/: X MB" (X < 15).
- [ ] **Step 5: Görsel denetim (spec §2 kaçınılacaklar listesi):** 1280 px ve 360 px'te her sayfa; yatay kaydırma yok; hiçbir yerde degrade hero, eş kart ızgarası, emoji yok; Türkçe karakterler ve "fi" harfleri doğru; Tile Swap yapboz resmi yalnızca Tile Swap sayfasında. Ekran görüntülerini kullanıcıya göster.
- [ ] **Step 6: Commit** `git add -A public tools site tests && git commit -m "Build full site"`. Push yok: repoyu kullanıcı açacak ve push'u onaylayacak.
