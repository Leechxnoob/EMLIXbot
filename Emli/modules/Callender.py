import calendar
from datetime import datetime

from telethon import *
from telethon.tl import functions
from telethon.tl import types
from telethon.tl.types import *

from Emli import *
from Emli.events import register

@register(pattern="^/calendar")
async def _(event):
    if event.fwd_from:
        return

    try:
        edit = await event.reply("`Searching...`")
        today = datetime.today()
        input_ = calendar.month(today.year, today.month)
        await edit.edit(f"```{input_}```")
    except Exception as err:
        await event.reply("Exception Occured:- " + str(err))")
