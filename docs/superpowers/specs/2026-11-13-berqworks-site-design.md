# berqworks.com: tasarım belgesi

13 Kasım 2026. Bu belge, kod yazmadan önce yapılan tasarım konuşmasının sonucudur.

## 1. Amaç

berqworks.com sıfırdan yapılıyor. Site BerqWorks stüdyosunu tanıtır. Stüdyonun üç Android oyunu var, üçü de yakında yayınlanacak. Her oyunun kendi tanıtım sayfası olur; oyun yayınlanınca o sayfaya Google Play bağlantısı eklenir. Site ayrıca oyunların yasal sayfalarını ve oyunların okuduğu dosyaları taşır. Yasal metinler daha önce ayrı oyun repolarından da sunuluyordu (ör. `github.com/berqworks/mahjong-caravan`); o sayfalar artık olmayacak, bütün yasal metinler bu sitede durur. Site bitene kadar ara yayın yapılmaz (kullanıcının kararı, 13 Kasım 2026).

## 2. Hedefler, hedef olmayanlar, kaçınılacaklar

Hedefler:

- Ziyaretçi stüdyoyu ve üç oyunu ilk ekranlarda anlar; bir oyuna tıklayınca o oyuna özel, ayrıntılı bir sayfa açılır.
- Site İngilizce (varsayılan) ve Türkçe.
- Bölüm 7'deki adreslerin hepsi çalışır.
- Bir oyun yayınlanınca sayfasında yalnızca "Yakında" alanı Play düğmesine döner; düzen değişmez.

Hedef olmayanlar:

- Tarayıcıda oynanan oyun, blog, haber, ayrı "Hakkında" sayfası.
- Oyun dışı programlar (şu an yok; ileride eklenebilir ama şimdi yer açılmaz).
- Fiyat (hiçbir yerde rakam yok), Play bağlantısı, çıkış tarihi.
- Analitik, çerez, üçüncü taraf istek (fontlar dahil her şey sitenin kendisinden yüklenir).

Kaçınılacaklar (site teknik olarak çalışsa bile bunlar başarısızlık sayılır):

- Sitenin yapay zekâ işi ya da hazır şablon gibi görünmesi: ortalanmış degrade "hero", eş kartlardan ızgara, hazır ikon setleri, emoji süsleme, mor-mavi degradeler, her bölüme aynı kalıp.
- Geliştiricinin kişisel adının sitenin herhangi bir yerinde geçmesi (metin, meta etiket, alt metin, dosya adı).
- Eski siteyi referans almak. Tek kaynak `~/Desktop/site-gerekli-dosyalar/{mahjong,tile-swap-puzzle,water-sort}`; her klasördeki `brief.md` metinlerin ve sayıların doğruluk kaynağıdır. `_eski-repo-yedek/` yalnızca kurtarma içindir, kullanılmaz.
- Tile Swap'ın yapay zekâ ile üretilmiş yapboz resimlerini ve kategori kapaklarını (`art/puzzle-images/`, `art/category-covers/`) ayrı dosyalar olarak sitede süs ya da vitrin öğesi yapmak. Oyunun ekran görüntüleri ve videoları ise (içlerinde bu resimler görünse de) Tile Swap sayfasında diğer oyunlardaki gibi kullanılır (kullanıcının kararı). Öne çıkanlar bölümündeki yer değiştirme hareketi de bu resimlerden biriyle yapılabilir; ana sayfa ve stüdyo bölümünde bu resimler yer almaz.
- Yasal adreslerden birinin kırılması.

## 3. Kısıtlar

- Barındırma: site `berqworks/berqworks.github.io` reposuna yüklenir (kullanıcı yeniden oluşturacak). GitHub Pages bu repodan `berqworks.github.io`'yu, Netlify aynı repodan `berqworks.com`'u yayınlar; iki yer aynı hazır dosyaları sunar. GitHub Pages derleme çalıştırmaz ve sunucu tarafı yönlendirme yapamaz.
- Her Netlify üretim yayını kredi harcar: push'lar toplu yapılır. Commit ve push yalnızca kullanıcı onayıyla.
- Repoya ham PNG'ler (kaynak klasörde ~487 MB) girmez. Yayınlanan sitenin toplamı hedef olarak ~15 MB'ın altında kalır.
- Bütün yazı tiplerinde Türkçe karakterler sorunsuz çizilmeli ve metin rahat okunmalı (kullanıcının fontlardaki tek önceliği).

