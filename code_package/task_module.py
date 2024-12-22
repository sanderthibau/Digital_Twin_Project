
from ads_communication_module import read_twincat_structure,write_twincat_variable, select_useful_data, write_buffer


def fast_loop(period, event_f, lock, plc, fHandle):
    last_counter = 0
    while not event_f.wait(period):

        with lock:
            
            buffer_dict = read_twincat_structure(plc)
            
        print(last_counter)
        sorted_buffer = select_useful_data(buffer_dict, last_counter)
        
        last_counter = sorted_buffer['aDataCounter'][-1]
        
        write_buffer('databuffer.csv', sorted_buffer, lock)
        
        
        print('fast loop')
        

        
        



def slow_loop(period, event_s, lock, plc):
    while not event_s.wait(period):
        with lock:
            #write_twincat_variable("MAIN.iCounter", 0, plc)
            None
        print('slow loop')
