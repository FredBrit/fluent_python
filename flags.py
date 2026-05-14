import time
from pathlib import Path
from typing import Callable
import httpx

POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()
BASE_URL = 'https://www.fluentpython.com/data/flags'
DEST_DIR = Path('C:/Users/Fedor/Downloads/flags')

def save_flag(img: bytes, filename: str) -> None:
    (DEST_DIR / filename).write_bytes(img)

def get_flag(cc: str) -> bytes:
    url = f'{BASE_URL}/{cc}/{cc}.gif'.lower()
    resp = httpx.get(url, timeout=6.1, # Считается правильным добавлять разумный тайм-аут для сетевых операций, чтобы избежать ненужной блокировки на несколько минут.
                   follow_redirects=True) # По умолчанию HTTPX не выполняет перенаправление
    resp.raise_for_status()
    return resp.content

def download_many(cc_list: list[str]) -> int:
    for cc in sorted(cc_list):
        image = get_flag(cc)
        save_flag(image, f'{cc}.gif')
        print(cc, end=' ', flush=True) # Аргумент flush=True необходим, потому что по умолчанию Python буферизует выходные строки, т. е. напечатанные символы отображаются только после вывода символа перевода строки.
    return len(cc_list)

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