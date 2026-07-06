import random
from typing import Union

from pyrogram.enums import ButtonStyle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import OWNER_ID
from VIVAANXMUSIC import app
from VIVAANXMUSIC.utils.formatters import time_to_seconds


# 🎨 Dynamic Color Generator
def get_style_map():
    styles = [ButtonStyle.PRIMARY, ButtonStyle.SUCCESS, ButtonStyle.DANGER]
    random.shuffle(styles)
    return {1: styles[0], 2: styles[1], 3: styles[2], 4: styles[0]}


def queue_markup(
    _,
    DURATION,
    CPLAY,
    videoid,
    played: Union[bool, int] = None,
    dur: Union[bool, int] = None,
):
    sm = get_style_map()
    
    not_dur = [
        [
            InlineKeyboardButton(
                text=_["QU_B_1"],
                callback_data=f"GetQueued {CPLAY}|{videoid}",
                style=sm[1]
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data="close",
                style=sm[3]
            ),
        ]
    ]
    
    dur_btn = [
        [
            InlineKeyboardButton(
                text=_["QU_B_2"].format(played, dur),
                callback_data="GetTimer",
                style=sm[1]
            )
        ],
        [
            InlineKeyboardButton(
                text=_["QU_B_1"],
                callback_data=f"GetQueued {CPLAY}|{videoid}",
                style=sm[2]
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data="close",
                style=sm[3]
            ),
        ],
    ]
    
    upl = InlineKeyboardMarkup(not_dur if DURATION == "Unknown" else dur_btn)
    return upl


def queue_back_markup(_, CPLAY):
    sm = get_style_map()
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data=f"queue_back_timer {CPLAY}",
                    style=sm[1]
                ),
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                    style=sm[3]
                ),
            ]
        ]
    )
    return upl


def aq_markup(_, chat_id):
    sm = get_style_map()
    buttons = [
        [
            InlineKeyboardButton(
                text="✙ ʌᴅᴅ ϻє ɪη ʏσυʀ ɢʀσυᴘ ✙", 
                url=f"https://t.me/{app.username}?startgroup=true",
                style=sm[1]
            )
        ],
        [
            InlineKeyboardButton(
                text="⌯ ᴍᴜsɪᴄ-ʙᴏᴛ ⌯", 
                url="https://t.me/Kavya_Music_Bot",
                style=sm[2]
            ),
            InlineKeyboardButton(
                text="⌯ ᴀʟʟ-ʙᴏᴛs ⌯", 
                url="https://t.me/betabot_hub/6701",
                style=sm[3]
            ),
        ],
        [
            InlineKeyboardButton(
                text="⌯ ᴘʀᴏᴍᴏ ⌯", 
                user_id=OWNER_ID,
                style=sm[1]
            ),
            InlineKeyboardButton(
                text="⌯ ᴄʟᴏsᴇ ⌯", 
                callback_data="close",
                style=sm[3]
            ),
        ],
    ]

    return buttons
