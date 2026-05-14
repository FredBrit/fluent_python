#!/usr/bin/env python3
import asyncio
import socket # низкоуровневая сетевая библиотека (нужна для исключения socket.gaierror)
from keyword import kwlist # список всех ключевых слов Python (['and', 'as', 'assert', ...])

MAX_KEYWORD_LEN = 4

async def probe(domain: str) -> tuple[str, bool]:
    loop = asyncio.get_running_loop() # Получить ссылку на цикл событий asyncio для будущего использования
    # Функция  asyncio.get_running_loop  была  добавлена  в  версии 
    # Python 3.7 для использования внутри сопрограмм, как показано в probe. Если работающего цикла нет, то она возбуждает исключение RuntimeError. 
    # Ее реализация проще и быстрее, чем функции  asyncio.get_event_loop,  которая  может  при  необходимости запустить цикл событий. 
    # Начиная с версии Python 3.10 asyncio.get_event_loop  объявлена  нерекомендуемой и в конечном итоге станет псевдонимом asyncio.get_running_loop.
    try:
        await loop.getaddrinfo(domain, None) # асинхронная версия socket.getaddrinfo(). Выполняет DNS-запрос для разрешения доменного имени в IP-адрес. await — приостанавливает выполнение до получения результата
    except socket.gaierror:
        return (domain, False)
    return (domain, True)

async def main() -> None: # main должна быть сопрограммой, чтобы в ней можно было использовать await
    names = (kw for kw in kwlist if len(kw) <= MAX_KEYWORD_LEN)
    domains = (f'{name}.dev'.lower() for name in names)
    coros = [probe(domain) for domain in domains]
    for coro in asyncio.as_completed(coros): # asyncio.as_completed  – генератор, отдающий переданные ему сопрограммы в порядке их завершения, а не в порядке подачи. Он похож на функцию futures.as_completed
        domain, found = await coro # В этот момент мы знаем, что сопрограмма завершилась, потому что так работает as_completed. 
        # Поэтому выражение await не заблокирует выполнение, но оно все равно необходимо, чтобы получить результат от coro. 
        # Если coro возбуждала необработанное исключение, то оно будет заново возбуждено в этой точке.
        mark = '+' if found else ' '
        print(f'{mark} {domain}')

if __name__ == '__main__': 
    # asyncio.run запускает цикл событий и возвращает управление только после выхода из него. 
    # asyncio.run() — рекомендуемый способ запуска асинхронного кода (Python 3.7+)
    # Создаёт новый цикл событий, запускает main(), закрывает цикл
    # реализовать main  как сопрограмму и выполнить ее внутри блока if __name__ == '__main__':
    asyncio.run(main())