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

TITLE_FONT_PATH = "VIVAANXMUSIC/assets/thumb/font2.ttf"
META_FONT_PATH = "VIVAANXMUSIC/assets/thumb/font.ttf"
CANVAS_SIZE = (1280, 720)

# ----------------- HELPER FUNCTIONS ----------------- #

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
    
def draw_exact_icons(draw, cx, cy, icon, fill=(255, 255, 255)):
    if icon == "prev":
        draw.polygon([(cx + 14, cy - 16), (cx - 2, cy), (cx + 14, cy + 16)], fill=fill)
        draw.polygon([(cx - 2, cy - 16), (cx - 18, cy), (cx - 18, cy + 16)], fill=fill)
        draw.rounded_rectangle([(cx - 24, cy - 16), (cx - 18, cy + 16)], radius=2, fill=fill)
    elif icon == "pause":
        draw.rounded_rectangle([(cx - 14, cy - 20), (cx - 4, cy + 20)], radius=4, fill=fill)
        draw.rounded_rectangle([(cx + 4, cy - 20), (cx + 14, cy + 20)], radius=4, fill=fill)
    elif icon == "next":
        draw.polygon([(cx - 14, cy - 16), (cx + 2, cy), (cx - 14, cy + 16)], fill=fill)
        draw.polygon([(cx + 2, cy - 16), (cx + 18, cy), (cx + 18, cy + 16)], fill=fill)
        draw.rounded_rectangle([(cx + 18, cy - 16), (cx + 24, cy + 16)], radius=2, fill=fill)
    elif icon == "vol_down":
        draw.polygon([(cx - 8, cy - 6), (cx, cy - 6), (cx + 10, cy - 14), (cx + 10, cy + 14), (cx, cy + 6), (cx - 8, cy + 6)], fill=fill)
    elif icon == "vol_up":
        draw.polygon([(cx - 12, cy - 6), (cx - 4, cy - 6), (cx + 6, cy - 14), (cx + 6, cy + 14), (cx - 4, cy + 6), (cx - 12, cy + 6)], fill=fill)
        draw.arc([(cx + 2, cy - 8), (cx + 14, cy + 8)], start=-60, end=60, fill=fill, width=3)
        draw.arc([(cx - 2, cy - 16), (cx + 22, cy + 16)], start=-50, end=50, fill=fill, width=3)
    elif icon == "quote":
        draw.rounded_rectangle([(cx - 20, cy - 16), (cx + 20, cy + 12)], radius=5, outline=fill, width=3)
        draw.polygon([(cx - 6, cy + 11), (cx + 6, cy + 11), (cx, cy + 22)], fill=fill)
        draw.text((cx - 6, cy - 2), "”", fill=fill, font=load_font(META_FONT_PATH, 32), anchor="mm")
        draw.text((cx + 6, cy - 2), "”", fill=fill, font=load_font(META_FONT_PATH, 32), anchor="mm")
    elif icon == "list":
        for i in range(3):
            draw.line([(cx - 10, cy - 12 + (i*12)), (cx + 20, cy - 12 + (i*12))], fill=fill, width=4)
            draw.ellipse([(cx - 22, cy - 15 + (i*12)), (cx - 16, cy - 9 + (i*12))], fill=fill)

# ----------------- MAIN THUMBNAIL GENERATOR ----------------- #

