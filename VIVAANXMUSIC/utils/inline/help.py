import random
from typing import Union
from pyrogram.enums import ButtonStyle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from VIVAANXMUSIC import app


# 🎨 Dynamic Color Generator (Uniform color per panel render)
def get_dynamic_style():
    """
    Returns two styles: 
    1. grid_style (Applied to all main category buttons so they match)
    2. bottom_style (Applied to the bottom navigation buttons like Back/Close)
    Every time the panel is called, these colors will shuffle.
    """
    styles = [ButtonStyle.PRIMARY, ButtonStyle.SUCCESS, ButtonStyle.DANGER]
    random.shuffle(styles)
    return styles[0], styles[1]


def help_pannel(_, START: Union[bool, int] = None):
    # Fetch the randomized uniform colors for this specific menu load
    grid_style, bottom_style = get_dynamic_style()
    
    first = [InlineKeyboardButton(text="✯ CĿΘSЄ ✯", callback_data=f"close", style=bottom_style)]
    second = [
        InlineKeyboardButton(
            text="≡ BΛCK ≡",
            callback_data=f"settingsback_helper",
            style=bottom_style
        ),
    ]
    mark = second if START else first
    
    # 5x3 Grid exactly like the reference photo
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="ΛDMIη", callback_data="help_callback hb1", style=grid_style),
                InlineKeyboardButton(text="ΛUTH", callback_data="help_callback hb2", style=grid_style),
                InlineKeyboardButton(text="G-CΛST", callback_data="help_callback hb3", style=grid_style),
            ],
            [
                InlineKeyboardButton(text="BL-CHΛT", callback_data="help_callback hb4", style=grid_style),
                InlineKeyboardButton(text="BL-USЄR", callback_data="help_callback hb5", style=grid_style),
                InlineKeyboardButton(text="C-PLΛY", callback_data="help_callback hb6", style=grid_style),
            ],
            [
                InlineKeyboardButton(text="G-BΛη", callback_data="help_callback hb7", style=grid_style),
                InlineKeyboardButton(text="LΘΘP", callback_data="help_callback hb8", style=grid_style),
                InlineKeyboardButton(text="ΛUTΘ-PLΛY", callback_data="help_callback hb9", style=grid_style),
            ],
            [
                InlineKeyboardButton(text="PIηG", callback_data="help_callback hb10", style=grid_style),
                InlineKeyboardButton(text="PLΛY", callback_data="help_callback hb11", style=grid_style),
                InlineKeyboardButton(text="SHUFFLЄ", callback_data="help_callback hb12", style=grid_style),
            ],
            [
                InlineKeyboardButton(text="SЄЄK", callback_data="help_callback hb13", style=grid_style),
                InlineKeyboardButton(text="SΘηG", callback_data="help_callback hb14", style=grid_style),
                InlineKeyboardButton(text="SPЄЄD", callback_data="help_callback hb15", style=grid_style),
            ],
            mark,
        ]
    )
    return upl


def help_back_markup(_):
    grid_style, bottom_style = get_dynamic_style()
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="≡ BΛCK ≡",
                    callback_data=f"settings_back_helper",
                    style=bottom_style
                ),
            ]
        ]
    )
    return upl


def private_help_panel(_):
    grid_style, bottom_style = get_dynamic_style()
    buttons = [
        [
            InlineKeyboardButton(
                text="HЄLP ɅИD CΘMMɅИDS",
                url=f"https://t.me/{app.username}?start=help",
                style=grid_style
            ),
        ],
    ]
    return buttons
