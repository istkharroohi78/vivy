import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# ======================================================
# 🔑 Core Credentials
API_ID = int(getenv("API_ID", "24168862"))
API_HASH = getenv("API_HASH", "916a9424dd1e58ab7955001ccc0172b3")
BOT_TOKEN = getenv("BOT_TOKEN")

# ======================================================
# 👤 Owner / Bot Info
OWNER_ID = int(getenv("OWNER_ID", 7473021518))
OWNER_USERNAME = getenv("OWNER_USERNAME", "TheSigmacoder")
BOT_USERNAME = getenv("BOT_USERNAME", "SonaliMusicBot")
BOT_NAME = getenv("BOT_NAME", "Sonali Music")
ASSUSERNAME = getenv("ASSUSERNAME")

# ======================================================
# 🗄 Database / Logger
MONGO_DB_URI = getenv("MONGO_DB_URI")
LOGGER_ID = int(getenv("LOGGER_ID", "-1003834337399"))

# 🔥 Error logging fix
DEBUG_IGNORE_LOG = getenv("DEBUG_IGNORE_LOG", "False").lower() == "true"

# ======================================================
# 🔥 Sudo Users (IMPORTANT FIX)
AYU = [OWNER_ID]

# ======================================================
# 🌐 External APIs
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
YTPROXY_URL = getenv("YTPROXY_URL", "https://tgapi.xbitcode.com")
YT_API_KEY = getenv("YT_API_KEY", "xbit_gzlb5IbFpZZ_nIFsU7kDuM0-IokPM6Db")

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
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/TEAM-ISTKHAR/vivy")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv("GIT_TOKEN")

# ======================================================
# 📢 Support
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/IamIstkhar")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/THUNDERDEVS")

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
# 🖼 Images
START_IMG_URL = getenv("START_IMG_URL", "https://files.catbox.moe/x5lytj.jpg")
PING_IMG_URL = getenv("PING_IMG_URL", "https://files.catbox.moe/leaexg.jpg")

# 🔥 FIX (missing vars)
PING_VID_URL = PING_IMG_URL
START_VID_URL = START_IMG_URL

PLAYLIST_IMG_URL = "https://files.catbox.moe/b0e4vk.jpg"
STATS_IMG_URL = "https://files.catbox.moe/psya34.jpg"

# ======================================================
# ⚙️ Runtime
BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

# ======================================================
# ⏱ Time Converter
def time_to_seconds(time: str) -> int:
    return sum(int(x) * 60**i for i, x in enumerate(reversed(time.split(":"))))

DURATION_LIMIT = time_to_seconds(f"{DURATION_LIMIT_MIN}:00")

# ======================================================
# 🎭 UI / Messages
AYU_EMOJIS = ["💞","🦋","🔍","🧪","⚡️","🔥","🎩","🌈","🍷","🥂","🥃","🕊️","🪄","💌","🧨"]

AYU_MESSAGES = [
    "ʜᴇʟʟᴏ {0}, 🥀\n\nɪᴛ'ꜱ {1}",
    "ʜɪɪ {0}, ɪ'ᴍ {1} 🎵"
]

# ======================================================
# 🔒 Validation
if SUPPORT_CHANNEL and not re.match(r"(?:http|https)://", SUPPORT_CHANNEL):
    raise SystemExit("Invalid SUPPORT_CHANNEL URL")

if SUPPORT_CHAT and not re.match(r"(?:http|https)://", SUPPORT_CHAT):
    raise SystemExit("Invalid SUPPORT_CHAT URL")