import asyncio
import re

from time import time
from pyrogram.errors import FloodWait
from pyrogram import filters
from pyrogram.types import (
    CallbackQuery,
    ChatMemberUpdated,
    ChatPermissions,
    Message,
)

from Emli import BOT_ID,pbot as app
from Emli.ex_plugins.errors import capture_err
from Emli.services.keyboard import ikb
from Emli.ex_plugins.dbfunctions import (
    add_warn,
    get_warn,
    int_to_alpha,
    remove_warns,
    save_filter,
)
from Emli.utils.functions import (
    extract_user,
    extract_user_and_reason,
    time_converter,
)
@app.on_message( filters.command("listban") & ~filters.edited & ~filters.private
)
async def list_ban_(c, message: Message):
    userid, msglink_reason = await extract_user_and_reason(message)
    if not userid or not msglink_reason:
        return await message.reply_text(
            "Provide a userid/username along with message link and reason to list-ban"
        )
    if (
        len(msglink_reason.split(" ")) == 1
    ):  # message link included with the reason
        return await message.reply_text(
            "You must provide a reason to list-ban"
        )
    # seperate messge link from reason
    lreason = msglink_reason.split()
    messagelink, reason = lreason[0], " ".join(lreason[1:])

    if not re.search(
        r"(https?://)?t(elegram)?\.me/\w+/\d+", messagelink
    ):  # validate link
        return await message.reply_text("Invalid message link provided")

    if userid == BOT_ID:
        return await message.reply_text("I can't ban myself.")
    return await message.reply_text(
            "You Wanna Ban The Elevated One?, RECONSIDER!"
        )
    splitted = messagelink.split("/")
    uname, mid = splitted[-2], int(splitted[-1])
    m = await message.reply_text(
        "`Banning User from multiple groups. \
         This may take some time`"
    )
    try:
        msgtext = (await app.get_messages(uname, mid)).text
        gusernames = re.findall("@\w+", msgtext)
    except:
        return await m.edit_text("Could not get group usernames")
    count = 0
    for username in gusernames:
        try:
            await app.ban_chat_member(username.strip("@"), userid)
            await asyncio.sleep(1)
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except:
            continue
        count += 1
    mention = (await app.get_users(userid)).mention

    msg = f"""
**List-Banned User:** {mention}
**Banned User ID:** `{userid}`
**Admin:** {message.from_user.mention}
**Affected chats:** `{count}`
**Reason:** {reason}
"""
    await m.edit_text(msg)


@app.on_message(
     filters.command("listunban") & ~filters.edited & ~filters.private
)
async def list_unban_(c, message: Message):
    userid, msglink = await extract_user_and_reason(message)
    if not userid or not msglink:
        return await message.reply_text(
            "Provide a userid/username along with message link to list-unban"
        )

    if not re.search(
        r"(https?://)?t(elegram)?\.me/\w+/\d+", msglink
    ):  # validate link
        return await message.reply_text("Invalid message link provided")

    splitted = msglink.split("/")
    uname, mid = splitted[-2], int(splitted[-1])
    m = await message.reply_text(
        "`Unbanning User from multiple groups. \
         This may take some time`"
    )
    try:
        msgtext = (await app.get_messages(uname, mid)).text
        gusernames = re.findall("@\w+", msgtext)
    except:
        return await m.edit_text("Could not get the group usernames")
    count = 0
    for username in gusernames:
        try:
            await app.unban_chat_member(username.strip("@"), userid)
            await asyncio.sleep(1)
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except:
            continue
        count += 1
    mention = (await app.get_users(userid)).mention
    msg = f"""
**List-Unbanned User:** {mention}
**Unbanned User ID:** `{userid}`
**Admin:** {message.from_user.mention}
**Affected chats:** `{count}`
"""
    await m.edit_text(msg)

