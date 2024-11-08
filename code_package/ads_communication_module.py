import matplotlib.pyplot as plt
import pyads
import time



AMSNETID = "192.168.0.3.1.1" #local netid

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


if __name__ == "__main__":
    plc = pyads.Connection(AMSNETID, pyads.PORT_TC3PLC1)
    plc.open()
    x = []
    tlist = []
    for e in range(100):
        start_time = time.time()
        read_twincat_variable("MAIN.iCounter", plc)
        x.append(e)
        tlist.append(time.time() - start_time)
    plc.close()
    print("done")

    print(tlist)

    plt.figure(1)
    plt.hist([1,2,3],[1,2,3])
    print("graph")
    plt.show
