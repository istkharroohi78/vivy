import random
from pyrogram.enums import ButtonStyle
from pyrogram.types import InlineKeyboardButton

import config
from VIVAANXMUSIC import app

# 🎨 Dynamic Color Generator
def get_style_map():
    styles = [ButtonStyle.PRIMARY, ButtonStyle.SUCCESS, ButtonStyle.DANGER]
    random.shuffle(styles)
    return {1: styles[0], 2: styles[1], 3: styles[2], 4: styles[0]}


def start_panel(_):
    sm = get_style_map()
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"], 
                url=f"https://t.me/{app.username}?startgroup=true",
                style=sm[1]
            ),
            InlineKeyboardButton(
                text=_["S_B_2"], 
                url=config.SUPPORT_CHAT,
                style=sm[2]
            ),
        ],
    ]
    return buttons


def private_panel(_):
    sm = get_style_map()
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?startgroup=true",
                style=sm[1]
            )
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_9"], 
                callback_data="sbot_cb",
                style=sm[2]
            ),  
            InlineKeyboardButton(
                text=_["S_B_13"], 
                callback_data="abot_cb",
                style=sm[3]
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_4"], 
                callback_data="settings_back_helper",
                style=sm[1]
            ),
        ],
    ]
    return buttons
