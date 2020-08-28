import aiohttp
# TODO 还未写完

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

def request():
    a = ''
    async with aiohttp.ClientSession() as session:
        a = await fetch(session, 'http://httpbin.org/post')
    return a