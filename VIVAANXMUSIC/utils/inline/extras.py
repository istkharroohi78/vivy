import random
from pyrogram.enums import ButtonStyle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import SUPPORT_CHAT


# 🎨 Dynamic Color Generator
def get_style_map():
    styles = [ButtonStyle.PRIMARY, ButtonStyle.SUCCESS, ButtonStyle.DANGER]
    random.shuffle(styles)
    return {1: styles[0], 2: styles[1], 3: styles[2], 4: styles[0]}


def botplaylist_markup(_):
    sm = get_style_map()
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_9"], 
                url=SUPPORT_CHAT,
                style=sm[1]
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"], 
                callback_data="close",
                style=sm[3]
            ),
        ],
    ]
    return buttons


def close_markup(_):
    sm = get_style_map()
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                    style=sm[3]
                ),
            ]
        ]
    )
    return upl


def supp_markup(_):
    sm = get_style_map()
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["S_B_9"],
                    url=SUPPORT_CHAT,
                    style=sm[1]
                ),
            ]
        ]
    )
    return upl
