
import pyads
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from multithreading_module import make_pool, make_lock, make_event, make_queue
from task_module import fast_loop, slow_loop
from csv_plot_module import plot_figure, initiate_plot, animate

AMSNETID = "192.168.0.3.1.1"




if __name__ == "__main__":

    #send simulation data to TwinCat for testing purposes

    with open('tests/simulate_model.py') as file:
        exec(file.read())


    # Code to execute when run as a script
    print('starting the digital twin')


    # Create event and lock object in threading
    stop_event = make_event()
    lock = make_lock()
    queue_data = make_queue()
    queue_calculated = make_queue()

    # open connection to PLC
    plc = pyads.Connection(AMSNETID, pyads.PORT_TC3PLC1)
    plc.open()
    
    # Gain time by using a fixed handle for frequently used variables
    #fHandle = plc.get_handle('MAIN.fArray')
    #tHandle = plc.get_handle('MAIN.tArray')

    with make_pool(2) as pool:

        pool.submit(fast_loop, 0.99, stop_event, lock, plc, queue_data, queue_calculated)
        pool.submit(slow_loop, 5, stop_event, lock, plc)


        fig,axs,lines,plot_arrays = initiate_plot()
        csv_lock = make_lock()

    
        #plot_figure(fig, axs, lock, plot_arrays, lines, int=1000)
        anim = animation.FuncAnimation(fig=fig, func=animate, fargs=(csv_lock,plot_arrays,lines,axs, fig, queue_data, queue_calculated, False), blit=True, interval=1000, repeat=False)

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
    
