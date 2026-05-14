import asyncio, time
from pathlib import Path
from typing import Callable
from httpx import AsyncClient


POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()
BASE_URL = 'https://www.fluentpython.com/data/flags'
DEST_DIR = Path('C:/Users/Fedor/Downloads/flags')

def save_flag(img: bytes, filename: str) -> None:
    (DEST_DIR / filename).write_bytes(img)

async def download_one(client: AsyncClient, cc: str):
    # download_one должна быть платформенной сопрограммой, чтобы она могла вызвать await  для сопрограммы get_flag, которая выполняет HTTP-запрос. 
    # Затем она отображает загруженный флаг и сохраняет изображение
    image = await get_flag(client, cc)
    save_flag(image, f'{cc}.gif')
    print(cc, end=' ', flush=True)
    return cc

async def get_flag(client: AsyncClient, cc: str) -> bytes: # get_flag должна получить AsyncClient, чтобы сделать запрос
    url = f'{BASE_URL}/{cc}/{cc}.gif'.lower()
    resp = await client.get(url, timeout=6.1, follow_redirects=True) # Метод get экземпляра httpx.AsyncClient возвращает объект ClientResponse, который заодно является асинхронным контекстным менеджером
    return resp.read() # Операции  сетевого  ввода-вывода  реализованы  в  виде  методов-сопрограмм,  чтобы  их  можно  было  асинхронно  вызывать  из  цикла  событий asyncio.

def download_many(cc_list: list[str]) -> int:
    return asyncio.run(supervisor(cc_list)) 
# Выполнять  цикл  событий,  приводящий  в  действие  объект  сопрограммы 
# supervisor(cc_list), пока тот не вернет управление. Эта строка блокирует выполнение  на  все  время  работы  цикла  событий.  
# Ее  результатом  является значение, возвращенное supervisor.

async def supervisor(cc_list: list[str]) -> int:
    async with AsyncClient() as client:
        # Асинхронные операции HTTP-клиента в httpx – это методы класса AsyncClient, 
        # который  также  является  асинхронным  контекстным  менеджером,  
        # т.  е. контекстным  менеджером  с  асинхронными  методами  инициализации и очистки
        to_do = [download_one(client, cc) for cc in sorted(cc_list)] # Построить список объектов сопрограмм (планов-выполнения), вызвав сопрограмму  download_one по разу для каждого флага.
        res = await asyncio.gather(*to_do)
        # Ждать  завершения  сопрограммы  asyncio.gather,  которая  принимает  один или несколько допускающих ожидание аргументов, 
        # asyncio.gather() запускает все сопрограммы конкурентно и ждёт, пока все завершатся.
        # Возвращает список результатов в том же порядке, в каком были переданы сопрограммы
    return len(res)


def main(downloader: Callable[[list[str]], int]) -> None: 
    # При  вызове  main  необходимо  указывать  функцию,  которая  производит загрузку;  таким образом, main можно будет использовать 
    # как библиотечную функцию, способную работать и с другими реализациями download_many в примерах threadpool  и ascyncio
    DEST_DIR.mkdir(exist_ok=True)
    t0 = time.perf_counter()
    count = downloader(POP20_CC)
    elapsed = time.perf_counter() - t0
    print(f'\n{count} downloads in {elapsed:.2f}s')

if __name__ == '__main__':
    main(download_many)    