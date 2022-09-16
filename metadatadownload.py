import asyncio
import aiohttp
import os

async def main():
    url = "https://y25vmzcpansexlwvslmfbgxynlejyk6jm4oou6jl57iz4nm2t5ua.arweave.net/xrtWZE8DZEuu1ZLYUJr4asicK8lnHOp5K-_RnjWan2g/"
    for i in range(1, 10002):
        if not os.path.isfile(f"metadata/{i}.json"):
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{url}{i}.json") as request:
                    data = await request.json()
                    with open(f"metadata/{i}.json", "w") as f:
                        f.write(str(data))


async def check():

    last = 0
    for i in range(1, 10002):
        if not os.path.isfile(f"metadata/{i}.json"):
            if (last+1) != i:
                print(f"start:{i}")
            last = i
        else:
            if (last+1) == i:
                print(f"end:{i}")



asyncio.run(check())
