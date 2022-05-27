
#copyright @shado_hackers. In telegram
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


import re
from random import choice

import requests
from bs4 import BeautifulSoup

import cloudscraper 
from Emli import pbot
from pyrogram import Client, filters
from pyrogram.types import Update


@pbot.on_message(filters.command("direct"))
async def direct_link_generator(c: Client, update: Update):
    if not len(update.command) == 2:
        m = "Usage: `/direct <url>`"
        await update.reply_text(
            parse_mode="md",
            text=m)
        return

    text = update.command[1]
    if text:
        links = re.findall(r'\bhttps?://.*\.\S+', text)
    else:
        return
    reply = []
    if not links:
        await update.reply_text("No links found!")
        return
    for link in links:
        if 'drive.google.com' in link:
            reply += gdrive(link)
        elif 'mediafire.com' in link:
            reply += mediafire(link)
        elif 'sourceforge.net' in link:
             reply += sourceforge(link)
        elif 'github.com' in link:
             reply += github(link)
        elif 'anonfiles.com' in link:
              reply += anonfiles(link)
        elif 'androidfilehost.com' in link:
              reply += androidfilehost(link)
        elif 'mdisk.me' in link:
              reply += mdisk(link)
        else:
            reply.append(re.findall(
                r"\bhttps?://(.*?[^/]+)", link)[0] + ' is not supported')

    await update.reply_text("\n".join(reply))

def gdrive(url: str) -> str:
    """ GDrive direct links generator """
    drive = 'https://drive.google.com'
    try:
        link = re.findall(r'\bhttps?://drive\.google\.com\S+', url)[0]
    except IndexError:
        reply = "`No Google drive links found`\n"
        return reply
    file_id = ''
    reply = ''
    if link.find("view") != -1:
        file_id = link.split('/')[-2]
    elif link.find("open?id=") != -1:
        file_id = link.split("open?id=")[1].strip()
    elif link.find("uc?id=") != -1:
        file_id = link.split("uc?id=")[1].strip()
    url = f'{drive}/uc?export=download&id={file_id}'
    download = requests.get(url, stream=True, allow_redirects=False)
    cookies = download.cookies
    try:
        # In case of small file size, Google downloads directly
        dl_url = download.headers["location"]
        if 'accounts.google.com' in dl_url:  # non-public file
            reply += '`Link is not public!`\n'
            return reply
        name = 'Direct Download Link'
    except KeyError:
        # In case of download warning page
        page = BeautifulSoup(download.content, 'lxml')
        export = drive + page.find('a', {'id': 'uc-download-link'}).get('href')
        name = page.find('span', {'class': 'uc-name-size'}).text
        response = requests.get(export,
                                stream=True,
                                allow_redirects=False,
                                cookies=cookies)
        dl_url = response.headers['location']
        if 'accounts.google.com' in dl_url:
            reply += '`Link is not public!`\n'
            return reply
    reply += f'[{name}]({dl_url})\n'
    return reply


def mediafire(url: str) -> str:
    """ MediaFire direct links generator """
    try:
        link = re.findall(r'\bhttps?://.*mediafire\.com\S+', url)[0]
    except IndexError:
        reply = "`No MediaFire links found`\n"
        return reply
    reply = ''
    page = BeautifulSoup(requests.get(link).content, 'lxml')
    info = page.find('a', {'aria-label': 'Download file'})
    dl_url = info.get('href')
    size = re.findall(r'\(.*\)', info.text)[0]
    name = page.find('div', {'class': 'filename'}).text
    reply += f'[{name} {size}]({dl_url})\n'
    return reply



def sourceforge(url: str) -> str:
    try:
        link = re.findall(r'\bhttps?://.*sourceforge\.net\S+', url)[0]
    except IndexError:
        reply = "No SourceForge links found\n"
        return reply
    file_path = re.findall(r'/files(.*)/download', link)
    if not file_path:
        file_path = re.findall(r'/files(.*)', link)
    file_path = file_path[0]
    reply = f"Mirrors for <code>{file_path.split('/')[-1]}</code>\n"
    project = re.findall(r'projects?/(.*?)/files', link)[0]
    mirrors = f'https://sourceforge.net/settings/mirror_choices?' \
        f'projectname={project}&filename={file_path}'
    page = BeautifulSoup(requests.get(mirrors).content, 'lxml')
    info = page.find('ul', {'id': 'mirrorList'}).findAll('li')
    for mirror in info[1:]:
        name = re.findall(r'\((.*)\)', mirror.text.strip())[0]
        dl_url = f'https://{mirror["id"]}.dl.sourceforge.net/project/{project}/{file_path}'
        reply += f'<a href="{dl_url}">{name}</a> '
    return reply

