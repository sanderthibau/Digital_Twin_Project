import numpy as np
import csv
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation



def save_buffercsv(sorted_buffer):
    with open("databuffer.csv", "w", newline='') as outfile:
            csvwriter = csv.writer(outfile)
            len_buffer = len(sorted_buffer['aDataCounter'])
            for i in range(len_buffer):
                csvwriter.writerow([sorted_buffer[key][i] for key in sorted_buffer])


def read_csvHeader(csvFile, lock):
    with lock:
        with open(csvFile, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                headers = row
                break
    return headers

def read_csvData(csvFile, lock, noheader=True):
    with lock:
        with open(csvFile, 'r') as file:
                reader = csv.reader(file)
                if noheader:
                    next(reader, None)
                buffer_array = [] #np.empty((0,4)) 
                for line in reader:
                    floats = np.fromiter([float(e) for e in line], float)
                    buffer_array.append(floats) #np.append(buffer_array, np.array([floats]), axis=0)
    return np.asarray(buffer_array)

def create_dict_HeadersAndData(headers, buffer_array):
    dict = {}
    amountofValues = len(headers)
    for i in range(amountofValues):
          dict[headers[i]] = buffer_array[:,i]

    return dict



def initiate_plot(rows=2, cols=1, n_plot=500, labels=('aInputTorque','aSensorAngle'), ylabels=('Input [T]','Sensor [rad]'), ylimits=((-20,20),(-0.01, 0.31))):
    fig, axs = plt.subplots(nrows=rows, ncols=cols, layout='constrained')
    i = 0
    plot_arrays = np.full((len(labels)+1,n_plot), np.nan)
    
    lines = []
    for ax in axs:
         ax.set_ylabel(ylabels[i])
         ax.set_ylim(ylimits[i])
         
         line, = ax.plot([], [], label=labels[i])
         lines.append(line)

         ax.set_xlabel('Time [s]')
         ax.set_xlim((0,1000))
         ax.set_xticklabels([])

         ax.legend()

         i += 1
    return fig, axs, lines, plot_arrays

def animate(iter, lock, plot_arrays, lines, n_plot=500, n_step=10 , keys=('aInputTorque','aSensorAngle')):
        
    # update data from data base
        
    start = time.perf_counter()
    headers = read_csvHeader('databuffer.csv', lock)
    data =  read_csvData('databuffer.csv', lock)
    #print(data)
    plotstep_dict = create_dict_HeadersAndData(headers, data)
    stop = time.perf_counter()
    #print(stop-start)
            
    buffer_length = plotstep_dict['aTime'].shape[0]
    


        


        # set data on line object

        #print(plot_arrays[0,-1])
        #print(plotstep_dict['aDataCounter'])
    #print(plot_arrays[0,:])


    if plot_arrays[0,-1] != plotstep_dict['aDataCounter'][-1] or np.isnan(plot_arrays[0,-1]):
        
        plot_arrays[0,:] = np.concatenate((plot_arrays[0,:],plotstep_dict['aDataCounter']))[-n_plot:]
        


        for i in range(len(lines)):
            plot_arrays[i+1,:] = np.concatenate((plot_arrays[i+1,:],plotstep_dict[keys[i]]))[-n_plot:]
            lines[i].set_data(plot_arrays[0,:], plot_arrays[i+1,:])



        #lines[i].set_data(dict_data['aDataCounter'][-50:iter], dict_data[keys[i]][-50:iter])
        

    # rescale axes
    rescale = False

    # for ax, y, t in zip(axs, ydata, tdata):
    #      if y < ax.get_ylimit()[0]:
    #           ax.set_limits(y, ax.get_limit()[1])
            

        
        
    return lines    
        
def plot_figure(lock):

    ani = animation.FuncAnimation(fig=fig, func=animate, fargs=(lock,), blit=True, interval=1000, repeat=False)
    
    return ani


     



if __name__ == "__main__":
    fig,axs,lines, plot_arrays=initiate_plot()
    from multithreading_module import make_lock
    lock = make_lock()
    
    animation = plot_figure(lock)
    print('carry on bro')
    

    

    



    


    
    
    
    
    testing = 0
    if testing == 1:

        filename = 'database.csv'
        head = read_csvHeader(filename)
        data = read_csvData(filename)

        dictionary = create_dict_HeadersAndData(head, data)



        #data = np.genfromtxt('database.csv', delimiter=', ', dtype= float) #[('aDataCounter', int), ('aTime', int), ('aInputTorque', float), ('aSensorAngle', float)], names=True)
        #print(data)

        start = time.perf_counter()
        
        
        
        with open('database.csv', 'r') as file:


            # reading the csv file using DictReader
            csv_reader = csv.DictReader(file)
            
            # converting the file to dictionary
            # by first converting to list
            # and then converting the list to dict
            dict_from_csv = dict(list(csv_reader)[0])
            
 
            # making a list from the keys of the dict
            list_of_column_names = list(dict_from_csv.keys())
 
            # displaying the list of column names
            print("List of column names : ", read_csvHeader('database.csv'))


            reader = csv.reader(file)
            next(reader, None)
            buffer_array = np.empty((0,4)) 
            for line in reader:
                floats = [float(e) for e in line]
                buffer_array = np.append(buffer_array, np.array([floats]), axis=0)
        
        stop = time.perf_counter()
        print(f"reading csv took {stop-start} seconds")  
        
        
        #plt.plot(buffer_array[:,0]/100,buffer_array[:,3]*100)
        #plt.show()

# if iter == step_amount:

        #     for key in keys:
        #         plotstep_dict[key] = dict_data[key][(iter)*n_step:]
        #         plotstep_dict['aTime'] = dict_data['aTime'][(iter)*n_step:]
        #     iter = 0

        # else:
        #     for key in keys:
        #         plotstep_dict[key] = dict_data[key][(iter)*n_step:(iter+1)*n_step]
        #         plotstep_dict['aTime'] = dict_data['aTime'][(iter)*n_step:(iter+1)*n_step]
            

