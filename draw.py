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
    font_headline_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
    font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
    font_region = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 10)
    font_footer = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
except:
    font_title = ImageFont.load_default()
    font_headline = ImageFont.load_default()
    font_headline_small = ImageFont.load_default()
    font_body = ImageFont.load_default()
    font_small = ImageFont.load_default()
    font_region = ImageFont.load_default()
    font_footer = ImageFont.load_default()

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
COLOR_FOOTER_BG = (230, 230, 230)

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

def wrap_text(draw, text, font, max_width, max_lines=2):
    """Wrap text to fit within max_width, up to max_lines.
    Returns list of lines."""
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
                    break
            current = w
    
    if current and len(lines) < max_lines:
        lines.append(current)
    
    # If we still have more words but no more lines, truncate last line
    if len(lines) >= max_lines and current and current != lines[-1]:
        # Try to fit as much as possible on last line with ellipsis
        last_line = lines[-1]
        while last_line:
            test = last_line + "…"
            bbox = draw.textbbox((0, 0), test, font=font)
            if bbox[2] - bbox[0] <= max_width:
                lines[-1] = test
                break
            last_line = last_line[:-1]
    
    return lines

def draw_masthead():
    """Draw the top masthead with date, centered with margins."""
    masthead_h = 90
    draw_rounded_rect(draw, (0, 0, W, masthead_h), 0, fill=COLOR_MASTHEAD_BG)
    
    # Title - measure and ensure it fits with margins
    title = "Sunday 22 November 2026 — The World in One Day"
    margin = 40
    max_width = W - 2 * margin
    
    # Try current font, if too wide reduce size
    bbox = draw.textbbox((0, 0), title, font=font_title)
    title_w = bbox[2] - bbox[0]
    
    if title_w > max_width:
        # Reduce font size
        font_size = 36 * max_width // title_w
        if font_size < 20:
            font_size = 20
        try:
            font_title_sized = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font_title_sized = ImageFont.load_default()
    else:
        font_title_sized = font_title
    
    # Draw centered
    draw.text((W // 2, 32), title, font=font_title_sized, fill=COLOR_MASTHEAD_TEXT, anchor="mm")
    
    # Decorative line
    draw.line([(100, 70), (W - 100, 70)], fill=(255, 255, 255, 100), width=2)
    
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
        draw.line([(cx, cy-s//2), (cx, cy+s//2)], fill=color, width=1)
    
    elif symbol_type == "boat":  # Nigeria boat
        draw.polygon([(cx-s, cy+s//2), (cx-s//2, cy-s//2), (cx+s//2, cy-s//2), (cx+s, cy+s//2)], fill=color)
        draw.line([(cx-s//2, cy-s//2), (cx-s//2, cy-s)], fill=color, width=2)
    
    elif symbol_type == "storm":  # Brazil storm
        draw.polygon([(cx, cy-s), (cx-s//2, cy), (cx, cy-s//3), (cx+s//2, cy)], fill=color)
        draw.line([(cx-s, cy+s//3), (cx+s, cy+s//3)], fill=color, width=1)
        draw.line([(cx-s//2, cy+s//2), (cx+s//2, cy+s//2)], fill=color, width=1)
    
    elif symbol_type == "cricket":  # Australia cricket
        draw.line([(cx-s, cy), (cx+s, cy)], fill=color, width=2)
        draw.line([(cx, cy-s), (cx, cy+s)], fill=color, width=2)
        draw.ellipse([cx-3, cy-3, cx+3, cy+3], outline=color, width=1)
    
    elif symbol_type == "car":  # BYD car
        draw.rectangle([cx-s, cy, cx+s, cy+s//2], outline=color, width=1)
        draw.ellipse([cx-s-2, cy+s//2-2, cx-s+2, cy+s//2+2], fill=color)
        draw.ellipse([cx+s-2, cy+s//2-2, cx+s+2, cy+s//2+2], fill=color)
    
    else:
        # Default: circle
        draw.ellipse([cx-s, cy-s, cx+s, cy+s], outline=color, width=2)

def get_symbol(headline, region):
    """Map story to symbol type."""
    h = headline.lower()
    if "cop31" in h or "climate" in h:
        return "globe"
    elif "iran" in h and ("base" in h or "missile" in h or "drone" in h):
        return "missile"
    elif "houthi" in h or "saudi" in h:
        return "missile"
    elif "russia" in h and "kryvyi" in h:
        return "missile"
    elif "russia" in h and "poland" in h:
        return "missile"
    elif "fbi" in h or "database" in h:
        return "database"
    elif "trump" in h or "credit card" in h:
        return "chart"
    elif "anthropic" in h or "ipo" in h:
        return "chart"
    elif "voyager" in h:
        return "satellite"
    elif "icj" in h or "rohingya" in h or "genocide" in h:
        return "scales"
    elif "boat" in h or "capsized" in h or "nigeria" in h:
        return "boat"
    elif "storm" in h or "brazil" in h or "tupanciret" in h:
        return "storm"
    elif "australia" in h or "cricket" in h or "england" in h:
        return "cricket"
    elif "byd" in h or "defender" in h:
        return "car"
    elif region == "Global":
        return "globe"
    elif region == "Middle East":
        return "missile"
    elif region == "Europe":
        return "missile"
    elif region == "Americas":
        return "chart"
    elif region == "Economy":
        return "chart"
    elif region == "Science":
        return "satellite"
    elif region == "Asia":
        return "scales"
    elif region == "Africa":
        return "boat"
    elif region == "Sport":
        return "cricket"
    return "globe"

def shorten_headline(h):
    """Shorten long headlines to reasonable length."""
    replacements = {
        "COP31 in Antalya closes in on final climate deal after overtime": "COP31 Antalya: Final Climate Deal Near After Overtime",
        "Iran attacks US bases in Bahrain; industrial site fire": "Iran Strikes US Bases in Bahrain; Industrial Site Fire",
        "Saudi-led coalition intercepts Houthi missile and drone": "Saudi Coalition Intercepts Houthi Missile & Drone",
        "Russia double-tap strike on Kryvyi Rih kills two, wounds 60": "Russia Double-Tap Strike on Kryvyi Rih: 2 Dead, 60 Hurt",
        "Russian missiles and drone land in Poland; NATO vows to defend every inch": "Russian Missiles & Drone Land in Poland; NATO Vows Defense",
        "FBI probes suspected hack of US criminal-justice database": "FBI Probes Suspected Hack of US Criminal-Justice Database",
        "Trump proposes 10% cap on credit card interest rates": "Trump Proposes 10% Cap on Credit Card Rates",
        "Anthropic IPO draws $120 billion retail demand": "Anthropic IPO Draws $120B Retail Demand",
        "Voyager becomes first human-made object 1 light-day from Earth": "Voyager Reaches 1 Light-Day from Earth",
        "ICJ finds evidence of Rohingya genocide; Myanmar rejects ruling": "ICJ Finds Rohingya Genocide; Myanmar Rejects Ruling",
        "Boat capsized in Nigeria's Bayelsa state, at least 24 dead": "Boat Capsizes in Bayelsa, Nigeria: 24 Dead",
        "Supercell storm devastates southern Brazil town, kills 3": "Supercell Storm Devastates Tupanciretã, Brazil: 3 Dead",
        "Australia chase record 188 to beat England in MCG T20 opener": "Australia Chase Record 188 to Beat England at MCG",
        "Dutch court bars BYD SUV in Europe over Defender resemblance": "Dutch Court Bars BYD SUV in Europe Over Defender Design",
    }
    return replacements.get(h, h)

def shorten_fact(f):
    """Shorten fact to one line."""
    replacements = {
        "Nearly 200 countries at COP31 in Antalya negotiated a third and 'final' text into Sunday morning after drafts stripped of fossil-fuel language drew threats of walkout, with a closing plenary set for later Sunday.": "Nearly 200 nations near final text after fossil-fuel walkout threats",
        "Iran's IRGC claimed missile-and-drone attacks on two US bases in Bahrain (Sheikh Isa and Juffair), and Bahrain said a civilian industrial facility on Sitra Island was hit and set on fire, with no injuries reported.": "IRGC claims missile/drone strikes on 2 US bases; Sitra facility hit",
        "The Saudi-led coalition intercepted a ballistic missile and a drone launched toward western Saudi Arabia and Riyadh as Houthi attacks on Taiz killed one and wounded seven, deepening Gulf escalation.": "Saudi intercepts Houthi missile/drone; Taiz attack kills 1, wounds 7",
        "Ballistic missiles and follow-up drone strikes on Zelensky's hometown Kryvyi Rih killed a 7-year-old boy and a 20-year-old paramedic and wounded 60, part of a barrage of 27 ballistic missiles, 84 cruise missiles and 404 drones.": "Missiles/drones hit Zelensky's hometown; boy (7) & paramedic (20) killed, 60 hurt",
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

# Load stories
with open("/root/makefun/news-image-20261122/data-news.json") as f:
    raw_stories = json.load(f)

stories = []
for s in raw_stories:
    stories.append({
        "headline": shorten_headline(s["headline"]),
        "fact": shorten_fact(s["summary_1line"]),
        "symbol": get_symbol(s["headline"], s["region"]),
        "region": s["region"],
    })

# Grid layout: 14 cards, arranged to fill canvas evenly
# Use 3 rows: 5, 5, 4 cards - stretch to full width
masthead_h = draw_masthead()

# Footer area
footer_h = 40
footer_y = H - footer_h

# Available area for cards
available_top = masthead_h + 15
available_bottom = footer_y - 15
available_height = available_bottom - available_top

# Grid configuration
row_counts = [5, 5, 4]  # 14 cards in 3 rows
num_rows = len(row_counts)
row_height = available_height // num_rows

margin_x = 20
margin_y = 10

card_index = 0
for row_idx, num_cards in enumerate(row_counts):
    row_y = available_top + row_idx * (row_height + margin_y)
    
    # Calculate card width for this row (stretch to fill width)
    total_gap = margin_x * (num_cards - 1)
    card_w = (W - 2 * margin_x - total_gap) // num_cards
    card_h = row_height
    
    for col_idx in range(num_cards):
        if card_index >= len(stories):
            break
        
        story = stories[card_index]
        x = margin_x + col_idx * (card_w + margin_x)
        y = row_y
        
        # Card background
        draw_rounded_rect(draw, (x, y, x + card_w, y + card_h), 8, 
                          fill=COLOR_CARD_BG, outline=COLOR_BORDER, width=1)
        
        # Card inner padding
        pad = 12
        inner_x = x + pad
        inner_y = y + pad
        inner_w = card_w - 2 * pad
        inner_h = card_h - 2 * pad
        
        # Region tag (top-left)
        region = story["region"]
        rcolor = REGION_COLORS.get(region, (100, 100, 100))
        tag_w = min(90, inner_w - 40)  # Ensure tag doesn't exceed card
        tag_h = 20
        draw_rounded_rect(draw, (inner_x, inner_y, inner_x + tag_w, inner_y + tag_h), 4,
                          fill=rcolor)
        draw.text((inner_x + tag_w // 2, inner_y + tag_h // 2), region, font=font_region, fill=(255,255,255), anchor="mm")
        
        # Symbol (top-right) - ensure it stays within card
        sym_size = 20
        sym_x = x + card_w - pad - sym_size // 2
        sym_y = y + pad + sym_size // 2 + 4
        draw_symbol(draw, sym_x, sym_y, story["symbol"], rcolor, size=sym_size)
        
        # Headline - wrap to fit card width (max 2 lines)
        headline_y = inner_y + tag_h + 8
        headline_max_w = inner_w
        
        # Try regular headline font first
        headline_lines = wrap_text(draw, story["headline"], font_headline, headline_max_w, max_lines=2)
        
        # If too many lines or text still too wide, try smaller font
        if len(headline_lines) > 2:
            headline_lines = wrap_text(draw, story["headline"], font_headline_small, headline_max_w, max_lines=2)
        
        # Draw headline lines
        line_height = 20
        for li, line in enumerate(headline_lines):
            draw.text((inner_x, headline_y + li * line_height), line, font=font_headline if len(headline_lines) <= 1 else font_headline_small, fill=COLOR_TEXT)
        
        # Fact - wrap to fit card width (max 3 lines, but fit in remaining space)
        fact_y = headline_y + len(headline_lines) * line_height + 6
        fact_max_w = inner_w
        fact_lines = wrap_text(draw, story["fact"], font_body, fact_max_w, max_lines=3)
        
        # Limit lines to fit in card
        max_fact_lines = max(1, (inner_h - (fact_y - inner_y)) // 16)
        fact_lines = fact_lines[:max_fact_lines]
        
        for li, line in enumerate(fact_lines):
            draw.text((inner_x, fact_y + li * 16), line, font=font_body, fill=COLOR_TEXT_MUTED)
        
        card_index += 1

# Draw footer
draw_rounded_rect(draw, (0, footer_y, W, H), 0, fill=COLOR_FOOTER_BG)
footer_text = "Sources: Reuters, Al Jazeera, AP, SBS · make.fun news-image-20261122"
draw.text((W // 2, footer_y + footer_h // 2), footer_text, font=font_footer, fill=COLOR_TEXT_MUTED, anchor="mm")

# Save
img.save("/root/makefun/news-image-20261122/entry.png", "PNG", optimize=True)
print("Saved entry.png")
