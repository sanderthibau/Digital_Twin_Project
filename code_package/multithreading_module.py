import time
import threading
import concurrent.futures


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

