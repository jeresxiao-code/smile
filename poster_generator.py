from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import argparse
import csv
import json
import math

W, H = 1080, 1440
NAVY = "#061D55"
ORANGE = "#FF8500"
BLUE = "#1D75D8"
CREAM = "#FFF8EC"
CARD = "#FFF3DE"
CARD_BLUE = "#EAF5FF"
LIGHT_ORANGE = "#F7D7A6"
LIGHT_BLUE = "#8FC6FF"
WHITE = "#FFFFFF"
OUT = Path("output")
OUT.mkdir(exist_ok=True)


def find_font():
    candidates = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            return p
    return None

FONT_PATH = find_font()


def font(size):
    if FONT_PATH:
        return ImageFont.truetype(FONT_PATH, size)
    return ImageFont.load_default()


def draw_center(draw, text, y, size, fill=NAVY):
    f = font(size)
    box = draw.textbbox((0, 0), text, font=f)
    x = (W - (box[2] - box[0])) / 2
    draw.text((x, y), text, font=f, fill=fill)


def wrap_cn(text, max_chars):
    lines, cur = [], ""
    for ch in text:
        cur += ch
        if len(cur) >= max_chars:
            lines.append(cur)
            cur = ""
    if cur:
        lines.append(cur)
    return lines[:2]


def rounded(draw, xy, r, fill, outline=None, width=2):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)


def draw_burst(draw, x, y, color=ORANGE):
    for ang in [-35, 0, 35]:
        rad = math.radians(ang)
        x2 = x + math.cos(rad) * 45
        y2 = y + math.sin(rad) * 45
        draw.line((x, y, x2, y2), fill=color, width=8)


def draw_icon(draw, cx, cy, name):
    draw.ellipse((cx - 82, cy - 82, cx + 82, cy + 82), fill=WHITE)
    if name == "idea":
        draw.ellipse((cx - 32, cy - 40, cx + 32, cy + 24), outline=NAVY, width=6)
        draw.rectangle((cx - 20, cy + 25, cx + 20, cy + 48), outline=NAVY, width=6)
        draw.line((cx, cy - 72, cx, cy - 102), fill=ORANGE, width=6)
    elif name == "gear":
        draw.ellipse((cx - 50, cy - 50, cx + 50, cy + 50), outline=BLUE, width=12)
        draw.ellipse((cx - 16, cy - 16, cx + 16, cy + 16), fill=BLUE)
        draw.text((cx - 20, cy - 34), "✓", font=font(52), fill=NAVY)
    elif name == "growth":
        draw.line((cx - 55, cy + 45, cx - 55, cy - 10), fill=BLUE, width=18)
        draw.line((cx, cy + 45, cx, cy - 35), fill=BLUE, width=18)
        draw.line((cx + 55, cy + 45, cx + 55, cy - 65), fill=NAVY, width=18)
        draw.line((cx - 65, cy + 25, cx - 15, cy - 20, cx + 20, cy - 2, cx + 70, cy - 60), fill=ORANGE, width=8)
    elif name == "ai":
        rounded(draw, (cx - 52, cy - 38, cx + 52, cy + 38), 18, WHITE, NAVY, 6)
        draw.ellipse((cx - 28, cy - 8, cx - 12, cy + 8), fill=NAVY)
        draw.ellipse((cx + 12, cy - 8, cx + 28, cy + 8), fill=NAVY)
    elif name == "target":
        for r in [60, 38, 16]:
            draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=NAVY if r != 16 else BLUE, width=6)
        draw.line((cx - 50, cy + 50, cx + 50, cy - 50), fill=ORANGE, width=7)
    elif name == "book":
        rounded(draw, (cx - 58, cy - 55, cx + 5, cy + 55), 8, WHITE, NAVY, 5)
        rounded(draw, (cx - 5, cy - 55, cx + 58, cy + 55), 8, WHITE, BLUE, 5)
    elif name == "money":
        draw.ellipse((cx - 52, cy - 52, cx + 52, cy + 52), outline=ORANGE, width=8)
        draw.text((cx - 22, cy - 43), "¥", font=font(68), fill=NAVY)
    else:
        draw.ellipse((cx - 58, cy - 58, cx + 58, cy + 58), outline=BLUE, width=6)
        draw.line((cx - 58, cy, cx + 58, cy), fill=BLUE, width=5)
        draw.line((cx, cy - 58, cx, cy + 58), fill=BLUE, width=5)


