"""
Generates og-image.png at 1200x630 — the standard OG image dimensions
that Facebook, LinkedIn, Twitter, WhatsApp, and Discord all expect.

Design: matches the site's dark mode rendering.
  - Background: #0f0f0f (same as site's --bg in dark mode)
  - Heading: #e8e8e8, serif, large
  - URL: #6b6b6b (muted), serif, smaller

Re-run this script if you ever want to tweak the image. Output goes
into the repo root so it's served by Vercel at /og-image.png.
"""

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1200, 630
BG_COLOR = (15, 15, 15)        # #0f0f0f
FG_COLOR = (232, 232, 232)     # #e8e8e8
MUTED_COLOR = (136, 136, 136)  # #888

NAME_TEXT = "Abdullah Chaudhry"
URL_TEXT = "abdullahnyle.dev"

# Liberation Serif is the closest match available for our serif stack
SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_REGULAR = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"

img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

name_font = ImageFont.truetype(SERIF_BOLD, size=88)
url_font = ImageFont.truetype(SERIF_REGULAR, size=40)

# Measure text boxes so we can center them precisely
name_bbox = draw.textbbox((0, 0), NAME_TEXT, font=name_font)
name_w = name_bbox[2] - name_bbox[0]
name_h = name_bbox[3] - name_bbox[1]

url_bbox = draw.textbbox((0, 0), URL_TEXT, font=url_font)
url_w = url_bbox[2] - url_bbox[0]
url_h = url_bbox[3] - url_bbox[1]

GAP = 32  # space between the name and the URL line

total_h = name_h + GAP + url_h
start_y = (HEIGHT - total_h) // 2

# Slight visual adjustment: pull the block up by ~5% since the optical
# center sits a bit above the mathematical center for text blocks
start_y -= int(HEIGHT * 0.03)

name_x = (WIDTH - name_w) // 2
name_y = start_y - name_bbox[1]  # offset by the bbox top to make y=0 the top of glyphs
draw.text((name_x, name_y), NAME_TEXT, font=name_font, fill=FG_COLOR)

url_x = (WIDTH - url_w) // 2
url_y = start_y + name_h + GAP - url_bbox[1]
draw.text((url_x, url_y), URL_TEXT, font=url_font, fill=MUTED_COLOR)

img.save("og-image.png", "PNG", optimize=True)
print(f"Generated og-image.png at {WIDTH}x{HEIGHT}")
