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

# ---- 守破離(有料・単発): 型の三段階を幾何学で(守=完全 / 破=欠け / 離=痕跡) ----
def _square(d, cx, cy, s, **kw):
    d.rectangle([cx-s, cy-s, cx+s, cy+s], **kw)

def shuhari():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    cy, s = 300, 66
    xs = [795, 965, 1135]
    # 守: 完全な四角(型そのまま)
    _square(d, xs[0], cy, s, outline=INK, width=2)
    # 破: 上辺の中央が開き、外れた一片がずれて置かれる
    d.line([(xs[1]-s, cy-s), (xs[1]-22, cy-s)], fill=INK, width=2)
    d.line([(xs[1]+22, cy-s), (xs[1]+s, cy-s)], fill=INK, width=2)
    d.line([(xs[1]+s, cy-s), (xs[1]+s, cy+s)], fill=INK, width=2)
    d.line([(xs[1]+s, cy+s), (xs[1]-s, cy+s)], fill=INK, width=2)
    d.line([(xs[1]-s, cy+s), (xs[1]-s, cy-s)], fill=INK, width=2)
    d.line([(xs[1]-20, cy-s-16), (xs[1]+20, cy-s-16)], fill=ACCENT, width=4)  # 外れた一片
    # 離: 四隅の痕跡だけ残り、中心に芯(本を忘るな)
    c = 20
    for dx, dy in [(-s, -s), (s, -s), (s, s), (-s, s)]:
        x0, y0 = xs[2]+dx, cy+dy
        d.line([(x0 - (c if dx > 0 else -c), y0), (x0, y0)], fill=INK, width=2)
        d.line([(x0, y0 - (c if dy > 0 else -c)), (x0, y0)], fill=INK, width=2)
    d.ellipse([xs[2]-9, cy-9, xs[2]+9, cy+9], fill=ACCENT)
    # タイトル
    draw_spaced(d, "守破離", 118, 214, font(140), INK, 22)
    d.line([(126, 404), (300, 404)], fill=ACCENT, width=3)
    d.text((126, 436), "型を守り、破り、そして離れる", font=font(42), fill=INK)
    return _save(img, "shuhari_cover.png")

# ---- ネガティブ・ケイパビリティ(有料・単発): 閉じない円 + 宙吊りの点 ----
def negcap():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    cx, cy, r = 1018, 300, 170
    # 閉じない円(下部に開き=結論を出さない)
    d.arc([cx-r, cy-r, cx+r, cy+r], start=110, end=430, fill=INK, width=2)
    # 宙吊りの点(未解決を、閉じずに抱える)
    d.ellipse([cx-11, cy-11, cx+11, cy+11], fill=ACCENT)
    # 見出し(長い語なので和文フレーズを主役、概念名を副題)
    draw_spaced(d, "わからなさに耐える", 118, 244, font(72), INK, 5)
    d.line([(126, 366), (300, 366)], fill=ACCENT, width=3)
    d.text((126, 398), "ネガティブ・ケイパビリティ", font=font(38), fill=INK)
    return _save(img, "negcap_cover.png")

# ---- 大器晩成(有料・単発): 外へ開き続ける渦巻き(完成点を持たない成長) ----
def taikibansei():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    cx, cy = 995, 335
    # 中心の小さな種(始点)
    d.ellipse([cx-6, cy-6, cx+6, cy+6], fill=ACCENT)
    # 外へ開き続ける渦巻き(閉じずに終わる=完成点を持たない)
    import math as _m
    pts = []
    turns = 2.6
    steps = 260
    for i in range(steps + 1):
        t = i / steps
        theta = t * turns * 2 * _m.pi
        r = 10 + t * 190
        pts.append((cx + r * _m.sin(theta), cy - r * _m.cos(theta)))
    d.line(pts, fill=INK, width=2, joint="curve")
    # 渦の先端(まだ閉じていない=成長の途中)をアクセントで示す
    ex, ey = pts[-1]
    d.ellipse([ex-7, ey-7, ex+7, ey+7], fill=ACCENT)
    # タイトル
    draw_spaced(d, "大器晩成", 118, 214, font(120), INK, 20)
    d.line([(126, 372), (300, 372)], fill=ACCENT, width=3)
    d.text((126, 404), "大器は、完成しない", font=font(42), fill=INK)
    return _save(img, "taikibansei_cover.png")

