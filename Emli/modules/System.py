import subprocess
import time
import os
import requests
import speedtest
import json
import sys
import traceback
import psutil
import platform
import sqlalchemy
import Emli.modules.helper_funcs.git_api as git

from datetime import datetime
from platform import python_version, uname
from telethon import version as tlthn
from telegram import Update, Bot, Message, Chat, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, version as pybot
from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler, Filters
from telegram.ext.dispatcher import run_async
from telegram.error import BadRequest, Unauthorized

from Emli import DEV_USERS, LOGGER, StartTime, dispatcher
from Emli.modules.disable import DisableAbleCommandHandler, DisableAbleRegexHandler
from Emli.modules.helper_funcs.misc import delete
from Emli.modules.helper_funcs.chat_status import  dev_plus, sudo_plus
from Emli.modules.sql.clear_cmd_sql import get_clearcmd


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def convert(speed):
    return round(int(speed) / 1048576, 2)
    
@dev_plus
def status(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    query = update.callback_query

    msg = "*Bot information*\n"
    msg += f"Python: `{python_version()}`\n"
    msg += f"Python Tg Bot: `{pybot.__version__}`\n"
    msg += f"Telethon: `{tlthn.__version__}`\n"
    msg += f"SQLAlchemy: `{sqlalchemy.__version__}`\n"
    msg += f"GitHub API: `{str(git.vercheck())}`\n"
    uptime = get_readable_time((time.time() - StartTime))
    msg += f"🕜Uptime: `{uptime}`\n\n"
    uname = platform.uname()
    msg += "*🗃️System information*\n"
    msg += f"OS: `{uname.system}`\n"
    msg += f"Version: `{uname.version}`\n"
    msg += f"Release: `{uname.release}`\n"
    msg += f"💽Processor: `{uname.processor}`\n"
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    msg += f"Boot time: `{bt.day}/{bt.month}/{bt.year} - {bt.hour}:{bt.minute}:{bt.second}`\n"
    msg += f"CPU cores: `{psutil.cpu_count(logical=False)} physical, {psutil.cpu_count()} logical`\n"
    msg += f"CPU freq: `{psutil.cpu_freq().current:.2f}Mhz`\n"
    msg += f"CPU usage: `{psutil.cpu_percent()}%`\n"
    ram = psutil.virtual_memory()
    msg += f"RAM: `{get_size(ram.total)} - {get_size(ram.used)} used ({ram.percent}%)`\n"
    disk = psutil.disk_usage('/')
    msg += f"Disk usage: `{get_size(disk.total)} total - {get_size(disk.used)} used ({disk.percent}%)`\n"
    swap = psutil.swap_memory()
    msg += f"SWAP: `{get_size(swap.total)} - {get_size(swap.used)} used ({swap.percent}%)`\n"

    message.reply_text(
        text = msg,
        parse_mode = ParseMode.MARKDOWN,
        disable_web_page_preview = True,
    )

STATUS_HANDLER = DisableAbleCommandHandler("status", status, run_async=True)
dispatcher.add_handler(STATUS_HANDLER)
