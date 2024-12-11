import csv
from ads_communication_module import read_twincat_structure,write_twincat_variable, select_useful_data, write_buffer

last_counter = 0
def fast_loop(period, event_f, lock, plc, fHandle):
    while not event_f.wait(period):
        with lock:
            buffer_dict = read_twincat_structure(plc)
            #print(var)
        
        sorted_buffer = select_useful_data(buffer_dict, last_counter)
        
        write_buffer('databuffer.csv', sorted_buffer)
        database_file = 'databuffer.csv'

        with open(database_file, "w", newline='') as outfile:
            csvwriter = csv.writer(outfile)
            csvwriter.writerow(sorted_buffer)

            len_buffer = len(sorted_buffer['aDataCounter'])
            for i in range(len_buffer):
                csvwriter.writerow([sorted_buffer[key][i] for key in sorted_buffer])
        print('fast')
        

        
        



def slow_loop(period, event_s, lock, plc):
    while not event_s.wait(period):
        with lock:
            #write_twincat_variable("MAIN.iCounter", 0, plc)
            None
        print('slow loop')
