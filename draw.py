#!/usr/bin/env python3
"""
Draw the news infographic for Sunday 22 November 2026.
Renders to entry.png at exactly 1024x1024.
"""

from PIL import Image, ImageDraw, ImageFont
import json

# Canvas
W, H = 1024, 1024
img = Image.new('RGB', (W, H), (245, 245, 245))  # Light gray background
draw = ImageDraw.Draw(img)

# Fonts
try:
    font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
    font_headline = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
    font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
    font_region = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 10)
except:
    font_title = ImageFont.load_default()
    font_headline = ImageFont.load_default()
    font_body = ImageFont.load_default()
    font_small = ImageFont.load_default()
    font_region = ImageFont.load_default()

# Colors
COLOR_BG = (245, 245, 245)
COLOR_CARD_BG = (255, 255, 255)
COLOR_MASTHEAD_BG = (25, 45, 75)
COLOR_MASTHEAD_TEXT = (255, 255, 255)
COLOR_ACCENT = (200, 40, 40)
COLOR_TEXT = (30, 30, 30)
COLOR_TEXT_MUTED = (100, 100, 100)
COLOR_BORDER = (200, 200, 200)
COLOR_REGION_BG = (230, 240, 255)
COLOR_REGION_TEXT = (30, 60, 120)

# Region colors
REGION_COLORS = {
    "Global": (0, 120, 180),
    "Middle East": (180, 80, 0),
    "Europe": (0, 100, 60),
    "Americas": (160, 0, 80),
    "Economy": (120, 60, 180),
    "Science": (0, 140, 100),
    "Asia": (200, 100, 0),
    "Africa": (80, 140, 0),
    "Sport": (180, 0, 120),
}

