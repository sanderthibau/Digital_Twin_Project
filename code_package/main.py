import threading
import concurrent.futures
import time
import pyads
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from multithreading_module import make_pool, make_lock, make_event
from task_module import fast_loop, slow_loop
from csv_plot_module import plot_figure, initiate_plot, animate

AMSNETID = "192.168.0.3.1.1"

if __name__ == "__main__":
    # Code to execute when run as a script
    print('starting the digital twin')

    # Create event and lock object in threading
    stop_event = make_event()
    lock = make_lock()

    # open connection to PLC
    plc = pyads.Connection(AMSNETID, pyads.PORT_TC3PLC1)
    plc.open()
    
    # Gain time by using a fixed handle for frequently used variables
    #fHandle = plc.get_handle('MAIN.fArray')
    #tHandle = plc.get_handle('MAIN.tArray')

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:

        pool.submit(fast_loop, 0.1, stop_event, lock, plc, "MAIN.iCounter")
        pool.submit(slow_loop, 5, stop_event, lock, plc)


        fig,axs,lines, plot_arrays = initiate_plot()
        lock = make_lock()
    
        animation = animation.FuncAnimation(fig=fig, func=animate, fargs=(lock,plot_arrays,lines), blit=True, interval=10, repeat=False)

        def on_close(event):
            print("Stopping threads...")
            stop_event.set()  # Signal threads to stop
            pool.shutdown(wait=True)  # Wait for threads to finish
            print("All threads stopped.")

        fig.canvas.mpl_connect('close_event', on_close)

        plt.show()

        
    

        


    #plc.release_handle(fHandle)
    #plc.release_handle(tHandle)
    plc.close()
    
