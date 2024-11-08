import threading
import concurrent.futures
import time
import pyads

from multithreading_module import make_pool, make_lock, make_event
from task_module import fast_loop, slow_loop

AMSNETID = "192.168.0.3.1.1"

if __name__ == "__main__":
    # Code to execute when run as a script
    print('starting the digital twin')

    # Create event and lock object in threading
    event = make_event()
    lock = make_lock()

    # open connection to PLC
    plc = pyads.Connection(AMSNETID, pyads.PORT_TC3PLC1)
    plc.open()
    
    # Gain time by using a fixed handle for frequently used variables
    #fHandle = plc.get_handle('MAIN.fArray')
    #tHandle = plc.get_handle('MAIN.tArray')

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:

        pool.submit(fast_loop, 0.50, event, lock, plc, "MAIN.iCounter")
        pool.submit(slow_loop, 5, event, lock, plc)

        time.sleep(10)
        event.set()

    #plc.release_handle(fHandle)
    #plc.release_handle(tHandle)
    plc.close()
    