## 4. Yaklaşımlar

1. **Bağımlılıksız küçük Python üretim betiği + repoya giren hazır çıktı (seçilen).** Şablonlar ve tek bir veri dosyasından EN/TR sayfalar, oyun sayfaları, yasal sayfalar ve eski adres kopyaları üretilir; betik korunması gereken adresleri denetler. Netlify'da derleme çalışmaz, derleme süresi harcanmaz; GitHub Pages'ta da aynı dosyalar çalışır. Bedeli: betiğin bakımı bizde.
2. **Eleventy gibi hazır bir üretici.** Aynı iş, yaygın araçla; ama Node bağımlılığı ve paket güncellemeleri getirir. Üç oyunluk site için fazla.
3. **Her sayfa elle yazılmış HTML.** İki dil, üç oyun, 8 yasal belge ve eski kopyalar yüzünden aynı düzeltme birçok dosyada yapılır ve bir adres sessizce bozulabilir.

Kullanıcı 1'i seçti.

## 5. Kullanıcının verdiği kararlar

### Ana sayfa

- En üstte stüdyo tanıtımı, altında üç oyun **alt alta**. Logo (uygulama ikonu) sırayla **solda, sağda, solda**; metin karşı tarafta. Sıra: Mahjong Caravan (logo solda), Tile Swap (sağda), Water Sort (solda).
- Her oyun satırı **kendi renk dünyasında** bir bant (kullanıcı "her oyun kendi renginde" seçeneğini seçti):
  - Mahjong Caravan: çuha yeşili `#1f5a3e`, metin `#f5efe0`, vurgu altın `#e0a63a` / `#d8a54a`.
  - Tile Swap: gece gökyüzü degradesi `#1B1740 → #332B70`, metin `#FAEEDA`, vurgu turuncu `#FFA94D`.
  - Water Sort: koyu lacivert `#0F1424`, metin `#F4F6FB`, vurgu `#FFC857`.
- Satır içeriği: ad, brief'teki tek cümlelik kart metni, "Yakında · Android" (Tile Swap'ta ayrıca "3–8 yaş"), "Oyunu tanı →". Satırın tamamı tıklanabilir.
- Tanıtım metni (kullanıcı metni bana bıraktı; adı geçmeyen son hâli onaylandı):
  - TR: "BerqWorks oyun ve uygulama yapan bağımsız bir stüdyo. Fikirden tasarıma, koddan mağazaya kadar her adım aynı masada atılıyor. Şu an üç Android oyunu yayına hazırlanıyor: yetişkinler için sakin bir mahjong, 3–8 yaş arası çocuklar için bir resim yapbozu ve solmuş sahneleri yeniden renklendiren bir sıralama bulmacası. Bu oyunların hiçbirinde süreye karşı yarışıp kaybetmezsin. Her bulmacanın bir çözümü var. Takıldığında oyun bunu açıkça söylüyor."
  - EN: "BerqWorks is an independent studio that makes games and apps. Every step, from the first sketch to the store listing, happens at the same desk. Three Android games are on the way: a calm mahjong solitaire for grown-ups, a picture puzzle for children aged 3 to 8, and a sorting puzzle that brings faded scenes back to color. None of them has a clock you can lose to. Every puzzle has a solution, and when you're stuck, the game tells you so."
- Tanıtım bölümünün zemini nötr kâğıt tonu (taslakta `#f3efe6`, metin `#191714`).

### Oyun sayfası

Ana sayfadaki bant tıklanınca bütün sayfanın rengi olur. Üç sayfa aynı iskelet, farklı renk ve içerik. Bölümler sırayla (kullanıcı taslağı "güzel" diye onayladı):

