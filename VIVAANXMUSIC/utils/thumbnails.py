import asyncio
import os
import re
import uuid
import math
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from youtubesearchpython.__future__ import VideosSearch

# अपनी फाइल्स के हिसाब से इन्हें कन्फर्म कर लें
from config import YOUTUBE_IMG_URL
from VIVAANXMUSIC.core.dir import CACHE_DIR

LOGGER = __import__('logging').getLogger(__name__)

# 🟢 PILLOW COMPATIBILITY FIX
try:
    LANCZOS = Image.Resampling.LANCZOS
except AttributeError:
    LANCZOS = Image.LANCZOS

# 🟢 FONTS SETUP (सुनिश्चित करें कि यह पाथ सही हो)
TITLE_FONT_PATH = "VIVAANXMUSIC/assets/thumb/font2.ttf"
META_FONT_PATH = "VIVAANXMUSIC/assets/thumb/font.ttf"
CANVAS_SIZE = (1280, 720)

# ----------------- HELPER FUNCTIONS ----------------- #

def fit_cover(image, size):
    """इमेज को बिना स्ट्रेच किए परफेक्ट साइज़ में क्रॉप करता है।"""
    ratio = max(size[0] / image.size[0], size[1] / image.size[1])
    new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
    resized = image.resize(new_size, LANCZOS)
    
    left = (new_size[0] - size[0]) // 2
    top = (new_size[1] - size[1]) // 2
    right = left + size[0]
    bottom = top + size[1]
    
    return resized.crop((left, top, right, bottom))

def get_mask(size, radius, antialias=4):
    """स्मूथ और राउंडेड कॉर्नर्स के लिए मास्क जनरेट करता है।"""
    mask = Image.new("L", (size[0] * antialias, size[1] * antialias), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0] * antialias, size[1] * antialias), radius=radius * antialias, fill=255)
    return mask.resize(size, LANCZOS)

def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def format_views(view_count_str):
    """Views को शॉर्ट फॉर्म (K, M, B) में बदलता है।"""
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
    """परफेक्ट स्टार शेप ड्रा करने के लिए।"""
    points = []
    for i in range(10):
        angle = i * math.pi / 5 - math.pi / 2
        radius = size if i % 2 == 0 else size * 0.4
        points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    draw.polygon(points, fill=fill)
    
def draw_exact_icons(draw, cx, cy, icon, fill=(255, 255, 255)):
    """इन आइकॉन्स को अब और भी शार्प और परफेक्ट अलाइनमेंट के साथ सेट किया गया है।"""
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
    
    # 🟢 AUTOPLAY FIX: टेम्परेरी फाइल्स के लिए यूनिक नाम
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
