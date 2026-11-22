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
    font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
    font_headline = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
    font_headline_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13)
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

def wrap_text(text, font, max_width, draw_obj, max_lines=2):
    """Wrap text to fit within max_width, up to max_lines."""
    words = text.split()
    lines = []
    current = ""
    
    for w in words:
        test = current + (" " if current else "") + w
        bbox = draw_obj.textbbox((0, 0), test, font=font)
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
    
    # If we still have more words and hit max_lines, truncate last line with ellipsis
    if len(lines) == max_lines and current and current != lines[-1]:
        # Try to fit ellipsis
        last = lines[-1]
        while last and draw_obj.textbbox((0, 0), last + "…", font=font)[2] > max_width:
            last = last[:-1]
        lines[-1] = last + "…"
    
    return lines

def draw_masthead():
    """Draw the top masthead with date, centered with margins."""
    masthead_h = 90
    draw_rounded_rect(draw, (0, 0, W, masthead_h), 0, fill=COLOR_MASTHEAD_BG)
    
    # Title - measure and center with 40px margins on each side
    title = "Sunday 22 November 2026 — The World in One Day"
    max_title_width = W - 80  # 40px margins
    
    # If too wide, reduce font size (but we pre-sized to 32 which should fit)
    bbox = draw.textbbox((0, 0), title, font=font_title)
    title_w = bbox[2] - bbox[0]
    
    if title_w > max_title_width:
        # Shouldn't happen with font size 32, but fallback
        draw.text((W//2, 32), title, font=font_title, fill=COLOR_MASTHEAD_TEXT, anchor="mm")
    else:
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
    
    elif symbol_type == "gavel":  # Court/ICJ
        draw.rectangle([cx-2, cy-s, cx+2, cy], fill=color)
        draw.rectangle([cx-8, cy-s-4, cx+8, cy-s], fill=color)
    
    elif symbol_type == "boat":  # Nigeria boat
        draw.line([(cx-s, cy+s//2), (cx+s, cy+s//2)], fill=color, width=2)
        draw.line([(cx-s, cy+s//2), (cx-s//2, cy-s//2)], fill=color, width=2)
        draw.line([(cx+s, cy+s//2), (cx+s//2, cy-s//2)], fill=color, width=2)
    
    elif symbol_type == "storm":  # Brazil storm
        draw.line([(cx-s, cy-s), (cx, cy+s)], fill=color, width=2)
        draw.line([(cx, cy+s), (cx+s, cy-s)], fill=color, width=2)
        draw.line([(cx-s//2, cy), (cx+s//2, cy)], fill=color, width=1)
    
    elif symbol_type == "cricket":  # Australia cricket
        draw.line([(cx-s, cy), (cx+s, cy)], fill=color, width=2)
        draw.line([(cx, cy-s), (cx, cy+s)], fill=color, width=2)
        draw.ellipse([cx-3, cy-3, cx+3, cy+3], outline=color, width=1)
    
    elif symbol_type == "car":  # BYD car
        draw.rectangle([cx-s, cy, cx+s, cy+s//2], outline=color, width=1)
        draw.rectangle([cx-s//2, cy-s//2, cx+s//2, cy], outline=color, width=1)
        draw.ellipse([cx-s, cy+s//2-2, cx-s+4, cy+s//2+2], fill=color)
        draw.ellipse([cx+s-4, cy+s//2-2, cx+s, cy+s//2+2], fill=color)

# ---- Load data ----
with open("/root/makefun/news-image-20261122/data-news.json") as f:
    raw_stories = json.load(f)

def get_symbol(headline, region):
    h = headline.lower()
    if "cop31" in h or "climate" in h: return "globe"
    if "iran" in h and ("missile" in h or "attack" in h or "base" in h): return "missile"
    if "houthi" in h or "saudi" in h: return "missile"
    if "kryvyi" in h or "zelensky" in h: return "missile"
    if "poland" in h or "missile" in h: return "missile"
    if "fbi" in h or "database" in h or "breach" in h: return "database"
    if "trump" in h or "credit" in h or "interest" in h: return "chart"
    if "anthropic" in h or "ipo" in h or "stock" in h: return "chart"
    if "voyager" in h: return "satellite"
    if "icj" in h or "genocide" in h or "court" in h: return "scales"
    if "nigeria" in h or "boat" in h or "capsiz" in h: return "boat"
    if "brazil" in h or "storm" in h or "tupanciret" in h: return "storm"
    if "australia" in h or "cricket" in h or "england" in h: return "cricket"
    if "byd" in h or "defender" in h: return "car"
    # Region fallback
    if region == "Global": return "globe"
    if region == "Middle East": return "missile"
    if region == "Europe": return "missile"
    if region == "Americas": return "chart"
    if region == "Economy": return "chart"
    if region == "Science": return "satellite"
    if region == "Asia": return "scales"
    if region == "Africa": return "boat"
    if region == "Sport": return "cricket"
    return "globe"

def shorten_headline(h):
    """Shorten long headlines to reasonable length before wrapping."""
    replacements = {
        "COP31 in Antalya closes in on final climate deal after overtime": "COP31 Antalya: Final Climate Deal After Overtime",
        "Iran attacks US bases in Bahrain; industrial site fire": "Iran Attacks US Bases in Bahrain; Industrial Site Fire",
        "Saudi-led coalition intercepts Houthi missile and drone": "Saudi-Led Coalition Intercepts Houthi Missile & Drone",
        "Russia double-tap strike on Kryvyi Rih kills two, wounds 60": "Russia Double-Tap Strike on Kryvyi Rih: 2 Dead, 60 Hurt",
        "Russian missiles and drone land in Poland; NATO vows to defend every inch": "Russian Missiles & Drone Land in Poland; NATO Vows Defense",
        "FBI probes suspected hack of US criminal-justice database": "FBI Probes Suspected Hack of US Criminal-Justice Database",
        "Trump proposes 10% cap on credit card interest rates": "Trump Proposes 10% Cap on Credit Card Interest Rates",
        "Anthropic IPO draws $120 billion retail demand": "Anthropic IPO Draws $120B Retail Demand, Stock Down 15%",
        "Voyager becomes first human-made object 1 light-day from Earth": "Voyager Reaches 1 Light-Day from Earth, 49 Years On",
        "ICJ finds evidence of Rohingya genocide; Myanmar rejects ruling": "ICJ Finds Rohingya Genocide; Myanmar Rejects Ruling",
        "Boat capsized in Nigeria's Bayelsa state, at least 24 dead": "Boat Capsizes in Nigeria's Bayelsa: 24 Dead, 24 Rescued",
        "Supercell storm devastates southern Brazil town, kills 3": "Supercell Storm Hits S. Brazil: 3 Dead, 8K Homes Damaged",
        "Australia chase record 188 to beat England in MCG T20 opener": "Australia Chase Record 188 to Beat England at MCG",
        "Dutch court bars BYD SUV in Europe over Defender resemblance": "Dutch Court Bars BYD SUV in Europe Over Defender Design",
    }
    return replacements.get(h, h[:80])

def shorten_fact(f):
    """Shorten facts to fit in card."""
    replacements = {
        "Nearly 200 countries at COP31 in Antalya negotiated a third and 'final' text into Sunday morning after drafts stripped of fossil-fuel language drew threats of walkout, with a closing plenary set for later Sunday.": "Nearly 200 nations reach final text after fossil-fuel walkout threats.",
        "Iran's IRGC claimed missile-and-drone attacks on two US bases in Bahrain (Sheikh Isa and Juffair), and Bahrain said a civilian industrial facility on Sitra Island was hit and set on fire, with no injuries reported.": "IRGC claims missile-drone strikes on 2 US bases; industrial site on Sitra hit.",
        "The Saudi-led coalition intercepted a ballistic missile and a drone launched toward western Saudi Arabia and Riyadh as Houthi attacks on Taiz killed one and wounded seven, deepening Gulf escalation.": "Saudi coalition intercepts missile & drone; Houthi attacks on Taiz kill 1.",
        "Ballistic missiles and follow-up drone strikes on Zelensky's hometown Kryvyi Rih killed a 7-year-old boy and a 20-year-old paramedic and wounded 60, part of a barrage of 27 ballistic missiles, 84 cruise missiles and 404 drones.": "Missiles & drones hit Zelensky's hometown: boy (7) & paramedic (20) killed, 60 wounded.",
        "A Kh-101 cruise missile, a second missile and a jet-powered drone fell in southeastern Poland near Coalition-of-the-Willing exercises; Tusk called it an intentional provocation and NATO chief Rutte pledged 'NATO will defend every inch of Polish territory'.": "Kh-101 & drone fall in SE Poland; NATO pledges to defend every inch.",
        "The FBI is investigating a suspected breach of the nationwide database used by federal, state and local law enforcement to share warrants, criminal histories and background checks.": "Suspected breach of nationwide criminal-history & warrant database.",
        "President Trump said he would back a 10% cap on credit card interest rates with Democrats' support, and again criticised the Federal Reserve's rate policy, citing India's 7% growth.": "Proposes 10% cap with Dem support; criticizes Fed, cites India's 7% growth.",
        "Anthropic's share sale attracted about $120 billion in retail demand and over $500 billion institutional interest, even as the stock fell nearly 15% on Friday; an Anthropic mathematician separately claimed Claude helped solve the Riemann hypothesis.": "$120B retail, $500B+ institutional demand; stock down ~15%.",
        "Forty-nine years after launch, NASA's Voyager spacecraft became the first human-made object to sit one light-day away from Earth, a milestone in deep-space exploration.": "First human-made object at 1 light-day (25.9B km), 49 yrs after launch.",
        "The International Court of Justice found Myanmar's forces committed genocide against the Rohingya, targeting 800,000 people and killing about 10,000; Myanmar called the verdict unfair while Malaysia moves to resettle 10,000 Rohingya.": "Myanmar forces targeted 800K, killed ~10K; Myanmar rejects verdict.",
        "A boat carrying mourners to a burial ceremony capsized in Nigeria's Bayelsa state, killing at least 24 people; 24 others were rescued and the operator fled the scene, police said.": "Mourners' boat capsizes in Bayelsa; 24 dead, 24 rescued, operator flees.",
        "A supercell storm with 114 kmph winds tore through Tupanciretã in Rio Grande do Sul, killing three, injuring 162 and damaging around 8,000 homes, forcing nearly all of the town's 20,000 residents to leave.": "114 km/h winds hit Tupanciretã; 3 dead, 162 hurt, 8K homes damaged.",
        "Australia beat world number one England by three wickets in the first T20 at the Melbourne Cricket Ground, completing the highest successful run chase at the ground and ending England's seven-match winning streak.": "Record 188 chase at MCG ends England's 7-match streak; Aus win by 3 wkts.",
        "The Hague court ruled BYD's Fangchengbao Ti7 infringes the EU design of JLR's Defender, barring its sale in Europe and production at BYD's planned Hungary plant pending resolution.": "Hague rules Ti7 infringes Defender design; bars EU sale & Hungary production.",
    }
    return replacements.get(f, f[:140])

stories = []
for s in raw_stories:
    stories.append({
        "headline": shorten_headline(s["headline"]),
        "fact": shorten_fact(s["summary_1line"]),
        "symbol": get_symbol(s["headline"], s["region"]),
        "region": s["region"],
    })

# ---- Layout: 3 rows with 5, 5, 4 cards = 14 total ----
masthead_h = draw_masthead()

# Footer
footer_h = 40
footer_text = "Sources: Reuters, Al Jazeera, AP, SBS · make.fun news-image-20261122"

# Available space for cards
top_margin = 15
bottom_margin = 15
available_h = H - masthead_h - footer_h - top_margin - bottom_margin

# 3 rows
rows = 3
cards_per_row = [5, 5, 4]  # Total 14
row_heights = [available_h // rows] * rows
# Distribute remainder
for i in range(available_h % rows):
    row_heights[i] += 1

start_y = masthead_h + top_margin
margin_x = 20
gap_x = 15
gap_y = 15

print(f"Canvas: {W}x{H}")
print(f"Masthead: {masthead_h}px, Footer: {footer_h}px")
print(f"Card area: {available_h}px height, rows: {row_heights}")

# Pre-calculate max card width per row
max_cols = max(cards_per_row)  # 5
card_w = (W - 2 * margin_x - (max_cols - 1) * gap_x) // max_cols
print(f"Card width: {card_w}px")

story_idx = 0
for row_idx, (num_cols, row_h) in enumerate(zip(cards_per_row, row_heights)):
    y = start_y + sum(row_heights[:row_idx]) + row_idx * gap_y
    
    # Calculate x positions to center the row
    row_total_w = num_cols * card_w + (num_cols - 1) * gap_x
    row_start_x = (W - row_total_w) // 2
    
    for col in range(num_cols):
        if story_idx >= len(stories):
            break
        
        story = stories[story_idx]
        x = row_start_x + col * (card_w + gap_x)
        
        # Ensure card fits
        if x + card_w > W - margin_x:
            card_w = W - margin_x - x
        if y + row_h > H - footer_h - bottom_margin:
            row_h = H - footer_h - bottom_margin - y
        
        # Card background
        draw_rounded_rect(draw, (x, y, x + card_w, y + row_h), 8, 
                          fill=COLOR_CARD_BG, outline=COLOR_BORDER, width=1)
        
        # Inner padding
        pad = 12
        inner_x = x + pad
        inner_y = y + pad
        inner_w = card_w - 2 * pad
        inner_h = row_h - 2 * pad
        
        # Region tag (top-left inside card)
        region = story["region"]
        rcolor = REGION_COLORS.get(region, (100, 100, 100))
        tag_text = region
        tag_font = font_region
        tag_pad_x, tag_pad_y = 8, 4
        bbox = draw.textbbox((0, 0), tag_text, font=tag_font)
        tag_w = bbox[2] - bbox[0] + 2 * tag_pad_x
        tag_h = bbox[3] - bbox[1] + 2 * tag_pad_y
        
        draw_rounded_rect(draw, (inner_x, inner_y, inner_x + tag_w, inner_y + tag_h), 4, fill=rcolor)
        draw.text((inner_x + tag_w//2, inner_y + tag_h//2), tag_text, font=tag_font, fill=(255,255,255), anchor="mm")
        
        # Symbol (top-right inside card)
        sym_size = min(24, inner_h // 6)
        sym_x = x + card_w - pad - sym_size // 2
        sym_y = inner_y + sym_size // 2
        draw_symbol(draw, sym_x, sym_y, story["symbol"], rcolor, size=sym_size)
        
        # Headline - wrap to max 2 lines
        headline_y = inner_y + tag_h + 8
        headline_max_w = inner_w
        # Try regular headline font first
        headline_lines = wrap_text(story["headline"], font_headline, headline_max_w, draw, max_lines=2)
        if len(headline_lines) > 2 or any(draw.textbbox((0,0), l, font=font_headline)[2] > headline_max_w for l in headline_lines):
            # Fallback to smaller font
            headline_lines = wrap_text(story["headline"], font_headline_small, headline_max_w, draw, max_lines=2)
        
        for li, line in enumerate(headline_lines):
            draw.text((inner_x, headline_y + li * (font_headline.size + 2)), line, font=font_headline if len(headline_lines) <= 2 else font_headline_small, fill=COLOR_TEXT)
        
        # Fact - wrap to fill remaining space (max lines based on available height)
        fact_y = headline_y + len(headline_lines) * (font_headline.size + 2) + 6
        fact_max_w = inner_w
        fact_max_lines = max(1, (inner_y + inner_h - fact_y) // (font_body.size + 2))
        fact_lines = wrap_text(story["fact"], font_body, fact_max_w, draw, max_lines=fact_max_lines)
        
        for li, line in enumerate(fact_lines):
            if fact_y + li * (font_body.size + 2) <= y + row_h - pad - font_body.size:
                draw.text((inner_x, fact_y + li * (font_body.size + 2)), line, font=font_body, fill=COLOR_TEXT_MUTED)
        
        story_idx += 1

# Draw footer
footer_y = H - footer_h + footer_h // 2
draw.text((W//2, footer_y), footer_text, font=font_footer, fill=COLOR_TEXT_MUTED, anchor="mm")

# Save
img.save("/root/makefun/news-image-20261122/entry.png", "PNG", optimize=True)
print("Saved entry.png")
