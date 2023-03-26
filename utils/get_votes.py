import aiohttp
from loader import baza_link

async def get(page):
    URL = (
        f"{baza_link}?size=2000&page={page}"
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                raise Exception("Server xatoligi")
