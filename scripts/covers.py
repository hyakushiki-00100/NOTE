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

# ---- 序破急(有料・単発): 拍の密度が変わる目盛り(序=無拍節 / 破=拍子 / 急=詰まる。配分1:3:1) ----
def johakyu():
    import math as _m
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    x0, x1 = 792, 1192
    base = 340
    span = x1 - x0
    jo_end = x0 + span * 0.2          # 序 = 1/5
    ha_end = x0 + span * 0.8          # 破 = 3/5
    # 序: 拍を刻まない(ゆるやかな波線のみ)
    wave = []
    steps = 60
    for i in range(steps + 1):
        t = i / steps
        x = x0 + t * (jo_end - x0)
        wave.append((x, base - 14 * _m.sin(t * 2 * _m.pi)))
    d.line(wave, fill=INK, width=2, joint="curve")
    # 破: 等間隔の拍(構造が入り、いちばん長い)
    for i in range(7):
        x = jo_end + (ha_end - jo_end) * (i / 6)
        d.line([(x, base - 30), (x, base + 30)], fill=INK, width=2)
    d.line([(jo_end, base), (ha_end, base)], fill=INK, width=1)
    # 急: 拍が詰まり、加速して切れる
    n = 9
    for i in range(n):
        t = i / (n - 1)
        x = ha_end + (x1 - ha_end) * (t ** 1.6)
        d.line([(x, base - 30), (x, base + 30)], fill=ACCENT, width=2)
    d.line([(ha_end, base), (x1, base)], fill=ACCENT, width=1)
    # 区間ラベル
    fs = font(26)
    d.text((x0 + (jo_end - x0) / 2 - 13, base + 56), "序", font=fs, fill=INK)
    d.text((jo_end + (ha_end - jo_end) / 2 - 13, base + 56), "破", font=fs, fill=INK)
    d.text((ha_end + (x1 - ha_end) / 2 - 13, base + 56), "急", font=fs, fill=ACCENT)
    # タイトル
    draw_spaced(d, "序破急", 118, 214, font(140), INK, 22)
    d.line([(126, 404), (300, 404)], fill=ACCENT, width=3)
    d.text((126, 436), "時間の、重心をどこに置くか", font=font(38), fill=INK)
    return _save(img, "johakyu_cover.png")

# ---- 初心忘るべからず(有料・単発): 消えない基準線と、三つの起点 ----
def shoshin():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    x0, x1 = 800, 1190
    base = 430          # 未熟だった地点 = ものさしの原点
    step = 58
    # 基準線(破線): 消さずに残す「未熟だった自分」
    x = x0
    while x < x1:
        d.line([(x, base), (min(x + 11, x1), base)], fill=INK, width=1)
        x += 20
    # 三段の階段(段階ごとに上がる)。各段の始点が「初心」
    seg = (x1 - x0) / 3.4
    starts = []
    px, py = x0, base
    for i in range(3):
        y = base - step * i
        starts.append((px, y))
        d.line([(px, y), (px + seg, y)], fill=INK, width=2)     # その段を進む
        nx = px + seg
        ny = y - step
        if i < 2:
            d.line([(nx, y), (nx, ny)], fill=INK, width=2)       # 次の段へ上がる
        else:
            # 老後の初心: まだ続いている(閉じない)
            d.line([(nx, y), (nx, ny + 14)], fill=INK, width=2)
        px, py = nx, ny
    # 三つの初心(起点)をアクセントで示す
    for (sx, sy) in starts:
        d.ellipse([sx - 7, sy - 7, sx + 7, sy + 7], fill=ACCENT)
    # 基準線から現在地までの落差(ものさし)
    lastx = starts[-1][0] + seg
    d.line([(lastx, base), (lastx, base - step * 2)], fill=ACCENT, width=1)
    # タイトル
    draw_spaced(d, "初心", 118, 214, font(150), INK, 26)
    d.line([(126, 404), (300, 404)], fill=ACCENT, width=3)
    d.text((126, 436), "未熟だった自分を、捨てない", font=font(38), fill=INK)
    return _save(img, "shoshin_cover.png")

# ---- 推敲(有料・単発): 「推す」(一方向)と「敲く」(往復する迷い)の対比、そして一点の決着 ----
def suikou():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    x0 = 800
    y_push, y_knock = 260, 420
    length = 300
    # 推す: 迷いのない一方向の直線
    d.line([(x0, y_push), (x0 + length, y_push)], fill=INK, width=2)
    d.polygon([(x0 + length, y_push), (x0 + length - 14, y_push - 8),
               (x0 + length - 14, y_push + 8)], fill=INK)
    # 敲く: 同じ地点への往復(迷い)を繰り返す
    kx = x0
    n = 5
    step = length / n
    for i in range(n):
        top = y_knock - 22 if i % 2 == 0 else y_knock
        bot = y_knock
        d.line([(kx, bot), (kx, top)], fill=ACCENT, width=2)
        d.line([(kx, top), (kx + step, bot if i % 2 == 0 else top - 22)], fill=ACCENT, width=1)
        kx += step
    d.line([(x0, y_knock), (x0 + length, y_knock)], fill=ACCENT, width=1)
    # 決着の点(韓愈の一言が置かれた場所)
    d.ellipse([x0 + length + 30 - 7, (y_push + y_knock) // 2 - 7,
               x0 + length + 30 + 7, (y_push + y_knock) // 2 + 7], fill=INK)
    # ラベル
    fs = font(24)
    d.text((x0 - 58, y_push - 14), "推", font=fs, fill=INK)
    d.text((x0 - 58, y_knock - 14), "敲", font=fs, fill=ACCENT)
    # タイトル
    draw_spaced(d, "推敲", 118, 214, font(150), INK, 26)
    d.line([(126, 404), (300, 404)], fill=ACCENT, width=3)
    d.text((126, 436), "一字に、驢馬を止める", font=font(38), fill=INK)
    return _save(img, "suikou_cover.png")

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
    elif len(argv) >= 2 and argv[1] == "johakyu":
        johakyu()
    elif len(argv) >= 2 and argv[1] == "shoshin":
        shoshin()
    elif len(argv) >= 2 and argv[1] == "suikou":
        suikou()
    elif len(argv) >= 3 and argv[1] == "sekki":
        sekki(argv[2])
    else:
        raise SystemExit(__doc__)

if __name__ == "__main__":
    main(sys.argv)
