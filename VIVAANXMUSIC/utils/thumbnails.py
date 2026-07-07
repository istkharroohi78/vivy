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

# 🟢 PILLOW COMPATIBILITY FIX (Anti-Crash for Autoplay)
try:
    LANCZOS = Image.Resampling.LANCZOS
except AttributeError:
    LANCZOS = Image.LANCZOS

# 🟢 FONT PATHS
TITLE_FONT_PATH = "VIVAANXMUSIC/assets/thumb/font2.ttf"
META_FONT_PATH = "VIVAANXMUSIC/assets/thumb/font.ttf"
CANVAS_SIZE = (1280, 720)

# ----------------- HELPER FUNCTIONS ----------------- #

def fit_cover(image, size):
    """Resizes and crops image to perfectly fit the given size."""
    ratio = max(size[0] / image.size[0], size[1] / image.size[1])
    resized = image.resize((int(image.size[0] * ratio), int(image.size[1] * ratio)), LANCZOS)
    return resized.crop((max((resized.size[0] - size[0]) // 2, 0), 
                         max((resized.size[1] - size[1]) // 2, 0), 
                         min(resized.size[0], size[0]), 
                         min(resized.size[1], size[1])))

def get_mask(size, radius, antialias=4):
    """Creates a high-quality rounded mask."""
    mask = Image.new("L", (size[0] * antialias, size[1] * antialias), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0] * antialias, size[1] * antialias), radius=radius * antialias, fill=255)
    return mask.resize(size, LANCZOS)

def load_font(path, size):
    """Safely loads fonts without crashing if missing."""
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def draw_text_with_shadow(draw, position, text, font, fill=(255, 255, 255), shadow=(0, 0, 0, 150)):
    """Draws text with a subtle shadow for premium readability."""
    x, y = position
    draw.text((x + 2, y + 2), text, fill=shadow, font=font)
    draw.text((x, y), text, fill=fill, font=font)

def format_views(view_count_str):
    """Smartly formats views to K, M, B for cleaner UI."""
    try:
        views_num = int(re.sub(r"\D", "", view_count_str))
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
    """Safely cuts long text and adds '...'"""
    clean_text = " ".join(str(text or "").split())
    if len(clean_text) <= limit:
        return clean_text
    return clean_text[: max(limit - 3, 0)].rstrip() + "..."

def draw_premium_icons(draw, cx, cy, icon, fill=(255, 255, 255)):
    """Draws sharp, proportional vector icons directly on the image."""
    if icon == "prev":
        draw.polygon([(cx + 12, cy - 14), (cx - 4, cy), (cx + 12, cy + 14)], fill=fill)
        draw.polygon([(cx - 4, cy - 14), (cx - 20, cy), (cx - 4, cy + 14)], fill=fill)
    elif icon == "pause":
        draw.rounded_rectangle([(cx - 14, cy - 18), (cx - 4, cy + 18)], radius=3, fill=fill)
        draw.rounded_rectangle([(cx + 4, cy - 18), (cx + 14, cy + 18)], radius=3, fill=fill)
    elif icon == "next":
        draw.polygon([(cx - 12, cy - 14), (cx + 4, cy), (cx - 12, cy + 14)], fill=fill)
        draw.polygon([(cx + 4, cy - 14), (cx + 20, cy), (cx + 4, cy + 14)], fill=fill)
    elif icon == "vol_down":
        draw.polygon([(cx - 6, cy - 4), (cx, cy - 4), (cx + 8, cy - 12), (cx + 8, cy + 12), (cx, cy + 4), (cx - 6, cy + 4)], fill=fill)
    elif icon == "vol_up":
        draw.polygon([(cx - 12, cy - 5), (cx - 4, cy - 5), (cx + 4, cy - 13), (cx + 4, cy + 13), (cx - 4, cy + 5), (cx - 12, cy + 5)], fill=fill)
        draw.arc([(cx - 2, cy - 8), (cx + 10, cy + 8)], start=-60, end=60, fill=fill, width=3)
        draw.arc([(cx - 6, cy - 16), (cx + 18, cy + 16)], start=-50, end=50, fill=fill, width=3)

# ----------------- MAIN THUMBNAIL GENERATOR ----------------- #

