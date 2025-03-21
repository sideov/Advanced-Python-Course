import sys
import time
import logging
import multiprocessing
import threading
import codecs

logging.basicConfig(
    filename="artifacts/task3-parallel_app.txt",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(processName)s: %(message)s",
)


def process_A(queue_in: multiprocessing.Queue, queue_out: multiprocessing.Queue):
    logging.info("Процесс A запущен")
    local_msgs = []
    last_sent = time.time() - 5

    while True:
        try:
            msg = queue_in.get(timeout=0.5)
            if msg == "exit":
                logging.info("Процесс A получил команду завершения")
                break
            local_msgs.append(msg)
            logging.info(f"Процесс A получил сообщение: {msg}")
        except Exception as e:
            pass

        if local_msgs and (time.time() - last_sent >= 5):
            msg_to_send = local_msgs.pop(0).lower()
            logging.info(f"Процесс A отправляет сообщение в B: {msg_to_send}")
            queue_out.put(msg_to_send)
            last_sent = time.time()
    queue_out.put("exit")
    logging.info("Процесс A завершен")


def process_B(queue_in, queue_out):
    logging.info("Процесс B запущен")
    while True:
        msg = queue_in.get()
        if msg == "exit":
            logging.info("Процесс B получил команду завершения")
            break
        encoded = codecs.encode(msg, 'rot_13')
        out_msg = str(encoded)
        print(out_msg)
        logging.info(f"Процесс B обработал сообщение: {out_msg}")
        queue_out.put(out_msg)
    logging.info("Процесс B завершен")


def main_receiver(queue_from_B: multiprocessing.Queue):
    while True:
        msg = queue_from_B.get()
        if msg == "exit":
            logging.info("Главный процесс получил сигнал завершения от процесса B")
            break
        logging.info(f"Главный процесс получил сообщение от B: {msg}")


if __name__ == "__main__":
    queue_A = multiprocessing.Queue()
    queue_AB = multiprocessing.Queue()
    queue_B = multiprocessing.Queue()

    proc_A = multiprocessing.Process(target=process_A, args=(queue_A, queue_AB), name="Process-A")
    proc_B = multiprocessing.Process(target=process_B, args=(queue_AB, queue_B), name="Process-B")
    proc_A.start()
    proc_B.start()

    receiver_thread = threading.Thread(target=main_receiver, args=(queue_B,))
    receiver_thread.start()

    logging.info("Главный процесс запущен")

    while True:
        try:
            user_input = sys.stdin.readline().strip()
            if not user_input:
                continue
            logging.info(f"Главный процесс отправляет сообщение в A: {user_input}")
            queue_A.put(user_input)
            if user_input == "exit":
                break
        except KeyboardInterrupt:
            break

    proc_A.join()
    proc_B.join()
    queue_B.put("exit")
    receiver_thread.join()
    logging.info("Главный процесс завершен")
