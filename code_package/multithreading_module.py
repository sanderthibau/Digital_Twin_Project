import threading
import concurrent.futures
from queue import Queue
import multiprocessing


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

def make_queue(max_size=100):
    print("queue")
    return Queue(max_size)




##TEST

if __name__ == "__main__":
    import pyads
    import multiprocessing
    import numpy as np
    from collections import OrderedDict
    import time

    AMSNETID = "192.168.0.3.1.1"
    plc = pyads.Connection(AMSNETID, pyads.PORT_TC3PLC1)

    DataSize = 500
    number = 10
    a = np.random.rand(DataSize)


    #var_names = ['A','B','C','D','E','F','G','H','I','J']
    start = time.perf_counter()
    var_names = [f'A{i}' for i in range(number)]
    
    #print(var_names)
    
    PLCtypes = [pyads.PLCTYPE_REAL for _ in range(len(var_names))]
    stop1 = time.perf_counter()
    var_lists = [np.random.rand(DataSize) for _ in range(len(var_names))]
    stop2 = time.perf_counter()

    struct_def = tuple((var_name,PLCtype, DataSize) for var_name, PLCtype in zip(var_names, PLCtypes))
    #print(struct_def)
    stop3 = time.perf_counter()

    print(f'DataSize={DataSize}, number of arrays={number}, {-start+stop1}s: var_names + types, {stop2- stop1}s: lists, {stop3-stop2}s: struct tuple')

    ordered_dict_vars = OrderedDict([(var_name, var) for var_name, var in zip(var_names,var_lists)])


    connect = 1
    if connect:

        plc.open()
        plc.write_by_name('MAIN.a', a)
        plc.close()
        plc.open()
        a2 = plc.read_by_name('MAIN.a')

        print(f'length = {len(a2)}')
        plc.write_structure_by_name('Global.Struc', ordered_dict_vars, struct_def)
        plc.close()

    # process_pool = concurrent.futures.ProcessPoolExecutor()
    # thread_pool = make_pool(1)
    # mpQueue = multiprocessing.Queue()

    # def proces1(queue):
    #     while not queue.empty():
    #         data = queue.get()
    #         data *= data
    #         print(data)

    # with process_pool:
    #     process_pool.submit(proces1, mpQueue)
