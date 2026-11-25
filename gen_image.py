#!/usr/bin/env python3
"""Deterministic editorial infographic: world news of Wednesday 25 November 2026."""

import os

from PIL import Image, ImageDraw, ImageFont

SCALE = 2
OUT = 1024
CANVAS = OUT * SCALE

BG = (244, 240, 231)
CARD = (255, 252, 247)
INK = (30, 33, 38)
SUB = (68, 66, 60)
RULE = (196, 188, 174)
CREAM = (255, 250, 242)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# Muted accents, one per story.
SLATE = (46, 82, 108)
RUST = (146, 76, 50)
WINE = (120, 62, 66)
TEAL = (34, 94, 102)
OLIVE = (104, 96, 50)
FOREST = (44, 94, 72)

STORIES = (
    {
        "title": "New US tariffs",
        "sub": "China's capped rate is 20%",
        "accent": SLATE,
        "icon": "tariff",
    },
    {
        "title": "Samara plants hit",
        "sub": "Two Rosneft refineries struck",
        "accent": RUST,
        "icon": "refinery",
    },
    {
        "title": "Four killed in Gaza",
        "sub": "Official and family in Shati",
        "accent": WINE,
        "icon": "building",
    },
    {
        "title": "Shenzhou-24 launches",
        "sub": "First Pakistani astronaut",
        "accent": TEAL,
        "icon": "rocket",
    },
    {
        "title": "Iowa stockpile gone",
        "sub": "Nearly 5 tons of lead azide",
        "accent": OLIVE,
        "icon": "blast",
    },
    {
        "title": "Garment pay up 36%",
        "sub": "New floor is 17,000 taka",
        "accent": FOREST,
        "icon": "shirt",
    },
)


def font(path, size):
    return ImageFont.truetype(path, size)


def text_width(fnt, text):
    return fnt.getlength(text)


def fit_line(text, path, max_size, min_size, max_width):
    for size in range(max_size, min_size - 1, -2):
        fnt = font(path, size)
        if text_width(fnt, text) <= max_width:
            return fnt, size
    fnt = font(path, min_size)
    return fnt, min_size


def line_height(fnt):
    ascent, descent = fnt.getmetrics()
    return ascent + descent + 4


def draw_center(draw, text, cx, y, fnt, fill):
    w = text_width(fnt, text)
    draw.text((cx - w / 2.0, y), text, font=fnt, fill=fill)
    return w


def tracked(draw, text, cx, y, fnt, fill, gap):
    width = sum(text_width(fnt, ch) for ch in text) + gap * (len(text) - 1)
    x = cx - width / 2.0
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += text_width(fnt, ch) + gap


