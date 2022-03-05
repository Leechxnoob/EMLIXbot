import re
from requests import get
from hurry.filesize import size as sizee
import rapidjson as json
from bs4 import BeautifulSoup
from Emli import pbot

from Emli.utils.devices import GetDevice

from hurry.filesize import size as sizee
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Update
from requests import get
from yaml import Loader, load


# Important credits:
# * The ofox command was originally developed by MrYacha.
# * The /twrp, /specs, /whatis, /variants, /samcheck and /samget
# commands were originally developed by KassemSYR.
#
# This module was inspired by Android Helper Bot by Vachounet.
# None of the code is taken from the bot itself, to avoid confusion.
# Please don't remove these comment, show respect to module contributors.

err_not_found: "Couldn't find any results matching your query."
err_api: "Couldn't reach the API."
err_example_device: "Why are you trying to get the example device?"
err_json: "Tell the rom maintainer to fix their OTA json. I'm sure this won't work with OTA and it won't work with this bot too"
btn_dl: "Click here to Download"
cmd_example: "Please type your device **codename**!\nFor example, `/{} lavender"
maintainer: "**Maintainer:** {}\n"
android_version: "**Android Version:** `{}`\n"
download: "**Download:** [{}]({})\n"
build_size: "**Build Size:** `{}`\n"



REALME_FIRM = "https://raw.githubusercontent.com/RealmeUpdater/realme-updates-tracker/master/data/latest.yml"


@pbot.on_message(filters.command("realmeui"))
async def realmeui(c: Client, update: Update):
    if len(update.command) != 2:
        message = "Please write a codename, example: `/realmeui RMX2061`"
        await update.reply_text(message)
        return

    codename = update.command[1]

    yaml_data = load(get(REALME_FIRM).content, Loader=Loader)
    data = [i for i in yaml_data if codename in i['codename']]

    if len(data) < 1:
        await update.reply_text("Provide a valid codename!")
        return

    for fw in data:
        reg = fw['region']
        link = fw['download']
        device = fw['device']
        version = fw['version']
        cdn = fw['codename']
        sys = fw['system']
        size = fw['size']
        date = fw['date']
        md5 = fw['md5']

        btn = reg + ' | ' + version

        keyboard = [[InlineKeyboardButton(text=btn, url=link)]]

    text = f"**RealmeUI - Last build for {codename}:**"
    text += f"\n\n**Device:** `{device}`"
    text += f"\n**System:** `{sys}`"
    text += f"\n**Size:** `{size}`"
    text += f"\n**Date:** `{date}`"
    text += f"\n**MD5:** `{md5}`"

    await update.reply_text(text,
                            reply_markup=InlineKeyboardMarkup(keyboard),
                            parse_mode="markdown")


@pbot.on_message(filters.command("samspec"))
async def specs(bot, update):
    if not len(update.command) == 2:
        message = "Please write your codename or model into it,\ni.e <code>/specs herolte</code> or <code>/specs sm-g610f</code>"
        await bot.send_message(chat_id=update.chat.id, text=message)
        return
    device = update.command[1]
    data = GetDevice(device).get()
    if data:
        name = data["name"]
        model = data["model"]
        device = name.lower().replace(" ", "-")
    else:
        message = "coudn't find your device, chack device & try!"
        await bot.send_message(chat_id=update.chat.id, text=message)
        return
    sfw = get(f"https://sfirmware.com/samsung-{model.lower()}/")
    if sfw.status_code == 200:
        page = BeautifulSoup(sfw.content, "lxml")
        message = "<b>Device:</b> Samsung {}\n".format(name)
        res = page.find_all("tr", {"class": "mdata-group-val"})
        res = res[2:]
        for info in res:
            title = re.findall(r"<td>.*?</td>", str(info))[0].strip().replace("td", "b")
            data = (
                re.findall(r"<td>.*?</td>", str(info))[-1].strip().replace("td", "code")
            )
            message += "• {}: <code>{}</code>\n".format(title, data)
        await bot.send_message(chat_id=update.chat.id, text=message)
    else:
        giz = get(f"https://www.gizmochina.com/product/samsung-{device}/")
        if giz.status_code == 404:
            message = "device specs not found in bot databases!"
            await bot.send_message(chat_id=update.chat.id, text=message)
            return
        page = BeautifulSoup(giz.content, "lxml")
        message = "<b>Device:</b> Samsung {}\n".format(name)
        for info in page.find_all("div", {"class": "aps-feature-info"}):
            title = info.find("strong").text
            data = info.find("span").text
            message += "• {}: <code>{}</code>\n".format(title, data)
        await bot.send_message(chat_id=update.chat.id, text=message)