def github(url: str) -> str:
    """ github direct links generator """
    try:
        link = re.findall(r'\bhttps?://.*github\.com\S+', url)[0]
    except IndexError:
        reply = "`No github links found`\n"
        return reply
    reply = ''
    page = BeautifulSoup(requests.get(link).content, 'lxml')
    info = page.find('a', {'aria-label': 'Download file'})
    dl_url = info.get('href')
    size = re.findall(r'\(.*\)', info.text)[0]
    name = page.find('div', {'class': 'filename'}).text
    reply += f'[{name} {size}]({dl_url})\n'
    return reply

def androidfilehost(url: str) -> str:
    """AFH direct links generator"""
    try:
        link = re.findall(r'\bhttps?://.*androidfilehost.*fid.*\S+', url)[0]
    except IndexError:
        reply = "`No AFH links found`\n"
        return reply
    fid = re.findall(r'\?fid=(.*)', link)[0]
    session = requests.Session()
    user_agent = useragent()
    headers = {'user-agent': user_agent}
    res = session.get(link, headers=headers, allow_redirects=True)
    headers = {
        'origin': 'https://androidfilehost.com',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'user-agent': user_agent,
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'x-mod-sbb-ctype': 'xhr',
        'accept': '*/*',
        'referer': f'https://androidfilehost.com/?fid={fid}',
        'authority': 'androidfilehost.com',
        'x-requested-with': 'XMLHttpRequest',
    }
    data = {
        'submit': 'submit',
        'action': 'getdownloadmirrors',
        'fid': f'{fid}'
    }
    mirrors = None
    reply = ''
    error = "`Error: Can't find Mirrors for the link`\n"
    try:
        req = session.post(
            'https://androidfilehost.com/libs/otf/mirrors.otf.php',
            headers=headers,
            data=data,
            cookies=res.cookies)
        mirrors = req.json()['MIRRORS']
    except (json.decoder.JSONDecodeError, TypeError):
        reply += error
    if not mirrors:
        reply += error
        return reply
    for item in mirrors:
        name = item['name']
        dl_url = item['url']
        reply += f'[{name}]({dl_url}) '
    return reply

def anonfiles(url: str) -> str:
    reply = ''
    html_s = requests.get(url).content
    soup = BeautifulSoup(html_s, "html.parser")
    _url = soup.find("a", attrs={"class": "btn-primary"})["href"]
    name = _url.rsplit("/", 1)[1]
    dl_url = _url.replace(" ", "%20")
    reply += f'[{name}]({dl_url})\n'
    return reply

def onedrive(link: str) -> str:
    link_without_query = urlparse(link)._replace(query=None).geturl()
    direct_link_encoded = str(standard_b64encode(bytes(link_without_query, "utf-8")), "utf-8")
    direct_link1 = f"https://api.onedrive.com/v1.0/shares/u!{direct_link_encoded}/root/content"
    resp = requests.head(direct_link1)
    if resp.status_code != 302:
        return "`Error: Unauthorized link, the link may be private`"
    dl_link = resp.next.url
    file_name = dl_link.rsplit("/", 1)[1]
    resp2 = requests.head(dl_link)
    dl_size = humanbytes(int(resp2.headers["Content-Length"]))
    return f"[{file_name} ({dl_size})]({dl_link})"

def mdis_k(urlx):
    scraper = cloudscraper.create_scraper(interpreter="nodejs", allow_brotli=False)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"
    }
    apix = f"http://x.egraph.workers.dev/?param={urlx}"
    response = scraper.get(apix, headers=headers)
    query = response.json()
    return query

def mdisk_ddl(url: str) -> str:

    check = re.findall(r"\bhttps?://.*mdisk\S+", url)
    if not check:
        textx = f"Invalid mdisk url"
        return textx
    else:
        try:
            fxl = url.split("/")
            urlx = fxl[-1]
            uhh = mdis_k(urlx)
            text = f'{uhh["download"]}'
            return text
        except ValueError:
            textx = f"The content is deleted."
            return textx

def useragent():
    useragents = BeautifulSoup(
        requests.get(
            'https://developers.whatismybrowser.com/'
            'useragents/explore/operating_system_name/android/').content,
        'lxml').findAll('td', {'class': 'useragent'})
    user_agent = choice(useragents)
    return user_agent.text


__help__ = """
 ❍ /direct - get any file useing link
"""
__mod_name__ = "Direct link🖇️"
