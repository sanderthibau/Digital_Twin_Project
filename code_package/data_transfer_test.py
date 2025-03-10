import pyads
import multiprocessing
import queue
import numpy as np
from collections import OrderedDict
import time
import concurrent.futures

def init_pool_processes(q, plc):
    global queue

    queue = q

def proces1():
    for i in range(10):
        queue.put(i)

def proces2():
    print('in')

    for i in range(10):
        print(queue.get())

def proces3(Queue, plc, type, DataSizes, number_in_struct, test_size):
    ds = len(DataSizes)
    transfer_time_read = np.zeros((ds,5))
    transfer_time_put = np.zeros((ds,5))
    

    plc.open()

    print('in process3')

    for s in range(ds):
        plc.write_by_name('MAIN.a', np.random.rand(DataSizes[s]))


        #var_names = [f'A{i}' for i in range(number)]
        #plc.write_structure_by_name('Global.Struc', ordered_dict_vars, struct_def)
    
        read_times = np.zeros(test_size)
        put_times = np.zeros(test_size)
        
        for i in range(test_size):

            start = time.perf_counter()
            A = plc.read_by_name('MAIN.a', pyads.PLCTYPE_REAL * DataSizes[s])
            #od_readstruct = plc.read_structure_by_name('Global.Struc', struct_def)

            read_time = time.perf_counter() - start
            read_times[i] = read_time

            start = time.perf_counter_ns()
            Queue.put(A)
            #Queue.put(od_readstruct)
            put_time = time.perf_counter_ns() - start
            put_times[i] = put_time


        transfer_time_read[s] = (np.mean(read_times), np.min(read_times), np.max(read_times), np.percentile(read_times, 5), np.percentile(read_times, 95))
        transfer_time_put[s] = (np.mean(put_times), np.min(put_times), np.max(put_times), np.percentile(put_times, 5), np.percentile(put_times, 95))

    np.savez('transfer_times'+f'_{type}', TimeRead=transfer_time_read, TimePut=transfer_time_put)

    print('done_read_put')
    plc.close()


def proces33(Queue, plc, type, DataSizes, number_in_struct, test_size):
    ds = len(DataSizes)
    transfer_time_read = np.zeros((ds,5))
    transfer_time_put = np.zeros((ds,5))
    

    plc.open()
    print('in process33')

    for s in range(ds):
        #plc.write_by_name('MAIN.a', np.random.rand(DataSizes[s]))


        var_names = [f'A{i}' for i in range(number_in_struct)]
        PLCtypes = [pyads.PLCTYPE_REAL for _ in range(number_in_struct)]
        var_lists = [np.random.rand(DataSizes[s]) for _ in range(number_in_struct)]
        ordered_dict_vars = OrderedDict([(var_name, var) for var_name, var in zip(var_names,var_lists)])
        struct_def = tuple((var_name,PLCtype, DataSizes[s]) for var_name, PLCtype in zip(var_names, PLCtypes))
        plc.write_structure_by_name('Global.Struc', ordered_dict_vars, struct_def)
        

        read_times = np.zeros(test_size)
        put_times = np.zeros(test_size)
        
        for i in range(test_size):

            start = time.perf_counter()
            #A = plc.read_by_name('MAIN.a', pyads.PLCTYPE_REAL * DataSizes[s])
            od_readstruct = plc.read_structure_by_name('Global.Struc', struct_def)

            read_time = time.perf_counter() - start
            read_times[i] = read_time

            start = time.perf_counter_ns()
            Queue.put(od_readstruct)
            #Queue.put(od_readstruct)
            put_time = time.perf_counter_ns() - start
            put_times[i] = put_time

        transfer_time_read[s] = (np.mean(read_times), np.min(read_times), np.max(read_times), np.percentile(read_times, 5), np.percentile(read_times, 95))
        transfer_time_put[s] = (np.mean(put_times), np.min(put_times), np.max(put_times), np.percentile(put_times, 5), np.percentile(put_times, 95))

    np.savez('transfer_times'+f'_{type}_struct', TimeRead=transfer_time_read, TimePut=transfer_time_put)

    print('done_read_put')
    plc.close()

def proces4(Queue, type, DataSizes, test_size):
    ds = len(DataSizes)
    transfer_time_get = np.zeros((ds,5))

    print('get')

    for s in range(ds):
        
        get_times = np.zeros(test_size)
        for i in range(test_size):

            while Queue.empty():
                time.sleep(0.0001)
            start = time.perf_counter_ns()
            x = Queue.get()
            get_time = time.perf_counter_ns() - start
            get_times[i] = get_time
        
        transfer_time_get[s] = (np.mean(get_times), np.min(get_times), np.max(get_times), np.percentile(get_times, 5), np.percentile(get_times, 95)) 

    np.save('get_times'+f'_{type}', transfer_time_get)


    print('done_get')
     
def proces44(Queue, type, DataSizes, test_size):
    ds = len(DataSizes)
    transfer_time_get = np.zeros((ds,5)) 
    print('get')

    for s in range(ds):
        
        get_times = np.zeros(test_size)
        for i in range(test_size):

            while Queue.empty():
                time.sleep(0.0001)

            start = time.perf_counter_ns()
            x = Queue.get()
            get_time = time.perf_counter_ns() - start
            get_times[i] = get_time

        
        transfer_time_get[s] = (np.mean(get_times), np.min(get_times), np.max(get_times), np.percentile(get_times, 5), np.percentile(get_times, 95))

    np.save('get_times'+f'_{type}_struct', transfer_time_get)


    print('done_get')
    