@pbot.on_message(filters.command("specs"))
async def specs(c: Client, update: Update):
    if len(update.command) != 2:
        message = (
            "Please write your codename or model into it,\ni.e <code>/specs lavender</code> or <code>/specs riva</code>")
        await c.send_message(
            chat_id=update.chat.id,
            text=message)
        return
    device = update.command[1]
    data = GetDevice(device).get()
    if data:
        name = data['name']
        model = data['model']
        device = name.lower().replace(' ', '-')
    else:
        message = "coudn't find your device, chack device & try!"
        await c.send_message(
            chat_id=update.chat.id,
            text=message)
        return
    sfw = get(f"https://www.gizmochina.com/product/xiaomi-{device}/")
    if sfw.status_code == 200:
        page = BeautifulSoup(sfw.content, 'lxml')
        message = '<b>Device:</b> Xiaomi {}\n'.format(name)
        res = page.find_all('tr', {'class': 'mdata-group-val'})
        res = res[2:]
        for info in res:
            title = re.findall(r'<td>.*?</td>', str(info)
                               )[0].strip().replace('td', 'b')
            data = re.findall(r'<td>.*?</td>', str(info)
                              )[-1].strip().replace('td', 'code')
            message += "• {}: <code>{}</code>\n".format(title, data)

    else:
        message = "Device specs not found in bot database, make sure this is a Xiaomi device!"
        await c.send_message(
            chat_id=update.chat.id,
            text=message)
        return

    await c.send_message(
        chat_id=update.chat.id,
        text=message)

pbot.on_message(filters.command(["evo", "evox"]))
async def evo(c: Client, update: Update):

    chat_id = update.chat.id,
    try:
        device = update.command[1]
    except Exception:
        device = ''

    if device == "example":
        reply_text = (chat_id, "err_example_device")
        await update.reply_text(reply_text, disable_web_page_preview=True)
        return

    if device == "x00t":
        device = "X00T"

    if device == "x01bd":
        device = "X01BD"

    if device == '':
        reply_text = (chat_id, "cmd_example").format("evo")
        await update.reply_text(reply_text, disable_web_page_preview=True)
        return

    fetch = get(
        f'https://raw.githubusercontent.com/Evolution-X-Devices/official_devices/master/builds/{device}.json'
    )

    if fetch.status_code in [500, 504, 505]:
        await update.reply_text(
            "Emli have been trying to connect to Github User Content, It seem like Github User Content is down"
        )
        return

    if fetch.status_code == 200:
        try:
            usr = json.loads(fetch.content)
            filename = usr['filename']
            url = usr['url']
            version = usr['version']
            maintainer = usr['maintainer']
            maintainer_url = usr['telegram_username']
            size_a = usr['size']
            size_b = sizee(int(size_a))

            reply_text = (chat_id, "download").format(filename, url)
            reply_text += (chat_id, "build_size").format(size_b)
            reply_text += (chat_id, "android_version").format(version)
            reply_text += (chat_id, "maintainer").format(
                f"[{maintainer}](https://t.me/{maintainer_url})")

            btn = tld(chat_id, "btn_dl")
            keyboard = [[InlineKeyboardButton(
                text=btn, url=url)]]
            await update.reply_text(reply_text, reply_markup=InlineKeyboardMarkup(keyboard), disable_web_page_preview=True)
            return

        except ValueError:
            reply_text = (chat_id, "err_json")
            await update.reply_text(reply_text, disable_web_page_preview=True)
            return

    elif fetch.status_code == 404:
        reply_text = (chat_id, "err_not_found")
        await update.reply_text(reply_text, disable_web_page_preview=True)
        return





_mod_name_ = "realme"
