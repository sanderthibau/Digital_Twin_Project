
from ads_communication_module import read_twincat_structure,write_twincat_variable, select_useful_data, write_buffer
from model_module import model
from cartesian_robot_module import sys_response


def fast_loop(period, event_f, lock, plc, queue_data, fHandle, input_keys=['aInputTorque']):
    last_counter = 0
    initial_state = [[0],[0],[0],[0]]

    while not event_f.wait(period):

        with lock:
            
            buffer_dict = read_twincat_structure(plc)
            
        
        sorted_buffer = select_useful_data(buffer_dict, last_counter)
        queue_data.put(sorted_buffer)
        
        last_counter = sorted_buffer['aDataCounter'][-1]
        
        #write_buffer('databuffer.csv', sorted_buffer, lock)

        """
        The first two columns of the buffer are the datacounter and time, then all other data follows.
        The keys of inputs and outputs should be given to allow the program to function generally for all models.
        """
        inputs = []
        for key in input_keys:
            inputs.append(sorted_buffer[key])




        
        print('fast loop')
        

        
        



def slow_loop(period, event_s, lock, plc):
    while not event_s.wait(period):
        with lock:
            #write_twincat_variable("MAIN.iCounter", 0, plc)
            None
        print('slow loop')
