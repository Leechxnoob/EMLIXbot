
import os
import requests
from requests.utils import requote_uri
from pyrogram import Client, filters
from pyrogram.types import *
from Emli import pbot 

API = "https://api.safone.tech/google?query="


@pbot.on_message(filters.command("gs"))
async def google(query):
    r = requests.get(API + requote_uri(query))
    informations = r.json()["results"]
    results = []
    for info in informations:
        text = f"Title: {info['title']}"
        text += f"\nDescription: {info['description']}"
        text += f"\n\nMade by @shado_hackers"
        results.append(
            {
                "title": info['title'],
                "description": info['description'],
                "text": text,
                "link": info['link']
            }
        )
    return results