def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    """Draw a rounded rectangle."""
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def draw_masthead():
    """Draw the top masthead with date."""
    masthead_h = 90
    draw_rounded_rect(draw, (0, 0, W, masthead_h), 0, fill=COLOR_MASTHEAD_BG)
    
    # Title
    title = "Sunday 22 November 2026 — The World in One Day"
    draw.text((W//2, 32), title, font=font_title, fill=COLOR_MASTHEAD_TEXT, anchor="mm")
    
    # Decorative line
    draw.line([(100, 70), (W-100, 70)], fill=(255, 255, 255, 100), width=2)
    
    return masthead_h

def draw_symbol(draw, cx, cy, symbol_type, color, size=24):
    """Draw a simple symbolic icon for each story type."""
    s = size // 2
    
    if symbol_type == "globe":  # COP31 / Global
        draw.ellipse([cx-s, cy-s, cx+s, cy+s], outline=color, width=2)
        draw.line([(cx, cy-s), (cx, cy+s)], fill=color, width=2)
        draw.line([(cx-s, cy), (cx+s, cy)], fill=color, width=2)
        draw.line([(cx-s*0.7, cy-s*0.7), (cx+s*0.7, cy+s*0.7)], fill=color, width=2)
        draw.line([(cx+s*0.7, cy-s*0.7), (cx-s*0.7, cy+s*0.7)], fill=color, width=2)
    
    elif symbol_type == "missile":  # Iran/Israel/Poland strikes
        draw.line([(cx, cy-s), (cx, cy+s//2)], fill=color, width=3)
        # Triangle tip
        draw.polygon([(cx, cy-s), (cx-5, cy-s+8), (cx+5, cy-s+8)], fill=color)
        # Fins
        draw.line([(cx-4, cy+s//2), (cx-8, cy+s)], fill=color, width=2)
        draw.line([(cx+4, cy+s//2), (cx+8, cy+s)], fill=color, width=2)
    
    elif symbol_type == "flame":  # Fire/industrial site
        draw.polygon([(cx, cy-s), (cx-s//2, cy+s//2), (cx, cy), (cx+s//2, cy+s//2)], fill=color)
        draw.polygon([(cx, cy-s//2), (cx-s//3, cy), (cx, cy-s//4), (cx+s//3, cy)], fill=(255, 160, 0))
    
    elif symbol_type == "chart":  # Economy/IPO
        points = [(cx-s, cy+s), (cx-s//2, cy), (cx, cy+s//2), (cx+s//2, cy-s//2), (cx+s, cy-s)]
        draw.line(points, fill=color, width=3)
        for px, py in points:
            draw.ellipse([px-2, py-2, px+2, py+2], fill=color)
    
    elif symbol_type == "scales":  # ICJ / Justice
        draw.line([(cx-s, cy+s), (cx+s, cy+s)], fill=color, width=2)
        draw.line([(cx, cy+s), (cx, cy)], fill=color, width=2)
        draw.line([(cx-s, cy), (cx-s, cy-s)], fill=color, width=2)
        draw.line([(cx-s-6, cy-s), (cx-s+6, cy-s)], fill=color, width=2)
        draw.line([(cx+s, cy), (cx+s, cy-s)], fill=color, width=2)
        draw.line([(cx+s-6, cy-s), (cx+s+6, cy-s)], fill=color, width=2)
    
    elif symbol_type == "satellite":  # Voyager
        draw.ellipse([cx-8, cy-4, cx+8, cy+4], outline=color, width=2)
        draw.line([(cx-14, cy), (cx-8, cy)], fill=color, width=2)
        draw.line([(cx+8, cy), (cx+14, cy)], fill=color, width=2)
        draw.line([(cx, cy-10), (cx, cy-4)], fill=color, width=2)
        draw.line([(cx, cy+4), (cx, cy+10)], fill=color, width=2)
        draw.line([(cx, cy-4), (cx, cy-14)], fill=color, width=1)
        draw.ellipse([cx-3, cy-16, cx+3, cy-14], fill=color)
    
    elif symbol_type == "shield":  # FBI / database security
        draw.polygon([(cx, cy-s), (cx+s, cy), (cx, cy+s), (cx-s, cy)], outline=color, width=2)
        draw.line([(cx, cy-s+4), (cx, cy+s-4)], fill=color, width=2)
        draw.line([(cx-s+4, cy), (cx+s-4, cy)], fill=color, width=2)
    
    elif symbol_type == "card":  # Credit card
        draw.rounded_rectangle([cx-s, cy-s, cx+s, cy+s], radius=3, outline=color, width=2)
        draw.line([(cx-s+6, cy-4), (cx+s-6, cy-4)], fill=color, width=2)
        draw.line([(cx-s+6, cy+2), (cx+s-6, cy+2)], fill=color, width=1)
    
    elif symbol_type == "boat":  # Nigeria boat
        draw.polygon([(cx-s, cy+s//2), (cx-s//2, cy+s), (cx+s//2, cy+s), (cx+s, cy+s//2)], fill=color)
        draw.line([(cx, cy-s), (cx, cy+s//2)], fill=color, width=2)
        draw.polygon([(cx, cy-s), (cx-s//2, cy-s//2), (cx+s//2, cy-s//2)], fill=color)
    
    elif symbol_type == "wave":  # Brazil storm
        draw.line([(cx-s, cy), (cx-s//2, cy-s), (cx, cy), (cx+s//2, cy-s), (cx+s, cy)], fill=color, width=3)
        draw.line([(cx-s, cy+4), (cx-s//2, cy-s+4), (cx, cy+4), (cx+s//2, cy-s+4), (cx+s, cy+4)], fill=color, width=2)
    
    elif symbol_type == "cricket":  # Australia cricket
        # Bat
        draw.line([(cx-10, cy+s), (cx, cy-s)], fill=color, width=3)
        draw.line([(cx, cy-s), (cx+10, cy+s)], fill=color, width=3)
        # Ball
        draw.ellipse([cx-4, cy+4, cx+4, cy+12], fill=color)
        # Stumps hint
        draw.line([(cx-6, cy+8), (cx-6, cy+14)], fill=color, width=1)
        draw.line([(cx, cy+8), (cx, cy+14)], fill=color, width=1)
        draw.line([(cx+6, cy+8), (cx+6, cy+14)], fill=color, width=1)
    
    elif symbol_type == "gavel":  # Dutch court / BYD
        # Handle
        draw.line([(cx, cy+s), (cx, cy-s//2)], fill=color, width=4)
        # Head
        draw.rounded_rectangle([cx-12, cy-s//2-8, cx+12, cy-s//2+4], radius=2, fill=color)
    
    elif symbol_type == "car":  # BYD SUV / car outline
        draw.rounded_rectangle([cx-s, cy, cx+s, cy+s], radius=2, outline=color, width=2)
        draw.rounded_rectangle([cx-s//2, cy-s//2, cx+s//2, cy], radius=2, outline=color, width=2)
        draw.ellipse([cx-s+2, cy+s-2, cx-s+8, cy+s+4], fill=color)  # wheels
        draw.ellipse([cx+s-8, cy+s-2, cx+s-2, cy+s+4], fill=color)

# --- MAIN DRAWING ---

# 1. Masthead
masthead_h = draw_masthead()

# 2. Card layout - 3 columns, 5 rows for 14 cards (but we need 12 per task)
# Using smaller cards to fit 5 rows
card_w = 310
card_h = 170
margin_x = 20
margin_y = 10
start_y = masthead_h + 20
cols = 3

# Stories to render (12 from JSON as per task, plus 2 more if they fit)
stories = [
    {
        "headline": "COP31 Antalya: Final Climate Deal",
        "fact": "Nearly 200 nations reach agreement after overnight talks",
        "symbol": "globe",
        "region": "Global",
    },
    {
        "headline": "Iran Strikes US Bases in Bahrain",
        "fact": "Missile & drone attacks on Sheikh Isa & Juffair; industrial fire on Sitra",
        "symbol": "missile",
        "region": "Middle East",
    },
    {
        "headline": "Saudi Coalition Downs Houthi Missile",
        "fact": "Ballistic missile & drone intercepted; attacks on Taiz kill 1, wound 7",
        "symbol": "missile",
        "region": "Middle East",
    },
    {
        "headline": "Russia Hits Zelensky's Hometown Kryvyi Rih",
        "fact": "Double-tap strike kills 2 (incl. 7-yr-old), wounds 60; massive barrage",
        "symbol": "missile",
        "region": "Europe",
    },
    {
        "headline": "Russian Missiles Land in Poland",
        "fact": "Kh-101 cruise missile & drone fall in SE Poland; NATO pledges defense",
        "symbol": "missile",
        "region": "Europe",
    },
    {
        "headline": "FBI Probes US Justice Database Hack",
        "fact": "Suspected breach of nationwide criminal-history & warrant system",
        "symbol": "shield",
        "region": "Americas",
    },
    {
        "headline": "Trump Backs 10% Credit-Card Rate Cap",
        "fact": "Proposes cap with Dem support; again criticizes Fed rate policy",
        "symbol": "card",
        "region": "Americas",
    },
    {
        "headline": "Anthropic IPO Draws $120B Retail Demand",
        "fact": "Over $500B institutional interest; stock down ~15% on debut",
        "symbol": "chart",
        "region": "Economy",
    },
    {
        "headline": "Voyager 1 Reaches 1 Light-Day from Earth",
        "fact": "First human-made object at 25.9B km, 49 years after launch",
        "symbol": "satellite",
        "region": "Science",
    },
    {
        "headline": "ICJ Finds Rohingya Genocide Evidence",
        "fact": "Myanmar forces targeted 800K, killed ~10K; Myanmar rejects verdict",
        "symbol": "scales",
        "region": "Asia",
    },
    {
        "headline": "Nigeria Boat Capsize Kills 24+",
        "fact": "Mourners' boat overturns in Bayelsa; 24 rescued, operator flees",
        "symbol": "boat",
        "region": "Africa",
    },
    {
        "headline": "Supercell Storm Devastates S. Brazil",
        "fact": "114 km/h winds hit Tupanciretã; 3 dead, 162 injured, 8K homes damaged",
        "symbol": "wave",
        "region": "Americas",
    },
    {
        "headline": "Australia Chase 188 to Beat England at MCG",
        "fact": "Record T20 chase at MCG ends England's 7-match streak; Aus win by 3 wkts",
        "symbol": "cricket",
        "region": "Sport",
    },
    {
        "headline": "Dutch Court Bars BYD SUV in Europe",
        "fact": "Hague rules Fangchengbao Ti7 infringes Defender design; sales barred",
        "symbol": "gavel",
        "region": "Economy",
    },
]

print(f"Drawing {len(stories)} cards...")

for i, story in enumerate(stories):
    col = i % cols
    row = i // cols
    x = margin_x + col * (card_w + margin_x)
    y = start_y + row * (card_h + margin_y)
    
    # Check bounds
    if y + card_h > H - 10:
        print(f"Warning: Card {i} would overflow, skipping")
        break
    
    # Card background
    draw_rounded_rect(draw, (x, y, x + card_w, y + card_h), 8, 
                      fill=COLOR_CARD_BG, outline=COLOR_BORDER, width=1)
    
    # Region tag (top-left)
    region = story["region"]
    rcolor = REGION_COLORS.get(region, (100, 100, 100))
    tag_w = 80
    tag_h = 20
    draw_rounded_rect(draw, (x + 10, y + 10, x + 10 + tag_w, y + 10 + tag_h), 4,
                      fill=rcolor)
    draw.text((x + 10 + tag_w//2, y + 20), region, font=font_region, fill=(255,255,255), anchor="mm")
    
    # Symbol (top-right)
    sym_x = x + card_w - 30
    sym_y = y + 30
    draw_symbol(draw, sym_x, sym_y, story["symbol"], rcolor, size=36)
    
    # Headline - wrap if needed (max 2 lines)
    headline = story["headline"]
    words = headline.split()
    lines = []
    current = ""
    for w in words:
        test = current + (" " if current else "") + w
        bbox = draw.textbbox((0,0), test, font=font_headline)
        if bbox[2] - bbox[0] <= card_w - 30:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    
    for li, line in enumerate(lines[:2]):
        draw.text((x + 15, y + 45 + li * 22), line, font=font_headline, fill=COLOR_TEXT)
    
    # Fact (wrapped to max 3 lines)
    fact = story["fact"]
    words = fact.split()
    lines = []
    current = ""
    for w in words:
        test = current + (" " if current else "") + w
        bbox = draw.textbbox((0,0), test, font=font_body)
        if bbox[2] - bbox[0] <= card_w - 30:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    
    fact_y = y + 45 + len(lines) * 22 + 5  # Start after headline (use actual headline line count)
    # Wait, we need to use the headline line count
    headline_lines = len(lines) if len(lines) <= 2 else 2
    fact_y = y + 45 + headline_lines * 22 + 5
    for li, line in enumerate(lines[:3]):
        draw.text((x + 15, fact_y + li * 18), line, font=font_body, fill=COLOR_TEXT_MUTED)

# Save
img.save("/root/makefun/news-image-20261122/entry.png", "PNG", optimize=True)
print("Saved entry.png")

# Verify
import os
size = os.path.getsize("/root/makefun/news-image-20261122/entry.png")
print(f"File size: {size} bytes ({size/1024:.1f} KB)")