if __name__ == '__main__':
    AMSNETID = "192.168.0.3.1.1"

    AMSNETID = "5.134.123.108.1.1"
    
    plc = pyads.Connection(AMSNETID, pyads.PORT_TC3PLC1)

    DataSize = 10000
    test_size = 100
    number = 1
    a = [i for i in range(10000)]#np.random.rand(DataSize)

    # pools and queues    

    mpoolQueue = multiprocessing.Queue()
    Queue = queue.Queue()    
    process_pool = concurrent.futures.ProcessPoolExecutor(max_workers=1,initializer=init_pool_processes, initargs=(mpoolQueue,))
    thread_pool = concurrent.futures.ThreadPoolExecutor()

    #var_names = ['A','B','C','D','E','F','G','H','I','J']
    start = time.perf_counter()

    var_names = [f'A{i}' for i in range(number)]

    #print(var_names)
    PLCtypes = [pyads.PLCTYPE_REAL for _ in range(len(var_names))]

    stop1 = time.perf_counter()
    var_lists = [np.random.rand(DataSize) for _ in range(len(var_names))]
    ordered_dict_vars = OrderedDict([(var_name, var) for var_name, var in zip(var_names,var_lists)])
    stop2 = time.perf_counter()

    struct_def = tuple((var_name,PLCtype, DataSize) for var_name, PLCtype in zip(var_names, PLCtypes))
    #print(struct_def)
    stop3 = time.perf_counter()

    print(f'DataSize={DataSize}, number of arrays={number}, {-start+stop1}s: var_names + types, {stop2- stop1}s: lists, {stop3-stop2}s: struct tuple')

    plc.write_structure_by_name('Global.Struc', ordered_dict_vars, struct_def)
    od_readstruct = plc.read_structure_by_name('Global.Struc', struct_def)
    

    DataSizes = [50] + [500*i for i in range(1, 11)]
    number_in_struct = 10 #[i for i in range(1,11)]
    ds = len(DataSizes)

    np.savez('parameters',  DataSizes=np.array(DataSizes))

    transfer_time_read = np.zeros((ds,5))
    transfer_time_put = np.zeros((ds,5))
    transfer_time_get = np.zeros((ds,5))

    test_size = 100

    connect = 0
    if connect:

        plc.open()

        plc.write_by_name('MAIN.a', np.random.rand(DataSize))

        for s in range(ds):
            plc.write_by_name('MAIN.a', np.random.rand(DataSizes[s]))

            read_times = np.zeros(test_size)
            put_times = np.zeros(test_size)
            get_times = np.zeros(test_size)
            for i in range(test_size):

                start = time.perf_counter()
                A = plc.read_by_name('MAIN.a')
                read_time = time.perf_counter() - start
                read_times[i] = read_time

                start = time.perf_counter_ns()
                Queue.put(A)
                put_time = time.perf_counter_ns() - start
                put_times[i] = put_time

                start = time.perf_counter_ns()
                x = Queue.get(A)
                get_time = time.perf_counter_ns() - start
                get_times[i] = get_time



            transfer_time_read[s] = (np.mean(read_times), np.min(read_times), np.max(read_times), np.percentile(read_times, 5), np.percentile(read_times, 95))
            transfer_time_put[s] = (np.mean(put_times), np.min(put_times), np.max(put_times), np.percentile(put_times, 5), np.percentile(put_times, 95))
            transfer_time_get[s] = (np.mean(get_times), np.min(get_times), np.max(get_times), np.percentile(get_times, 5), np.percentile(get_times, 95))

        

        np.savez('transfer_times', TimeRead=transfer_time_read, TimePut=transfer_time_put, TimeGet=transfer_time_get)

        plc.close()

        # plc.open()

        # a2 = plc.read_by_name('MAIN.a')

        
        # plc.write_structure_by_name('Global.Struc', ordered_dict_vars, struct_def)
        # od_readstruct = plc.read_structure_by_name('Global.Struc', struct_def)
        # plc.close()
        # print(f'last = {a2[-1]}')
        # #print(f'check structure : {od_readstruct}')
        # x = od_readstruct['A9'][-1]
        # print(x)

    ## PROCESSPOOL
    mpool = 0
    if mpool:
        with process_pool:
            process_pool.submit(proces1)
            print('procespool')
            time.sleep(2)
            process_pool.submit(proces2)

    Type = ['multithreading', 'multiprocessing', 'manager_queue']
    load = 1
    if load:
        Type = ['L_'+e for e in Type]


    ## MULTITHREADING
    mt = 0
    if mt:
        print('thread')
        with thread_pool:
            thread_pool.submit(proces3, Queue, plc, Type[0], DataSizes, number_in_struct, test_size)
            time.sleep(25)
            thread_pool.submit(proces4, Queue, Type[0], DataSizes, test_size)

    ## MULTIPROCESS
    mp = 0
    if mp:
        mpQueue = multiprocessing.Queue()
        p1 = multiprocessing.Process(target=proces33, args=(mpQueue, plc, Type[1], DataSizes, number_in_struct, test_size)) 
        p2 = multiprocessing.Process(target=proces44, args=(mpQueue, Type[1], DataSizes, test_size))
        print('mproces')

        # Start both processes 
        p1.start()
        time.sleep(2)
        
        p2.start() 
  
        # Wait for processes to finish 
        p1.join()

        
        p2.join()

    mngr = 1
    if mngr:
        with multiprocessing.Manager() as manager: 
        # Create a queue within the context of the manager 
            q = manager.Queue() 
            print('manager')
            # Create two instances of the Process class, one for each function 
            p1 = multiprocessing.Process(target=proces3, args=(q, plc, Type[2], DataSizes, number_in_struct, test_size)) 
            p2 = multiprocessing.Process(target=proces4, args=(q, Type[2], DataSizes, test_size)) 
    
            # Start both processes 
            p1.start()
            time.sleep(5) 
            p2.start() 
    
            # Wait for both processes to finish 
            p1.join() 
            p2.join() 