1. **Giriş:** ikon, ad, tek cümle, "Yakında Google Play'de" alanı (yayında Play düğmesi olur). Yanında oyunun imza anı video olarak: sessiz, döngüde, otomatik oynar.
2. **Nasıl oynanır:** brief'teki kısa açıklama.
3. **Öne çıkanlar:** brief'in 4. bölümünden en önemli özellikler. Bu bölüme gelince oyuna özgü bir hareket oynar: Mahjong'da taşlar katman katman iner (CC0 taş SVG'leri, `art/tiles/`); Water Sort'ta gri sahne bölge maskesiyle bölge bölge renklenir (`art/atlas-pages/*_color.png` + `*_region-mask.png`); Tile Swap'ta parçalar yer değiştirip yerine oturur.
4. **Ekranlar:** ekran görüntüleri; sayfanın diline göre `en_` ya da `tr_` dosyaları.
5. **Bilgi:** platform ve ekran yönü, yaş, diller, fiyat ifadesi (rakamsız), reklamın ne zaman çıktığı, internet gereksinimi. Değerler brief'lerden; brief'lerin 11. bölümündeki düzeltmeler uygulanır (ör. Mahjong yaşı "Yetişkinler · içerik derecesi PEGI 3", Water Sort fiyat satırı brief §6'daki metin).
6. **Alt kısım:** o oyunun yasal belgeleri ve destek e-postası `berqworks@gmail.com`.

Water Sort dikey oyun: videosu ve ekran görüntüleri dikey yerleşir.

### Yazı tipleri

- Stüdyo: başlıklarda **Fraunces**, metinde **Instrument Sans** (ikisi de SIL OFL; Google Fonts deposundan indirilip siteye gömülür).
- Oyun sayfalarının başlıklarında oyunun kendi fontu: Mahjong **Nunito**, Tile Swap **Baloo 2 SemiBold**, Water Sort **Aileron**. Dosyalar kaynak klasörlerde.
- Uzun metin 18 px, satır aralığı 1,6.
- Bütün sitede `font-variant-ligatures: none` (Aileron'un "fi" birleşimi tek parça çizilmiş; kullanıcı farkı gördü ve kapatılmasını onayladı). Her sayfada doğru `lang` etiketi (`tr` / `en`), böylece büyük harfe çevirmede "i" → "İ" olur.
- Denetlendi: altı fontun hepsinde ç ğ ı İ ö ş ü â î û var. ₺ bazılarında yok; fiyat gösterilmediği için önemsiz.

## 6. Benim önerdiğim ve kullanıcının itiraz etmediği kararlar

- **Dil ve adresler:** İngilizce `/`, Türkçe `/tr/` altında. Oyun sayfaları `/games/<id>/` ve `/tr/games/<id>/`. Oyun id'leri: `mahjong-caravan`, `tile-swap-puzzle`, `water-sort`. Türkçe tarayıcıyla ilk kez gelen ziyaretçi `/tr/` karşılığına yönlendirilir; TR/EN düğmesindeki seçim `localStorage` anahtarı `bw-lang` ile hatırlanır (yasal sayfalar da bu anahtarı kullanıyor) ve seçim yapılmışsa otomatik yönlendirme olmaz. Sayfalarda `hreflang` bağlantıları.
- **Asıl alan adı (benim kararım):** `https://berqworks.com`. `canonical`, `hreflang`, `og:image` ve site haritası bu adı kullanır; eski adres kopyaları dahil her sayfanın `canonical` etiketi berqworks.com'daki asıl adresi gösterir. `berqworks.github.io` aynı dosyaları sunar ama ayrıca tanıtılmaz.
- **Menü:** Oyunlar · İletişim · TR/EN. İletişim sayfanın altındaki e-postaya gider. Ayrı Hakkında sayfası yok.
- **Yasal sayfalar:** üstte oyunun renginde ince başlık şeridi, metin açık ve sade zeminde. TR ve EN gövdeler aynı sayfada; `#tr` / `#en` dili seçer, bölüm kimlikleri `tr-N` / `en-N`. Kaynak dosyalar (`legal/<belge>.<dil>.html`) yalnızca gövdedir; başlık, "Son güncelleme" tarihi ve dil düğmesi şablondan gelir. Tarihler: hepsi "13 Kasım 2026" / "13 November 2026". Water Sort belgelerinde ayrıca "Sürüm 1" / "Version 1" gösterilir (oyundaki `POLICY_VERSION` ile aynı); Mahjong ve Tile Swap'ta sürüm yok. Yasal metinler kaynak klasördeki son hâlleriyle yayınlanır; Tile Swap Kullanım Koşulları §10'daki yeni simge cümlesi de dahil (kullanıcının kararı).
- **Hareket ve medya:** `prefers-reduced-motion` açıkken animasyon yok, videolar yerine durgun kare. Videolar küçültülür (H.264 MP4, poster görseliyle) ve ekrana yaklaşınca yüklenir. Görseller WebP'ye çevrilir, uygun boyutlarda. Eski çekimler (`_tablet-*`, `_desktop-preview-*`, `*_test-recording*`, `eski-kedi-ikonu/`) kullanılmaz.
- **Klasör düzeni (benim kararım):** kaynaklar (şablonlar, veri, CSS, JS, betik) repoda ayrı bir klasörde; üretilmiş site `public/` altında ve repoya girer. Netlify'ın yayın klasörü `public/`, derleme komutu yok (`netlify.toml`). GitHub Pages, derleme yapmayan küçük bir GitHub Actions iş akışıyla `public/` klasörünü olduğu gibi yayınlar (Pages ayarında kaynak "GitHub Actions" seçilir). `docs/` yalnızca belgeler içindir ve yayınlanmaz; böylece tasarım belgeleri sitede görünmez.

## 7. Bozulmaması gereken adresler

Betik her üretimde bunların hepsinin çıktıda olduğunu denetler; biri eksikse hata verir.

| Adres | Not |
|---|---|
| `/games/water-sort/privacy-policy.html`, `terms-of-use.html`, `kvkk.html` | oyunun içinde kayıtlı, sonuna `#tr`/`#en` eklenir |
| `/games/mahjong-caravan/privacy-policy.html`, `terms-of-use.html`, `kvkk.html` | asıl adresler |
| `/games/tile-swap-puzzle/privacy-policy.html`, `terms-of-use.html` | asıl adresler (KVKK yok) |
| `/mahjong-caravan/privacy-policy.html`, `terms-of-use.html` | eski adres, oyunun içinde kayıtlı; asıl sayfanın birebir kopyası |
| `/tile-swap-puzzle/privacy-policy.html`, `terms-of-use.html` | eski adres, oyunun içinde kayıtlı; birebir kopya |
| `/games/water-sort/config.json` | `water-sort/config.json` bayt bayt aynı kopyalanır; oyun açılışta okur |
| `/app-ads.txt` | kök dizinde; tek satır `google.com, pub-3762683248469893, DIRECT, f08c47fec0942fa0` (AdMob'un standart satırı, benim kararım; kullanıcı AdMob panelindeki satırla karşılaştırmalı) |

Adresler hem `berqworks.github.io` hem `berqworks.com` üzerinde aynı yolla çalışır. Eski adreslerdeki kopyalar yönlendirme değil, gerçek dosya olmalı (GitHub Pages sunucu tarafı yönlendirme yapamaz). İçlerindeki göreli bağlantılar ve `canonical` asıl adresi göstermeli.

## 8. Kurucuya bırakılanlar

- Şablon dili ve betiğin iç yapısı (Python standart kütüphanesi dışında bağımlılık yok).
- Ana sayfa ve oyun sayfalarının ayrıntılı görsel tasarımı: boşluklar, tipografi ölçüleri, hareketlerin zamanlaması. Onaylanan taslaklar `.superpowers/brainstorm/` altında (`oyun-listesi.html`, `oyun-sayfasi.html`); bunlar kaba taslaktır, son tasarım bölüm 2'deki kaçınılacaklara karşı denetlenir.
- Her oyunda hangi video ve ekran görüntülerinin, kaç tanesinin kullanılacağı (brief'lerdeki önerilere göre).
- Öne çıkanlar bölümünde kaç özellik gösterileceği (4–6).
- Favicon ve paylaşım görseli (Open Graph): stüdyo için kodla çizilmiş basit bir işaret; oyun sayfalarında oyunun ikonu ya da Play öne çıkan görseli.
- Telefon görünümü: zikzak düzen dar ekranda alt alta tek sütuna iner.
