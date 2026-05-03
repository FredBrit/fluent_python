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
    return resp.content

def download_one(cc: str): # Функция,  загружающая  одно  изображение;  ее  будет  исполнять  каждый поток.
    image = get_flag(cc)
    save_flag(image, f'{cc}.gif')
    print(cc, end=' ', flush=True)
    return cc

def download_many(cc_list: list[str]) -> int:
    cc_list = cc_list[:5]
    with futures.ThreadPoolExecutor(max_workers=3) as executor:
        to_do: list[futures.Future] = []
        for cc in sorted(cc_list): # Обойти коды стран в алфавитном порядке, чтобы было понятно, что результаты поступают не по порядку
            future = executor.submit(download_one, cc) # Метод executor.submit  планирует  выполнение  вызываемого  объекта  и  возвращает объект future, представляющий ожидаемую операцию.
            to_do.append(future) # Сохранить каждый будущий объект, чтобы впоследствии его можно было извлечь с помощью функции as_completed.
            print(f'Scheduled for {cc}: {future}') # В ывести сообщение, содержащее код страны и соответствующий ему будущий объект future.
    
        for count, future in enumerate(futures.as_completed(to_do), 1): # as_completed отдает будущие объекты по мере их завершения.
            res: str = future.result() # Получить результат этого объекта future
            print(f'{future} result: {res!r}') # Отобразить объект future и результат его выполнения
    return count

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