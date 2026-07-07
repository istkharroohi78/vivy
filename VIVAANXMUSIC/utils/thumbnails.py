import asyncio
import os
import re
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

# Fonts setup (Make sure you have these in your bot's folder)
TITLE_FONT_PATH = "VIVAANXMUSIC/assets/thumb/font2.ttf"
META_FONT_PATH = "VIVAANXMUSIC/assets/thumb/font.ttf"
CANVAS_SIZE = (1280, 720)

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

def draw_exact_icons(draw, cx, cy, icon, fill=(255, 255, 255)):
    """Drawing icons to exactly match the provided image reference."""
    if icon == "prev":
        draw.polygon([(cx + 15, cy - 18), (cx - 2, cy), (cx + 15, cy + 18)], fill=fill)
        draw.polygon([(cx - 2, cy - 18), (cx - 19, cy), (cx - 2, cy + 18)], fill=fill)
    elif icon == "pause":
        draw.rounded_rectangle([(cx - 16, cy - 22), (cx - 4, cy + 22)], radius=4, fill=fill)
        draw.rounded_rectangle([(cx + 4, cy - 22), (cx + 16, cy + 22)], radius=4, fill=fill)
    elif icon == "next":
        draw.polygon([(cx - 15, cy - 18), (cx + 2, cy), (cx - 15, cy + 18)], fill=fill)
        draw.polygon([(cx + 2, cy - 18), (cx + 19, cy), (cx + 2, cy + 18)], fill=fill)
    elif icon == "vol_down":
        draw.polygon([(cx - 4, cy - 4), (cx + 2, cy - 4), (cx + 8, cy - 10), (cx + 8, cy + 10), (cx + 2, cy + 4), (cx - 4, cy + 4)], fill=fill)
    elif icon == "vol_up":
        draw.polygon([(cx - 10, cy - 5), (cx - 4, cy - 5), (cx + 2, cy - 12), (cx + 2, cy + 12), (cx - 4, cy + 5), (cx - 10, cy + 5)], fill=fill)
        draw.arc([(cx - 2, cy - 6), (cx + 8, cy + 6)], start=-60, end=60, fill=fill, width=2)
        draw.arc([(cx - 5, cy - 12), (cx + 13, cy + 12)], start=-50, end=50, fill=fill, width=2)
    elif icon == "quote":
        draw.rounded_rectangle([(cx - 14, cy - 12), (cx + 14, cy + 10)], radius=3, outline=fill, width=2)
        draw.polygon([(cx - 4, cy + 9), (cx + 4, cy + 9), (cx, cy + 16)], fill=fill)
        draw.text((cx, cy - 5), "”", fill=fill, font=load_font(META_FONT_PATH, 30), anchor="mm")
    elif icon == "list":
        for i in range(3):
            draw.line([(cx - 10, cy - 10 + (i*10)), (cx + 15, cy - 10 + (i*10))], fill=fill, width=3)
            draw.ellipse([(cx - 18, cy - 11 + (i*10)), (cx - 14, cy - 7 + (i*10))], fill=fill)

