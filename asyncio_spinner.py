# asyncio.run(coro())
# Вызывается из регулярной функции для управления объектом сопрограммы, 
# который обычно является точкой входа в весь асинхронный код программы, 
# как supervisor в этом примере. Этот вызов блокирует выполнение, 
# пока coro не вернет управление. Функция run() возвращает значение, возвращенное coro.


# asyncio.create_task(coro())
# Вызывается  из  сопрограммы,  чтобы  запланировать  выполнение  другой сопрограммы.  Этот  вызов  не  приостанавливает  текущую  сопрограмму. 
# Он возвращает экземпляр Task – объект, который обертывает объект сопрограммы и предоставляет методы для управления ей и опроса ее состояния.


# await coro()
# Вызывается из сопрограммы, чтобы передать управление объекту сопрограммы, возвращенному coro(). 
# Этот вызов приостанавливает текущую сопрограмму до возврата из coro. Значением выражения await является значение, возвращенное coro.


# ВАЖНО!!!
# Никогда  не  используйте  time.sleep(...)  в  сопрограммах  asyncio, если не хотите приостановить всю программу в целом. 
# Если сопрограмма хочет потратить некоторое время, ничего не делая, она должна вызвать await  asyncio.sleep(DELAY). 
# Так она уступит управление циклу событий asyncio, который может дать поработать другим ожидающим сопрограммам. 






import asyncio
import itertools

async def spin(msg: str) -> None: # Платформенные  сопрограммы  определяются  с  помощью  ключевых  слов async def.
    for char in itertools.cycle(r'\|/-'):
        status = f'\r{char} {msg}'
        print(status, flush=True, end='')
        try:
            await asyncio.sleep(.1) # Использовать await asyncio.sleep(.1) вместо time.sleep(.1)
        except asyncio.CancelledError: # Когда вызывается метод cancel объекта Task, управляющего этой сопрограммой,  возбуждается  исключение  asyncio.CancelledError.  Время  выходить  из цикла.
            break
    blanks = ' ' * len(status)
    print(f'\r{blanks}\r', end='')

async def slow() -> int:
    await asyncio.sleep(3) # Использовать await asyncio.sleep(.1) вместо time.sleep(.1)
    return 42

async def supervisor() -> int:
    spinner = asyncio.create_task(spin('thinking!')) # asyncio.create_task  планирует выполнение spin сразу после возврата экземпляра asyncio.Task.
    print(f'spinner object: {spinner}')
    result = await slow() # Ключевое слово await вызывает slow, блокируя supervisor до возврата из slow. Значение, возвращенное slow, присваивается переменной result.
    spinner.cancel() # Метод Task.cancel возбуждает исключение CancelledError внутри сопрограммы spin
    return result

def main() -> None:
    result = asyncio.run(supervisor())
    # Функция asyncio.run  запускает цикл событий, активирующий сопрограмму, 
    # которая в конечном итоге приведет в действие и другие сопрограммы. Функция main  остается блокированной, пока supervisor  не вернет управление. 
    # Значение, возвращенное supervisor, станет значением, возвращенным asyncio.run.  
    print(f'Answer: {result}')

if __name__ == '__main__':
    main()