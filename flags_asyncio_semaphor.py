import asyncio, time
from pathlib import Path
from httpx import AsyncClient

POP20_CC = ('CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR').split()
BASE_URL = 'https://www.fluentpython.com/data/flags'
DEST_DIR = Path('C:/Users/Fedor/Downloads/flags')
DEST_DIR.mkdir(exist_ok=True)

# Глобальный семафор
semaphore = asyncio.Semaphore(5)

async def get_flag(client: AsyncClient, cc: str) -> bytes:
    url = f'{BASE_URL}/{cc}/{cc}.gif'.lower()
    resp = await client.get(url, timeout=6.1, follow_redirects=True)
    return resp.read()

async def download_one(client: AsyncClient, cc: str) -> str:
    start = time.time()
    async with semaphore:  # ← ограничение конкурентности
        print(f"[{cc}] начало в {start:.2f}")
        image = await get_flag(client, cc)
        (DEST_DIR / f'{cc}.gif').write_bytes(image)
        end=time.time()
        print(f"[{cc}] конец в {end:.2f} (длился {end - start:.2f}с)")
        return cc

async def supervisor() -> int:
    async with AsyncClient() as client:
        to_do = [download_one(client, cc) for cc in POP20_CC]
        results = await asyncio.gather(*to_do)
        return len(results)

def main():
    count = asyncio.run(supervisor())
    print(f'\n{count} downloads completed.')

if __name__ == '__main__':
    main()