async def get_thumb(videoid, user_id=None):
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_path = os.path.join(CACHE_DIR, f"{videoid}_{user_id}_exact_ui.png")
    
    if os.path.isfile(cache_path):
        return cache_path

    url = f"https://www.youtube.com/watch?v={videoid}"
    temp_thumb_path = os.path.join(CACHE_DIR, f"thumb_{videoid}.png")

    try:
        results = VideosSearch(url, limit=1)
        results_data = (await results.next()).get("result", [])
        if not results_data:
            return YOUTUBE_IMG_URL

        result = results_data[0]
        title = trim_text(re.sub(r"[^\w\s&\-']", " ", result.get("title", "")).strip(), 28)
        duration = str(result.get("duration") or "00:00")
        views_str = format_views((result.get("viewCount") or {}).get("text") or "0")
        channel = trim_text(str((result.get("channel") or {}).get("name") or "Unknown"), 30)
        
        thumbnails = result.get("thumbnails", [{}])
        thumbnail_url = thumbnails[-1].get("url", thumbnails[0].get("url", "")).split("?")[0]

        async with aiohttp.ClientSession() as session:
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
        
        # Exact Blur and Darkening as your image
        background = background.filter(ImageFilter.GaussianBlur(35))
        background = ImageEnhance.Brightness(background).enhance(0.25)
        scene = background.copy()
        
        # Load Fonts
        font_title = load_font(TITLE_FONT_PATH, 38)
        font_artist = load_font(META_FONT_PATH, 22)
        font_time = load_font(META_FONT_PATH, 18)
        font_views = load_font(TITLE_FONT_PATH, 38)
        font_small = load_font(TITLE_FONT_PATH, 20)

        # --------------------------------------------------
        # LEFT SIDE: EXACT ART CARD PROPORTIONS
        # --------------------------------------------------
        art_size = 560
        art_x, art_y = 60, 80
        
        art_content = fit_cover(source_image, (art_size, art_size))
        art_mask = get_mask((art_size, art_size), 40)
        
        left_panel = Image.new("RGBA", (art_size, art_size), (0,0,0,0))
        left_panel.paste(art_content, (0,0), art_mask)
        
        overlay_draw = ImageDraw.Draw(left_panel)
        overlay_draw.text((25, art_size - 90), f"{views_str}", fill=(255, 255, 255), font=font_views)
        overlay_draw.text((25, art_size - 40), "VIEWS", fill=(255, 255, 255), font=font_small)
        
        overlay_draw.text((art_size - 25, art_size - 75), "OFFICIAL", fill=(255, 255, 255), font=font_small, anchor="ra")
        overlay_draw.text((art_size - 25, art_size - 40), "VIDEO", fill=(255, 255, 255), font=font_small, anchor="ra")

        scene.paste(left_panel, (art_x, art_y), left_panel)
        
        draw = ImageDraw.Draw(scene)

        # --------------------------------------------------
        # RIGHT SIDE: EXACT TEXT & CONTROLS ALIGNMENT
        # --------------------------------------------------
        right_x = 680
        right_w = 1200
        
        # Title and Artist
        draw.text((right_x, 140), title, fill=(255, 255, 255), font=font_title)
        draw.text((right_x, 200), channel, fill=(170, 180, 190), font=font_artist)
        
        # Top Icons (Star and 3 Dots)
        draw.ellipse([(1080, 145), (1120, 185)], fill=(255, 255, 255, 180))
        draw.text((1100, 166), "☆", fill=(0, 0, 0), font=load_font(META_FONT_PATH, 24), anchor="mm")
        
        draw.ellipse([(1140, 145), (1180, 185)], fill=(255, 255, 255, 180))
        for i in range(3):
            draw.ellipse([(1158, 155 + (i*10)), (1162, 159 + (i*10))], fill=(0, 0, 0))

        # Progress Bar
        bar_y = 280
        draw.rounded_rectangle([(right_x, bar_y), (right_w, bar_y + 8)], radius=4, fill=(180, 180, 180))
        
        prog_x = right_x + int((right_w - right_x) * 0.05) # 5% completion like 0:03
        draw.rounded_rectangle([(right_x, bar_y), (prog_x, bar_y + 8)], radius=4, fill=(255, 255, 255))
        draw.ellipse([(prog_x - 10, bar_y - 4), (prog_x + 10, bar_y + 12)], fill=(255, 255, 255))
        
        # Timestamps
        draw.text((right_x, bar_y + 25), "0:03", fill=(200, 200, 200), font=font_time)
        try:
            dur_w = draw.textlength(f"-{duration}", font=font_time)
        except:
            dur_w = draw.textsize(f"-{duration}", font=font_time)[0]
        draw.text((right_w - dur_w, bar_y + 25), f"-{duration}", fill=(200, 200, 200), font=font_time)

        # Media Controls (Centered vertically below progress)
        ctrl_y = 420
        draw_exact_icons(draw, right_x + 80, ctrl_y, "prev")
        draw_exact_icons(draw, (right_x + right_w) // 2, ctrl_y, "pause")
        draw_exact_icons(draw, right_w - 80, ctrl_y, "next")

        # Volume Controls
        vol_y = 550
        draw_exact_icons(draw, right_x + 15, vol_y, "vol_down")
        draw.rounded_rectangle([(right_x + 50, vol_y - 3), (right_w - 45, vol_y + 3)], radius=3, fill=(255, 255, 255))
        draw_exact_icons(draw, right_w - 10, vol_y, "vol_up")

        # Bottom Icons (Lyrics Quote & List)
        btm_y = 630
        draw_exact_icons(draw, right_x + 150, btm_y, "quote")
        draw_exact_icons(draw, right_w - 150, btm_y, "list")

        # Cleanup
        try:
            os.remove(temp_thumb_path)
        except:
            pass

        scene.save(cache_path)
        return cache_path

    except Exception as e:
        LOGGER.error(f"Thumbnail Error: {e}")
        return YOUTUBE_IMG_URL
                       
