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
    font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
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

def draw_symbol(draw, cx, cy, symbol_type, color, size=20):
    """Draw a simple symbolic icon for each story type."""
    s = size // 2
    
    if symbol_type == "globe":  # COP31 / Global
        draw.ellipse([cx-s, cy-s, cx+s, cy+s], outline=color, width=2)
        draw.line([(cx, cy-s), (cx, cy+s)], fill=color, width=1)
        draw.line([(cx-s, cy), (cx+s, cy)], fill=color, width=1)
        draw.line([(cx-s*0.7, cy-s*0.7), (cx+s*0.7, cy+s*0.7)], fill=color, width=1)
        draw.line([(cx+s*0.7, cy-s*0.7), (cx-s*0.7, cy+s*0.7)], fill=color, width=1)
    
    elif symbol_type == "missile":  # Iran/Israel/Poland strikes
        draw.line([(cx, cy-s), (cx, cy+s//2)], fill=color, width=2)
        draw.polygon([(cx, cy-s), (cx-4, cy-s+6), (cx+4, cy-s+6)], fill=color)
        draw.line([(cx-3, cy+s//2), (cx-6, cy+s)], fill=color, width=1)
        draw.line([(cx+3, cy+s//2), (cx+6, cy+s)], fill=color, width=1)
    
    elif symbol_type == "flame":  # Fire/industrial site
        draw.polygon([(cx, cy-s), (cx-s//2, cy+s//2), (cx, cy), (cx+s//2, cy+s//2)], fill=color)
        draw.polygon([(cx, cy-s//2), (cx-s//3, cy), (cx, cy-s//4), (cx+s//3, cy)], fill=(255, 160, 0))
    
    elif symbol_type == "chart":  # Economy/IPO
        points = [(cx-s, cy+s), (cx-s//2, cy), (cx, cy+s//2), (cx+s//2, cy-s//2), (cx+s, cy-s)]
        draw.line(points, fill=color, width=2)
        for px, py in points:
            draw.ellipse([px-1, py-1, px+1, py+1], fill=color)
    
    elif symbol_type == "scales":  # ICJ / Justice
        draw.line([(cx-s, cy+s), (cx+s, cy+s)], fill=color, width=1)
        draw.line([(cx, cy+s), (cx, cy)], fill=color, width=1)
        draw.line([(cx-s, cy), (cx-s, cy-s)], fill=color, width=1)
        draw.line([(cx-s-5, cy-s), (cx-s+5, cy-s)], fill=color, width=1)
        draw.line([(cx+s, cy), (cx+s, cy-s)], fill=color, width=1)
        draw.line([(cx+s-5, cy-s), (cx+s+5, cy-s)], fill=color, width=1)
    
    elif symbol_type == "satellite":  # Voyager
        draw.ellipse([cx-6, cy-3, cx+6, cy+3], outline=color, width=1)
        draw.line([(cx-10, cy), (cx-6, cy)], fill=color, width=1)
        draw.line([(cx+6, cy), (cx+10, cy)], fill=color, width=1)
        draw.line([(cx, cy-8), (cx, cy-3)], fill=color, width=1)
        draw.line([(cx, cy+3), (cx, cy+8)], fill=color, width=1)
        draw.line([(cx, cy-3), (cx, cy-11)], fill=color, width=1)
        draw.ellipse([cx-2, cy-13, cx+2, cy-11], fill=color)
    
    elif symbol_type == "database":  # FBI database
        draw.rectangle([cx-s, cy-s//2, cx+s, cy+s//2], outline=color, width=1)
        draw.ellipse([cx-s, cy-s//2-3, cx+s, cy-s//2+3], outline=color, width=1)
        draw.ellipse([cx-s, cy+s//2-3, cx+s, cy+s//2+3], outline=color, width=1)
        draw.line([(cx-s, cy-s//2), (cx-s, cy+s//2)], fill=color, width=1)
        draw.line([(cx+s, cy-s//2), (cx+s, cy+s//2)], fill=color, width=1)
    
    elif symbol_type == "card":  # Credit card
        draw.rounded_rectangle([cx-s, cy-s//2, cx+s, cy+s//2], radius=2, outline=color, width=1)
        draw.line([(cx-s+4, cy-s//2+4), (cx+s-4, cy-s//2+4)], fill=color, width=1)
        draw.line([(cx-s+4, cy), (cx+s-4, cy)], fill=color, width=1)
    
    elif symbol_type == "boat":  # Nigeria boat
        draw.polygon([(cx-s, cy+s//2), (cx-s//2, cy+s), (cx+s//2, cy+s), (cx+s, cy+s//2), (cx+s//2, cy), (cx-s//2, cy)], outline=color, width=1)
        draw.line([(cx, cy), (cx, cy-s)], fill=color, width=1)
        draw.line([(cx, cy-s), (cx+6, cy-s//2)], fill=color, width=1)
        draw.line([(cx, cy-s), (cx-6, cy-s//2)], fill=color, width=1)
    
    elif symbol_type == "wave":  # Supercell storm
        for i in range(3):
            y_off = cy - s + i * (s * 2 // 3)
            draw.line([(cx-s, y_off), (cx-s//2, y_off-s//3), (cx, y_off), (cx+s//2, y_off-s//3), (cx+s, y_off)], fill=color, width=1)
        draw.line([(cx, cy-s), (cx, cy+s)], fill=color, width=1)
    
    elif symbol_type == "cricket":  # Cricket bat and ball
        draw.line([(cx-s, cy+s//2), (cx+s//2, cy-s)], fill=color, width=2)
        draw.ellipse([cx+s//2-4, cy-s-4, cx+s//2+4, cy-s+4], outline=color, width=1)
        draw.line([(cx+s//2-3, cy-s-3), (cx+s//2+3, cy-s+3)], fill=color, width=1)
        draw.line([(cx+s//2-3, cy-s+3), (cx+s//2+3, cy-s-3)], fill=color, width=1)
    
    elif symbol_type == "gavel":  # Court ruling / BYD
        draw.rectangle([cx-s//2, cy-s, cx+s//2, cy+s//2], fill=color)
        draw.line([(cx-s, cy+s//2), (cx+s, cy+s//2)], fill=color, width=2)
        draw.line([(cx-s, cy+s//2+3), (cx+s, cy+s//2+3)], fill=color, width=1)
    
    elif symbol_type == "car":  # Car outline / BYD SUV
        draw.line([(cx-s, cy+s//2), (cx-s, cy)], fill=color, width=1)
        draw.line([(cx-s, cy), (cx-s//2, cy-s//2)], fill=color, width=1)
        draw.line([(cx-s//2, cy-s//2), (cx+s//2, cy-s//2)], fill=color, width=1)
        draw.line([(cx+s//2, cy-s//2), (cx+s, cy)], fill=color, width=1)
        draw.line([(cx+s, cy), (cx+s, cy+s//2)], fill=color, width=1)
        draw.ellipse([cx-s//2-3, cy+s//2-3, cx-s//2+3, cy+s//2+3], outline=color, width=1)
        draw.ellipse([cx+s//2-3, cy+s//2-3, cx+s//2+3, cy+s//2+3], outline=color, width=1)

# --- MAIN DRAWING ---

# 1. Masthead
masthead_h = draw_masthead()

# 2. Load stories from JSON
with open("/root/makefun/news-image-20261122/data-news.json", "r") as f:
    raw_stories = json.load(f)

# Map each story to our format with short headlines and symbols
symbol_map = {
    "Global": "globe",
    "Middle East": "missile",
    "Europe": "missile",
    "Americas": "flame",
    "Economy": "chart",
    "Science": "satellite",
    "Asia": "scales",
    "Africa": "boat",
    "Sport": "cricket",
}

# Custom symbol overrides for specific stories
def get_symbol(headline, region):
    h = headline.lower()
    if "cop31" in h or "climate" in h:
        return "globe"
    if "iran" in h and ("strike" in h or "attack" in h or "missile" in h):
        return "missile"
    if "saudi" in h or "houthi" in h:
        return "missile"
    if "kryvyi" in h or "zelensky" in h:
        return "missile"
    if "poland" in h or ("missile" in h and "nato" in h):
        return "missile"
    if "fbi" in h or "database" in h or "hack" in h:
        return "database"
    if "trump" in h or "credit" in h or "card" in h:
        return "card"
    if "anthropic" in h or "ipo" in h:
        return "chart"
    if "voyager" in h:
        return "satellite"
    if "icj" in h or "rohingya" in h or "genocide" in h:
        return "scales"
    if "boat" in h or "capsize" in h or "nigeria" in h:
        return "boat"
    if "supercell" in h or "storm" in h or "brazil" in h:
        return "wave"
    if "australia" in h or "cricket" in h or "mcg" in h or "t20" in h:
        return "cricket"
    if "dutch" in h or "court" in h or "byd" in h:
        return "gavel"
    return symbol_map.get(region, "globe")

# Short headlines (max ~35 chars for legibility)
def shorten_headline(h):
    replacements = {
        "COP31 in Antalya closes in on final climate deal after overtime": "COP31 Antalya: Final Climate Deal",
        "Iran attacks US bases in Bahrain; industrial site fire": "Iran Strikes US Bases in Bahrain",
        "Saudi-led coalition intercepts Houthi missile and drone": "Saudi Coalition Downs Houthi Missile",
        "Russia double-tap strike on Kryvyi Rih kills two, wounds 60": "Russia Hits Kryvyi Rih, Kills 2",
        "Russian missiles and drone land in Poland; NATO vows to defend every inch": "Russian Missiles Land in Poland",
        "FBI probes suspected hack of US criminal-justice database": "FBI Probes Justice Database Hack",
        "Trump proposes 10% cap on credit card interest rates": "Trump Backs 10% Credit-Card Cap",
        "Anthropic IPO draws $120 billion retail demand": "Anthropic IPO Draws $120B Demand",
        "Voyager becomes first human-made object 1 light-day from Earth": "Voyager Reaches 1 Light-Day Out",
        "ICJ finds evidence of Rohingya genocide; Myanmar rejects ruling": "ICJ Finds Rohingya Genocide",
        "Boat capsized in Nigeria's Bayelsa state, at least 24 dead": "Nigeria Boat Capsize Kills 24+",
        "Supercell storm devastates southern Brazil town, kills 3": "Supercell Storm Hits S. Brazil",
        "Australia chase record 188 to beat England in MCG T20 opener": "Australia Chase 188 to Beat England",
        "Dutch court bars BYD SUV in Europe over Defender resemblance": "Dutch Court Bars BYD SUV in EU",
    }
    return replacements.get(h, h[:40])

# Short facts (one line, wrapped to max 3 lines)
def shorten_fact(f):
    replacements = {
        "Nearly 200 countries at COP31 in Antalya negotiated a third and 'final' text into Sunday morning after drafts stripped of fossil-fuel language drew threats of walkout, with a closing plenary set for later Sunday.": "Nearly 200 nations reach final deal after overnight talks",
        "Iran's IRGC claimed missile-and-drone attacks on two US bases in Bahrain (Sheikh Isa and Juffair), and Bahrain said a civilian industrial facility on Sitra Island was hit and set on fire, with no injuries reported.": "Missile & drone attacks on 2 US bases; industrial fire on Sitra",
        "The Saudi-led coalition intercepted a ballistic missile and a drone launched toward western Saudi Arabia and Riyadh as Houthi attacks on Taiz killed one and wounded seven, deepening Gulf escalation.": "Ballistic missile & drone intercepted; Taiz attacks kill 1, wound 7",
        "Ballistic missiles and follow-up drone strikes on Zelensky's hometown Kryvyi Rih killed a 7-year-old boy and a 20-year-old paramedic and wounded 60, part of a barrage of 27 ballistic missiles, 84 cruise missiles and 404 drones.": "Double-tap strike kills 2 (incl. child), wounds 60; huge barrage",
        "A Kh-101 cruise missile, a second missile and a jet-powered drone fell in southeastern Poland near Coalition-of-the-Willing exercises; Tusk called it an intentional provocation and NATO chief Rutte pledged 'NATO will defend every inch of Polish territory'.": "Kh-101 & drone fall in SE Poland; NATO pledges defense",
        "The FBI is investigating a suspected breach of the nationwide database used by federal, state and local law enforcement to share warrants, criminal histories and background checks.": "Suspected breach of nationwide criminal-history & warrant system",
        "President Trump said he would back a 10% cap on credit card interest rates with Democrats' support, and again criticised the Federal Reserve's rate policy, citing India's 7% growth.": "Proposes 10% cap with Dem support; criticizes Fed policy",
        "Anthropic's share sale attracted about $120 billion in retail demand and over $500 billion institutional interest, even as the stock fell nearly 15% on Friday; an Anthropic mathematician separately claimed Claude helped solve the Riemann hypothesis.": "$120B retail, $500B+ institutional demand; stock down ~15%",
        "Forty-nine years after launch, NASA's Voyager spacecraft became the first human-made object to sit one light-day away from Earth, a milestone in deep-space exploration.": "First human-made object at 1 light-day (25.9B km), 49 yrs after launch",
        "The International Court of Justice found Myanmar's forces committed genocide against the Rohingya, targeting 800,000 people and killing about 10,000; Myanmar called the verdict unfair while Malaysia moves to resettle 10,000 Rohingya.": "Myanmar forces targeted 800K, killed ~10K; Myanmar rejects verdict",
        "A boat carrying mourners to a burial ceremony capsized in Nigeria's Bayelsa state, killing at least 24 people; 24 others were rescued and the operator fled the scene, police said.": "Mourners' boat capsizes in Bayelsa; 24 dead, 24 rescued, operator flees",
        "A supercell storm with 114 kmph winds tore through Tupanciretã in Rio Grande do Sul, killing three, injuring 162 and damaging around 8,000 homes, forcing nearly all of the town's 20,000 residents to leave.": "114 km/h winds hit Tupanciretã; 3 dead, 162 hurt, 8K homes damaged",
        "Australia beat world number one England by three wickets in the first T20 at the Melbourne Cricket Ground, completing the highest successful run chase at the ground and ending England's seven-match winning streak.": "Record 188 chase at MCG ends England's 7-match streak; Aus win by 3 wkts",
        "The Hague court ruled BYD's Fangchengbao Ti7 infringes the EU design of JLR's Defender, barring its sale in Europe and production at BYD's planned Hungary plant pending resolution.": "Hague rules Ti7 infringes Defender design; bars EU sale & Hungary production",
    }
    return replacements.get(f, f[:120])

stories = []
for s in raw_stories:
    stories.append({
        "headline": shorten_headline(s["headline"]),
        "fact": shorten_fact(s["summary_1line"]),
        "symbol": get_symbol(s["headline"], s["region"]),
        "region": s["region"],
    })

# 3. Card layout - 4 columns x 4 rows = 16 slots (fits all 14)
card_w = 231
card_h = 195
margin_x = 20
margin_y = 15
start_y = masthead_h + 15
cols = 4

print(f"Drawing {len(stories)} cards in {cols} columns...")

for i, story in enumerate(stories):
    col = i % cols
    row = i // cols
    x = margin_x + col * (card_w + margin_x)
    y = start_y + row * (card_h + margin_y)
    
    # Ensure we don't go off canvas
    if y + card_h > H - 10:
        print(f"Warning: card {i} at row {row} would overflow")
        continue
    
    # Card background
    draw_rounded_rect(draw, (x, y, x + card_w, y + card_h), 8, 
                      fill=COLOR_CARD_BG, outline=COLOR_BORDER, width=1)
    
    # Region tag (top-left)
    region = story["region"]
    rcolor = REGION_COLORS.get(region, (100, 100, 100))
    tag_w = 70
    tag_h = 18
    draw_rounded_rect(draw, (x + 8, y + 8, x + 8 + tag_w, y + 8 + tag_h), 4,
                      fill=rcolor)
    draw.text((x + 8 + tag_w//2, y + 17), region, font=font_region, fill=(255,255,255), anchor="mm")
    
    # Symbol (top-right)
    sym_x = x + card_w - 22
    sym_y = y + 26
    draw_symbol(draw, sym_x, sym_y, story["symbol"], rcolor, size=24)
    
    # Headline
    draw.text((x + 12, y + 38), story["headline"], font=font_headline, fill=COLOR_TEXT)
    
    # Fact (wrapped to max 3 lines)
    fact = story["fact"]
    words = fact.split()
    lines = []
    current = ""
    for w in words:
        test = current + (" " if current else "") + w
        bbox = draw.textbbox((0,0), test, font=font_body)
        if bbox[2] - bbox[0] <= card_w - 24:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    
    for li, line in enumerate(lines[:3]):  # Max 3 lines
        draw.text((x + 12, y + 65 + li * 18), line, font=font_body, fill=COLOR_TEXT_MUTED)

# Save
img.save("/root/makefun/news-image-20261122/entry.png", "PNG", optimize=True)
print("Saved entry.png")
