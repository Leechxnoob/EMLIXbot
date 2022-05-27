import requests
import asyncio
import io
import os
import random
import re
import string
import subprocess
import textwrap
import nltk

from random import randint, randrange, uniform
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from telethon.tl.types import DocumentAttributeFilename, InputMessagesFilterDocument, InputMediaDice
from telethon import events
from zalgo_text import zalgo

from pyrogram import filters

from Emli import telethn, ubot, pgram, TEMP_DOWNLOAD_DIRECTORY, SUPPORT_CHAT, GOOGLE_CHROME_BIN, CHROME_DRIVER
from Emli import pbot as pgram


@telethn.on(events.NewMessage(pattern="^/news ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    infintyvar = event.pattern_match.group(1)
    main_url = f"https://inshorts.deta.dev/news?category={infintyvar}"
    stuber = await event.reply(
        f"Ok ! Fectching {infintyvar} From inshortsapi Server And Sending To News Channel",
    )
    await stuber.edit("All News Has Been Sucessfully fetched, sendning to you.")
    starknews = requests.get(main_url).json()
    for item in starknews["data"]:
        sedlyf = item["content"]
        img = item["imageUrl"]
        writter = item["author"]
        dateis = item["date"]
        readthis = item["readMoreUrl"]
        titles = item["title"]
        sed1 = img
        sedm = f"**Title : {titles}** \n{sedlyf} \nDate : {dateis} \nAuthor : {writter} \nReadMore : {readthis}"
        await pgram.send_photo(event.chat_id, sed1, caption=sedm)
        
