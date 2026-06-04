import math
from pyrogram.types import InlineKeyboardButton
from VIVAANXMUSIC import app
from VIVAANXMUSIC.utils.formatters import time_to_seconds


# 🎵 TRACK BUTTON
def track_markup(_, videoid, user_id, channel, fplay):
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
            )
        ],
    ]


# 🎛 PLAYER WITH TIMER (NEW PROGRESS BAR)
def stream_markup_timer(_, chat_id, played, dur):
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)

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
            )
        ],

        # 🎮 Controls
        [
            InlineKeyboardButton("▷", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton("II", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton("↻", callback_data=f"ADMIN Replay|{chat_id}"),
            InlineKeyboardButton("‣‣I", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton("▢", callback_data=f"ADMIN Stop|{chat_id}"),
        ],

        # 🔥 Autoplay Row
        [
            InlineKeyboardButton(
                text="❖ 𝐀ᴜᴛᴏ𝐏ʟᴀʏ ❖", 
                callback_data=f"ADMIN Autoplay|{chat_id}"
            )
        ],

        # 🎯 Bottom Buttons
        [
            InlineKeyboardButton(
                "✚ ᴀᴅᴅ ᴍᴇ ✚",
                url=f"https://t.me/{app.username}?startgroup=true"
            ),
            InlineKeyboardButton(
                "• ᴄʟᴏꜱᴇ •",
                callback_data="close"
            ),
        ],
    ]
    return buttons


# 🎛 PLAYER WITHOUT TIMER
def stream_markup(_, chat_id):
    return [
        # 🎮 Controls
        [
            InlineKeyboardButton("▷", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton("II", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton("↻", callback_data=f"ADMIN Replay|{chat_id}"),
            InlineKeyboardButton("‣‣I", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton("▢", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        # 🔥 Autoplay Row
        [
            InlineKeyboardButton(
                text="❖ 𝐀ᴜᴛᴏ𝐏ʟᴀʏ ❖", 
                callback_data=f"ADMIN Autoplay|{chat_id}"
            )
        ],
        # 🎯 Bottom Buttons
        [
            InlineKeyboardButton(
                "✚ ᴀᴅᴅ ᴍᴇ ✚",
                url=f"https://t.me/{app.username}?startgroup=true"
            ),
            InlineKeyboardButton(
                "• ᴄʟᴏꜱᴇ •",
                callback_data="close"
            ),
        ],
    ]


# ❖ AUTOPLAY PANEL BUTTONS ❖
def autoplay_markup(chat_id):
    return [
        [
            InlineKeyboardButton(
                text="✨ ᴇɴᴀʙʟᴇ",
                callback_data=f"ADMIN AutoOn|{chat_id}",
            ),
            InlineKeyboardButton(
                text="⚡ ᴅɪsᴀʙʟᴇ",
                callback_data=f"ADMIN AutoOff|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔙 ʙᴀᴄᴋ ᴛᴏ ᴘʟᴀʏᴇʀ",
                callback_data=f"ADMIN AutoRefresh|{chat_id}",
            )
        ]
    ]


# 🎶 PLAYLIST
def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"ROOHIPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"ROOHIPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]


# 🔴 LIVE STREAM
def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_3"],
                callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]


# 🎚 SLIDER
def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    query = f"{query[:20]}"
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="◁",
                callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {query}|{user_id}",
            ),
            InlineKeyboardButton(
                text="▷",
                callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
        ],
    ]
