import json
import os

import requests

from Emli import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY
from Emli import *
from Emli.events import register


@register(outgoing=True, pattern=r"^\.ts(?: |$)(.*)")
async def torrent(event):
    await event.edit("**Searching...**")
    query = event.pattern_match.group(1)
    response = requests.get(f"https://some-random-api.herokuapp.com/1337x?q={query}")
    try:
        ts = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        return await event.edit("**Error: API is down right now, try again later.**")
    if ts != response.json():
        return await event.edit("**Error: API is down right now, try again later.**")
    listdata = ""
    run = 0
    while True:
        try:
            run += 1
            r1 = ts[run]
            list1 = "<-----{}----->\nName: {}\nSeeders: {}\nSize: {}\nAge: {}\n<--Magnet Below-->\n{}\n\n\n".format(
                run, r1["name"], r1["seeder"], r1["size"], r1["age"], r1["magnet"]
            )
            listdata += list1
        except BaseException:
            break

    if not listdata:
        return await event.edit("**Error: No results found.**")

    await event.edit("**Uploading results...**")
    tsfileloc = f"{TEMP_DOWNLOAD_DIRECTORY}{query}.txt"
    with open(tsfileloc, "w+", encoding="utf8") as out_file:
        out_file.write(str(listdata))
    caption = f"Torrents for: `{query}`"
    await event.client.send_file(
        event.chat_id, tsfileloc, caption=caption, force_document=False
    )
    os.remove(tsfileloc)
    await event.delete()