def icon_tariff(draw, cx, cy, s, color, hole):
    w = max(8, s // 8)
    draw.line(
        (cx - s * 0.32, cy + s * 0.36, cx + s * 0.32, cy - s * 0.36),
        fill=color,
        width=w,
    )
    r = s * 0.16
    ring = max(6, s // 12)
    for ox, oy in ((-0.20, -0.22), (0.20, 0.22)):
        draw.ellipse(
            (cx + s * ox - r, cy + s * oy - r, cx + s * ox + r, cy + s * oy + r),
            outline=color,
            width=ring,
        )


def icon_refinery(draw, cx, cy, s, color, hole):
    # Two filled tanks, a pipe, and a flame on the right tank.
    for ox in (-0.22, 0.22):
        left = cx + s * ox - s * 0.15
        right = cx + s * ox + s * 0.15
        top = cy - s * 0.02
        bot = cy + s * 0.38
        draw.rounded_rectangle((left, top, right, bot), radius=s * 0.07, fill=color)
        draw.chord((left, top - s * 0.12, right, top + s * 0.14), 180, 360, fill=color)
        draw.rectangle((left + s * 0.04, cy + s * 0.08, right - s * 0.04, cy + s * 0.14), fill=hole)
    draw.rectangle((cx - s * 0.08, cy + s * 0.12, cx + s * 0.08, cy + s * 0.20), fill=color)
    flame = [
        (cx + s * 0.22, cy - s * 0.44),
        (cx + s * 0.36, cy - s * 0.18),
        (cx + s * 0.26, cy - s * 0.10),
        (cx + s * 0.20, cy - s * 0.20),
        (cx + s * 0.10, cy - s * 0.08),
        (cx + s * 0.12, cy - s * 0.30),
    ]
    draw.polygon(flame, fill=color)


def icon_building(draw, cx, cy, s, color, hole):
    left = cx - s * 0.28
    right = cx + s * 0.28
    top = cy - s * 0.36
    bot = cy + s * 0.40
    draw.rectangle((left, top, right, bot), fill=color)
    draw.rectangle((left - s * 0.08, bot - s * 0.04, right + s * 0.08, bot + s * 0.04), fill=color)
    win_w = s * 0.10
    win_h = s * 0.09
    for row in range(3):
        for col in range(2):
            x = left + s * 0.08 + col * s * 0.20
            y = top + s * 0.08 + row * s * 0.18
            draw.rectangle((x, y, x + win_w, y + win_h), fill=hole)


def icon_rocket(draw, cx, cy, s, color, hole):
    body = [
        (cx, cy - s * 0.46),
        (cx + s * 0.15, cy - s * 0.16),
        (cx + s * 0.15, cy + s * 0.20),
        (cx - s * 0.15, cy + s * 0.20),
        (cx - s * 0.15, cy - s * 0.16),
    ]
    draw.polygon(body, fill=color)
    draw.polygon(
        [
            (cx - s * 0.15, cy + s * 0.02),
            (cx - s * 0.38, cy + s * 0.28),
            (cx - s * 0.15, cy + s * 0.20),
        ],
        fill=color,
    )
    draw.polygon(
        [
            (cx + s * 0.15, cy + s * 0.02),
            (cx + s * 0.38, cy + s * 0.28),
            (cx + s * 0.15, cy + s * 0.20),
        ],
        fill=color,
    )
    draw.polygon(
        [
            (cx - s * 0.07, cy + s * 0.22),
            (cx, cy + s * 0.46),
            (cx + s * 0.07, cy + s * 0.22),
        ],
        fill=color,
    )
    draw.ellipse((cx - s * 0.07, cy - s * 0.08, cx + s * 0.07, cy + s * 0.06), fill=hole)


def icon_blast(draw, cx, cy, s, color, hole):
    r = s * 0.42
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=color, width=max(7, s // 11))
    left = cx - s * 0.13
    right = cx + s * 0.13
    top = cy - s * 0.18
    bot = cy + s * 0.24
    draw.rounded_rectangle((left, top, right, bot), radius=s * 0.04, fill=color)
    draw.rectangle((left, cy - s * 0.06, right, cy - s * 0.01), fill=hole)
    draw.rectangle((left, cy + s * 0.08, right, cy + s * 0.13), fill=hole)


def icon_shirt(draw, cx, cy, s, color, hole):
    shirt = [
        (cx - s * 0.10, cy - s * 0.26),
        (cx + s * 0.10, cy - s * 0.26),
        (cx + s * 0.14, cy - s * 0.08),
        (cx + s * 0.40, cy - s * 0.22),
        (cx + s * 0.44, cy - s * 0.04),
        (cx + s * 0.18, cy + s * 0.10),
        (cx + s * 0.18, cy + s * 0.40),
        (cx - s * 0.18, cy + s * 0.40),
        (cx - s * 0.18, cy + s * 0.10),
        (cx - s * 0.44, cy - s * 0.04),
        (cx - s * 0.40, cy - s * 0.22),
        (cx - s * 0.14, cy - s * 0.08),
    ]
    draw.polygon(shirt, fill=color)
    # Neck opening, punched back to the badge colour.
    draw.pieslice(
        (cx - s * 0.09, cy - s * 0.30, cx + s * 0.09, cy - s * 0.08),
        15,
        165,
        fill=hole,
    )


ICONS = {
    "tariff": icon_tariff,
    "refinery": icon_refinery,
    "building": icon_building,
    "rocket": icon_rocket,
    "blast": icon_blast,
    "shirt": icon_shirt,
}


def draw_header(draw):
    # Sizes below are in 2x pixels.
    kicker = font(BOLD, 36)
    date = font(BOLD, 128)
    weekday = font(SANS, 52)

    tracked(draw, "THE WORLD IN ONE IMAGE", CANVAS / 2, 48, kicker, SLATE, 8)
    draw_center(draw, "25 NOVEMBER 2026", CANVAS / 2, 108, date, INK)
    draw_center(draw, "Wednesday 25 November 2026", CANVAS / 2, 268, weekday, SUB)

    y = 360
    draw.line((80, y, CANVAS - 80, y), fill=RULE, width=3)
    # Short accent over the rule, centered.
    draw.line((CANVAS / 2 - 70, y, CANVAS / 2 + 70, y), fill=SLATE, width=8)


def draw_panel(draw, box, story):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=28, fill=CARD, outline=RULE, width=3)
    # Accent tab along the top edge, inset from the corners.
    draw.rectangle((x0 + 36, y0 + 2, x1 - 36, y0 + 14), fill=story["accent"])

    inner_w = (x1 - x0) - 64
    cx = (x0 + x1) / 2.0
    accent = story["accent"]

    title_font, _ = fit_line(story["title"], BOLD, 80, 58, inner_w)
    sub_font, _ = fit_line(story["sub"], SANS, 52, 40, inner_w)
    title_h = line_height(title_font)
    sub_h = line_height(sub_font)

    badge_r = 88
    gap_after_badge = 26
    gap_after_title = 18
    block_h = badge_r * 2 + gap_after_badge + title_h + gap_after_title + sub_h
    top_room = 28
    bottom_room = 26
    usable = (y1 - y0) - top_room - bottom_room
    offset = top_room + max(0, (usable - block_h) / 2.0)

    badge_cy = y0 + offset + badge_r
    draw.ellipse(
        (cx - badge_r, badge_cy - badge_r, cx + badge_r, badge_cy + badge_r),
        fill=accent,
    )
    ICONS[story["icon"]](draw, cx, badge_cy, 146, CREAM, accent)

    title_y = badge_cy + badge_r + gap_after_badge
    draw_center(draw, story["title"], cx, title_y, title_font, INK)

    rule_y = title_y + title_h + 2
    draw.line((cx - 40, rule_y, cx + 40, rule_y), fill=accent, width=5)

    sub_y = rule_y + gap_after_title - 6
    draw_center(draw, story["sub"], cx, sub_y, sub_font, SUB)

    # Guard: sublabel must stay inside the card.
    sub_bottom = sub_y + line_height(sub_font)
    if sub_bottom > y1 - 24:
        raise RuntimeError("sublabel overflows panel: " + story["title"])
    if text_width(title_font, story["title"]) > inner_w + 1:
        raise RuntimeError("title overflows panel: " + story["title"])
    if text_width(sub_font, story["sub"]) > inner_w + 1:
        raise RuntimeError("sublabel overflows panel: " + story["sub"])


def layout_panels():
    margin = 48
    gap = 28
    top = 392
    cols = 2
    rows = 3
    width = (CANVAS - margin * 2 - gap * (cols - 1)) / cols
    height = (CANVAS - top - margin - gap * (rows - 1)) / rows
    boxes = []
    for i in range(6):
        col = i % cols
        row = i // cols
        x0 = margin + col * (width + gap)
        y0 = top + row * (height + gap)
        boxes.append((x0, y0, x0 + width, y0 + height))
    return boxes


def render():
    image = Image.new("RGB", (CANVAS, CANVAS), BG)
    draw = ImageDraw.Draw(image)
    draw_header(draw)
    for box, story in zip(layout_panels(), STORIES):
        draw_panel(draw, box, story)
    final = image.resize((OUT, OUT), Image.Resampling.LANCZOS)
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    final.save(path, "PNG", compress_level=9)
    return path


if __name__ == "__main__":
    render()