def draw_poster(data, outfile):
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    draw_burst(draw, 95, 145)
    draw_burst(draw, 1000, 190)
    draw_center(draw, data["title_line_1"], 55, 82)
    draw_center(draw, data["title_line_2"], 150, 70)
    draw.line((190, 295, 330, 295), fill=ORANGE, width=4)
    draw.line((750, 295, 890, 295), fill=ORANGE, width=4)
    draw_center(draw, data["subtitle"], 270, 34)

    rounded(draw, (230, 350, 850, 415), 35, "#FFFDF7", LIGHT_ORANGE, 2)
    draw_center(draw, data["badge"], 363, 34)

    y = 450
    for idx, item in enumerate(data["items"]):
        is_blue = idx == 1
        fill = CARD_BLUE if is_blue else CARD
        outline = LIGHT_BLUE if is_blue else LIGHT_ORANGE
        num_color = BLUE if is_blue else ORANGE
        rounded(draw, (55, y, 1025, y + 210), 24, fill, outline, 2)
        draw_icon(draw, 185, y + 105, item.get("icon", "idea"))
        draw.line((330, y + 35, 330, y + 175), fill=outline, width=3)
        draw.ellipse((370, y + 45, 450, y + 125), fill=num_color)
        draw.text((386, y + 58), item.get("num", f"0{idx+1}"), font=font(42), fill=WHITE)
        draw.text((485, y + 48), item["title"], font=font(54), fill=NAVY)
        draw.line((485, y + 120, 970, y + 120), fill=outline, width=3)
        for li, line in enumerate(wrap_cn(item["desc"], 22)):
            draw.text((485, y + 138 + li * 38), line, font=font(28), fill=NAVY)
        y += 235

    rounded(draw, (55, 1165, 1025, 1325), 24, NAVY, NAVY, 2)
    draw_burst(draw, 110, 1245)
    draw_burst(draw, 965, 1245)
    fy = 1195
    for line in wrap_cn(data["footer"], 17):
        draw_center(draw, line, fy, 50, WHITE)
        fy += 62
    draw_center(draw, "→  " + data.get("bottom_note", "") + "  ←", 1355, 30)
    img.save(outfile)
    print(f"Saved: {outfile}")


def from_csv_row(row):
    return {
        "keyword": row["keyword"],
        "title_line_1": row["title_line_1"],
        "title_line_2": row["title_line_2"],
        "subtitle": row["subtitle"],
        "badge": row["badge"],
        "items": [
            {"num": "01", "title": row["item1_title"], "desc": row["item1_desc"], "icon": row["item1_icon"]},
            {"num": "02", "title": row["item2_title"], "desc": row["item2_desc"], "icon": row["item2_icon"]},
            {"num": "03", "title": row["item3_title"], "desc": row["item3_desc"], "icon": row["item3_icon"]},
        ],
        "footer": row["footer"],
        "bottom_note": row["bottom_note"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json")
    parser.add_argument("--csv")
    args = parser.parse_args()

    if args.json:
        data = json.loads(Path(args.json).read_text(encoding="utf-8"))
        draw_poster(data, OUT / f"{data.get('keyword', 'poster')}.png")

    if args.csv:
        with open(args.csv, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                data = from_csv_row(row)
                draw_poster(data, OUT / f"{data.get('keyword', 'poster')}.png")


if __name__ == "__main__":
    main()