# ---- 悠々自適(有料・単発): 自分のペースで進む、緩やかに蛇行する一本の道 ----
def yuyujiteki():
    import math as _m
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    x0, x1 = 800, 1190
    cy = 335
    pts = []
    steps = 200
    for i in range(steps + 1):
        t = i / steps
        x = x0 + t * (x1 - x0)
        y = cy + 95 * _m.sin(t * 2.3 * _m.pi) * (0.35 + 0.65 * t)
        pts.append((x, y))
    d.line(pts, fill=INK, width=2, joint="curve")
    # 道の途中で、急がず休む点(自分の適でとどまる場所。終点でも起点でもない)
    rx, ry = pts[int(steps * 0.62)]
    d.ellipse([rx-8, ry-8, rx+8, ry+8], fill=ACCENT)
    # タイトル
    draw_spaced(d, "悠々自適", 118, 214, font(120), INK, 20)
    d.line([(126, 372), (300, 372)], fill=ACCENT, width=3)
    d.text((126, 404), "自分の適を、自分で決める", font=font(38), fill=INK)
    return _save(img, "yuyujiteki_cover.png")

# ---- 知足(有料・単発): 縁ちょうどまで満ちた器(こぼれず、涸れず) ----
def chisoku():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    cx, cy, r = 980, 330, 160
    rim_y = cy - 18
    # 器(下半分の弧。上端が縁)
    d.arc([cx-r, cy-r, cx+r, cy+r], start=0, end=180, fill=INK, width=2)
    d.line([(cx-r, cy), (cx-r, rim_y)], fill=INK, width=2)
    d.line([(cx+r, cy), (cx+r, rim_y)], fill=INK, width=2)
    # 水面(縁ちょうど。こぼれず、涸れず)
    d.line([(cx-r, rim_y), (cx+r, rim_y)], fill=ACCENT, width=3)
    d.ellipse([cx-6, rim_y-6, cx+6, rim_y+6], fill=ACCENT)
    # タイトル
    draw_spaced(d, "知足", 118, 214, font(150), INK, 26)
    d.line([(126, 372), (300, 372)], fill=ACCENT, width=3)
    d.text((126, 404), "吾、唯だ足るを知る", font=font(40), fill=INK)
    return _save(img, "chisoku_cover.png")

# ---- 塞翁が馬(有料・単発): 禍福が糾える、二本の縒れた線 ----
def saiougauma():
    import math as _m
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    x0, x1 = 800, 1190
    cy = 335
    amp = 78
    steps = 220
    pts_a, pts_b = [], []
    for i in range(steps + 1):
        t = i / steps
        x = x0 + t * (x1 - x0)
        phase = t * 3.4 * _m.pi
        pts_a.append((x, cy + amp * _m.sin(phase)))
        pts_b.append((x, cy + amp * _m.sin(phase + _m.pi)))
    d.line(pts_a, fill=INK, width=2, joint="curve")
    d.line(pts_b, fill=ACCENT, width=2, joint="curve")
    # 交差点(福と禍が入れ替わる瞬間)
    for i in range(1, 4):
        cxp = x0 + (x1 - x0) * (i / 4)
        cyp = cy
        d.ellipse([cxp-4, cyp-4, cxp+4, cyp+4], fill=INK)
    # タイトル
    draw_spaced(d, "塞翁が馬", 118, 214, font(110), INK, 18)
    d.line([(126, 372), (300, 372)], fill=ACCENT, width=3)
    d.text((126, 404), "禍福は、糾える縄の如し", font=font(38), fill=INK)
    return _save(img, "saiougauma_cover.png")

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
    elif len(argv) >= 2 and argv[1] == "shuhari":
        shuhari()
    elif len(argv) >= 2 and argv[1] == "negcap":
        negcap()
    elif len(argv) >= 2 and argv[1] == "taikibansei":
        taikibansei()
    elif len(argv) >= 2 and argv[1] == "yuyujiteki":
        yuyujiteki()
    elif len(argv) >= 2 and argv[1] == "chisoku":
        chisoku()
    elif len(argv) >= 2 and argv[1] == "saiougauma":
        saiougauma()
    elif len(argv) >= 3 and argv[1] == "sekki":
        sekki(argv[2])
    else:
        raise SystemExit(__doc__)

if __name__ == "__main__":
    main(sys.argv)