async def get_thumb(videoid, user_id=None):
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_path = os.path.join(CACHE_DIR, f"{videoid}_{user_id}_v5.png")
    
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
        title = trim_text(re.sub(r"[^\w\s&\-']", " ", result.get("title", "")).strip(), 30)
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
        background = fit_cover(source_image, CANVAS_SIZE)
        
        background = background.filter(ImageFilter.GaussianBlur(40))
        background = ImageEnhance.Brightness(background).enhance(0.2)
        scene = background.copy()
        
        font_title = load_font(TITLE_FONT_PATH, 42)
        font_artist = load_font(META_FONT_PATH, 26)
        font_time = load_font(META_FONT_PATH, 20)
        font_views_num = load_font(TITLE_FONT_PATH, 48)
        font_views_text = load_font(TITLE_FONT_PATH, 22)

        art_size = 560
        art_x, art_y = 70, 80
        
        art_content = fit_cover(source_image, (art_size, art_size))
        art_mask = get_mask((art_size, art_size), 35)
        
        left_panel = Image.new("RGBA", (art_size, art_size), (0,0,0,0))
        left_panel.paste(art_content, (0,0), art_mask)
        
        overlay_draw = ImageDraw.Draw(left_panel)
        overlay_draw.text((40, art_size - 120), f"{views_str}", fill=(255, 255, 255), font=font_views_num)
        overlay_draw.text((40, art_size - 60), "VIEWS", fill=(255, 255, 255, 200), font=font_views_text)
        overlay_draw.text((art_size - 40, art_size - 100), "OFFICIAL", fill=(255, 255, 255), font=font_views_text, anchor="ra")
        overlay_draw.text((art_size - 40, art_size - 60), "VIDEO", fill=(255, 255, 255, 200), font=font_views_text, anchor="ra")

        scene.paste(left_panel, (art_x, art_y), left_panel)
        draw = ImageDraw.Draw(scene)

        right_x = 700
        right_w = 1210
        center_x = (right_x + right_w) // 2
        
        draw.text((right_x, 150), title, fill=(255, 255, 255), font=font_title)
        draw.text((right_x, 210), channel, fill=(180, 190, 200), font=font_artist)
        
        draw.ellipse([(right_w - 90, 150), (right_w - 40, 200)], fill=(255, 255, 255, 30))
        draw_star(draw, right_w - 65, 175, size=15, fill=(255, 255, 255))
        
        draw.ellipse([(right_w - 20, 150), (right_w + 30, 200)], fill=(255, 255, 255, 30))
        for i in range(3):
            draw.ellipse([(right_w + 2, 163 + (i*10)), (right_w + 8, 169 + (i*10))], fill=(255, 255, 255))

        bar_y = 330
        draw.rounded_rectangle([(right_x, bar_y), (right_w, bar_y + 8)], radius=4, fill=(255, 255, 255, 60))
        prog_x = right_x + int((right_w - right_x) * 0.1)
        draw.rounded_rectangle([(right_x, bar_y), (prog_x, bar_y + 8)], radius=4, fill=(255, 255, 255))
        draw.ellipse([(prog_x - 10, bar_y - 6), (prog_x + 10, bar_y + 14)], fill=(255, 255, 255))
        
        draw.text((right_x, bar_y + 20), "0:15", fill=(200, 200, 200), font=font_time)
        try:
            dur_w = draw.textlength(f"-{duration}", font=font_time)
        except:
            dur_w = draw.textsize(f"-{duration}", font=font_time)[0]
        draw.text((right_w - dur_w, bar_y + 20), f"-{duration}", fill=(200, 200, 200), font=font_time)

        ctrl_y = 470
        draw_exact_icons(draw, center_x - 120, ctrl_y, "prev")
        draw_exact_icons(draw, center_x, ctrl_y, "pause")
        draw_exact_icons(draw, center_x + 120, ctrl_y, "next")

        vol_y = 590
        vol_start = right_x + 40
        vol_end = right_w - 40
        draw_exact_icons(draw, vol_start - 25, vol_y, "vol_down")
        draw.rounded_rectangle([(vol_start + 10, vol_y - 4), (vol_end - 10, vol_y + 4)], radius=4, fill=(255, 255, 255, 80))
        draw.rounded_rectangle([(vol_start + 10, vol_y - 4), (vol_start + 120, vol_y + 4)], radius=4, fill=(255, 255, 255))
        draw_exact_icons(draw, vol_end + 25, vol_y, "vol_up")

        btm_y = 660
        draw_exact_icons(draw, center_x - 80, btm_y, "quote", fill=(255, 255, 255, 180))
        draw_exact_icons(draw, center_x + 80, btm_y, "list", fill=(255, 255, 255, 180))

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
