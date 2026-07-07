import asyncio
import os
import re
import uuid
import math
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

# 🟢 FONTS SETUP
TITLE_FONT_PATH = "VIVAANXMUSIC/assets/thumb/font2.ttf"
META_FONT_PATH = "VIVAANXMUSIC/assets/thumb/font.ttf"
CANVAS_SIZE = (1280, 720)

# ----------------- HELPER FUNCTIONS ----------------- #

def fit_cover(image, size):
    """Resizes and crops exactly to prevent 'images do not match' error."""
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
    """Draws a perfect star to fix the box character error."""
    points = []
    for i in range(10):
        angle = i * math.pi / 5 - math.pi / 2
        radius = size if i % 2 == 0 else size * 0.4
        points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    draw.polygon(points, fill=fill)
    
def draw_exact_icons(draw, cx, cy, icon, fill=(255, 255, 255)):
    """Scaled up icons to exactly match the original layout size."""
    if icon == "prev":
        draw.polygon([(cx + 18, cy - 20), (cx, cy), (cx + 18, cy + 20)], fill=fill)
        draw.polygon([(cx, cy - 20), (cx - 18, cy), (cx - 18, cy + 20)], fill=fill)
        draw.rounded_rectangle([(cx - 24, cy - 18), (cx - 18, cy + 18)], radius=2, fill=fill) # front bar
    elif icon == "pause":
        draw.rounded_rectangle([(cx - 18, cy - 24), (cx - 6, cy + 24)], radius=4, fill=fill)
        draw.rounded_rectangle([(cx + 6, cy - 24), (cx + 18, cy + 24)], radius=4, fill=fill)
    elif icon == "next":
        draw.polygon([(cx - 18, cy - 20), (cx, cy), (cx - 18, cy + 20)], fill=fill)
        draw.polygon([(cx, cy - 20), (cx + 18, cy), (cx + 18, cy + 20)], fill=fill)
        draw.rounded_rectangle([(cx + 18, cy - 18), (cx + 24, cy + 18)], radius=2, fill=fill) # back bar
    elif icon == "vol_down":
        draw.polygon([(cx - 6, cy - 5), (cx + 2, cy - 5), (cx + 10, cy - 12), (cx + 10, cy + 12), (cx + 2, cy + 5), (cx - 6, cy + 5)], fill=fill)
    elif icon == "vol_up":
        draw.polygon([(cx - 14, cy - 6), (cx - 6, cy - 6), (cx + 2, cy - 14), (cx + 2, cy + 14), (cx - 6, cy + 6), (cx - 14, cy + 6)], fill=fill)
        draw.arc([(cx - 2, cy - 8), (cx + 10, cy + 8)], start=-60, end=60, fill=fill, width=3)
        draw.arc([(cx - 5, cy - 15), (cx + 18, cy + 15)], start=-50, end=50, fill=fill, width=3)
    elif icon == "quote":
        draw.rounded_rectangle([(cx - 18, cy - 15), (cx + 18, cy + 12)], radius=4, outline=fill, width=3)
        draw.polygon([(cx - 6, cy + 10), (cx + 6, cy + 10), (cx, cy + 20)], fill=fill)
        # Inner tiny quotes
        draw.text((cx - 4, cy - 1), "”", fill=fill, font=load_font(META_FONT_PATH, 30), anchor="mm")
        draw.text((cx + 4, cy - 1), "”", fill=fill, font=load_font(META_FONT_PATH, 30), anchor="mm")
    elif icon == "list":
        for i in range(3):
            draw.line([(cx - 12, cy - 12 + (i*12)), (cx + 18, cy - 12 + (i*12))], fill=fill, width=3)
            draw.ellipse([(cx - 22, cy - 14 + (i*12)), (cx - 17, cy - 9 + (i*12))], fill=fill)

# ----------------- MAIN THUMBNAIL GENERATOR ----------------- #

