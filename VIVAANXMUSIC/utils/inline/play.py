import math
import random
from pyrogram.enums import ButtonStyle
from pyrogram.types import InlineKeyboardButton
from VIVAANXMUSIC import app
from VIVAANXMUSIC.utils.formatters import time_to_seconds

# 🎨 Dynamic Color Generator
def get_style_map():
    styles = [ButtonStyle.PRIMARY, ButtonStyle.SUCCESS, ButtonStyle.DANGER]
    random.shuffle(styles)
    return {1: styles[0], 2: styles[1], 3: styles[2], 4: styles[0]}


# 🎵 TRACK BUTTON
def track_markup(_, videoid, user_id, channel, fplay):
    sm = get_style_map()
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
                style=sm[1]
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
                style=sm[2]
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
                style=sm[3]
            )
        ],
    ]


# 🎛 PLAYER WITH TIMER (NEW PROGRESS BAR)
def stream_markup_timer(_, chat_id, played, dur):
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    sm = get_style_map()

    # 🔥 Progress Bar ▰▱
    total_blocks = 10
    filled_blocks = int((played_sec / duration_sec) * total_blocks) if duration_sec != 0 else 0
    bar = "▰" * filled_blocks + "▱" * (total_blocks - filled_blocks)

    buttons = [
        # ⏱ Timer + Bar
        [
            InlineKeyboardButton(
                text=f"{played} {bar} {dur}",
                callback_data="GetTimer",
                style=sm[1]
            )
        ],

        # 🎮 Controls
        [
            InlineKeyboardButton("▷", callback_data=f"ADMIN Resume|{chat_id}", style=sm[1]),
            InlineKeyboardButton("II", callback_data=f"ADMIN Pause|{chat_id}", style=sm[2]),
            InlineKeyboardButton("↻", callback_data=f"ADMIN Replay|{chat_id}", style=sm[3]),
            InlineKeyboardButton("‣‣I", callback_data=f"ADMIN Skip|{chat_id}", style=sm[4]),
            InlineKeyboardButton("▢", callback_data=f"ADMIN Stop|{chat_id}", style=sm[1]),
        ],

        # 🔥 Autoplay Row
        [
            InlineKeyboardButton(
                text="❖ 𝐀ᴜᴛᴏ𝐏ʟᴀʏ ❖", 
                callback_data=f"ADMIN Autoplay|{chat_id}",
                style=sm[2]
            )
        ],

        # 🎯 Bottom Buttons
        [
            InlineKeyboardButton(
                "✚ ᴀᴅᴅ ᴍᴇ ✚",
                url=f"https://t.me/{app.username}?startgroup=true",
                style=sm[1]
            ),
            InlineKeyboardButton(
                "• ᴄʟᴏꜱᴇ •",
                callback_data="close",
                style=sm[3]
            ),
        ],
    ]
    return buttons


# 🎛 PLAYER WITHOUT TIMER
def stream_markup(_, chat_id):
    sm = get_style_map()
    return [
        # 🎮 Controls
        [
            InlineKeyboardButton("▷", callback_data=f"ADMIN Resume|{chat_id}", style=sm[1]),
            InlineKeyboardButton("II", callback_data=f"ADMIN Pause|{chat_id}", style=sm[2]),
            InlineKeyboardButton("↻", callback_data=f"ADMIN Replay|{chat_id}", style=sm[3]),
            InlineKeyboardButton("‣‣I", callback_data=f"ADMIN Skip|{chat_id}", style=sm[4]),
            InlineKeyboardButton("▢", callback_data=f"ADMIN Stop|{chat_id}", style=sm[1]),
        ],
        # 🔥 Autoplay Row
        [
            InlineKeyboardButton(
                text="❖ 𝐀ᴜᴛᴏ𝐏ʟᴀʏ ❖", 
                callback_data=f"ADMIN Autoplay|{chat_id}",
                style=sm[2]
            )
        ],
        # 🎯 Bottom Buttons
        [
            InlineKeyboardButton(
                "✚ ᴀᴅᴅ ᴍᴇ ✚",
                url=f"https://t.me/{app.username}?startgroup=true",
                style=sm[1]
            ),
            InlineKeyboardButton(
                "• ᴄʟᴏꜱᴇ •",
                callback_data="close",
                style=sm[3]
            ),
        ],
    ]


# ❖ AUTOPLAY PANEL BUTTONS ❖
def autoplay_markup(chat_id):
    sm = get_style_map()
    return [
        [
            InlineKeyboardButton(
                text="✨ ᴇɴᴀʙʟᴇ",
                callback_data=f"ADMIN AutoOn|{chat_id}",
                style=sm[2]
            ),
            InlineKeyboardButton(
                text="⚡ ᴅɪsᴀʙʟᴇ",
                callback_data=f"ADMIN AutoOff|{chat_id}",
                style=sm[3]
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔙 ʙᴀᴄᴋ ᴛᴏ ᴘʟᴀʏᴇʀ",
                callback_data=f"ADMIN AutoRefresh|{chat_id}",
                style=sm[1]
            )
        ]
    ]


# 🎶 PLAYLIST
def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    sm = get_style_map()
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"ROOHIPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}",
                style=sm[1]
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"ROOHIPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}",
                style=sm[2]
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
                style=sm[3]
            ),
        ],
    ]


# 🔴 LIVE STREAM
def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    sm = get_style_map()
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_3"],
                callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}",
                style=sm[1]
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
                style=sm[3]
            ),
        ],
    ]


# 🎚 SLIDER
def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    query = f"{query[:20]}"
    sm = get_style_map()
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
                style=sm[1]
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
                style=sm[2]
            ),
        ],
        [
            InlineKeyboardButton(
                text="◁",
                callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}",
                style=sm[1]
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {query}|{user_id}",
                style=sm[3]
            ),
            InlineKeyboardButton(
                text="▷",
                callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}",
                style=sm[2]
            ),
        ],
    ]
