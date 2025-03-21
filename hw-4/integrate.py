import math
import time
import os
import logging
import concurrent.futures

cpu_num = os.cpu_count() or 1
logging.basicConfig(
    filename="artifacts/task2-parallel_integration.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def integrate_chunk(f, a, b, n_iter):
    logging.info(f"Запуск задачи: интегрирование на интервале [{a}, {b}] с {n_iter} итерациями")
    acc = 0.0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    logging.info(f"Задача завершена: интегрирование на интервале [{a}, {b}] с {n_iter} итерациями")
    return acc


def integrate(f, a, b, *, n_jobs=1, n_iter=10_000_000, executor_type='thread'):
    chunk_n_iter = n_iter // n_jobs
    total_range = b - a
    chunk_size = total_range / n_jobs

    if executor_type == 'thread':
        executor = concurrent.futures.ThreadPoolExecutor
    else:
        executor = concurrent.futures.ProcessPoolExecutor

    futures = []
    with executor(max_workers=n_jobs) as executor:
        for i in range(n_jobs):
            a_i = a + i * chunk_size
            b_i = a + (i + 1) * chunk_size if i < n_jobs - 1 else b
            futures.append(executor.submit(integrate_chunk, f, a_i, b_i, chunk_n_iter))
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    return sum(results)


def compare_integration(executor_type):
    times = {}
    for n_jobs in range(1, cpu_num * 2 + 1):
        start = time.time()
        result = integrate(math.cos, 0, math.pi / 2, n_jobs=n_jobs, executor_type=executor_type)
        elapsed = time.time() - start
        times[n_jobs] = elapsed
        logging.info(
            f"Тип: {executor_type:7} | n_jobs: {n_jobs:2d} | Результат: {result:.8f} | Время: {elapsed:.4f} сек")
    return times


if __name__ == '__main__':
    thread_times = compare_integration('thread')
    process_times = compare_integration('process')

    with open("artifacts/task2-integration_times.txt", "w") as f:
        f.write("n_jobs".center(10) + "ThreadTime(sec)".center(15) + "ProcessTime(sec)".center(10) + "\n")
        for n_jobs in range(1, cpu_num * 2 + 1):
            t_time = thread_times[n_jobs]
            p_time = process_times[n_jobs]
            f.write(f"{n_jobs}".center(10) + f"{t_time:.4f}".center(15) + f"{p_time:.4f}".center(10) + "\n")
