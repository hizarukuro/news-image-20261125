#!/usr/bin/env python3
"""Render the news-image-20261125 front page: one 1024x1024 image summing up
Wednesday 25 November 2026's world news. Written from scratch with PIL.

Every number on the page (hero/grid/brief numbers and map pins) is generated
from the single ordered STORIES list below; nothing is typed twice.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")
W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

# ---------------------------------------------------------------- palette
PAPER = (246, 239, 221)
INK = (28, 26, 22)
MUTED = (107, 98, 82)
CARD = (255, 253, 246)
BORDER = (216, 205, 178)
RED = (179, 39, 30)
NAVY = (31, 58, 95)
GOLD = (240, 226, 184)
LAND = (201, 210, 184)
LAND_LINE = (154, 165, 131)
STAMP_FILL = {
    "CONFIRMED": (46, 107, 52),
    "OFFICIAL": (31, 58, 95),
    "REPORTED": (138, 109, 0),
    "CLAIM": (179, 39, 30),
    "ONGOING": (106, 74, 138),
}

# ---------------------------------------------------------------- fonts
def F(size, bold=False, serif=False):
    name = "DejaVuSerif-Bold.ttf" if (serif and bold) else \
           "DejaVuSerif.ttf" if serif else \
           "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

# ---------------------------------------------------------------- data
TIMELINE = [
    ("00:18", "Shenzhou-24 lifts off"),
    ("00:30", "Australia CPI 4.9%"),
    ("03:56", "Shenzhou-24 docks at Tiangong"),
    ("06:30", "Kospi closes −6.2%"),
    ("07:14", "Ofgem: UK bills +26%"),
    ("09:39", "Eurostar cancels trains"),
    ("13:30", "US GDP 4.3%, claims 189k"),
    ("21:00", "Nasdaq closes −3.8%"),
]

STATS = [
    ("112", "drones fired at Ukraine"),
    ("88", "downed by Ukraine"),
    ("145", "drones downed over Samara"),
    ("4.9%", "Australia's October inflation"),
    ("4.3%", "US Q3 GDP, revised up"),
    ("€50bn", "EU tech fund proposed"),
]

DATECHECK = [
    "Jensen Huang returns as Nvidia CEO — Mon 23 Nov",
    "Vaibhav Sooryavanshi, 15, hits 204 off 53 balls in Doha — Tue 24 Nov",
    "WHO evacuates staff from Akwe hospital; Ebola team moved — Tue 24 Nov",
    "Huawei guilty on 10 of 12 counts, Brooklyn — verdict Tue 24 Nov (rejection Wed)",
    "Riyadh financial-district tower hit, 11 hurt — Tue 24 Nov (first hit Thu 19 Nov)",
    "Hamas security chief Naeem Abu Nahel killed in Gaza — Tue 24 Nov",
    "UN: 47,000 women killed by partners or family in 2025 — published Tue 24 Nov",
]

# Each story: field, region, place (lon, lat), map jitter, headline, body,
# chip, stamp, sources, brief one-liner, scene kind.
STORIES = [
    dict(field="SPACE", region="East Asia", place=(98.5, 39.8), j=(0, 0),
         headline="Pakistan's first astronaut flies to Tiangong",
         body="Launched 00:18 UTC, docked 03:56. Ali, 40, is the first Pakistani "
              "in orbit and the first foreigner on Tiangong.",
         chip="00:18 UTC LIFTOFF", stamp="CONFIRMED", sources="Reuters; Xinhua/CMSA",
         brief="", scene="rocket"),
    dict(field="MARKETS", region="East Asia", place=(127.0, 37.5), j=(0, 0),
         headline="AI doubts crash Asia's chip stocks",
         body="Kospi −6.2%, Samsung −9.9%, SK Hynix −11.1%; Nasdaq fell 3.8% "
              "and Nvidia 8.5% on Wednesday.",
         chip="KOSPI −6.2%", stamp="CONFIRMED", sources="AP; WSJ; CNN",
         brief="", scene="crash"),
    dict(field="WAR", region="Middle East", place=(56.5, 26.6), j=(0, 0),
         headline="Two oil tankers hit mines and burn in Hormuz, Iran says",
         body="Two tankers hit mines and caught fire; Iran says they took an "
              "'unauthorised route' — unverified.",
         chip="2 TANKERS ABLAZE", stamp="CLAIM", sources="Reuters (IRNA/IRGC)",
         brief="", scene="tanker"),
    dict(field="SECURITY", region="Oceania", place=(149.1, -35.3), j=(0, -7),
         headline="Solomons pick Australia for security",
         body="Canberra signs a security treaty with Honiara.",
         chip="A$740M · 10 YRS", stamp="OFFICIAL", sources="DFAT; Reuters; AP",
         brief="", scene="treaty"),
    dict(field="WAR", region="Middle East", place=(42.9, 14.8), j=(0, 0),
         headline="Coalition strikes Hodeidah port",
         body="Coalition hits Hodeidah; 4 drones downed over Ras Tanura.",
         chip="4 DRONES DOWNED", stamp="CONFIRMED", sources="SPA; Reuters",
         brief="", scene="port"),
    dict(field="ENERGY", region="Europe", place=(-0.1, 51.5), j=(0, -7),
         headline="UK energy bills to jump 26%",
         body="About 20m households hit; gas prices blamed.",
         chip="£2,166 A YEAR", stamp="OFFICIAL", sources="Ofgem; Reuters",
         brief="", scene="house"),
    dict(field="WAR", region="Europe", place=(30.5, 50.4), j=(0, 0),
         headline="Russian strikes black out five Ukraine regions",
         body="Overnight attack cuts power; nuclear plant loses grid.",
         chip="5 REGIONS DARK", stamp="CONFIRMED", sources="Reuters; DTEK",
         brief="", scene="blackout"),
    dict(field="WAR", region="Europe", place=(50.1, 53.2), j=(0, 0),
         headline="Ukraine says it hit two Russian refineries",
         body="Kyiv says Syzran and Kuibyshev refineries are on fire.",
         chip="2 REFINERIES HIT", stamp="REPORTED", sources="Reuters; Kyiv",
         brief="", scene="refinery"),
    dict(field="WAR", region="Middle East", place=(34.5, 31.5), j=(-6, 5),
         headline="Israeli strike kills Hamas security chief",
         body="Abuelouf, his wife and two children killed in Shati.",
         chip="2ND IN 24 H", stamp="CONFIRMED", sources="Reuters; Gaza",
         brief="", scene="building"),
    dict(field="LABOUR", region="South Asia", place=(90.4, 23.8), j=(0, 0),
         headline="Garment workers win 36% pay rise",
         body="Board lifts the floor to 17,000 taka from 1 December.",
         chip="+36% PAY", stamp="OFFICIAL", sources="Reuters",
         brief="", scene="sewing"),
    dict(field="CRIME", region="Latin America", place=(-75.5, 10.4), j=(0, 0),
         headline="Cartagena hostage siege ends",
         body="Troops storm an Éxito store; one gunman killed.",
         chip="20 FREED", stamp="CONFIRMED", sources="Reuters/AFP",
         brief="", scene="store"),
    dict(field="TRADE", region="North America", place=(-77.0, 38.9), j=(-7, -6),
         headline="US proposes tariffs on 14 economies",
         body="China up to 20%, EU 15%; hearing set for 25 January.",
         chip="UP TO 20%", stamp="OFFICIAL", sources="Reuters/USTR",
         brief="", scene="ship"),
    dict(field="POLITICS", region="Middle East", place=(35.2, 31.8), j=(6, -5),
         headline="Knesset backs Oct 7 inquiry",
         body="Preliminary reading passes 65–50; Netanyahu opposes.",
         chip="65–50", stamp="OFFICIAL", sources="Reuters",
         brief="", scene="chamber"),
    dict(field="DISASTER", region="SE Asia", place=(106.8, -6.6), j=(0, 0),
         headline="26 miners trapped in flooded gold mine",
         body="Shaft flooded on Monday; 11 people escaped alive.",
         chip="3 BODIES FOUND", stamp="CONFIRMED", sources="Reuters; police",
         brief="", scene="mine"),
    dict(field="POLITICS", region="Europe", place=(4.35, 50.85), j=(-6, -6),
         headline="Puigdemont to end nine years in exile",
         body="He returns 12 Dec; new independence plan on 17 Dec.",
         chip="HOME 12 DEC", stamp="OFFICIAL", sources="Reuters",
         brief="", scene="podium"),
    dict(field="TECHNOLOGY", region="East Asia", place=(116.4, 39.9), j=(0, 0),
         headline="", body="", chip="", stamp="OFFICIAL", sources="BBC; AFP",
         brief="BEIJING — Huawei rejects the Brooklyn verdict and vows to appeal.",
         scene=""),
    dict(field="DIPLOMACY", region="East Asia", place=(125.75, 39.0), j=(0, 0),
         headline="", body="", chip="", stamp="OFFICIAL", sources="Reuters; KCNA",
         brief="PYONGYANG — North Korea expels the Swiss envoy; 48 hours to leave.",
         scene=""),
    dict(field="DIPLOMACY", region="Africa", place=(32.5, 15.6), j=(0, 0),
         headline="", body="", chip="", stamp="OFFICIAL", sources="SUNA",
         brief="KHARTOUM — Sudan's army govt rejects Ethiopia's offer to host talks.",
         scene=""),
    dict(field="TECHNOLOGY", region="Europe", place=(4.35, 50.85), j=(6, 6),
         headline="", body="", chip="", stamp="OFFICIAL", sources="Reuters; Commission",
         brief="BRUSSELS — EU proposes a Quantum Act and a €50bn tech fund for AI firms.",
         scene=""),
    dict(field="LABOUR", region="Europe", place=(23.7, 38.0), j=(0, 0),
         headline="", body="", chip="", stamp="CONFIRMED", sources="Reuters",
         brief="ATHENS — 24-hour strike grounds flights and keeps ferries in port.",
         scene=""),
    dict(field="JUSTICE", region="Africa", place=(18.4, -33.9), j=(0, 0),
         headline="", body="", chip="", stamp="OFFICIAL", sources="Moneyweb",
         brief="CAPE TOWN — Court voids the 2022 Phala Phala report on Ramaphosa.",
         scene=""),
    dict(field="ECONOMY", region="North America", place=(-77.0, 38.9), j=(7, -6),
         headline="", body="", chip="", stamp="OFFICIAL", sources="Reuters; BEA",
         brief="WASHINGTON — US Q3 GDP revised up to 4.3%; jobless claims 189,000.",
         scene=""),
    dict(field="ECONOMY", region="Oceania", place=(149.1, -35.3), j=(0, 7),
         headline="", body="", chip="", stamp="OFFICIAL", sources="ABS",
         brief="CANBERRA — October inflation 4.9%; underlying 3.8%; fuel up 6.3%.",
         scene=""),
    dict(field="ECONOMY", region="Europe", place=(13.4, 52.5), j=(0, 0),
         headline="", body="", chip="", stamp="OFFICIAL", sources="Destatis",
         brief="BERLIN — Q3 growth revised down to 0.1%; investment falls 1.2%.",
         scene=""),
    dict(field="TRANSPORT", region="Europe", place=(-0.1, 51.5), j=(-7, 6),
         headline="", body="", chip="", stamp="CONFIRMED", sources="Reuters; Eurostar",
         brief="LONDON — Surprise Eurostar walkout cancels at least 6 trains.",
         scene=""),
    dict(field="SPORT", region="Africa", place=(28.2, -25.9), j=(0, 0),
         headline="", body="", chip="", stamp="CONFIRMED", sources="ICC",
         brief="CENTURION — Mulder 7/31 and 100 as South Africa sweep Bangladesh 2–0.",
         scene=""),
    dict(field="SCIENCE", region="East Asia", place=(139.7, 35.7), j=(0, 0),
         headline="", body="", chip="", stamp="OFFICIAL", sources="AFP/JAXA",
         brief="TOKYO — JAXA unveils the LUPEX Moon rover; launch set for 2028.",
         scene=""),
    dict(field="POLITICS", region="Africa", place=(36.8, -1.3), j=(0, 0),
         headline="", body="", chip="", stamp="REPORTED", sources="Kenyan press",
         brief="NAIROBI — Opposition boycotts electoral-commission talks.",
         scene=""),
    dict(field="TRANSPORT", region="Europe", place=(-0.1, 51.5), j=(7, 6),
         headline="", body="", chip="", stamp="OFFICIAL", sources="TfL",
         brief="LONDON — Tube drivers to strike Thu 12:00–Fri 12:00; no Circle line.",
         scene=""),
    dict(field="MARKETS", region="North America", place=(-74.0, 40.7), j=(0, 0),
         headline="", body="", chip="", stamp="CONFIRMED", sources="CNN",
         brief="NEW YORK — Stocks slide: Nasdaq −3.8%, S&P −2.6%, Dow −1.7%.",
         scene=""),
    dict(field="POLITICS", region="East Asia", place=(116.4, 39.9), j=(-8, -7),
         headline="", body="", chip="", stamp="REPORTED", sources="Reuters",
         brief="BEIJING — Anti-graft probe opens into Shanghai party chief Chen Jining.",
         scene=""),
    dict(field="DIPLOMACY", region="East Asia", place=(116.4, 39.9), j=(8, -7),
         headline="", body="", chip="", stamp="REPORTED", sources="Reuters",
         brief="BEIJING — Wang Yi meets Dutch counterpart over the Nexperia dispute.",
         scene=""),
    dict(field="WAR", region="Africa", place=(-8.0, 12.6), j=(0, 0),
         headline="", body="", chip="", stamp="REPORTED", sources="Reuters",
         brief="BAMAKO — Cheap FPV drones reshape the Sahel insurgency; 187 attacks.",
         scene=""),
    dict(field="WEATHER", region="North America", place=(-77.0, 38.9), j=(0, 7),
         headline="", body="", chip="", stamp="REPORTED", sources="Reuters",
         brief="WASHINGTON — Storm heads for the East Coast on Thanksgiving.",
         scene=""),
    dict(field="MARKETS", region="South Asia", place=(72.9, 19.1), j=(0, 0),
         headline="", body="", chip="", stamp="CONFIRMED", sources="Hindu BusinessLine",
         brief="MUMBAI — Sensex +1,502 to 83,938; Nifty +1.85%; rupee 8-month high.",
         scene=""),
]
for i, s in enumerate(STORIES):
    s["n"] = i + 1

N_STORIES = len(STORIES)
N_REGIONS = len({s["region"] for s in STORIES})
N_FIELDS = len({s["field"] for s in STORIES})
assert (N_STORIES, N_REGIONS, N_FIELDS) == (35, 9, 18), (N_STORIES, N_REGIONS, N_FIELDS)

# ---------------------------------------------------------------- helpers
def wrap(d, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def fit_lines(d, text, font, width, max_lines, min_size=9):
    """Wrap text; shrink the font until it fits in max_lines."""
    size = font.size
    while size > min_size:
        lines = wrap(d, text, font, width)
        if len(lines) <= max_lines:
            return lines, font
        size -= 1
        font = F(size, bold=True, serif=False) if font == F(font.size, bold=True) else F(size)
        # rebuild with same weight/style as the original font
    return wrap(d, text, font, width), font

def draw_stamp(d, x, y, stamp, size=8):
    f = F(size, bold=True)
    w = d.textlength(stamp, font=f) + 8
    d.rounded_rectangle([x, y, x + w, y + size + 5], radius=2, fill=STAMP_FILL[stamp])
    d.text((x + 4, y + 2), stamp, font=f, fill=(255, 255, 255))
    return w

def draw_chip(d, x, y, text, size=9):
    f = F(size, bold=True)
    w = d.textlength(text, font=f) + 8
    d.rounded_rectangle([x, y, x + w, y + size + 5], radius=2, fill=GOLD,
                        outline=(196, 164, 92))
    d.text((x + 4, y + 2), text, font=f, fill=INK)
    return w

def draw_num(d, x, y, n, size=13):
    f = F(9, bold=True)
    d.rectangle([x, y, x + size, y + size], fill=RED)
    t = str(n)
    tw = d.textlength(t, font=f)
    d.text((x + (size - tw) / 2, y + 2), t, font=f, fill=(255, 255, 255))

# ---------------------------------------------------------------- scenes
def scene(d, box, kind):
    """Draw a small flat illustration inside box (x, y, w, h)."""
    x, y, w, h = box
    cx, cy = x + w // 2, y + h // 2
    if kind == "rocket":
        d.rectangle([x, y, x + w, y + h], fill=(43, 52, 84))
        for fx, fy in [(0.05, 0.12), (0.15, 0.06), (0.25, 0.15), (0.35, 0.08),
                       (0.55, 0.10), (0.70, 0.05), (0.85, 0.14), (0.95, 0.07)]:
            sx, sy = x + int(fx * w), y + int(fy * h)
            d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
        d.rectangle([x + int(0.68 * w), y + int(0.10 * h),
                     x + int(0.95 * w), y + int(0.16 * h)], fill=(200, 200, 200))
        d.rectangle([x + int(0.68 * w), y + int(0.24 * h),
                     x + int(0.95 * w), y + int(0.30 * h)], fill=(200, 200, 200))
        d.rectangle([x + int(0.80 * w), y + int(0.10 * h),
                     x + int(0.83 * w), y + int(0.30 * h)], fill=(220, 220, 220))
        rx = x + int(0.30 * w)
        d.polygon([(rx, y + int(0.42 * h)), (rx + int(0.03 * w), y + int(0.16 * h)),
                   (rx + int(0.06 * w), y + int(0.42 * h))], fill=RED)
        d.rectangle([rx, y + int(0.42 * h), rx + int(0.06 * w),
                     y + int(0.78 * h)], fill=(245, 245, 245))
        d.rectangle([rx + int(0.02 * w), y + int(0.52 * h),
                     rx + int(0.04 * w), y + int(0.62 * h)], fill=NAVY)
        d.polygon([(rx, y + int(0.68 * h)), (rx - int(0.02 * w), y + int(0.82 * h)),
                   (rx, y + int(0.78 * h))], fill=RED)
        d.polygon([(rx + int(0.06 * w), y + int(0.68 * h)),
                   (rx + int(0.08 * w), y + int(0.82 * h)),
                   (rx + int(0.06 * w), y + int(0.78 * h))], fill=RED)
        d.polygon([(rx + int(0.015 * w), y + int(0.78 * h)),
                   (rx + int(0.03 * w), y + int(0.97 * h)),
                   (rx + int(0.045 * w), y + int(0.78 * h))], fill=(255, 170, 40))
        d.ellipse([x + int(0.10 * w), y + int(0.86 * h),
                   x + int(0.28 * w), y + int(0.99 * h)], fill=(230, 225, 215))
        d.ellipse([x + int(0.26 * w), y + int(0.90 * h),
                   x + int(0.44 * w), y + h], fill=(220, 214, 200))
    elif kind == "crash":
        d.rectangle([x, y, x + w, y + h], fill=(24, 32, 56))
        d.rectangle([x + int(0.05 * w), y + int(0.20 * h),
                     x + int(0.28 * w), y + int(0.82 * h)],
                    fill=(16, 22, 40), outline=(90, 110, 150))
        for i in range(4):
            px = x + int(0.08 * w) + i * int(0.05 * w)
            d.line([px, y + int(0.26 * h), px, y + int(0.76 * h)],
                   fill=(90, 110, 150), width=2)
        d.rectangle([x + int(0.11 * w), y + int(0.44 * h),
                     x + int(0.22 * w), y + int(0.60 * h)], fill=(40, 60, 100))
        d.text((x + int(0.13 * w), y + int(0.47 * h)), "AI",
               font=F(10, bold=True), fill=(255, 255, 255))
        pts = [(x + int(0.33 * w), y + int(0.14 * h)),
               (x + int(0.45 * w), y + int(0.28 * h)),
               (x + int(0.57 * w), y + int(0.24 * h)),
               (x + int(0.68 * w), y + int(0.46 * h)),
               (x + int(0.80 * w), y + int(0.42 * h)),
               (x + int(0.92 * w), y + int(0.66 * h))]
        d.line(pts, fill=RED, width=4)
        for px, py in pts:
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 255, 255))
        d.polygon([(x + int(0.92 * w), y + int(0.66 * h)),
                   (x + int(0.88 * w), y + int(0.60 * h)),
                   (x + int(0.90 * w), y + int(0.72 * h))], fill=RED)
        d.rectangle([x + int(0.33 * w), y + int(0.76 * h),
                     x + int(0.52 * w), y + int(0.90 * h)], fill=RED)
        d.text((x + int(0.35 * w), y + int(0.78 * h)), "−6.2%",
               font=F(9, bold=True), fill=(255, 255, 255))
    elif kind == "tanker":
        d.rectangle([x, y, x + w, y + h], fill=(232, 150, 80))
        d.rectangle([x, y + int(0.62 * h), x + w, y + h], fill=(38, 74, 96))
        d.rectangle([x + int(0.08 * w), y + int(0.52 * h),
                     x + int(0.62 * w), y + int(0.72 * h)], fill=(20, 20, 20))
        d.rectangle([x + int(0.62 * w), y + int(0.40 * h),
                     x + int(0.72 * w), y + int(0.72 * h)], fill=(30, 30, 30))
        d.rectangle([x + int(0.65 * w), y + int(0.46 * h),
                     x + int(0.70 * w), y + int(0.54 * h)], fill=(220, 220, 200))
        d.polygon([(x + int(0.20 * w), y + int(0.52 * h)),
                   (x + int(0.23 * w), y + int(0.30 * h)),
                   (x + int(0.26 * w), y + int(0.52 * h))], fill=(255, 170, 40))
        d.polygon([(x + int(0.38 * w), y + int(0.52 * h)),
                   (x + int(0.42 * w), y + int(0.24 * h)),
                   (x + int(0.46 * w), y + int(0.52 * h))], fill=(255, 120, 30))
        d.ellipse([x + int(0.16 * w), y + int(0.08 * h),
                   x + int(0.30 * w), y + int(0.28 * h)], fill=(120, 110, 100))
        d.ellipse([x + int(0.32 * w), y + int(0.02 * h),
                   x + int(0.48 * w), y + int(0.24 * h)], fill=(110, 100, 90))
        d.ellipse([x + int(0.10 * w), y + int(0.76 * h),
                   x + int(0.30 * w), y + int(0.86 * h)], fill=(255, 255, 255))
        d.ellipse([x + int(0.55 * w), y + int(0.80 * h),
                   x + int(0.80 * w), y + int(0.90 * h)], fill=(240, 240, 240))
        d.ellipse([x + int(0.82 * w), y + int(0.20 * h),
                   x + int(0.85 * w), y + int(0.26 * h)], fill=(40, 40, 40))
        d.ellipse([x + int(0.88 * w), y + int(0.30 * h),
                   x + int(0.91 * w), y + int(0.36 * h)], fill=(40, 40, 40))
    elif kind == "treaty":
        d.rectangle([x, y, x + w, y + h], fill=(214, 226, 240))
        d.rectangle([x+8, y+10, x+34, y+26], fill=(0, 40, 104))
        d.rectangle([x+40, y+10, x+66, y+26], fill=(0, 90, 60))
        d.rectangle([x+14, y+34, x+62, y+58], fill=(255, 255, 255), outline=INK)
        d.line([x+18, y+42, x+58, y+42], fill=MUTED, width=1)
        d.line([x+18, y+48, x+58, y+48], fill=MUTED, width=1)
        d.line([x+18, y+54, x+44, y+54], fill=MUTED, width=1)
        d.line([x+56, y+50, x+70, y+62], fill=INK, width=2)
    elif kind == "port":
        d.rectangle([x, y, x + w, y + h], fill=(222, 214, 190))
        d.rectangle([x, y+58, x+w, y+h], fill=(120, 110, 95))
        d.line([x+12, y+10, x+12, y+58], fill=INK, width=3)
        d.line([x+12, y+12, x+44, y+12], fill=INK, width=3)
        d.line([x+44, y+12, x+44, y+30], fill=INK, width=1)
        d.rectangle([x+38, y+30, x+50, y+40], fill=RED)
        d.line([x+56, y+22, x+56, y+58], fill=INK, width=3)
        d.line([x+56, y+24, x+70, y+24], fill=INK, width=2)
        d.rectangle([x+8, y+62, x+26, y+72], fill=(180, 60, 40))
        d.rectangle([x+28, y+62, x+46, y+72], fill=(40, 90, 140))
        d.rectangle([x+48, y+62, x+66, y+72], fill=(200, 160, 40))
        d.ellipse([x+52, y+6, x+68, y+22], fill=(140, 130, 115))
        d.ellipse([x+62, y+2, x+74, y+16], fill=(150, 140, 125))
    elif kind == "house":
        d.rectangle([x, y, x + w, y + h], fill=(226, 236, 244))
        d.rectangle([x+12, y+34, x+48, y+66], fill=(200, 90, 60))
        d.polygon([(x+8, y+36), (x+30, y+16), (x+52, y+36)], fill=(120, 50, 40))
        d.rectangle([x+24, y+48, x+36, y+66], fill=(90, 60, 40))
        d.rectangle([x+16, y+40, x+22, y+46], fill=(255, 240, 180))
        d.rectangle([x+38, y+40, x+44, y+46], fill=(255, 240, 180))
        d.polygon([(x+56, y+34), (x+60, y+24), (x+64, y+34)], fill=(255, 170, 40))
        d.polygon([(x+52, y+34), (x+58, y+20), (x+64, y+34)], fill=(255, 120, 30))
        d.rectangle([x+52, y+52, x+70, y+70], fill=(255, 255, 255), outline=INK)
        d.line([x+55, y+58, x+67, y+58], fill=INK, width=1)
        d.line([x+55, y+63, x+67, y+63], fill=INK, width=1)
    elif kind == "blackout":
        d.rectangle([x, y, x + w, y + h], fill=(18, 24, 44))
        for bx, bh in [(x+6, 34), (x+20, 48), (x+36, 28), (x+50, 42)]:
            d.rectangle([bx, y+h-bh-8, bx+12, y+h-8], fill=(40, 46, 70))
            d.rectangle([bx+3, y+h-bh-2, bx+6, y+h-bh+1], fill=(255, 220, 120))
        d.ellipse([x+58, y+10, x+62, y+14], fill=(255, 255, 255))
        d.ellipse([x+66, y+18, x+70, y+22], fill=(255, 255, 255))
        d.line([x+58, y+12, x+66, y+20], fill=(200, 200, 200), width=1)
        d.ellipse([x+14, y+8, x+18, y+12], fill=(255, 200, 80))
    elif kind == "refinery":
        d.rectangle([x, y, x + w, y + h], fill=(30, 28, 44))
        d.rectangle([x+8, y+30, x+20, y+70], fill=(90, 90, 100))
        d.rectangle([x+24, y+18, x+36, y+70], fill=(110, 110, 120))
        d.rectangle([x+40, y+38, x+52, y+70], fill=(90, 90, 100))
        d.rectangle([x+56, y+48, x+68, y+70], fill=(200, 200, 200))
        d.polygon([(x+26, y+18), (x+30, y+6), (x+34, y+18)], fill=(255, 170, 40))
        d.polygon([(x+42, y+38), (x+46, y+26), (x+50, y+38)], fill=(255, 120, 30))
        d.ellipse([x+10, y+4, x+26, y+18], fill=(120, 110, 100))
        d.line([x+20, y+30, x+36, y+30], fill=(150, 150, 160), width=2)
    elif kind == "building":
        d.rectangle([x, y, x + w, y + h], fill=(228, 222, 208))
        d.rectangle([x+14, y+14, x+52, y+66], fill=(170, 160, 140))
        for r in range(3):
            for c in range(3):
                d.rectangle([x+19+c*11, y+19+r*14, x+26+c*11, y+27+r*14],
                            fill=(60, 55, 45))
        d.rectangle([x+28, y+54, x+38, y+66], fill=(90, 70, 50))
        d.ellipse([x+44, y+4, x+66, y+22], fill=(140, 130, 115))
        d.ellipse([x+56, y+0, x+72, y+14], fill=(150, 140, 125))
        d.line([x+58, y+66, x+66, y+50], fill=RED, width=2)
        d.line([x+66, y+50, x+70, y+58], fill=RED, width=2)
    elif kind == "sewing":
        d.rectangle([x, y, x + w, y + h], fill=(238, 232, 214))
        d.rectangle([x+8, y+52, x+66, y+58], fill=(120, 90, 60))
        d.rectangle([x+14, y+30, x+34, y+52], fill=(60, 60, 70))
        d.rectangle([x+34, y+36, x+58, y+44], fill=(80, 80, 90))
        d.line([x+56, y+44, x+56, y+52], fill=(200, 200, 200), width=2)
        d.rectangle([x+40, y+52, x+66, y+56], fill=(200, 60, 60))
        d.ellipse([x+58, y+10, x+70, y+22], fill=(40, 90, 140))
        d.ellipse([x+44, y+14, x+54, y+24], fill=(200, 160, 40))
        d.line([x+52, y+22, x+58, y+16], fill=MUTED, width=1)
    elif kind == "store":
        d.rectangle([x, y, x + w, y + h], fill=(236, 230, 216))
        d.rectangle([x+8, y+20, x+66, y+62], fill=(245, 245, 240), outline=INK)
        for i, col in enumerate([(200, 60, 40), (245, 245, 240)] * 3):
            d.rectangle([x+8+i*10, y+20, x+18+i*10, y+30], fill=col)
        d.rectangle([x+28, y+40, x+46, y+62], fill=(60, 90, 140))
        d.rectangle([x+12, y+40, x+24, y+52], fill=(180, 220, 240))
        d.rectangle([x+50, y+40, x+62, y+52], fill=(180, 220, 240))
        d.rectangle([x+6, y+64, x+68, y+70], fill=(220, 180, 40))
        d.line([x+6, y+64, x+68, y+70], fill=INK, width=1)
    elif kind == "ship":
        d.rectangle([x, y, x + w, y + h], fill=(210, 228, 240))
        d.rectangle([x+6, y+44, x+68, y+58], fill=(30, 40, 60))
        d.rectangle([x+12, y+32, x+24, y+44], fill=(200, 60, 40))
        d.rectangle([x+26, y+32, x+38, y+44], fill=(40, 90, 140))
        d.rectangle([x+40, y+32, x+52, y+44], fill=(200, 160, 40))
        d.rectangle([x+18, y+20, x+30, y+32], fill=(200, 60, 40))
        d.rectangle([x+32, y+20, x+44, y+32], fill=(40, 120, 60))
        d.rectangle([x+56, y+28, x+66, y+44], fill=(230, 230, 220))
        d.ellipse([x+52, y+8, x+70, y+26], fill=(255, 255, 255), outline=RED)
        d.text((x+58, y+12), "%", font=F(10, bold=True), fill=RED)
        d.line([x+0, y+62, x+w, y+62], fill=(120, 160, 190), width=2)
    elif kind == "chamber":
        d.rectangle([x, y, x + w, y + h], fill=(226, 220, 200))
        d.rectangle([x+10, y+8, x+64, y+20], fill=(120, 60, 50))
        for r in range(3):
            for c in range(5):
                col = (40, 120, 60) if (r + c) % 3 else (180, 50, 40)
                d.ellipse([x+14+c*11, y+28+r*12, x+21+c*11, y+35+r*12], fill=col)
        d.rectangle([x+14, y+64, x+60, y+70], fill=(90, 70, 50))
    elif kind == "mine":
        d.rectangle([x, y, x + w, y + h], fill=(150, 130, 100))
        d.rectangle([x+24, y+6, x+50, y+72], fill=(30, 25, 20))
        for i in range(5):
            d.line([x+28, y+14+i*11, x+46, y+14+i*11], fill=(180, 160, 120), width=2)
        d.ellipse([x+12, y+60, x+20, y+68], fill=(220, 180, 40))
        d.ellipse([x+54, y+58, x+62, y+66], fill=(220, 180, 40))
        d.rectangle([x+56, y+30, x+70, y+44], fill=(60, 90, 140))
        d.line([x+63, y+44, x+63, y+58], fill=(60, 90, 140), width=3)
    elif kind == "podium":
        d.rectangle([x, y, x + w, y + h], fill=(220, 228, 240))
        d.rectangle([x+20, y+40, x+54, y+68], fill=(120, 80, 50))
        d.rectangle([x+24, y+46, x+50, y+52], fill=(200, 170, 120))
        d.ellipse([x+32, y+22, x+42, y+34], fill=(220, 180, 150))
        d.rectangle([x+28, y+34, x+46, y+42], fill=(40, 50, 70))
        d.line([x+30, y+34, x+24, y+26], fill=INK, width=1)
        d.line([x+44, y+34, x+50, y+26], fill=INK, width=1)
        d.ellipse([x+22, y+24, x+26, y+28], fill=INK)
        d.ellipse([x+48, y+24, x+52, y+28], fill=INK)
        d.rectangle([x+8, y+10, x+16, y+22], fill=(200, 40, 40))
        d.rectangle([x+58, y+10, x+66, y+22], fill=(0, 40, 104))

# ---------------------------------------------------------------- map
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 80),
     (-75, 73), (-65, 62), (-55, 52), (-60, 45), (-70, 42), (-75, 35),
     (-80, 32), (-81, 26), (-84, 30), (-90, 21), (-97, 16), (-105, 20),
     (-115, 28), (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    [(-78, 8), (-72, 11), (-62, 10), (-52, 5), (-50, 0), (-44, -3), (-35, -8),
     (-40, -20), (-48, -28), (-58, -35), (-65, -41), (-70, -54), (-73, -50),
     (-73, -37), (-70, -20), (-77, -12), (-80, -4)],
    [(-17, 15), (-10, 30), (-5, 35), (10, 37), (20, 32), (32, 31), (35, 28),
     (43, 12), (51, 11), (48, 2), (40, -5), (40, -15), (36, -25), (32, -29),
     (26, -34), (19, -35), (15, -27), (12, -18), (13, -10), (9, 4), (-8, 4),
     (-13, 8)],
    [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 51), (3, 53), (8, 57),
     (10, 59), (5, 60), (12, 62), (18, 66), (25, 71), (30, 70), (40, 68),
     (45, 66), (40, 60), (30, 55), (28, 45), (23, 40), (19, 42), (12, 44),
     (8, 44), (3, 43), (-1, 37)],
    [(40, 68), (50, 70), (60, 70), (70, 72), (80, 73), (90, 75), (100, 77),
     (110, 76), (120, 73), (130, 72), (140, 72), (150, 70), (160, 66),
     (162, 60), (158, 52), (142, 50), (140, 40), (135, 35), (130, 33),
     (127, 35), (122, 38), (120, 32), (115, 23), (109, 20), (105, 10),
     (100, 8), (97, 16), (92, 21), (88, 22), (80, 15), (77, 8), (73, 20),
     (66, 25), (60, 25), (57, 26), (52, 28), (48, 30), (44, 29), (40, 36),
     (36, 36), (30, 36), (27, 40), (40, 45), (40, 55)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (137, -35),
     (140, -38), (145, -38), (150, -37), (153, -27), (146, -19), (142, -11),
     (136, -12), (132, -11), (126, -14), (122, -17), (118, -20)],
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 36), (141, 39),
     (142, 42), (141, 45), (139, 44), (136, 38), (133, 35)],
]

def draw_map(d, box):
    x, y, w, h = box
    d.rectangle([x, y, x + w, y + h], fill=(232, 238, 244), outline=BORDER)
    lat_top, lat_bot = 78.0, -58.0
    def proj(lon, lat):
        px = x + (lon + 180.0) / 360.0 * w
        py = y + (lat_top - lat) / (lat_top - lat_bot) * h
        return (px, py)
    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND,
                  outline=LAND_LINE)
    for s in STORIES:
        lon, lat = s["place"]
        px, py = proj(lon, lat)
        px += s["j"][0]
        py += s["j"][1]
        r = 7
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED, outline=(255, 255, 255))
        t = str(s["n"])
        f = F(7, bold=True)
        tw = d.textlength(t, font=f)
        d.text((px - tw / 2, py - 5), t, font=f, fill=(255, 255, 255))

# ---------------------------------------------------------------- compose
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 24
    y = 6

    # 1. kicker
    left = "THE WORLD'S NEWS IN ONE PAGE"
    right = (f"{N_STORIES} STORIES · {N_REGIONS} REGIONS · {N_FIELDS} FIELDS "
             "· ALL FROM THIS WEDNESDAY")
    d.text((M, y), left, font=F(11, bold=True), fill=RED)
    d.text((W - M - d.textlength(right, font=F(10, bold=True)), y), right,
           font=F(10, bold=True), fill=INK)
    y += 16

    # 2. masthead
    mast = "Wednesday 25 November 2026"
    mf = F(46, bold=True, serif=True)
    d.text(((W - d.textlength(mast, font=mf)) / 2, y), mast, font=mf, fill=INK)
    y += 48
    sub = ("Pakistan's first astronaut flies to Tiangong  ◆  Asia's chip stocks "
           "crash  ◆  Tankers burn in Hormuz")
    sf = F(12)
    d.text(((W - d.textlength(sub, font=sf)) / 2, y), sub, font=sf, fill=MUTED)
    y += 16

    # 3. timeline strip
    d.rectangle([M, y, W - M, y + 56], fill=CARD, outline=BORDER)
    d.text((M + 8, y + 5), "THE DAY IN UTC", font=F(10, bold=True), fill=RED)
    d.line([M + 8, y + 19, W - M - 8, y + 19], fill=BORDER, width=1)
    cell_w = (W - 2 * M - 16) // 4
    for i, (t, label) in enumerate(TIMELINE):
        cx = M + 8 + (i % 4) * cell_w
        cy = y + 23 + (i // 4) * 17
        d.text((cx, cy), t, font=F(10, bold=True), fill=RED)
        d.text((cx + 38, cy), label, font=F(9), fill=INK)
    y += 60

    # 4. heroes
    heroes = STORIES[:3]
    cw = (W - 2 * M - 2 * 10) // 3
    chh = 192
    for i, s in enumerate(heroes):
        x = M + i * (cw + 10)
        d.rectangle([x, y, x + cw, y + chh], fill=CARD, outline=BORDER)
        scene(d, (x + 1, y + 1, cw - 2, 88), s["scene"])
        ty = y + 96
        draw_num(d, x + 8, ty, s["n"], size=14)
        d.text((x + 28, ty + 1), f"{s['field']} · {s['region']}",
               font=F(8, bold=True), fill=MUTED)
        chip_w = d.textlength(s["chip"], font=F(8, bold=True)) + 8
        draw_chip(d, x + cw - 8 - chip_w, ty, s["chip"], size=8)
        hy = ty + 18
        hf = F(15, bold=True)
        hlines, hf = fit_lines(d, s["headline"], hf, cw - 16, 2, min_size=12)
        for ln in hlines:
            d.text((x + 8, hy), ln, font=hf, fill=INK)
            hy += hf.size + 2
        bf = F(11)
        blines, bf = fit_lines(d, s["body"], bf, cw - 16, 2, min_size=10)
        by = hy + 2
        for ln in blines:
            d.text((x + 8, by), ln, font=bf, fill=INK)
            by += bf.size + 2
        sy = y + chh - 18
        draw_stamp(d, x + 8, sy, s["stamp"], size=8)
        src = s["sources"]
        sf2 = F(8)
        d.text((x + cw - 8 - d.textlength(src, font=sf2), sy + 2), src,
               font=sf2, fill=MUTED)
    y += chh + 4

    # 5. stat band
    d.text((M, y), "THE NUMBERS", font=F(10, bold=True), fill=RED)
    y += 14
    bw = (W - 2 * M - 5 * 8) // 6
    for i, (big, label) in enumerate(STATS):
        x = M + i * (bw + 8)
        d.rectangle([x, y, x + bw, y + 40], fill=CARD, outline=BORDER)
        d.text((x + 8, y + 3), big, font=F(16, bold=True), fill=RED)
        lf = F(8)
        ll = wrap(d, label, lf, bw - 16)
        ly = y + 23
        for ln in ll[:1]:
            d.text((x + 8, ly), ln, font=lf, fill=INK)
    y += 44

    # 6. grid (stories 4-15)
    grid = STORIES[3:15]
    gw = (W - 2 * M - 3 * 8) // 4
    gh = 80
    for r in range(3):
        for c in range(4):
            s = grid[r * 4 + c]
            x = M + c * (gw + 8)
            gy = y + r * (gh + 5)
            d.rectangle([x, gy, x + gw, gy + gh], fill=CARD, outline=BORDER)
            scene(d, (x + 1, gy + 1, 72, gh - 2), s["scene"])
            tx = x + 78
            tw = gw - 78 - 6
            tag = f"{s['field']} · {s['region']}"
            tf = F(7, bold=True)
            chip_w = d.textlength(s["chip"], font=F(7, bold=True)) + 8
            if d.textlength(tag, font=tf) + chip_w > tw - 4:
                tf = F(6, bold=True)
            d.text((tx, gy + 4), tag, font=tf, fill=MUTED)
            draw_chip(d, tx + tw - 2 - chip_w, gy + 3, s["chip"], size=7)
            hf = F(12, bold=True)
            hlines, hf = fit_lines(d, s["headline"], hf, tw, 2, min_size=10)
            hy = gy + 17
            for ln in hlines:
                d.text((tx, hy), ln, font=hf, fill=INK)
                hy += hf.size + 1
            bf = F(10)
            blines, bf = fit_lines(d, s["body"], bf, tw, 2, min_size=9)
            by = hy + 1
            for ln in blines:
                d.text((tx, by), ln, font=bf, fill=INK)
                by += bf.size + 1
            sy = gy + gh - 14
            draw_num(d, tx, sy, s["n"], size=11)
            draw_stamp(d, tx + 15, sy, s["stamp"], size=7)
            src = s["sources"]
            sf2 = F(7)
            sw = d.textlength(src, font=sf2)
            if sw > tw - 62:
                while sw > tw - 62 and len(src) > 4:
                    src = src[:-2]
                    sw = d.textlength(src + "…", font=sf2)
                src = src + "…"
            d.text((tx + tw - d.textlength(src, font=sf2), sy + 1), src,
                   font=sf2, fill=MUTED)
    y += 3 * gh + 2 * 5 + 6

    # 7. briefs (stories 16-35)
    d.text((M, y), "MORE OF THE DAY", font=F(11, bold=True), fill=RED)
    y += 15
    briefs = STORIES[15:]
    col_w = (W - 2 * M - 16) // 2
    for col in range(2):
        for row in range(10):
            s = briefs[col * 10 + row]
            bx = M + col * (col_w + 16)
            by = y + row * 12.5
            draw_num(d, bx, by, s["n"], size=12)
            text = f"{s['brief']} ({s['sources']})"
            bf = F(9)
            avail = col_w - 18
            while d.textlength(text, font=bf) > avail and bf.size > 8:
                bf = F(bf.size - 1)
            d.text((bx + 16, by + 1), text, font=bf, fill=INK)
    y += 10 * 12.5 + 6

    # 8. map
    d.text((M, y), "WHERE IT HAPPENED — PINS = STORY NUMBERS",
           font=F(11, bold=True), fill=RED)
    y += 14
    draw_map(d, (M, y, W - 2 * M, 80))
    y += 80 + 6

    # 9. date check
    d.rectangle([M, y, W - M, y + 76], outline=RED, width=2, fill=(253, 244, 238))
    d.text((M + 8, y + 4), "DATE CHECK — LEFT OUT AS OTHER DAYS' NEWS",
           font=F(10, bold=True), fill=RED)
    dc_col = (W - 2 * M - 24) // 2
    for i, item in enumerate(DATECHECK):
        cx = M + 8 + (i // 4) * (dc_col + 8)
        cy = y + 20 + (i % 4) * 11
        d.text((cx, cy), "✕ " + item, font=F(9), fill=INK)
    d.text(((W - d.textlength("Every story on this page happened, or was first "
           "reported, on Wednesday 25 November 2026 in some time zone.",
           font=F(9))) / 2, y + 20 + 4 * 11),
           "Every story on this page happened, or was first reported, on "
           "Wednesday 25 November 2026 in some time zone.",
           font=F(9), fill=MUTED)
    y += 80

    # 10. footer
    legend = ("CONFIRMED = two or more major outlets · OFFICIAL = on the record · "
              "REPORTED = one outlet's reporting · CLAIM = one side's account, "
              "unverified · ONGOING = still developing")
    d.text((M, y), legend, font=F(8), fill=INK)
    y += 11
    d.text((M, y), "Scenes are drawn illustrations, not photographs.",
           font=F(8), fill=MUTED)
    y += 11
    srcs = ("Sources: Reuters · AP · AFP · Xinhua · Ofgem · ABS · Destatis · DFAT · "
            "BBC · CNN · ICC · JAXA · KCNA · SUNA · TfL · USTR · BEA · Moneyweb · "
            "Hindu BusinessLine")
    d.text((M, y), srcs, font=F(8), fill=MUTED)
    y += 11

    print("bottom y =", y, "of", H)
    img.save(OUT, optimize=True)
    print("saved", OUT, os.path.getsize(OUT), "bytes")

if __name__ == "__main__":
    main()
