# ॠ Rudraa

from pyshorteners import Shortener
import os
import aiohttp

linkshortx_api=os.environ.get("linkshortx_api","5b2908ac9710e83f0a4186a74c25ca3e728faac6")

async def Short(link):
    share_link=link
    s=Shortener()
    url = s.dagd.short(share_link)
    return url

async def linkshortx(link):
    #Add A LinkShortx Shortner Custom
    try:
        api_url="https://linkshortx.in/api"
        params={'api': linkshortx_api,'url': link}
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url,params=params,raise_for_status=True) as response:
                data=await response.json()
                share_link =data["shortenedUrl"]
                return share_link
    except Exception as error:
        print(f"Linkshortx.in error :- {error}")