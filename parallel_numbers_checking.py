import sys, math
from time import perf_counter
from typing import NamedTuple
from multiprocessing import Process, SimpleQueue, cpu_count # SimpleQueue — это процесс-безопасная очередь, которая работает между разными процессами (в отличие от обычных очередей).
from multiprocessing import queues # В модуле multiprocessing.queues есть класс SimpleQueue, который нужен нам в аннотациях типов.

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    root = math.isqrt(n)
    for i in range(3, root + 1, 2):
        if n % i == 0:
            return False
    return True

PRIME_FIXTURE = [
    (2, True),
    (142702110479723, True),
    (299593572317531, True),
    (3333333333333301, True),
    (3333333333333333, False),
    (3333335652092209, False),
    (4444444444444423, True),
    (4444444444444444, False),
    (4444444488888889, False),
    (5555553133149889, False),
    (5555555555555503, True),
    (5555555555555555, False),
    (6666666666666666, False),
    (6666666666666719, True),
    (6666667141414921, False),
    (7777777536340681, False),
    (7777777777777753, True),
    (7777777777777777, False),
    (9999999999999917, True),
    (9999999999999999, False),
]

NUMBERS = [n for n, _ in PRIME_FIXTURE]


class PrimeResult(NamedTuple):  
    n: int
    prime: bool
    elapsed: float

JobQueue = queues.SimpleQueue[int]  # Это псевдоним типа SimpleQueue, которым функция main будет пользоваться для отправки чисел процессам-исполнителям
ResultQueue = queues.SimpleQueue[PrimeResult]  # Псевдоним второго типа SimpleQueue, который будет использован для сбора результатов в main. В очереди будут храниться кортежи, состоящие из проверяемого на простоту числа и кортежа Result.

def check(n: int) -> PrimeResult:  # Замеряет время выполнения is_prime(n)
    t0 = perf_counter()
    res = is_prime(n)
    return PrimeResult(n, res, perf_counter() - t0)

def worker(jobs: JobQueue, results: ResultQueue) -> None:
    # Бесконечный цикл: извлекает числа из jobs  
    while n := jobs.get():  
        results.put(check(n))
        # Условие while n := jobs.get():
        # jobs.get() блокирует выполнение, пока не появится элемент
        # Если получено число ≠ 0 → продолжаем
        # Если получено 0 → условие ложно → выходим из цикла
    results.put(PrimeResult(0, False, 0.0))  # Отправить PrimeResult(0, False, 0.0) обратно, чтобы главный цикл знал, что этот исполнитель работу закончил.

def start_jobs(
    procs: int, jobs: JobQueue, results: ResultQueue  
) -> None: # procs – количество процессов, которые будут параллельно проверять числа.
    for n in NUMBERS:
        jobs.put(n)  # Поместить подлежащие проверке числа в очередь jobs
    for _ in range(procs):

        # Сначала все числа помещаются в очередь
        # Затем для каждого процесса добавляется по одному 0
        # Каждый процесс, получив 0, завершится

        proc = Process(target=worker, args=(jobs, results)) # Создать  дочерние  процессы  для  всех  исполнителей.  Каждый  дочерний процесс будет исполнять цикл в собственном экземпляре функции worker, пока не извлечет 0 из очереди jobs.
        proc.start() # Запустить все дочерние процессы. 
        jobs.put(0) # Поместить в очередь по одному значению 0 для каждого процесса, чтобы завершить их. (Паттерн Poison Pill)



def main() -> None:
    if len(sys.argv) < 2:
        procs = cpu_count()
    else:
        procs = int(sys.argv[1])

    print(f'Checking {len(NUMBERS)} numbers with {procs} processes:')
    t0 = perf_counter()
    jobs: JobQueue = SimpleQueue() # Очереди
    results: ResultQueue = SimpleQueue() # Очереди
    start_jobs(procs, jobs, results) # Запустить proc процессов, которые будут выбирать данные из очереди jobs и посещать результаты в results
    checked = report(procs, results) # Извлечь и отобразить результаты; функция report определена в точке
    elapsed = perf_counter() - t0
    print(f'{checked} checks in {elapsed:.2f}s') # Показать количество проверенных чисел и общее затраченное время

def report(procs: int, results: ResultQueue) -> int:
    checked = 0
    procs_done = 0
    while procs_done < procs: # Цикл продолжается, пока не завершатся все дочерние процессы.
        n, prime, elapsed = results.get() # Получить один PrimeResult. Вызов метода очереди .get() блокирует выполнение до тех пор, пока в очереди не появится элемент. Можно также сделать этот вызов неблокирующим или задать тайм-аут.
        if n == 0: # Если n равно 0, то один процесс завершился; увеличить счетчик procs_done.
            procs_done += 1
        else:
            checked += 1  # В  противном  случае  увеличить  счетчик  checked (в  котором  хранится количест во проверенных чисел) и отобразить результаты.
            label = 'P' if prime else ' '
            print(f'{n:16}  {label} {elapsed:9.6f}s')
    return checked

if __name__ == '__main__':
    main()