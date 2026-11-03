"""Görselleri site için hazırlar (Pillow gerekir: pip install pillow).
- assets/games/<oyun>/*.jpg → aynı adla .webp (sitede WebP kullanılır; .jpg dosyaları eski bağlantılar için kalır)
- icon.png → icon.webp
- assets/og/home.jpg ve assets/og/<oyun>.jpg: 1200×630 paylaşım görselleri
Kullanım (depo kökünden): python3 tools/make_images.py  — ardından python3 tools/build_site.py
"""
import glob
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_site import GAMES, ROOT, plain  # noqa: E402

# Ekran görüntüsünün altından kırpılacak piksel (test reklamı bandı gibi istenmeyen alanlar).
CROP_BOTTOM = {
    "water-sort/en_page_complete.jpg": 30,
    "water-sort/tr_page_complete.jpg": 30,
}

BONE, TILE, EDGE, LINE = "#f3ede1", "#fbf8f1", "#cdbf9f", "#ddd3c1"
INK, MUTED, BRASS = "#1b2a22", "#56625a", "#8a6418"
FONTS = os.path.join(ROOT, "assets", "fonts")


def font(name, size, axes):
    f = ImageFont.truetype(os.path.join(FONTS, name), size)
    f.set_variation_by_axes(axes)
    return f


def serif(size, weight=400):
    return font("fraunces-latin.woff2", size, [144, weight])


def sans(size, weight=400):
    return font("atkinson-next-latin.woff2", size, [weight])


def to_webp():
    for path in sorted(glob.glob(os.path.join(ROOT, "assets", "games", "*", "*.jpg"))):
        key = "/".join(path.replace("\\", "/").split("/")[-2:])
        im = Image.open(path).convert("RGB")
        cut = CROP_BOTTOM.get(key, 0)
        if cut:
            im = im.crop((0, 0, im.width, im.height - cut))
        im.save(path[:-4] + ".webp", "WEBP", quality=82, method=6)
    for path in glob.glob(os.path.join(ROOT, "assets", "games", "*", "icon.png")):
        Image.open(path).save(path[:-4] + ".webp", "WEBP", quality=90, method=6)


def wrap(draw, text, fnt, width):
    lines, line = [], ""
    for word in text.split():
        test = (line + " " + word).strip()
        if draw.textlength(test, font=fnt) <= width or not line:
            line = test
        else:
            lines.append(line)
            line = word
    return lines + [line]


def framed(canvas, img_path, x, y, height=None, width=None):
    """Ekran görüntüsünü kemik rengi bir taş çerçeveye (düz kalınlık kenarıyla) yerleştirir."""
    im = Image.open(img_path).convert("RGB")
    if width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    else:
        im = im.resize((round(im.width * height / im.height), height), Image.LANCZOS)
    d = ImageDraw.Draw(canvas)
    pad = 8
    box = (x, y, x + im.width + 2 * pad, y + im.height + 2 * pad)
    d.rounded_rectangle((box[0], box[1] + 7, box[2], box[3] + 7), 8, fill=EDGE)
    d.rounded_rectangle(box, 8, fill=TILE, outline=LINE, width=2)
    canvas.paste(im, (x + pad, y + pad))
    return box


def text_block(canvas, title, sub, title_size=68):
    d = ImageDraw.Draw(canvas)
    d.text((72, 64), "BerqWorks", font=serif(34, 600), fill=INK)
    f = serif(title_size)
    y = 170
    for line in wrap(d, title, f, 470):
        d.text((72, y), line, font=f, fill=INK)
        y += round(title_size * 1.08)
    y += 18
    fs = sans(30)
    for line in wrap(d, sub, fs, 450):
        d.text((72, y), line, font=fs, fill=MUTED)
        y += 40
    d.text((72, 548), "berqworks.github.io", font=sans(26, 700), fill=BRASS)


def og_game(g):
    c = Image.new("RGB", (1200, 630), BONE)
    d = ImageDraw.Draw(c)
    gdir = os.path.join(ROOT, "assets", "games", g["id"])
    if g["shots"] == "landscape":
        d.rectangle((640, 210, 1200, 630), fill=g["color"])
        framed(c, os.path.join(gdir, g["hero"]["en"][0] + ".webp"), 560, 150, width=580)
    else:
        d.rectangle((700, 120, 1200, 630), fill=g["color"])
        framed(c, os.path.join(gdir, g["hero"]["en"][0] + ".webp"), 620, 60, height=480)
        framed(c, os.path.join(gdir, g["hero"]["en"][1] + ".webp"), 880, 110, height=480)
    text_block(c, plain(g["name"]), plain(g["short"]), 60)
    c.save(os.path.join(ROOT, "assets", "og", g["id"] + ".jpg"), "JPEG", quality=86, optimize=True, progressive=True)


def og_home():
    c = Image.new("RGB", (1200, 630), BONE)
    d = ImageDraw.Draw(c)
    by_id = {g["id"]: g for g in GAMES}
    d.rectangle((760, 250, 1200, 630), fill=by_id["mahjong-caravan"]["color"])
    gd = os.path.join(ROOT, "assets", "games")
    framed(c, os.path.join(gd, "tile-swap-puzzle", "en_4-oyun.webp"), 570, 60, width=400)
    framed(c, os.path.join(gd, "mahjong-caravan", "en_mid.webp"), 610, 330, width=400)
    framed(c, os.path.join(gd, "water-sort", "en_level.webp"), 990, 120, height=420)
    text_block(c, "Games you can take your time with", "Calm mobile games. No time limits, no energy meters.", 64)
    c.save(os.path.join(ROOT, "assets", "og", "home.jpg"), "JPEG", quality=86, optimize=True, progressive=True)


def main():
    to_webp()
    os.makedirs(os.path.join(ROOT, "assets", "og"), exist_ok=True)
    og_home()
    for g in GAMES:
        og_game(g)
    print("görseller hazır")


if __name__ == "__main__":
    main()
