import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# ======================================================
# 🔑 Core
API_ID = int(getenv("API_ID", "24168862"))
API_HASH = getenv("API_HASH", "916a9424dd1e58ab7955001ccc0172b3")
BOT_TOKEN = getenv("BOT_TOKEN")

# ======================================================
# 👤 Owner / Bot
OWNER_ID = int(getenv("OWNER_ID", 8723235165))
OWNER_USERNAME = getenv("OWNER_USERNAME", "ll_alexx_lll")
BOT_USERNAME = getenv("BOT_USERNAME", "Kavya_Music_RoBot")
BOT_NAME = getenv("BOT_NAME", "Kavya Music")
ASSUSERNAME = getenv("ASSUSERNAME")

# ======================================================
# 🗄 DB / Logs
MONGO_DB_URI = getenv("MONGO_DB_URI")
LOGGER_ID = int(getenv("LOGGER_ID", "-1003834337399"))

DEBUG_IGNORE_LOG = getenv("DEBUG_IGNORE_LOG", "False").lower() == "true"

# ======================================================
# ───── Bot Introduction Messages ───── #
AYU = ["💞", "🦋", "🔍", "🧪", "⚡️", "🔥", "🎩", "🌈", "🍷", "🥂", "🥃", "🕊️", "🪄", "💌", "🧨"]

# ======================================================
# 🌐 APIs
API_URL = getenv("API_URL")
API_KEY = getenv("API_KEY")
DEEP_API = getenv("DEEP_API")
REPLICATE_API_TOKEN = getenv("REPLICATE_API_TOKEN")
REPLICATE_API_TOKENS = getenv("REPLICATE_API_TOKENS", "")
HF_TOKEN = getenv("HF_TOKEN")
HF_TOKENS = getenv("HF_TOKENS", "")
OCR_SPACE_API_KEY = getenv("OCR_SPACE_API_KEY", "helloworld")

# ======================================================
# 🎵 Music API
# ✅ JioSaavn Working API Added Here
JIOSAAVN_API = getenv("JIOSAAVN_API", "https://saavn.me/search/songs?query=")

# ----------------- API RACING CONFIGURATION -----------------
# 1. Shruti API
API_URL = getenv("API_URL", "https://api.shrutibots.site")
API_KEY = getenv("API_KEY", "ShrutiBotsC0WH1GowF2HkGoKv4F3y")

# 2. Xbit API
YTPROXY_URL = getenv("YTPROXY_URL", "https://tgapi.xbitcode.com")
YT_API_KEY = getenv("YT_API_KEY" , "xbit_B4TNnBAoe6uoSM7NLFz-dk6X7GibJ6Bh")

# 3. Worker API
WORKER_FALLBACK_API_URL = getenv("WORKER_FALLBACK_API_URL", "https://youtubenewapi.skybotsdeveloper.workers.dev")
WORKER_FALLBACK_API_KEY = getenv("WORKER_FALLBACK_API_KEY", "itsmesid")

# 4. Inflex API
INFLEX_API_URL = getenv("INFLEX_API_URL", "https://teaminflex.xyz")
INFLEX_API_KEY = getenv("INFLEX_API_KEY", "INFLEX40920628D")


# ======================================================
# 🎧 Limits
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 17000))
SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION", "9999999"))
SONG_DOWNLOAD_DURATION_LIMIT = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "9999999"))
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", "5242880000"))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", "5242880000"))

# ======================================================
# 🤖 Assistant
AUTO_LEAVING_ASSISTANT = getenv("AUTO_LEAVING_ASSISTANT", "False")
AUTO_LEAVE_ASSISTANT_TIME = int(getenv("ASSISTANT_LEAVE_TIME", "9000"))

# ======================================================
# ☁️ Heroku
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

# ======================================================
# 🔄 Repo
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/istkharroohi78/vivy")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv("GIT_TOKEN")

# ======================================================
# 📢 Support
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/betabot_hub")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/betabot_support")

# ======================================================
# 🎧 Spotify
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET")

# ======================================================
# 🔐 Sessions
STRING1 = getenv("STRING_SESSION")
STRING2 = getenv("STRING_SESSION2")
STRING3 = getenv("STRING_SESSION3")
STRING4 = getenv("STRING_SESSION4")
STRING5 = getenv("STRING_SESSION5")
STRING6 = getenv("STRING_SESSION6")
STRING7 = getenv("STRING_SESSION7")

# ======================================================
# 🖼 MEDIA / IMAGES (ALL FIXED)

START_IMG_URL = getenv("START_IMG_URL", "https://files.catbox.moe/x5lytj.jpg")
PING_IMG_URL = getenv("PING_IMG_URL", "https://files.catbox.moe/leaexg.jpg")

# 🔥 REQUIRED FIXES
PING_VID_URL = PING_IMG_URL
START_VID_URL = START_IMG_URL


HELP_IMG_URL = "https://files.catbox.moe/m3fyh9.jpg"
PING_VID_URL = "https://files.catbox.moe/p82vwn.jpg"
PLAYLIST_IMG_URL = "https://files.catbox.moe/9m0pys.jpg"
STATS_VID_URL = "https://files.catbox.moe/gq4hkk.jpg"
TELEGRAM_AUDIO_URL = "https://files.catbox.moe/p82vwn.jpg"
TELEGRAM_VIDEO_URL = "https://files.catbox.moe/mmdz7d.jpg"
STREAM_IMG_URL = "https://files.catbox.moe/3fl186.jpg"
SOUNCLOUD_IMG_URL = "https://files.catbox.moe/drua0p.jpg"
YOUTUBE_IMG_URL = "https://files.catbox.moe/0yxqt1.jpg"
SPOTIFY_ARTIST_IMG_URL = SPOTIFY_ALBUM_IMG_URL = SPOTIFY_PLAYLIST_IMG_URL = YOUTUBE_IMG_URL
# ── Helpers 
# ======================================================
# ⚙️ Runtime
BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

# ======================================================
# ⏱ Time
def time_to_seconds(time: str) -> int:
    return sum(int(x) * 60**i for i, x in enumerate(reversed(time.split(":"))))

DURATION_LIMIT = time_to_seconds(f"{DURATION_LIMIT_MIN}:00")

# ======================================================
# 🔒 Validation
if SUPPORT_CHANNEL and not re.match(r"(?:http|https)://", SUPPORT_CHANNEL):
    raise SystemExit("Invalid SUPPORT_CHANNEL URL")

if SUPPORT_CHAT and not re.match(r"(?:http|https)://", SUPPORT_CHAT):
    raise SystemExit("Invalid SUPPORT_CHAT URL")
