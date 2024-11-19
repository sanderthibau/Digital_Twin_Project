import matplotlib.pyplot as plt
import pyads
import time



AMSNETID = "192.168.0.3.1.1" #local netid
BufferSize = 100

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

def search_index_nextStep(data_counter, previous_counter):
    """
    When a circular buffer is read out, this function searches the data point following on the last processed point.
    """
    try:
        index = data_counter.index(previous_counter+1)
    except:
        try:
            index = data_counter.index(previous_counter+2)
        except:
            index = 'NoIndexFound'
            print('More than 1 data point is missing, the digital twin is of track')
    return index

def select_useful_data(buffer_od, previous_counter):
    sorted_od = buffer_od
    return sorted_od

if __name__ == "__main__":
    plc = pyads.Connection(AMSNETID, pyads.PORT_TC3PLC1)
    plc.open()
    

    data = read_twincat_structure(plc)
    
    
    plc.close()
    x = []
    tlist = []

    plc.open()
    for e in range(1000):
        start_time = time.time()
        
    
        ord_dir = read_twincat_structure(plc)
    
        

        x.append(e)
        tlist.append(time.time() - start_time)
    plc.close()
    print("done")

    #print(ord_dir)

    
    plt.hist(tlist, 5)
    plt.xlabel('reading time')
    plt.ylabel('amount')
    plt.show()
    
