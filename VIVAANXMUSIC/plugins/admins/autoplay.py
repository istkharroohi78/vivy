import asyncio

from pyrogram import filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

from VIVAANXMUSIC import app
from VIVAANXMUSIC.utils.database import (
    get_autoplay,
    get_cmode,
    set_autoplay,
)
from VIVAANXMUSIC.utils.decorators.admins import AdminActual
from config import BANNED_USERS


#━━━━━━━━━━━ PANEL BUTTONS ━━━━━━━━━━━#

def autoplay_markup():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✨ ᴇɴᴀʙʟᴇ",
                    callback_data="autoplay_on",
                ),
                InlineKeyboardButton(
                    "⚡ ᴅɪsᴀʙʟᴇ",
                    callback_data="autoplay_off",
                ),
            ],
            [
                InlineKeyboardButton(
                    "🔄 ʀᴇғʀᴇsʜ",
                    callback_data="autoplay_refresh",
                )
            ]
        ]
    )


#━━━━━━━━━━━ AUTO DELETE ━━━━━━━━━━━#

async def delete_later(msg):
    await asyncio.sleep(60)

    try:
        await msg.delete()
    except:
        pass


#━━━━━━━━━━━ PANEL TEXT ━━━━━━━━━━━#

async def panel_text(chat_id, chat_title):

    status = await get_autoplay(chat_id)

    mode = "ᴇɴᴀʙʟᴇᴅ ✅" if status else "ᴅɪsᴀʙʟᴇᴅ ❌"

    return (
        f"✙ ʌᴅᴅ ϻє вᴧʙʏ ✙\n\n"
        f"❖ ᴀᴜᴛᴏ ᴘʟᴀʏ ᴄᴏɴᴛʀᴏʟ ᴘᴀɴᴇʟ\n\n"
        f"🏵️ ɢʀᴏᴜᴘ ɪᴅ › `{chat_id}`\n"
        f"🏖️ ɢʀᴏᴜᴘ ɴᴀᴍᴇ › {chat_title}\n"
        f"🍂 ᴀᴜᴛᴏ ᴘʟᴀʏ › {mode}\n\n"
        f"❏ ᴜsᴇ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs ᴛᴏ ᴄᴏɴᴛʀᴏʟ ᴀᴜᴛᴏᴘʟᴀʏ."
    )


#━━━━━━━━━━━ COMMAND HANDLER ━━━━━━━━━━━#

@app.on_message(
    filters.command(["autoplay", "cautoplay"])
    & filters.group
    & ~BANNED_USERS
)
@AdminActual
async def autoplay_control(_, message: Message, strings):

    command = message.command[0].lower()

    #━━━━━━━━━━━ CHANNEL MODE ━━━━━━━━━━━#

    if command.startswith("c"):
        chat_id = await get_cmode(message.chat.id)

        if chat_id is None:
            return await message.reply_text(
                "❌ ᴄʜᴀɴɴᴇʟ ᴍᴏᴅᴇ ɴᴏᴛ ᴇɴᴀʙʟᴇᴅ."
            )

        try:
            await app.get_chat(chat_id)

        except Exception:
            return await message.reply_text(
                "❌ ɪɴᴠᴀʟɪᴅ ʟɪɴᴋᴇᴅ ᴄʜᴀɴɴᴇʟ."
            )

    else:
        chat_id = message.chat.id

    chat_title = message.chat.title


    #━━━━━━━━━━━ /autoplay on-off ━━━━━━━━━━━#

    if len(message.command) > 1:

        option = message.command[1].lower()

        if option in ["on", "enable", "enabled", "yes"]:

            await set_autoplay(chat_id, True)

            return await message.reply_text(
                "✅ ᴀᴜᴛᴏ ᴘʟᴀʏ ʜᴀs ʙᴇᴇɴ ᴇɴᴀʙʟᴇᴅ."
            )

        elif option in ["off", "disable", "disabled", "no"]:

            await set_autoplay(chat_id, False)

            return await message.reply_text(
                "❌ ᴀᴜᴛᴏ ᴘʟᴀʏ ʜᴀs ʙᴇᴇɴ ᴅɪsᴀʙʟᴇᴅ."
            )


    #━━━━━━━━━━━ PANEL ━━━━━━━━━━━#

    text = await panel_text(chat_id, chat_title)

    msg = await message.reply_text(
        text=text,
        reply_markup=autoplay_markup(),
    )

    asyncio.create_task(delete_later(msg))


#━━━━━━━━━━━ CALLBACK BUTTONS ━━━━━━━━━━━#

@app.on_callback_query(filters.regex("^autoplay_"))
async def autoplay_buttons(client, callback_query: CallbackQuery):

    data = callback_query.data

    chat_id = callback_query.message.chat.id
    chat_title = callback_query.message.chat.title


    #━━━━━━━━━━━ ENABLE ━━━━━━━━━━━#

    if data == "autoplay_on":

        await set_autoplay(chat_id, True)

        await callback_query.answer(
            "✅ ᴀᴜᴛᴏ ᴘʟᴀʏ ᴇɴᴀʙʟᴇᴅ",
            show_alert=True
        )


    #━━━━━━━━━━━ DISABLE ━━━━━━━━━━━#

    elif data == "autoplay_off":

        await set_autoplay(chat_id, False)

        await callback_query.answer(
            "❌ ᴀᴜᴛᴏ ᴘʟᴀʏ ᴅɪsᴀʙʟᴇᴅ",
            show_alert=True
        )


    #━━━━━━━━━━━ REFRESH ━━━━━━━━━━━#

    elif data == "autoplay_refresh":

        await callback_query.answer(
            "🔄 ᴘᴀɴᴇʟ ʀᴇғʀᴇsʜᴇᴅ"
        )

    else:
        return


    #━━━━━━━━━━━ UPDATE PANEL ━━━━━━━━━━━#

    text = await panel_text(chat_id, chat_title)

    await callback_query.message.edit_text(
        text=text,
        reply_markup=autoplay_markup(),
    )
