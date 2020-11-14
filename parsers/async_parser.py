# import aiohttp
# import asyncio
# from utils import read_links_txt
#
# links = read_links_txt('input/images_links.txt')
#
#
# async def get(url):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url, ssl=False) as response:
#             return response.status
#
# loop = asyncio.get_event_loop()
# tasks = [get(link) for link in links]
# results = loop.run_until_complete(asyncio.gather(*tasks))
# print("Results: %s" % results)

import os
import pathlib
import aiohttp
import aiofiles
import asyncio
from utils import read_links_txt, get_file_name_from_url

from bs4 import BeautifulSoup
import re

links = 'https://en.wikipedia.org/wiki/Microcontroller'
img_dir = 'img/async'

pathlib.Path(img_dir).mkdir(parents=True, exist_ok=True)


async def parse_links(links):
    async with aiohttp.ClientSession() as session:
        async with session.get(links, ssl=False) as resp:
            bs = BeautifulSoup(await resp.text(), 'html.parser')
            url = bs.find_all('img', {'src': re.compile('.jpg')})
            for image in url:
                yield image['src']
                # print(image['src'] + '\n')


async def download(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as response:
            f = await aiofiles.open(os.path.join(img_dir, get_file_name_from_url(url)), mode='wb')
            await f.write(await response.read())
            await f.close()


async def main():
    async for url in parse_links(links):
        await download(url)

    # result = [download(link) for link in url]
    # return result

loop = asyncio.get_event_loop()
tasks = parse_links(links)
# loop.run_until_complete(asyncio.gather(*tasks))
loop.run_until_complete(main())
