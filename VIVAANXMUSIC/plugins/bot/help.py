from typing import Union
import random, config 
from pyrogram import filters, types, Client, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, InputMediaPhoto
from VIVAANXMUSIC import app
from VIVAANXMUSIC.utils import help_pannel
from VIVAANXMUSIC.utils.database import get_lang
from VIVAANXMUSIC.utils.decorators.language import LanguageStart, languageCB
from VIVAANXMUSIC.utils.inline.help import help_back_markup, private_help_panel
from config import BANNED_USERS, START_IMG_URL, SUPPORT_CHAT
from strings import get_string, helpers

# ====== AUTO FIX (IMPORTANT) ======
if not hasattr(helpers, "HELP_ABOUT"):
    helpers.HELP_ABOUT = "🤖 Hello {0}"

if not hasattr(helpers, "HELP_SUPPORT"):
    helpers.HELP_SUPPORT = "🛠 Hello {0}"

for i in range(1, 16):
    if not hasattr(helpers, f"HELP_{i}"):
        setattr(helpers, f"HELP_{i}", f"Help section {i}")
# =================================

START_IMG = [
    "https://files.catbox.moe/x5lytj.jpg",
    "https://files.catbox.moe/psya34.jpg",
    "https://files.catbox.moe/leaexg.jpg",
    "https://files.catbox.moe/b0e4vk.jpg",
    "https://files.catbox.moe/1b1wap.jpg",
    "https://files.catbox.moe/ommjjk.jpg",
    "https://files.catbox.moe/onurxm.jpg",
    "https://files.catbox.moe/97v75k.jpg",
    "https://files.catbox.moe/t833zy.jpg",
    "https://files.catbox.moe/472piq.jpg",
    "https://files.catbox.moe/qwjeyk.jpg",
    "https://files.catbox.moe/t0hopv.jpg",
    "https://files.catbox.moe/u5ux0j.jpg",
    "https://files.catbox.moe/h1yk4w.jpg",
    "https://files.catbox.moe/gl5rg8.jpg",
]


class BUTTONS(object):
    ABUTTON = [
        [
            InlineKeyboardButton("˹ sυᴘᴘσʀᴛ ˼", url="https://t.me/+odmRO_JAHs85YWNh"),
            InlineKeyboardButton("˹ υᴘᴅᴧᴛєs ˼", url="https://t.me/+odmRO_JAHs85YWNh")
        ],
        [
            InlineKeyboardButton("˹ ❍ᴡηєʀ ˼", user_id=config.OWNER_ID),
            InlineKeyboardButton("• ʙᴧᴄᴋ •", callback_data="settingsback_helper")
        ]
    ]

    INFO_BUTTON = [
        [
            InlineKeyboardButton("˹ ʀєᴘσ ˼", callback_data="gib_source"),
            InlineKeyboardButton("˹ ʏᴛ-ᴀᴘɪ ˼", callback_data="bot_info_data"),
            InlineKeyboardButton("˹ ʟᴧηɢᴜᴧɢє ˼", callback_data="LG"),
        ],
        [
                    InlineKeyboardButton("• ʙᴧᴄᴋ •", callback_data="settingsback_helper"),
        ]
    ]


@app.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
async def helper_private(client: app, update: Union[types.Message, types.CallbackQuery]):
    is_callback = isinstance(update, types.CallbackQuery)

    if is_callback:
        try:
            await update.answer()
        except:
            pass

        chat_id = update.message.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)
        keyboard = help_pannel(_, True)

        await update.edit_message_text(
            _["help_1"].format(SUPPORT_CHAT),
            reply_markup=keyboard
        )
    else:
        try:
            await update.delete()
        except:
            pass

        language = await get_lang(update.chat.id)
        _ = get_string(language)
        keyboard = help_pannel(_)

        await update.reply_photo(
            photo=START_IMG_URL,
            caption=_["help_1"].format(SUPPORT_CHAT),
            reply_markup=keyboard,
        )


@app.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(_["help_2"], reply_markup=InlineKeyboardMarkup(keyboard))


@app.on_callback_query(filters.regex("abot_cb") & ~BANNED_USERS)
async def about_cb(client, CallbackQuery):
    bot = await client.get_me()
    bot_mention = bot.mention

    await CallbackQuery.edit_message_text(
        helpers.HELP_ABOUT.format(bot_mention),
        reply_markup=InlineKeyboardMarkup(BUTTONS.INFO_BUTTON),
    )


@app.on_callback_query(filters.regex("sbot_cb") & ~BANNED_USERS)
async def support_cb(client, CallbackQuery):
    bot = await client.get_me()
    bot_mention = bot.mention

    await CallbackQuery.edit_message_text(
        helpers.HELP_SUPPORT.format(bot_mention),
        reply_markup=InlineKeyboardMarkup(BUTTONS.ABUTTON),
    )


@app.on_callback_query(filters.regex("back_cb") & ~BANNED_USERS)
async def back_cb(client, CallbackQuery):
    photo = random.choice(START_IMG)
    bot = await client.get_me()
    bot_mention = bot.mention

    await CallbackQuery.edit_message_media(
        media=InputMediaPhoto(
            media=photo,
            caption=helpers.HELP_ABOUT.format(bot_mention)
        ),
        reply_markup=InlineKeyboardMarkup(BUTTONS.INFO_BUTTON)
    )


@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    keyboard = help_back_markup(_)

    if cb.startswith("hb"):
        num = cb.replace("hb", "")
        text = getattr(helpers, f"HELP_{num}", "Help section")
        await CallbackQuery.edit_message_text(text, reply_markup=keyboard)
    
