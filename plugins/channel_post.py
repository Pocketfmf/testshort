#(©)Codexbotz

import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from .linkshortner import Short,linkshortx
from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON
from helper_func import encode

@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['start','users','broadcast','batch','genlink','stats']))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Please Wait...!", quote = True)
    try:
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("Something went Wrong..!")
        return
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://telegram.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    
    #added By Rudraa
    url=await Short(link)
    share_link=await linkshortx(link)

    # await reply_text.edit(f"<b>Here is your link</b>\n\n{link}\n\n**__Modern Link__** (__Recomended Link__) :\n\n `{url}`\n\n**", reply_markup=reply_markup, disable_web_page_preview = True)

    await reply_text.edit(
            f"<strong>Your Batch Files Stored in my Database!</strong>\n\n<strong><i>Modern Link</i></strong> (<i>Recomended Link</i>) :\n\n<code>{url}</code>\n\n<strong><i>Normal Link</i></strong>:\n\n<code>{link}</code>\n\n<strong>LinkShortx:</strong> <code>{share_link}</code>\n\n"
            f"Just Click the link to get your files!",
            reply_markup=InlineKeyboardMarkup(
               [    [
                        InlineKeyboardButton("😎Modern Link", url=url),InlineKeyboardButton("😒Normal Link",url=link)
                    ],[
                        InlineKeyboardButton("🔗LinkShortx",url=share_link)
                    ]
               ]
            ),
            disable_web_page_preview=True
        )



    if not DISABLE_CHANNEL_BUTTON:
        await post_message.edit_reply_markup(reply_markup)

@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):

    if DISABLE_CHANNEL_BUTTON:
        return

    converted_id = message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    try:
        await message.edit_reply_markup(reply_markup)
    except Exception as e:
        print(e)
        pass