async def get_thumb(videoid, user_id=None):
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_path = os.path.join(CACHE_DIR, f"{videoid}_{user_id}_premium_ui.png")
    
    if os.path.isfile(cache_path):
        return cache_path

    url = f"https://www.youtube.com/watch?v={videoid}"
    temp_thumb_path = os.path.join(CACHE_DIR, f"thumb_{videoid}.png")

    try:
        # 1. Fetch High-Quality Data from YouTube
        results = VideosSearch(url, limit=1)
        results_data = (await results.next()).get("result", [])
        if not results_data:
            return YOUTUBE_IMG_URL

        result = results_data[0]
        title = trim_text(re.sub(r"[^\w\s&\-']", " ", result.get("title", "")).strip(), 30)
        duration = str(result.get("duration") or "00:00")
        views_str = format_views((result.get("viewCount") or {}).get("text") or "0")
        channel = trim_text(str((result.get("channel") or {}).get("name") or "Unknown Artist"), 30)
        
        # Get highest quality thumbnail available
        thumbnails = result.get("thumbnails", [{}])
        thumbnail_url = thumbnails[-1].get("url", thumbnails[0].get("url", "")).split("?")[0]

        # 2. Download Thumbnail Safely
        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail_url) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(temp_thumb_path, mode="wb")
                    await f.write(await resp.read())
                    await f.close()
                else:
                    return YOUTUBE_IMG_URL

        # 3. Create Premium Base Layout
        source_image = Image.open(temp_thumb_path).convert("RGBA")
        
        # Super smooth blurred background
        background = fit_cover(source_image, CANVAS_SIZE)
        background = background.filter(ImageFilter.GaussianBlur(40))
        background = ImageEnhance.Brightness(background).enhance(0.4)
        background = ImageEnhance.Color(background).enhance(0.8)
        
        # Add a dark gradient overlay to make text pop guaranteed
        overlay = Image.new("RGBA", CANVAS_SIZE, (15, 15, 15, 140))
        scene = Image.alpha_composite(background, overlay)
        draw = ImageDraw.Draw(scene)
        
        # 4. Load Fonts
        font_huge = load_font(TITLE_FONT_PATH, 48)
        font_large = load_font(TITLE_FONT_PATH, 34)
        font_med = load_font(META_FONT_PATH, 24)
        font_small = load_font(META_FONT_PATH, 18)

        # --------------------------------------------------
        # LEFT SIDE: ART CARD WITH PREMIUM DROP SHADOW
        # --------------------------------------------------
        art_size = 540
        art_x, art_y = 60, 90
        
        art_content = fit_cover(source_image, (art_size, art_size))
        art_mask = get_mask((art_size, art_size), 45)
        
        # Apply mask and subtle border
        left_panel = Image.new("RGBA", (art_size, art_size), (0,0,0,0))
        left_panel.paste(art_content, (0,0), art_mask)
        ImageDraw.Draw(left_panel).rounded_rectangle((0, 0, art_size-1, art_size-1), radius=45, outline=(255, 255, 255, 40), width=2)
        
        # Draw floating text on art card
        overlay_draw = ImageDraw.Draw(left_panel)
        draw_text_with_shadow(overlay_draw, (35, art_size - 90), f"{views_str}", font_large)
        draw_text_with_shadow(overlay_draw, (35, art_size - 45), "VIEWS", font_med, fill=(220, 220, 220))
        
        # Add cinematic deep shadow behind the art card
        shadow = Image.new("RGBA", CANVAS_SIZE, (0,0,0,0))
        ImageDraw.Draw(shadow).rounded_rectangle((art_x + 15, art_y + 25, art_x + art_size - 5, art_y + art_size + 15), radius=45, fill=(0,0,0, 200))
        scene = Image.alpha_composite(scene, shadow.filter(ImageFilter.GaussianBlur(25)))
        scene.paste(left_panel, (art_x, art_y), left_panel)
        
        # Re-initialize draw
        draw = ImageDraw.Draw(scene)

        # --------------------------------------------------
        # RIGHT SIDE: SPOTIFY-STYLE PLAYBACK UI
        # --------------------------------------------------
        right_x = 660
        right_w = 1220
        
        # Titles and Channel
        draw_text_with_shadow(draw, (right_x, 160), title, font_huge)
        draw_text_with_shadow(draw, (right_x, 230), channel, font_med, fill=(190, 200, 210))
        
        # Icons Top Right
        draw.ellipse([(1120, 165), (1160, 205)], fill=(255, 255, 255, 40))
        draw_text_with_shadow(draw, (1130, 175), "★", load_font(META_FONT_PATH, 28))
        
        draw.ellipse([(1180, 165), (1220, 205)], fill=(255, 255, 255, 40))
        for i in range(3):
            draw.ellipse([(1198, 176 + (i*9)), (1203, 181 + (i*9))], fill=(255, 255, 255))

        # Premium Progress Bar
        bar_y = 330
        draw.rounded_rectangle([(right_x, bar_y), (right_w, bar_y + 6)], radius=3, fill=(255, 255, 255, 60))
        
        # Simulated Progress (30%)
        prog_x = right_x + int((right_w - right_x) * 0.30)
        draw.rounded_rectangle([(right_x, bar_y), (prog_x, bar_y + 6)], radius=3, fill=(255, 255, 255))
        draw.ellipse([(prog_x - 10, bar_y - 7), (prog_x + 10, bar_y + 13)], fill=(255, 255, 255))
        
        # Timestamps
        draw_text_with_shadow(draw, (right_x, bar_y + 25), "1:05", font_small, fill=(200, 200, 200))
        duration_width = draw.textlength(f"-{duration}", font=font_small)
        draw_text_with_shadow(draw, (right_w - duration_width, bar_y + 25), f"-{duration}", font_small, fill=(200, 200, 200))

        # Media Controls
        ctrl_y = 470
        draw_premium_icons(draw, right_x + 100, ctrl_y, "prev")
        draw_premium_icons(draw, (right_x + right_w) // 2, ctrl_y, "pause")
        draw_premium_icons(draw, right_w - 100, ctrl_y, "next")

        # Volume Controls
        vol_y = 600
        draw_premium_icons(draw, right_x + 15, vol_y, "vol_down", fill=(200, 200, 200))
        draw.rounded_rectangle([(right_x + 50, vol_y - 2), (right_w - 45, vol_y + 2)], radius=2, fill=(255, 255, 255, 50))
        draw.rounded_rectangle([(right_x + 50, vol_y - 2), (right_w - 150, vol_y + 2)], radius=2, fill=(255, 255, 255))
        draw_premium_icons(draw, right_w - 10, vol_y, "vol_up", fill=(200, 200, 200))

        # Final Cleanup
        try:
            os.remove(temp_thumb_path)
        except:
            pass

        scene.save(cache_path)
        return cache_path

    except Exception as e:
        LOGGER.error(f"Thumbnail Error: {e}")
        return YOUTUBE_IMG_URL
        
