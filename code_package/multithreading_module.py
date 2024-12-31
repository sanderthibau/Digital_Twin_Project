import threading
import concurrent.futures
from queue import Queue


def make_pool(amount_threads):
    return concurrent.futures.ThreadPoolExecutor(max_workers=amount_threads)

def make_lock():
    print("lock")
    return threading.Lock()

def make_thread(function):
    return threading.Thread(target=function)

def make_event():
    print("event")
    return threading.Event()

def make_queue(max_size=1000):
    print("queue")
    return Queue(max_size)