async def get_thumb(videoid, user_id=None):
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_path = os.path.join(CACHE_DIR, f"{videoid}_{user_id}_v5.png")
    
    if os.path.isfile(cache_path):
        return cache_path

    url = f"https://www.youtube.com/watch?v={videoid}"
    
    # 🟢 AUTOPLAY FIX: Generate unique temp file names
    unique_id = uuid.uuid4().hex[:8]
    temp_thumb_path = os.path.join(CACHE_DIR, f"temp_{videoid}_{unique_id}.png")

    try:
        results = VideosSearch(url, limit=1)
        results_data = (await results.next()).get("result", [])
        if not results_data:
            return YOUTUBE_IMG_URL

        result = results_data[0]
        # Titles cut perfectly so they don't hit the right side buttons
        title = trim_text(re.sub(r"[^\w\s&\-']", " ", result.get("title", "")).strip(), 25)
        duration = str(result.get("duration") or "00:00")
        views_str = format_views((result.get("viewCount") or {}).get("text") or "0")
        channel = trim_text(str((result.get("channel") or {}).get("name") or "Unknown Artist"), 30)
        
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

        # Base Image Setup
        source_image = Image.open(temp_thumb_path).convert("RGBA")
        background = fit_cover(source_image, CANVAS_SIZE)
        
        # Perfect background dimming and blur
        background = background.filter(ImageFilter.GaussianBlur(35))
        background = ImageEnhance.Brightness(background).enhance(0.25)
        scene = background.copy()
        
        # Fonts
        font_title = load_font(TITLE_FONT_PATH, 40)
        font_artist = load_font(META_FONT_PATH, 24)
        font_time = load_font(META_FONT_PATH, 18)
        font_views_num = load_font(TITLE_FONT_PATH, 45)
        font_views_text = load_font(TITLE_FONT_PATH, 20)

        # --------------------------------------------------
        # LEFT SIDE: LARGE ART CARD 
        # --------------------------------------------------
        art_size = 580
        art_x, art_y = 60, 70
        
        art_content = fit_cover(source_image, (art_size, art_size))
        art_mask = get_mask((art_size, art_size), 45)
        
        left_panel = Image.new("RGBA", (art_size, art_size), (0,0,0,0))
        left_panel.paste(art_content, (0,0), art_mask)
        
        overlay_draw = ImageDraw.Draw(left_panel)
        # Left Bottom text (e.g. 25 M / VIEWS)
        overlay_draw.text((35, art_size - 110), f"{views_str}", fill=(255, 255, 255), font=font_views_num)
        overlay_draw.text((35, art_size - 55), "VIEWS", fill=(255, 255, 255), font=font_views_text)
        
        # Right Bottom text (e.g. OFFICIAL / VIDEO)
        overlay_draw.text((art_size - 35, art_size - 95), "OFFICIAL", fill=(255, 255, 255), font=font_views_text, anchor="ra")
        overlay_draw.text((art_size - 35, art_size - 55), "VIDEO", fill=(255, 255, 255), font=font_views_text, anchor="ra")

        scene.paste(left_panel, (art_x, art_y), left_panel)
        
        draw = ImageDraw.Draw(scene)

        # --------------------------------------------------
        # RIGHT SIDE: PERFECT ALIGNMENT & LARGE UI
        # --------------------------------------------------
        right_x = 700
        right_w = 1220
        
        # Title and Artist
        draw.text((right_x, 140), title, fill=(255, 255, 255), font=font_title)
        draw.text((right_x, 200), channel, fill=(170, 180, 190), font=font_artist)
        
        # Top Icons (Star and 3 Dots) -> Box error fixed by drawing star
        draw.ellipse([(1100, 140), (1150, 190)], fill=(255, 255, 255, 180))
        draw_star(draw, 1125, 165, size=14, fill=(0, 0, 0)) # Fixed star
        
        draw.ellipse([(1170, 140), (1220, 190)], fill=(255, 255, 255, 180))
        for i in range(3):
            draw.ellipse([(1192, 153 + (i*10)), (1198, 159 + (i*10))], fill=(0, 0, 0))

        # Progress Bar -> Thicker exactly like original
        bar_y = 300
        draw.rounded_rectangle([(right_x, bar_y), (right_w, bar_y + 10)], radius=5, fill=(180, 180, 180))
        
        prog_x = right_x + int((right_w - right_x) * 0.05)
        draw.rounded_rectangle([(right_x, bar_y), (prog_x, bar_y + 10)], radius=5, fill=(255, 255, 255))
        draw.ellipse([(prog_x - 12, bar_y - 7), (prog_x + 12, bar_y + 17)], fill=(255, 255, 255))
        
        # Timestamps
        draw.text((right_x, bar_y + 25), "0:03", fill=(200, 200, 200), font=font_time)
        try:
            dur_w = draw.textlength(f"-{duration}", font=font_time)
        except:
            dur_w = draw.textsize(f"-{duration}", font=font_time)[0]
        draw.text((right_w - dur_w, bar_y + 25), f"-{duration}", fill=(200, 200, 200), font=font_time)

        # Media Controls -> Massive and crisp
        ctrl_y = 450
        draw_exact_icons(draw, right_x + 80, ctrl_y, "prev")
        draw_exact_icons(draw, (right_x + right_w) // 2, ctrl_y, "pause")
        draw_exact_icons(draw, right_w - 80, ctrl_y, "next")

        # Volume Controls -> Thicker line
        vol_y = 600
        draw_exact_icons(draw, right_x + 15, vol_y, "vol_down")
        draw.rounded_rectangle([(right_x + 50, vol_y - 4), (right_w - 45, vol_y + 4)], radius=4, fill=(255, 255, 255))
        draw_exact_icons(draw, right_w - 10, vol_y, "vol_up")

        # Bottom Icons -> Proper shape & size
        btm_y = 680
        draw_exact_icons(draw, right_x + 140, btm_y, "quote")
        draw_exact_icons(draw, right_w - 140, btm_y, "list")

        # Cleanup Temporary File
        try:
            if os.path.exists(temp_thumb_path):
                os.remove(temp_thumb_path)
        except:
            pass

        scene.save(cache_path)
        return cache_path

    except Exception as e:
        LOGGER.error(f"Thumbnail Error (Autoplay): {e}")
        try:
            if os.path.exists(temp_thumb_path):
                os.remove(temp_thumb_path)
        except:
            pass
        return YOUTUBE_IMG_URL
        
