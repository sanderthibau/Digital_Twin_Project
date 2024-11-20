import matplotlib.pyplot as plt
import numpy as np
import pyads
import time



AMSNETID = "192.168.0.3.1.1" #local netid
BufferSize = 10

def write_twincat_variable(var_name_TC, var_python, plc):
    #plc = pyads.Connection(AMSNETID, pyads.PORT_TC3PLC1)
    #plc.open()
    #print(f"Connected?: {plc.is_open}") #debugging statement, optional
    #print(f"Local Address? : {plc.get_local_address()}") #debugging statement, optional
    #write var
    plc.write_by_name(var_name_TC, var_python)
    #plc.close()


def read_twincat_variable(var_name, plc):
    #plc = pyads.Connection(AMSNETID, pyads.PORT_TC3PLC1)
    #plc.open()
    #print(f"Connected?: {plc.is_open}") #debugging statement, optional
    #print(f"Local Address? : {plc.get_local_address()}") #debugging statement, optional
    #read var
    #hand = plc.get_handle('MAIN.iCounter')
    varTC = plc.read_by_name(var_name)
    #plc.close()
    return varTC

def read_twincat_structure(plc, struct_name='Global.Buffer',
                           struct_def=(('aDataCounter', pyads.PLCTYPE_UDINT, BufferSize),
                                        ('aTime', pyads.PLCTYPE_ULINT, BufferSize),
                                        ('aInputTorque', pyads.PLCTYPE_REAL, BufferSize),
                                        ('aSensorAngle', pyads.PLCTYPE_REAL, BufferSize))):
    
    ordered_dictionary = plc.read_structure_by_name(struct_name, struct_def)
    return ordered_dictionary

def search_index_nextStep(data_counter, previous_counter, max_missing=1):
    """
    When a circular buffer is read out, this function searches the data point following on the last processed point.
    """
    if not isinstance(data_counter, np.ndarray):
        data_counter = np.array(data_counter)
    try:
        index = np.where(data_counter==previous_counter+1)[0][0]
    except:
        try:
            index = np.where((data_counter<previous_counter+2+max_missing)&(data_counter>previous_counter))[0][0]
        except:
            index = 'NoIndexFound'
            print('More than 1 data point is missing, the digital twin is off track')
        
    return index
def search_index_lastStep(data_counter):
    """
    The last data point added to the buffer has the highest value of Counter
    """
    if not isinstance(data_counter, np.ndarray):
        data_counter = np.array(data_counter)
    index = np.argmax(data_counter)
    return index

def put_array_chronologically(data_array, index_first, index_last):
    if not isinstance(data_array, np.ndarray):
        data_array = np.array(data_array)

    if index_last<index_first:
        sorted = np.concatenate((data_array[index_first:],data_array[:index_last+1]))
    else:
        sorted = data_array[index_first:index_last+1]
    return sorted

def select_useful_data(buffer_od, previous_counter):
    counters = buffer_od['aDataCounter']

    index_start = search_index_nextStep(counters, previous_counter)
    index_end = search_index_lastStep(counters)
    for varname, array in buffer_od.items():
        array_useful = put_array_chronologically(array, index_start, index_end)
        buffer_od[varname] = array_useful
    return buffer_od

if __name__ == "__main__":
    print('running')


    testing = 1
    if testing == 1:
        plc = pyads.Connection(AMSNETID, pyads.PORT_TC3PLC1)
        plc.open()
        buffer_od = read_twincat_structure(plc)
        plc.close()
        print(buffer_od)
        last_counter = 37
        array_of_counters = np.array(buffer_od['aDataCounter'])
        starting_index = search_index_nextStep(array_of_counters,last_counter)
        last_index = search_index_lastStep(array_of_counters)
        print(starting_index)
        print(last_index)
        sorted_array = put_array_chronologically(array_of_counters, starting_index, last_index)
        print(sorted_array)

        array_of_time = buffer_od['aTime']
        print(array_of_time)
        sorted_time = put_array_chronologically(array_of_time, starting_index, last_index)
        print(f'this is the time array sorted: {sorted_time}')



 
    # HISTOGRAM OF TIME TO READ BUFFER (100x[counter,time,torque,angle])
    # x = []
    # tlist = []

    # plc.open()
    # for e in range(1000):
    #     start_time = time.time()
        
    
    #     ord_dir = read_twincat_structure(plc)
    
        

    #     x.append(e)
    #     tlist.append(time.time() - start_time)
    # plc.close()
    # print("done")

    # #print(ord_dir)

    
    # plt.hist(tlist, 5)
    # plt.xlabel('reading time')
    # plt.ylabel('amount')
    # plt.show()

