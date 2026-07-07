import asyncio
import os
import re
import uuid
import math
import colorsys
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from youtubesearchpython.__future__ import VideosSearch

from config import YOUTUBE_IMG_URL
from VIVAANXMUSIC.core.dir import CACHE_DIR

LOGGER = __import__('logging').getLogger(__name__)

# 🟢 PILLOW COMPATIBILITY FIX
try:
    LANCZOS = Image.Resampling.LANCZOS
except AttributeError:
    LANCZOS = Image.LANCZOS

TITLE_FONT_PATH = "VIVAANXMUSIC/assets/thumb/font2.ttf"
META_FONT_PATH = "VIVAANXMUSIC/assets/thumb/font.ttf"
CANVAS_SIZE = (1280, 720)

WHITE = (255, 255, 255)
TEXT_GRAY = (180, 180, 180)

# ----------------- HELPER FUNCTIONS ----------------- #

def get_vibrant_color(image):
    """थंबनेल से सबसे आकर्षक रंग निकालता है (Glow Effect के लिए)"""
    img = image.copy().convert("RGB")
    img = img.resize((1, 1), resample=0)
    r, g, b = img.getpixel((0, 0))
    
    h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
    s = min(s + 0.5, 1.0) 
    v = min(v + 0.4, 1.0) 
    
    if s < 0.2: 
        h, s, v = 0.85, 0.9, 0.9
        
    r_new, g_new, b_new = colorsys.hsv_to_rgb(h, s, v)
    return (int(r_new*255), int(g_new*255), int(b_new*255))

def fit_cover(image, size):
    ratio = max(size[0] / image.size[0], size[1] / image.size[1])
    new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
    resized = image.resize(new_size, LANCZOS)
    
    left = (new_size[0] - size[0]) // 2
    top = (new_size[1] - size[1]) // 2
    right = left + size[0]
    bottom = top + size[1]
    
    return resized.crop((left, top, right, bottom))

def get_mask(size, radius, antialias=4):
    mask = Image.new("L", (size[0] * antialias, size[1] * antialias), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0] * antialias, size[1] * antialias), radius=radius * antialias, fill=255)
    return mask.resize(size, LANCZOS)

def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def format_views(view_count_str):
    try:
        views_num = int(re.sub(r"\D", "", str(view_count_str)))
        if views_num >= 1_000_000_000:
            return f"{views_num / 1_000_000_000:.1f} B"
        elif views_num >= 1_000_000:
            return f"{views_num // 1_000_000} M"
        elif views_num >= 1_000:
            return f"{views_num // 1_000} K"
        return str(views_num)
    except:
        return "Unknown"

def trim_text(text: str, limit: int) -> str:
    clean_text = " ".join(str(text or "").split())
    if len(clean_text) <= limit:
        return clean_text
    return clean_text[: max(limit - 3, 0)].rstrip() + "..."

def draw_star(draw, cx, cy, size, fill):
    points = []
    for i in range(10):
        angle = i * math.pi / 5 - math.pi / 2
        radius = size if i % 2 == 0 else size * 0.4
        points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    draw.polygon(points, fill=fill)
    
def draw_exact_icons(draw, cx, cy, icon, fill=WHITE):
    """आपके ओरिजिनल और एग्जैक्ट आइकॉन्स (No Changes Here)"""
    if icon == "prev":
        draw.polygon([(cx + 18, cy - 20), (cx, cy), (cx + 18, cy + 20)], fill=fill)
        draw.polygon([(cx, cy - 20), (cx - 18, cy), (cx - 18, cy + 20)], fill=fill)
    elif icon == "pause":
        draw.rounded_rectangle([(cx - 18, cy - 24), (cx - 6, cy + 24)], radius=4, fill=fill)
        draw.rounded_rectangle([(cx + 6, cy - 24), (cx + 18, cy + 24)], radius=4, fill=fill)
    elif icon == "next":
        draw.polygon([(cx - 18, cy - 20), (cx, cy), (cx - 18, cy + 20)], fill=fill)
        draw.polygon([(cx, cy - 20), (cx + 18, cy), (cx + 18, cy + 20)], fill=fill)
    elif icon == "vol_down":
        draw.polygon([(cx - 6, cy - 5), (cx + 2, cy - 5), (cx + 10, cy - 12), (cx + 10, cy + 12), (cx + 2, cy + 5), (cx - 6, cy + 5)], fill=fill)
    elif icon == "vol_up":
        draw.polygon([(cx - 14, cy - 6), (cx - 6, cy - 6), (cx + 2, cy - 14), (cx + 2, cy + 14), (cx - 6, cy + 6), (cx - 14, cy + 6)], fill=fill)
        draw.arc([(cx - 2, cy - 8), (cx + 10, cy + 8)], start=-60, end=60, fill=fill, width=3)
        draw.arc([(cx - 5, cy - 15), (cx + 18, cy + 15)], start=-50, end=50, fill=fill, width=3)
    elif icon == "quote":
        draw.rounded_rectangle([(cx - 20, cy - 16), (cx + 20, cy + 12)], radius=5, outline=fill, width=3)
        draw.polygon([(cx - 6, cy + 11), (cx + 6, cy + 11), (cx, cy + 22)], fill=fill)
        draw.text((cx - 6, cy - 2), "”", fill=fill, font=load_font(META_FONT_PATH, 32), anchor="mm")
        draw.text((cx + 6, cy - 2), "”", fill=fill, font=load_font(META_FONT_PATH, 32), anchor="mm")
    elif icon == "list":
        for i in range(3):
            draw.line([(cx - 12, cy - 12 + (i*12)), (cx + 20, cy - 12 + (i*12))], fill=fill, width=3)
            draw.ellipse([(cx - 22, cy - 14 + (i*12)), (cx - 17, cy - 9 + (i*12))], fill=fill)

