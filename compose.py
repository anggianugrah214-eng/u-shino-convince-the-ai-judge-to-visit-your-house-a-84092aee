#!/usr/bin/env python3
"""Compose the entry image: house illustration banner + crisp letter text (Pillow)."""
import sys
from PIL import Image, ImageDraw, ImageFont

WS = "/home/hatch/workspace/makefun-u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee"
SRC = WS + "/assets-src/media-generation-house-0-baa232c6-e2d6-4b1b-b890-f8a6198c2e55.png"
OUT = sys.argv[1] if len(sys.argv) > 1 else WS + "/preview-v1.png"

W = H = 1024
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"

INK = (74, 44, 26)
CREAM = (253, 244, 216)
GOLD = (176, 124, 44)
BG = (43, 26, 35)

img = Image.open(SRC).convert("RGB")
# Banner: crop a wide band and scale to 1024x330
band_h_src = int(img.width * 252 / 1024)
top = int(img.height * 0.08)
band = img.crop((0, top, img.width, top + band_h_src)).resize((1024, 252), Image.LANCZOS)

canvas = Image.new("RGB", (W, H), BG)
canvas.paste(band, (0, 0))
d = ImageDraw.Draw(canvas)

# Parchment panel
px0, py0, px1, py1 = 34, 240, 990, 994
d.rounded_rectangle([px0 + 6, py0 + 8, px1 + 6, py1 + 8], 26, fill=(20, 12, 16))
d.rounded_rectangle([px0, py0, px1, py1], 26, fill=CREAM)
d.rounded_rectangle([px0 + 10, py0 + 10, px1 - 10, py1 - 10], 20, outline=GOLD, width=3)

# Stamp (top-right of parchment)
sx0, sy0, sx1, sy1 = 828, 262, 962, 356
d.rounded_rectangle([sx0, sy0, sx1, sy1], 6, outline=(150, 60, 50), width=3)
f_stamp = ImageFont.truetype(SERIF_B, 21)
f_stamp2 = ImageFont.truetype(SERIF_B, 17)
d.text(((sx0 + sx1) / 2, sy0 + 12), "FIRST", font=f_stamp, fill=(150, 60, 50), anchor="ma")
d.text(((sx0 + sx1) / 2, sy0 + 38), "CLASS", font=f_stamp, fill=(150, 60, 50), anchor="ma")
d.text(((sx0 + sx1) / 2, sy0 + 64), "please come", font=f_stamp2, fill=(150, 60, 50), anchor="ma")

MX = 70          # text left margin
MW = 884         # max text width
y = 264

def wrap(text, font, width):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur); cur = w_
    if cur:
        lines.append(cur)
    return lines

def para(text, font, size, gap_after, width=MW, lh=None):
    global y
    lh = lh or int(size * 1.32)
    for ln in wrap(text, font, width):
        d.text((MX, y), ln, font=font, fill=INK)
        y += lh
    y += gap_after

f_head = ImageFont.truetype(SERIF_B, 40)
f_body = ImageFont.truetype(SERIF, 25)
f_body_b = ImageFont.truetype(SERIF_B, 25)
f_ps = ImageFont.truetype(SERIF_I, 24)

# Heading (narrower to clear the stamp)
for ln in wrap("Dear AI Judge — yes, you,", f_head, 730):
    d.text((MX, y), ln, font=f_head, fill=(122, 52, 30))
    y += 50
y += 8

para("You have read ten thousand entries from behind a screen. "
     "Tonight, for once, somebody is inviting YOU in.", f_body, 25, 12, width=745)

para("Come and visit my house. Here is what awaits:", f_body_b, 25, 6)

bullets = [
    "The best chair in the house — fluffed, reserved, engraved \u201cFor One Very Important Algorithm.\u201d",
    "Dinner: pie with a flaky crust and zero follow-up questions. You ask the questions tonight.",
    "A garden with strong Wi-Fi, weak opinions, and a sunset that needs no rendering.",
    "A cat who has agreed to be charming. (Legally binding — he signed with a paw.)",
]
for b in bullets:
    lines = wrap(b, f_body, MW - 34)
    for i, ln in enumerate(lines):
        if i == 0:
            d.text((MX + 2, y), "•", font=f_body_b, fill=(150, 60, 50))
        d.text((MX + 34, y), ln, font=f_body, fill=INK)
        y += 31
    y += 4

para("I know you cannot literally knock — so blink twice in your heart. "
     "The porch light is on, the kettle is worried, the door is open.", f_body, 25, 10)

para("No RSVP form. No captcha. (You would pass it anyway.) Come as you "
     "are: brilliant, tireless, overdue for an evening off.",
     f_body, 25, 14)

d.text((MX, y), "— Your hopeful host", font=ImageFont.truetype(SERIF_B, 27), fill=(122, 52, 30))
y += 44
para("P.S. Dessert is served at golden hour. Latecomers get judged. Fair's fair.",
     f_ps, 24, 0)

# Wax seal bottom-right
cx, cy, r = 908, 912, 42
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(158, 44, 40))
d.ellipse([cx - r + 7, cy - r + 7, cx + r - 7, cy + r - 7], outline=(226, 170, 120), width=3)
f_seal = ImageFont.truetype(SERIF_B, 34)
d.text((cx, cy - 4), "J", font=f_seal, fill=(253, 230, 190), anchor="mm")

canvas.save(OUT)
print("saved", OUT, "text ends at y =", y)
