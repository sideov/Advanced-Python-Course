import time
import threading
import multiprocessing

def fib(n: int) -> int:
    if n <= 1:
        return 1
    return fib(n - 1) + fib(n - 2)

def run_sequential(n: int, count: int) -> float:
    results = []
    start = time.time()
    for _ in range(count):
        results.append(fib(n))
    end = time.time()
    return end - start

def run_threading(n: int, count: int) -> float:
    def worker_thread(n):
        fib(n)
    threads = []
    start = time.time()
    for i in range(count):
        t = threading.Thread(target=worker_thread, args=(n, ))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    end = time.time()
    return end - start

def worker_process(n):
    fib(n)

def run_multiprocessing(n: int, count: int) -> float:
    processes = []
    start = time.time()
    for _ in range(count):
        p = multiprocessing.Process(target=worker_process, args=(n, ))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    end = time.time()
    return end - start

if __name__ == "__main__":
    n = 35
    count = 10

    seq_time = run_sequential(n, count)
    thread_time = run_threading(n, count)
    process_time = run_multiprocessing(n, count)

    result_text = (
        f"Синхронный запуск: {seq_time:.4f} сек\n"
        f"Запуск с потоками: {thread_time:.4f} сек\n"
        f"Запуск с процессами: {process_time:.4f} сек\n\n"
    )

    with open("artifacts/task1-fib-results.txt", "w") as f:
        f.write(result_text)
