import random
from typing import Union
from pyrogram.enums import ButtonStyle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from VIVAANXMUSIC import app


# 🎨 Dynamic Color Generator
def get_style_map():
    styles = [ButtonStyle.PRIMARY, ButtonStyle.SUCCESS, ButtonStyle.DANGER]
    random.shuffle(styles)
    return {1: styles[0], 2: styles[1], 3: styles[2], 4: styles[0]}


def help_pannel(_, START: Union[bool, int] = None):
    sm = get_style_map()
    
    first = [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"close", style=sm[3])]
    second = [
        InlineKeyboardButton(
            text=_["BACK_BUTTON"],
            callback_data=f"settingsback_helper",
            style=sm[1]
        ),
    ]
    mark = second if START else first
    
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["H_B_25"],
                    callback_data="help_callback hb1",
                    style=sm[1]
                ),
                InlineKeyboardButton(
                    text=_["H_B_26"],
                    callback_data="help_callback hb2",
                    style=sm[2]
                ),
                InlineKeyboardButton(
                    text=_["H_B_28"],
                    callback_data="help_callback hb3",
                    style=sm[3]
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["H_B_27"],
                    callback_data="help_callback hb4",
                    style=sm[3]
                ),
                InlineKeyboardButton(
                    text=_["H_B_31"],
                    callback_data="help_callback hb5",
                    style=sm[1]
                ),
                InlineKeyboardButton(
                    text=_["H_B_29"],
                    callback_data="help_callback hb6",
                    style=sm[2]
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["H_B_33"],
                    callback_data="help_callback hb7",
                    style=sm[2]
                ),
                InlineKeyboardButton(
                    text=_["H_B_30"],
                    callback_data="help_callback hb8",
                    style=sm[3]
                ),
                InlineKeyboardButton(
                    text=_["H_B_32"],
                    callback_data="help_callback hb9",
                    style=sm[1]
                ),
            ],
            # Autoplay Or Nightmode Button
            [
                InlineKeyboardButton(
                    text=_["H_B_34"],
                    callback_data="help_callback hb10",
                    style=sm[1]
                ),
                InlineKeyboardButton(
                    text=_["H_B_35"],
                    callback_data="help_callback hb11",
                    style=sm[2]
                ),
            ],
            mark,
        ]
    )
    return upl


def help_back_markup(_):
    sm = get_style_map()
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data=f"settings_back_helper",
                    style=sm[1]
                ),
            ]
        ]
    )
    return upl


def private_help_panel(_):
    sm = get_style_map()
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_4"],
                url=f"https://t.me/{app.username}?start=help",
                style=sm[1]
            ),
        ],
    ]
    return buttons
