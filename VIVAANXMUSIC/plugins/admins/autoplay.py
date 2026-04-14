from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from VIVAANXMUSIC import app
from VIVAANXMUSIC.utils.database import get_autoplay, get_cmode, set_autoplay
from VIVAANXMUSIC.utils.decorators.admins import AdminActual
from config import BANNED_USERS


# 🎨 Fancy Button UI
def autoplay_markup():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✨ ᴇɴᴀʙʟᴇ", callback_data="autoplay_on"),
                InlineKeyboardButton("⚡ ᴅɪꜱᴀʙʟᴇ", callback_data="autoplay_off"),
            ],
            [
                InlineKeyboardButton("🔄 ʀᴇꜰʀᴇꜱʜ", callback_data="autoplay_refresh")
            ]
        ]
    )


@app.on_message(filters.command(["autoplay", "cautoplay"]) & filters.group & ~BANNED_USERS)
@AdminActual
async def autoplay_control(_, message: Message, strings):

    command = message.command[0].lower()

    if command.startswith("c"):
        chat_id = await get_cmode(message.chat.id)
        if chat_id is None:
            return await message.reply_text("❌ ᴄʜᴀɴɴᴇʟ ᴍᴏᴅᴇ ɴᴏᴛ ᴇɴᴀʙʟᴇᴅ.")
        try:
            await app.get_chat(chat_id)
        except Exception:
            return await message.reply_text("❌ ɪɴᴠᴀʟɪᴅ ʟɪɴᴋᴇᴅ ᴄʜᴀɴɴᴇʟ.")
    else:
        chat_id = message.chat.id

    status = "✨ ᴇɴᴀʙʟᴇᴅ" if await get_autoplay(chat_id) else "⚡ ᴅɪꜱᴀʙʟᴇᴅ"

    await message.reply_text(
        f"🎛 **ᴀᴜᴛᴏᴘʟᴀʏ ᴄᴏɴᴛʀᴏʟ ᴘᴀɴᴇʟ**\n\n"
        f"➻ ꜱᴛᴀᴛᴜꜱ : {status}\n\n"
        f"⟢ ᴜꜱᴇ ʙᴜᴛᴛᴏɴꜱ ʙᴇʟᴏᴡ ᴛᴏ ᴄᴏɴᴛʀᴏʟ",
        reply_markup=autoplay_markup()
    )


# 🔘 Button Handler
@app.on_callback_query(filters.regex("^autoplay_"))
async def autoplay_buttons(client, callback_query):

    data = callback_query.data
    chat_id = callback_query.message.chat.id

    if data == "autoplay_on":
        await set_autoplay(chat_id, True)
        text = "✨ ᴀᴜᴛᴏᴘʟᴀʏ ᴇɴᴀʙʟᴇᴅ"

    elif data == "autoplay_off":
        await set_autoplay(chat_id, False)
        text = "⚡ ᴀᴜᴛᴏᴘʟᴀʏ ᴅɪꜱᴀʙʟᴇᴅ"

    elif data == "autoplay_refresh":
        status = "✨ ᴇɴᴀʙʟᴇᴅ" if await get_autoplay(chat_id) else "⚡ ᴅɪꜱᴀʙʟᴇᴅ"
        return await callback_query.message.edit_text(
            f"🎛 **ᴀᴜᴛᴏᴘʟᴀʏ ᴄᴏɴᴛʀᴏʟ ᴘᴀɴᴇʟ**\n\n"
            f"➻ ꜱᴛᴀᴛᴜꜱ : {status}\n\n"
            f"⟢ ᴜꜱᴇ ʙᴜᴛᴛᴏɴꜱ ʙᴇʟᴏᴡ ᴛᴏ ᴄᴏɴᴛʀᴏʟ",
            reply_markup=autoplay_markup()
        )

    else:
        return

    await callback_query.answer("ᴜᴘᴅᴀᴛᴇᴅ ✓")

    status = "✨ ᴇɴᴀʙʟᴇᴅ" if await get_autoplay(chat_id) else "⚡ ᴅɪꜱᴀʙʟᴇᴅ"

    await callback_query.message.edit_text(
        f"🎛 **ᴀᴜᴛᴏᴘʟᴀʏ ᴄᴏɴᴛʀᴏʟ ᴘᴀɴᴇʟ**\n\n"
        f"➻ ꜱᴛᴀᴛᴜꜱ : {status}\n\n"
        f"⟢ ᴜꜱᴇ ʙᴜᴛᴛᴏɴꜱ ʙᴇʟᴏᴡ ᴛᴏ ᴄᴏɴᴛʀᴏʟ",
        reply_markup=autoplay_markup()
    )