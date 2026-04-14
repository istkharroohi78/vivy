import asyncio
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from VIVAANXMUSIC import app
from VIVAANXMUSIC.utils.database import get_autoplay, get_cmode, set_autoplay
from VIVAANXMUSIC.utils.decorators.admins import AdminActual
from config import BANNED_USERS


# 🎨 Fancy Buttons
def autoplay_markup():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✨ ᴇɴᴀʙʟᴇ", callback_data="autoplay_on"),
                InlineKeyboardButton("⚡ ᴅɪꜱᴀʙʟᴇ", callback_data="autoplay_off"),
            ],
            [
                InlineKeyboardButton("🔄 ʀᴇꜰʀᴇꜱʜ", callback_data="autoplay_refresh"),
                InlineKeyboardButton("✖ ᴄʟᴏꜱᴇ", callback_data="autoplay_close"),
            ]
        ]
    )


# ⏳ Auto Delete Function (non-blocking)
async def delete_later(msg):
    await asyncio.sleep(20)
    try:
        await msg.delete()
    except:
        pass


# 🎛 Command Handler
@app.on_message(filters.command(["autoplay", "cautoplay"]) & filters.group & ~BANNED_USERS)
@AdminActual
async def autoplay_control(_, message: Message, strings):

    command = message.command[0].lower()

    # Channel mode check
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

    msg = await message.reply_text(
        f"🎛 **ᴀᴜᴛᴏᴘʟᴀʏ ᴄᴏɴᴛʀᴏʟ ᴘᴀɴᴇʟ**\n\n"
        f"➻ ꜱᴛᴀᴛᴜꜱ : {status}\n\n"
        f"⟢ ᴜꜱᴇ ʙᴜᴛᴛᴏɴꜱ ʙᴇʟᴏᴡ ᴛᴏ ᴄᴏɴᴛʀᴏʟ",
        reply_markup=autoplay_markup()
    )

    # 🔥 Auto delete after 20 sec (non-blocking)
    asyncio.create_task(delete_later(msg))


# 🔘 Button Handler
@app.on_callback_query(filters.regex("^autoplay_"))
async def autoplay_buttons(client, callback_query):

    data = callback_query.data
    chat_id = callback_query.message.chat.id

    if data == "autoplay_on":
        await set_autoplay(chat_id, True)

    elif data == "autoplay_off":
        await set_autoplay(chat_id, False)

    elif data == "autoplay_refresh":
        pass

    elif data == "autoplay_close":
        return await callback_query.message.delete()

    else:
        return

    await callback_query.answer("ᴜᴘᴅᴀᴛᴇᴅ ✓")

    status = "✨ ᴇɴᴀʙʟᴇᴅ" if await get_autoplay(chat_id) else "⚡ ᴅɪꜱᴀʙʟᴇᴅ"

    msg = await callback_query.message.edit_text(
        f"🎛 **ᴀᴜᴛᴏᴘʟᴀʏ ᴄᴏɴᴛʀᴏʟ ᴘᴀɴᴇʟ**\n\n"
        f"➻ ꜱᴛᴀᴛᴜꜱ : {status}\n\n"
        f"⟢ ᴜꜱᴇ ʙᴜᴛᴛᴏɴꜱ ʙᴇʟᴏᴡ ᴛᴏ ᴄᴏɴᴛʀᴏʟ",
        reply_markup=autoplay_markup()
    )

    # 🔥 Auto delete after 20 sec again
    asyncio.create_task(delete_later(msg))