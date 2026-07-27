#!/usr/bin/env python3
"""note カバー生成(1280x670・ブランド3色・IPA明朝)。

使い方:
  python3 scripts/covers.py wabisabi
  python3 scripts/covers.py sekki <slug>     # 例: risshu(data/sekki_schedule.tsv を参照)

ブランド3色: 背景 #F7F5F0 / 文字 #2B2B28 / アクセント #2C3E50。
フォントは IPA明朝(なければ IPAゴシックに自動フォールバック)。
"""
import math, os, sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 670
BG = (247, 245, 240)
INK = (43, 43, 40)
ACCENT = (44, 62, 80)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FONT_CANDIDATES = [
    "/usr/share/fonts/opentype/ipafont-mincho/ipam.ttf",   # IPA明朝(第一候補)
    "/usr/share/fonts/truetype/fonts-japanese-mincho.ttf",
    "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf",   # ゴシック(代替)
    "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf",
]

def _font_path():
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            return p
    raise SystemExit("日本語フォントが見つかりません(IPA明朝を推奨: apt-get install -y fonts-ipafont-mincho)")

FONT = _font_path()

def font(sz):
    return ImageFont.truetype(FONT, sz)

def draw_spaced(d, text, x, y, f, fill, spacing):
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill)
        bb = d.textbbox((0, 0), ch, font=f)
        x += (bb[2] - bb[0]) + spacing
    return x

def _save(img, name):
    out = os.path.join(ROOT, "covers", name)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out)
    assert Image.open(out).size == (W, H), "サイズが 1280x670 でない"
    print("saved", out, Image.open(out).size)
    return out

# ---- 侘び寂び(有料・単発): 同心円 + わずかな非対称 ----
def wabisabi():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    cx, cy = 965, 300
    d.arc([cx-195, cy-195, cx+195, cy+195], start=-58, end=232, fill=INK, width=2)
    d.ellipse([cx-128, cy-128, cx+128, cy+128], outline=INK, width=2)
    d.ellipse([cx-62, cy-62, cx+62, cy+62], outline=ACCENT, width=2)
    d.ellipse([cx+150-11, cy+150-11, cx+150+11, cy+150+11], fill=ACCENT)
    draw_spaced(d, "侘び寂び", 118, 214, font(140), INK, 22)
    d.line([(126, 404), (300, 404)], fill=ACCENT, width=3)
    d.text((126, 436), "欠けたところに、光がたまる", font=font(42), fill=INK)
    return _save(img, "wabisabi_cover.png")

# ---- 二十四節気シリーズ(無料・連載): シリーズ見出し + 24分割の年輪 ----
CYCLE = ["立春","雨水","啓蟄","春分","清明","穀雨","立夏","小満","芒種","夏至","小暑","大暑",
         "立秋","処暑","白露","秋分","寒露","霜降","立冬","小雪","大雪","冬至","小寒","大寒"]

def _load_schedule():
    rows = {}
    with open(os.path.join(ROOT, "data", "sekki_schedule.tsv"), encoding="utf-8") as fh:
        for line in fh:
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            c = line.rstrip("\n").split("\t")
            # slug, 節気, よみ, 概算日, カバー一言, 季節メモ
            rows[c[0]] = {"term": c[1], "yomi": c[2], "date": c[3], "phrase": c[4]}
    return rows

def sekki(slug):
    row = _load_schedule()[slug]
    term, yomi, phrase = row["term"], row["yomi"], row["phrase"]
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # シリーズ帯(侘び寂びには無い差別化)
    d.line([(70, 74), (1210, 74)], fill=ACCENT, width=2)
    draw_spaced(d, "二十四節気", 70, 92, font(34), ACCENT, 10)
    d.text((70, 150), "── 季節のことば", font=font(24), fill=INK)
    # 24分割の年輪(立春を上、時計回り。該当節気をアクセント)
    cx, cy = 980, 360
    R_out, R_in, R_hi = 182, 150, 128
    d.ellipse([cx-R_out, cy-R_out, cx+R_out, cy+R_out], outline=INK, width=1)
    idx = CYCLE.index(term)
    for i in range(24):
        th = math.radians(i * 15)
        sx, sy = cx + R_in*math.sin(th), cy - R_in*math.cos(th)
        ex, ey = cx + R_out*math.sin(th), cy - R_out*math.cos(th)
        if i == idx:
            hx, hy = cx + R_hi*math.sin(th), cy - R_hi*math.cos(th)
            d.line([(hx, hy), (ex, ey)], fill=ACCENT, width=5)
            d.ellipse([ex-9, ey-9, ex+9, ey+9], fill=ACCENT)
        else:
            d.line([(sx, sy), (ex, ey)], fill=INK, width=2)
    # 節気名(主役)
    draw_spaced(d, term, 74, 300, font(150), INK, 20)
    d.line([(80, 496), (250, 496)], fill=ACCENT, width=3)
    d.text((80, 522), f"{yomi} ── {phrase}", font=font(36), fill=INK)
    return _save(img, f"sekki_{slug}_cover.png")

def main(argv):
    if len(argv) >= 2 and argv[1] == "wabisabi":
        wabisabi()
    elif len(argv) >= 3 and argv[1] == "sekki":
        sekki(argv[2])
    else:
        raise SystemExit(__doc__)

if __name__ == "__main__":
    main(sys.argv)
