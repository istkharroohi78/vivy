import random
from typing import Union
from pyrogram.enums import ButtonStyle
from pyrogram.types import InlineKeyboardButton

# 🎨 Dynamic Color Generator
def get_style_map():
    styles = [ButtonStyle.PRIMARY, ButtonStyle.SUCCESS, ButtonStyle.DANGER]
    random.shuffle(styles)
    return {1: styles[0], 2: styles[1], 3: styles[2], 4: styles[0]}


def setting_markup(_):
    sm = get_style_map()
    buttons = [
        [
            InlineKeyboardButton(text=_["ST_B_1"], callback_data="AU", style=sm[1]),
            InlineKeyboardButton(text=_["ST_B_3"], callback_data="LG", style=sm[2]),
        ],
        [
            InlineKeyboardButton(text=_["ST_B_2"], callback_data="PM", style=sm[3]),
        ],
        [
            InlineKeyboardButton(text=_["ST_B_4"], callback_data="VM", style=sm[1]),
        ],
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", style=sm[3]),
        ],
    ]
    return buttons


def vote_mode_markup(_, current, mode: Union[bool, str] = None):
    sm = get_style_map()
    buttons = [
        [
            InlineKeyboardButton(text="Vᴏᴛɪɴɢ ᴍᴏᴅᴇ ➜", callback_data="VOTEANSWER", style=sm[1]),
            InlineKeyboardButton(
                text=_["ST_B_5"] if mode == True else _["ST_B_6"],
                callback_data="VOMODECHANGE",
                style=sm[2]
            ),
        ],
        [
            InlineKeyboardButton(text="-2", callback_data="FERRARIUDTI M", style=sm[3]),
            InlineKeyboardButton(
                text=f"ᴄᴜʀʀᴇɴᴛ : {current}",
                callback_data="ANSWERVOMODE",
                style=sm[1]
            ),
            InlineKeyboardButton(text="+2", callback_data="FERRARIUDTI A", style=sm[2]),
        ],
        [
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data="settings_helper",
                style=sm[1]
            ),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", style=sm[3]),
        ],
    ]
    return buttons


def auth_users_markup(_, status: Union[bool, str] = None):
    sm = get_style_map()
    buttons = [
        [
            InlineKeyboardButton(text=_["ST_B_7"], callback_data="AUTHANSWER", style=sm[1]),
            InlineKeyboardButton(
                text=_["ST_B_8"] if status == True else _["ST_B_9"],
                callback_data="AUTH",
                style=sm[2]
            ),
        ],
        [
            InlineKeyboardButton(text=_["ST_B_1"], callback_data="AUTHLIST", style=sm[3]),
        ],
        [
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data="settings_helper",
                style=sm[1]
            ),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", style=sm[3]),
        ],
    ]
    return buttons


def playmode_users_markup(
    _,
    Direct: Union[bool, str] = None,
    Group: Union[bool, str] = None,
    Playtype: Union[bool, str] = None,
):
    sm = get_style_map()
    buttons = [
        [
            InlineKeyboardButton(text=_["ST_B_10"], callback_data="SEARCHANSWER", style=sm[1]),
            InlineKeyboardButton(
                text=_["ST_B_11"] if Direct == True else _["ST_B_12"],
                callback_data="MODECHANGE",
                style=sm[2]
            ),
        ],
        [
            InlineKeyboardButton(text=_["ST_B_13"], callback_data="AUTHANSWER", style=sm[3]),
            InlineKeyboardButton(
                text=_["ST_B_8"] if Group == True else _["ST_B_9"],
                callback_data="CHANNELMODECHANGE",
                style=sm[1]
            ),
        ],
        [
            InlineKeyboardButton(text=_["ST_B_14"], callback_data="PLAYTYPEANSWER", style=sm[2]),
            InlineKeyboardButton(
                text=_["ST_B_8"] if Playtype == True else _["ST_B_9"],
                callback_data="PLAYTYPECHANGE",
                style=sm[3]
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data="settings_helper",
                style=sm[1]
            ),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", style=sm[3]),
        ],
    ]
    return buttons
