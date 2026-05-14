from concurrent import futures
import httpx, time
from pathlib import Path
from typing import Callable



POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()
BASE_URL = 'https://www.fluentpython.com/data/flags'
DEST_DIR = Path('C:/Users/fedor/Downloads/flags')

def save_flag(img: bytes, filename: str) -> None:
    (DEST_DIR / filename).write_bytes(img)

def get_flag(cc: str) -> bytes:
    url = f'{BASE_URL}/{cc}/{cc}.gif'.lower()
    resp = httpx.get(url, timeout=6.1, # Считается правильным добавлять разумный тайм-аут для сетевых операций, чтобы избежать ненужной блокировки на несколько минут.
                   follow_redirects=True) # По умолчанию HTTPX не выполняет перенаправление
    resp.raise_for_status()
    return resp.content # возвращает в формате bytes

def download_one(cc: str): # Функция,  загружающая  одно  изображение;  ее  будет  исполнять  каждый поток.
    image = get_flag(cc)
    save_flag(image, f'{cc}.gif')
    print(cc, end=' ', flush=True)
    return cc

def download_many(cc_list: list[str]) -> int:
    with futures.ThreadPoolExecutor(max_workers=64) as executor: 
        # Создать  экземпляр  ThreadPoolExecutor  как  контекстный  менеджер;  
        # метод executor.__exit__  вызовет  executor.shutdown(wait=True),  который  блокирует  выполнение программы до завершения всех потоков.
        # По умолчанию создаётся столько потоков, сколько ядер CPU × 5 (но для I/O-bound задач это нормально)
        res = executor.map(download_one, sorted(cc_list))
        # Метод map похож на встроенную функцию map с тем исключением, что функция download_one конкурентно вызывается из нескольких потоков; 
        # он возвращает генератор, который можно обойти для получения значений, возвращенных каждой функцией, 
        # – в данном случае каждое обращение к download_one возвращает код страны.
    return len(list(res))
        # Вернуть количество полученных результатов. Если функция в каком-то потоке возбудила исключение, 
        # то оно возникнет в этом месте, когда неявный вызов next() из конструктора list попытается получить соответствующее значение от итератора, возвращенного методом map.

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