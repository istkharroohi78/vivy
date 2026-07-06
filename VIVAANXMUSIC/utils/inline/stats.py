import random
from pyrogram.enums import ButtonStyle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# 🎨 Dynamic Color Generator
def get_style_map():
    styles = [ButtonStyle.PRIMARY, ButtonStyle.SUCCESS, ButtonStyle.DANGER]
    random.shuffle(styles)
    return {1: styles[0], 2: styles[1], 3: styles[2], 4: styles[0]}


def stats_buttons(_, status):
    sm = get_style_map()
    
    not_sudo = [
        InlineKeyboardButton(
            text=_["SA_B_1"],
            callback_data="TopOverall",
            style=sm[1]
        )
    ]
    
    sudo = [
        InlineKeyboardButton(
            text=_["SA_B_2"],
            callback_data="bot_stats_sudo",
            style=sm[1]
        ),
        InlineKeyboardButton(
            text=_["SA_B_3"],
            callback_data="TopOverall",
            style=sm[2]
        ),
    ]
    
    upl = InlineKeyboardMarkup(
        [
            sudo if status else not_sudo,
            [
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                    style=sm[3]
                ),
            ],
        ]
    )
    return upl


def back_stats_buttons(_):
    sm = get_style_map()
    
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data="stats_back",
                    style=sm[1]
                ),
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                    style=sm[3]
                ),
            ],
        ]
    )
    return upl
