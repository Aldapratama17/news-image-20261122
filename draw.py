#!/usr/bin/env python3
"""
Draw the news infographic for Sunday 22 November 2026.
Renders to entry.png at exactly 1024x1024.
"""

from PIL import Image, ImageDraw, ImageFont
import json

# Canvas
W, H = 1024, 1024
img = Image.new('RGB', (W, H), (245, 245, 245))
draw = ImageDraw.Draw(img)

# Fonts - load with error handling
def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

font_title = load_font("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
font_headline_18 = load_font("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
font_headline_17 = load_font("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 17)
font_headline_16 = load_font("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
font_headline_15 = load_font("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
font_fact_16 = load_font("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
font_fact_15 = load_font("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
font_fact_14 = load_font("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
font_region = load_font("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 10)
font_ticker = load_font("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13)
font_ticker_text = load_font("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
font_footer = load_font("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)

# Colors
COLOR_BG = (245, 245, 245)
COLOR_CARD_BG = (255, 255, 255)
COLOR_MASTHEAD_BG = (25, 45, 75)
COLOR_MASTHEAD_TEXT = (255, 255, 255)
COLOR_ACCENT = (200, 40, 40)
COLOR_TEXT = (30, 30, 30)
COLOR_TEXT_MUTED = (80, 80, 80)
COLOR_BORDER = (200, 200, 200)
COLOR_REGION_BG = (230, 240, 255)
COLOR_REGION_TEXT = (30, 60, 120)
COLOR_FOOTER_BG = (230, 230, 230)
COLOR_TICKER_BG = (25, 45, 75)
COLOR_TICKER_TEXT = (255, 255, 255)
COLOR_TICKER_LABEL = (255, 200, 80)

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
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def can_text_fit(draw, text, font, max_width, max_lines):
    """Check if ENTIRE text fits in max_lines at this font size."""
    words = text.split()
    lines = []
    current = ""
    
    for w in words:
        test = current + (" " if current else "") + w
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
                if len(lines) >= max_lines:
                    return False
            current = w
    
    if current:
        lines.append(current)
    
    return len(lines) <= max_lines

def wrap_text_full(draw, text, font, max_width, max_lines):
    """Wrap text to fit within max_width, up to max_lines. Assumes text fits."""
    words = text.split()
    lines = []
    current = ""
    
    for w in words:
        test = current + (" " if current else "") + w
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    
    if current:
        lines.append(current)
    
    return lines[:max_lines]

def fit_headline(draw, text, max_width, max_lines=3):
    """Shrink font from 18 down to 15 until ENTIRE headline fits."""
    fonts = [
        (18, font_headline_18, 22),
        (17, font_headline_17, 21),
        (16, font_headline_16, 20),
        (15, font_headline_15, 19),
    ]
    for size, font, line_h in fonts:
        if can_text_fit(draw, text, font, max_width, max_lines):
            lines = wrap_text_full(draw, text, font, max_width, max_lines)
            return lines, font, line_h
    # Fallback at 15pt - force fit by truncating at clause boundaries
    text = truncate_at_clauses(draw, text, font_headline_15, max_width, max_lines)
    lines = wrap_text_full(draw, text, font_headline_15, max_width, max_lines)
    return lines, font_headline_15, 19

def truncate_at_clauses(draw, text, font, max_width, max_lines):
    """Truncate text at semicolons/colons first, then commas, until it fits."""
    if can_text_fit(draw, text, font, max_width, max_lines):
        return text
    
    # First try splitting on semicolons and colons (stronger boundaries)
    for sep in [';', ':', ',']:
        parts = []
        current = ""
        for ch in text:
            current += ch
            if ch == sep:
                parts.append(current.strip())
                current = ""
        if current.strip():
            parts.append(current.strip())
        
        if len(parts) > 1:
            # Try dropping trailing parts
            while parts:
                test = " ".join(parts)
                if can_text_fit(draw, test, font, max_width, max_lines):
                    return test
                parts.pop()
    
    # If nothing works, return first few words
    words = text.split()
    while words:
        test = " ".join(words)
        if can_text_fit(draw, test, font, max_width, max_lines):
            return test
        words.pop()
    
    return text[:50]

def fit_fact(draw, text, max_width, max_lines):
    """Fit fact text, trying fonts from 16 down to 14."""
    fonts = [
        (16, font_fact_16, 21),
        (15, font_fact_15, 19),
        (14, font_fact_14, 18),
    ]
    for size, font, line_h in fonts:
        if can_text_fit(draw, text, font, max_width, max_lines):
            lines = wrap_text_full(draw, text, font, max_width, max_lines)
            return lines, font, line_h
    # Fallback
    lines = wrap_text_full(draw, text, font_fact_14, max_width, max_lines)
    return lines, font_fact_14, 18

def clean_fact(text):
    """Remove trailing dangling & or , and ensure complete thought."""
    text = text.strip()
    # Remove trailing & or ,
    while text.endswith(('&', ',', ';')):
        text = text[:-1].strip()
    # If it ends mid-sentence without punctuation, find last comma/semicolon to end cleanly
    if text and text[-1] not in '.!?':
        last_comma = text.rfind(',')
        last_semi = text.rfind(';')
        cut = max(last_comma, last_semi)
        if cut > len(text) * 0.6:  # Only cut if we keep most of the text
            text = text[:cut].strip()
    return text

def shorten_headline(text):
    """Shorten headline by dropping trailing clauses at comma/colon, never mid-word."""
    # Pre-shortened headlines that fit well in 3 lines at 15pt within 165px
    replacements = {
        "COP31 in Antalya closes in on final climate deal after overtime": "COP31 Antalya closes in on final climate deal",
        "Iran attacks US bases in Bahrain; industrial site fire": "Iran attacks US bases in Bahrain; industrial site fire",
        "Saudi-led coalition intercepts Houthi missile and drone": "Saudi-led coalition intercepts Houthi missile and drone",
        "Russia double-tap strike on Kryvyi Rih kills two, wounds 60": "Russia double-tap strike on Kryvyi Rih; 2 dead, 60 hurt",
        "Russian missiles and drone land in Poland; NATO vows to defend every inch": "Russian missiles & drone land in Poland; NATO vows to defend",
        "FBI probes suspected hack of US criminal-justice database": "FBI probes hack of US criminal-justice database",
        "Trump proposes 10% cap on credit card interest rates": "Trump proposes 10% cap on credit card interest rates",
        "Anthropic IPO draws $120 billion retail demand": "Anthropic IPO draws $120B retail demand",
        "Voyager becomes first human-made object 1 light-day from Earth": "Voyager reaches 1 light-day from Earth",
        "ICJ finds evidence of Rohingya genocide; Myanmar rejects ruling": "ICJ finds Rohingya genocide; Myanmar rejects ruling",
        "Boat capsized in Nigeria's Bayelsa state, at least 24 dead": "Boat capsized in Nigeria Bayelsa; at least 24 dead",
        "Supercell storm devastates southern Brazil town, kills 3": "Supercell storm devastates S Brazil town; kills 3",
        "Australia chase record 188 to beat England in MCG T20 opener": "Australia chase 188 to beat England in MCG T20",
        "Dutch court bars BYD SUV in Europe over Defender resemblance": "Dutch court bars BYD SUV in Europe over Defender",
    }
    return replacements.get(text, text)

def get_symbol(headline, region):
    h = headline.lower()
    if "cop31" in h or "climate" in h: return "globe"
    if "iran" in h or "houthi" in h or "saudi" in h: return "missile"
    if "russia" in h or "kryvyi" in h: return "explosion"
    if "poland" in h or "nato" in h: return "shield"
    if "fbi" in h or "hack" in h or "database" in h: return "database"
    if "trump" in h or "credit" in h: return "money"
    if "anthropic" in h or "ipo" in h: return "chart"
    if "voyager" in h or "space" in h: return "rocket"
    if "icj" in h or "rohingya" in h or "genocide" in h: return "scale"
    if "boat" in h or "nigeria" in h or "capsized" in h: return "waves"
    if "storm" in h or "brazil" in h: return "storm"
    if "australia" in h or "cricket" in h or "t20" in h: return "cricket"
    if "byd" in h or "court" in h or "defender" in h: return "gavel"
    return "pin"

def draw_symbol(draw, cx, cy, symbol_type, color, size=32):
    s = size // 2
    if symbol_type == "globe":
        draw.ellipse([cx-s, cy-s, cx+s, cy+s], outline=color, width=2)
        draw.line([(cx, cy-s), (cx, cy+s)], fill=color, width=1)
        draw.line([(cx-s, cy), (cx+s, cy)], fill=color, width=1)
        draw.line([(cx-s*0.7, cy-s*0.7), (cx+s*0.7, cy+s*0.7)], fill=color, width=1)
    elif symbol_type == "missile":
        draw.line([(cx, cy-s), (cx, cy+s)], fill=color, width=3)
        draw.polygon([(cx, cy-s), (cx-4, cy-s+8), (cx+4, cy-s+8)], fill=color)
        draw.line([(cx-6, cy+2), (cx+6, cy-2)], fill=color, width=2)
    elif symbol_type == "explosion":
        import math
        for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
            rad = math.radians(angle)
            x1 = cx + int(s * 0.3 * math.cos(rad))
            y1 = cy + int(s * 0.3 * math.sin(rad))
            x2 = cx + int(s * math.cos(rad))
            y2 = cy + int(s * math.sin(rad))
            draw.line([(x1, y1), (x2, y2)], fill=color, width=2)
        draw.ellipse([cx-s//2, cy-s//2, cx+s//2, cy+s//2], outline=color, width=2)
    elif symbol_type == "shield":
        pts = [(cx, cy-s), (cx+s, cy-s//2), (cx+s, cy+s//2), (cx, cy+s), (cx-s, cy+s//2), (cx-s, cy-s//2)]
        draw.polygon(pts, outline=color, width=2)
        draw.line([(cx, cy-s//2), (cx, cy+s//2)], fill=color, width=1)
    elif symbol_type == "database":
        draw.ellipse([cx-s, cy-s//3, cx+s, cy+s//3], outline=color, width=2)
        draw.line([(cx-s, cy-s//3), (cx-s, cy+s//3*2)], fill=color, width=2)
        draw.line([(cx+s, cy-s//3), (cx+s, cy+s//3*2)], fill=color, width=2)
        draw.ellipse([cx-s, cy+s//3*2-s//3, cx+s, cy+s//3*2+s//3], outline=color, width=2)
    elif symbol_type == "money":
        draw.line([(cx, cy-s), (cx, cy+s)], fill=color, width=2)
        draw.line([(cx-s, cy-4), (cx+s, cy-4)], fill=color, width=2)
        draw.line([(cx-s, cy+4), (cx+s, cy+4)], fill=color, width=2)
        draw.text((cx-2, cy-1), "$", font=font_region, fill=color, anchor="mm")
    elif symbol_type == "chart":
        draw.line([(cx-s, cy+s), (cx-s, cy-s), (cx+s, cy-s)], fill=color, width=2)
        draw.line([(cx-s, cy+s), (cx+s, cy-s*0.5)], fill=color, width=2)
        draw.line([(cx-s, cy), (cx+s, cy*0.2)], fill=(180,180,180), width=1)
    elif symbol_type == "rocket":
        draw.line([(cx, cy-s), (cx, cy+s//2)], fill=color, width=3)
        draw.polygon([(cx-6, cy+s//2), (cx+6, cy+s//2), (cx, cy+s)], fill=color)
        draw.line([(cx-4, cy+s//2), (cx-8, cy+s)], fill=color, width=2)
        draw.line([(cx+4, cy+s//2), (cx+8, cy+s)], fill=color, width=2)
    elif symbol_type == "scale":
        draw.line([(cx-s, cy), (cx+s, cy)], fill=color, width=2)
        draw.line([(cx, cy-s), (cx, cy)], fill=color, width=2)
        draw.polygon([(cx-s, cy), (cx-s+4, cy-6), (cx-s-4, cy-6)], fill=color)
        draw.polygon([(cx+s, cy), (cx+s-4, cy-6), (cx+s+4, cy-6)], fill=color)
    elif symbol_type == "waves":
        for i in range(3):
            y_off = cy - s + i * (2*s//3)
            draw.line([(cx-s, y_off), (cx-s//2, y_off-4), (cx, y_off), (cx+s//2, y_off-4), (cx+s, y_off)], fill=color, width=2)
    elif symbol_type == "storm":
        draw.line([(cx, cy-s), (cx, cy)], fill=color, width=3)
        draw.line([(cx-6, cy), (cx+6, cy)], fill=color, width=3)
        for i in range(3):
            draw.line([(cx-8+i*4, cy+2), (cx-4+i*4, cy+8)], fill=color, width=2)
    elif symbol_type == "cricket":
        draw.ellipse([cx-s, cy, cx+s, cy+2*s], outline=color, width=2)
        draw.line([(cx, cy), (cx, cy-s)], fill=color, width=3)
        draw.line([(cx, cy-s), (cx-8, cy-s//2)], fill=color, width=2)
    elif symbol_type == "gavel":
        draw.rectangle([cx-2, cy-s, cx+2, cy+s//2], fill=color)
        draw.rectangle([cx-s*1.5, cy+s//2-4, cx+s*1.5, cy+s//2+4], fill=color)
    else:
        draw.ellipse([cx-s//2, cy-s//2, cx+s//2, cy+s//2], fill=color)

# Load stories
with open("/root/makefun/news-image-20261122/data-news.json") as f:
    raw_stories = json.load(f)

stories = []
for s in raw_stories:
    stories.append({
        "headline": shorten_headline(s["headline"]),
        "fact": clean_fact(s["summary_1line"]),
        "symbol": get_symbol(s["headline"], s["region"]),
        "region": s["region"],
    })

# Layout dimensions
masthead_h = 80
footer_h = 36
ticker_h = 36
margin_x = 16
margin_y = 8

# Draw masthead
draw_rounded_rect(draw, (0, 0, W, masthead_h), 0, fill=COLOR_MASTHEAD_BG)
title = "Sunday 22 November 2026 — The World in One Day"
bbox = draw.textbbox((0, 0), title, font=font_title)
title_w = bbox[2] - bbox[0]
if title_w > W - 80:
    font_title = load_font("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(36 * (W - 80) / title_w))
draw.text((W // 2, masthead_h // 2), title, font=font_title, fill=COLOR_MASTHEAD_TEXT, anchor="mm")
draw.line([(80, masthead_h - 8), (W - 80, masthead_h - 8)], fill=(255, 255, 255, 100), width=2)

# Available space for cards
cards_top = masthead_h + 10
cards_bottom = H - footer_h - ticker_h - 10
cards_height = cards_bottom - cards_top

# Grid: 3 rows (5, 5, 4)
row_counts = [5, 5, 4]
num_rows = len(row_counts)
row_h = cards_height // num_rows

card_index = 0
for row_idx, num_cards in enumerate(row_counts):
    row_y = cards_top + row_idx * row_h
    total_gap = margin_x * (num_cards - 1)
    card_w = (W - 2 * margin_x - total_gap) // num_cards
    card_h = row_h - margin_y
    
    for col_idx in range(num_cards):
        if card_index >= len(stories):
            break
        story = stories[card_index]
        x = margin_x + col_idx * (card_w + margin_x)
        y = row_y
        
        # Card background
        draw_rounded_rect(draw, (x, y, x + card_w, y + card_h), 8,
                          fill=COLOR_CARD_BG, outline=COLOR_BORDER, width=1)
        
        pad = 10
        inner_x = x + pad
        inner_y = y + pad
        inner_w = card_w - 2 * pad
        inner_h = card_h - 2 * pad
        
        region = story["region"]
        rcolor = REGION_COLORS.get(region, (100, 100, 100))
        
        # Region tag (top-left)
        tag_text = region
        bbox = draw.textbbox((0, 0), tag_text, font=font_region)
        tag_w = min(bbox[2] - bbox[0] + 16, inner_w - 40)
        tag_h = 18
        draw_rounded_rect(draw, (inner_x, inner_y, inner_x + tag_w, inner_y + tag_h), 4, fill=rcolor)
        draw.text((inner_x + tag_w // 2, inner_y + tag_h // 2), tag_text, font=font_region, fill=(255,255,255), anchor="mm")
        
        # Symbol (top-right) - larger 32px
        sym_size = 32
        sym_x = x + card_w - pad - sym_size // 2
        sym_y = y + pad + tag_h // 2
        draw_symbol(draw, sym_x, sym_y, story["symbol"], rcolor, size=sym_size)
        
        # Headline area - starts below tag
        headline_y = inner_y + tag_h + 6
        headline_max_w = inner_w
        
        # Fit headline in up to 3 lines, shrinking font from 18 down to 15
        headline_lines, used_font, line_h = fit_headline(draw, story["headline"], headline_max_w, 3)
        
        # Draw headline
        for li, line in enumerate(headline_lines):
            draw.text((inner_x, headline_y + li * line_h), line, font=used_font, fill=COLOR_TEXT)
        
        # Fact area - use remaining space, up to 6 lines
        fact_y = headline_y + len(headline_lines) * line_h + 4
        fact_max_h = inner_y + inner_h - fact_y
        max_fact_lines = min(6, max(2, fact_max_h // 20))
        
        # Fit fact in available lines, font 16 down to 14
        fact_lines, fact_font, fact_line_h = fit_fact(draw, story["fact"], headline_max_w, max_fact_lines)
        
        for li, line in enumerate(fact_lines):
            draw.text((inner_x, fact_y + li * fact_line_h), line, font=fact_font, fill=COLOR_TEXT_MUTED)
        
        card_index += 1

# Ticker band: "ALSO TODAY" + 4 one-liners
ticker_y = H - footer_h - ticker_h
draw_rounded_rect(draw, (0, ticker_y, W, ticker_y + ticker_h), 0, fill=COLOR_TICKER_BG)

ticker_items = [
    "Belgium national strike to shut airspace Monday",
    "Bangladesh PM blames India for fresh unrest",
    "Antonsen ends Sen's 13-match streak, Hong Kong Open",
    "Nebraska ends 31-game top-25 drought, beats Ohio State"
]

label = "ALSO TODAY"
label_bbox = draw.textbbox((0, 0), label, font=font_ticker)
label_w = label_bbox[2] - label_bbox[0]
label_x = 20
label_y = ticker_y + ticker_h // 2
draw.text((label_x, label_y), label, font=font_ticker, fill=COLOR_TICKER_LABEL, anchor="lm")

# Items to the right of label
items_text = " · ".join(ticker_items)
items_x = label_x + label_w + 16
items_max_w = W - items_x - 20

# Fit items in one line
if can_text_fit(draw, items_text, font_ticker_text, items_max_w, 1):
    items_lines = wrap_text_full(draw, items_text, font_ticker_text, items_max_w, 1)
    draw.text((items_x, label_y), items_lines[0], font=font_ticker_text, fill=COLOR_TICKER_TEXT, anchor="lm")

# Footer
footer_y = H - footer_h
draw_rounded_rect(draw, (0, footer_y, W, H), 0, fill=COLOR_FOOTER_BG)
footer_text = "Sources: Reuters, Al Jazeera, AP, SBS · make.fun news-image-20261122"
draw.text((W // 2, footer_y + footer_h // 2), footer_text, font=font_footer, fill=COLOR_TEXT_MUTED, anchor="mm")

# Save
img.save("/root/makefun/news-image-20261122/entry.png", "PNG", optimize=True)
print("Saved entry.png")