# ----------------- MAIN THUMBNAIL GENERATOR ----------------- #

async def get_thumb(videoid, user_id=None):
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_path = os.path.join(CACHE_DIR, f"{videoid}_{user_id}_perfect_v7.png")
    
    if os.path.isfile(cache_path):
        return cache_path

    url = f"https://www.youtube.com/watch?v={videoid}"
    unique_id = uuid.uuid4().hex[:8]
    temp_thumb_path = os.path.join(CACHE_DIR, f"temp_{videoid}_{unique_id}.png")

    try:
        results = VideosSearch(url, limit=1)
        results_data = (await results.next()).get("result", [])
        if not results_data:
            return YOUTUBE_IMG_URL

        result = results_data[0]
        # टाइटल की लम्बाई 22 तक फिक्स की है ताकि वो बटन्स के ऊपर न चढ़े
        title = trim_text(re.sub(r"[^\w\s&\-']", " ", result.get("title", "")).strip(), 22)
        duration = str(result.get("duration") or "00:00")
        views_str = format_views((result.get("viewCount") or {}).get("text") or "0")
        channel = trim_text(str((result.get("channel") or {}).get("name") or "Unknown Artist"), 35)
        
        thumbnails = result.get("thumbnails", [{}])
        thumbnail_url = thumbnails[-1].get("url", thumbnails[0].get("url", "")).split("?")[0]

        async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0"}) as session:
            async with session.get(thumbnail_url) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(temp_thumb_path, mode="wb")
                    await f.write(await resp.read())
                    await f.close()
                else:
                    return YOUTUBE_IMG_URL

        source_image = Image.open(temp_thumb_path).convert("RGBA")
        
        # 🎨 DYNAMIC GLOW COLOR
        theme_color = get_vibrant_color(source_image)
        glow_color = (*theme_color, 150) # सॉफ्ट ट्रांसपेरेंट ग्लो

        background = fit_cover(source_image, CANVAS_SIZE)
        
        # 🟢 डार्क सिनेमैटिक ब्लर (बिल्कुल इमेज की तरह)
        background = background.filter(ImageFilter.GaussianBlur(75))
        background = ImageEnhance.Brightness(background).enhance(0.25)
        scene = background.copy()
        
        # 🟢 Fonts 
        font_title = load_font(TITLE_FONT_PATH, 42)
        font_artist = load_font(META_FONT_PATH, 24)
        font_time = load_font(META_FONT_PATH, 20)
        font_views_num = load_font(TITLE_FONT_PATH, 48)
        font_views_text = load_font(TITLE_FONT_PATH, 22)

        # --------------------------------------------------
        # 1. LEFT SIDE: SQUARE ART CARD WITH GLOW & OVERLAY
        # --------------------------------------------------
        art_size = 560 
        art_x, art_y = 60, 80
        
        # Glow Effect 
        glow_layer = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow_layer)
        glow_spread = 20
        glow_draw.rounded_rectangle(
            [(art_x - glow_spread, art_y - glow_spread), (art_x + art_size + glow_spread, art_y + art_size + glow_spread)],
            radius=50, fill=glow_color
        )
        glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(45))
        scene.paste(glow_layer, (0, 0), glow_layer)
        
        # Main Art Content
        art_content = fit_cover(source_image, (art_size, art_size))
        art_mask = get_mask((art_size, art_size), 45)
        
        left_panel = Image.new("RGBA", (art_size, art_size), (0,0,0,0))
        left_panel.paste(art_content, (0,0), art_mask)
        
        overlay_draw = ImageDraw.Draw(left_panel)
        # Views & Official Text (बिल्कुल रेफरेंस इमेज की पोजीशन)
        overlay_draw.text((40, art_size - 120), f"{views_str}", fill=WHITE, font=font_views_num)
        overlay_draw.text((40, art_size - 60), "VIEWS", fill=WHITE, font=font_views_text)
        
        overlay_draw.text((art_size - 40, art_size - 100), "OFFICIAL", fill=WHITE, font=font_views_text, anchor="ra")
        overlay_draw.text((art_size - 40, art_size - 60), "VIDEO", fill=WHITE, font=font_views_text, anchor="ra")

        scene.paste(left_panel, (art_x, art_y), left_panel)
        draw = ImageDraw.Draw(scene, "RGBA")

        # --------------------------------------------------
        # 2. RIGHT SIDE: UI ALIGNMENT
        # --------------------------------------------------
        right_x = 680
        right_w = 1210
        center_x = (right_x + right_w) // 2
        
        title_y = 120
        draw.text((right_x, title_y), title, fill=WHITE, font=font_title)
        draw.text((right_x, title_y + 60), channel, fill=TEXT_GRAY, font=font_artist)
        
        # Top Icons (Star & Dots - राइट अलाइन एकदम इमेज जैसा)
        # Star Button
        draw.ellipse([(1090, title_y), (1140, title_y + 50)], fill=(255, 255, 255, 60))
        draw_star(draw, 1115, title_y + 25, size=14, fill=WHITE) 
        
        # Dots Button
        draw.ellipse([(1160, title_y), (1210, title_y + 50)], fill=(255, 255, 255, 60))
        for i in range(3):
            draw.ellipse([(1182, title_y + 13 + (i*10)), (1188, title_y + 19 + (i*10))], fill=WHITE)

        # --------------------------------------------------
        # 3. WHITE PROGRESS BAR
        # --------------------------------------------------
        bar_y = 290
        draw.rounded_rectangle([(right_x, bar_y), (right_w, bar_y + 8)], radius=4, fill=(255, 255, 255, 60))
        prog_x = right_x + int((right_w - right_x) * 0.1) 
        draw.rounded_rectangle([(right_x, bar_y), (prog_x, bar_y + 8)], radius=4, fill=WHITE)
        draw.ellipse([(prog_x - 12, bar_y - 8), (prog_x + 12, bar_y + 16)], fill=WHITE)
        
        # Timestamps
        time_y = bar_y + 25
        draw.text((right_x, time_y), "0:03", fill=TEXT_GRAY, font=font_time)
        try:
            dur_w = draw.textlength(f"-{duration}", font=font_time)
        except:
            dur_w = draw.textsize(f"-{duration}", font=font_time)[0]
        draw.text((right_w - dur_w, time_y), f"-{duration}", fill=TEXT_GRAY, font=font_time)

        # --------------------------------------------------
        # 4. BIG WHITE MEDIA CONTROLS
        # --------------------------------------------------
        ctrl_y = 440
        draw_exact_icons(draw, center_x - 130, ctrl_y, "prev", fill=WHITE)
        draw_exact_icons(draw, center_x, ctrl_y, "pause", fill=WHITE)
        draw_exact_icons(draw, center_x + 130, ctrl_y, "next", fill=WHITE)

        # --------------------------------------------------
        # 5. VOLUME CONTROLS
        # --------------------------------------------------
        vol_y = 570
        draw_exact_icons(draw, right_x + 20, vol_y, "vol_down", fill=WHITE)
        draw.rounded_rectangle([(right_x + 60, vol_y - 4), (right_w - 60, vol_y + 4)], radius=4, fill=WHITE)
        draw_exact_icons(draw, right_w - 20, vol_y, "vol_up", fill=WHITE)

        # --------------------------------------------------
        # 6. BOTTOM ICONS
        # --------------------------------------------------
        btm_y = 660
        draw_exact_icons(draw, center_x - 90, btm_y, "quote", fill=WHITE)
        draw_exact_icons(draw, center_x + 90, btm_y, "list", fill=WHITE)

        try:
            if os.path.exists(temp_thumb_path):
                os.remove(temp_thumb_path)
        except:
            pass

        scene.save(cache_path)
        return cache_path

    except Exception as e:
        LOGGER.error(f"Thumbnail Error: {e}")
        try:
            if os.path.exists(temp_thumb_path):
                os.remove(temp_thumb_path)
        except:
            pass
        return YOUTUBE_IMG_URL
