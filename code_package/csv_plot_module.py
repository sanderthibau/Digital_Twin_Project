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



def initiate_plot(rows=2, cols=1, n_plot=1500, 
                  labels=('aInputTorque','aSensorAngle'),                   
                  ylabels=('Input [T]','Sensor [rad]'), 
                  ylimits=((-20,30),(-0.01, 0.31)),
                  outputs=('aSensorAngle',)):
    
    """
    This prepares the figure and the axes to be updated by the animate function.
    If a parameter is a tuple an it consistsof only 1 element,
    write:       ('element',)
    to make sure it is seen as a tuple, because ('element') may be seen as a string.
    
    """
    
    fig, axs = plt.subplots(nrows=rows, ncols=cols, layout='constrained')
    
    plot_arrays = np.full((len(labels)+1,n_plot), np.nan)
    calculated_arrays = np.full((len(outputs)+1,n_plot), np.nan)
    
    
    i = 0
    lines = []
    lines_calculated = []
    for ax in axs:
        line, = ax.plot([], [], label=labels[i])
        lines.append(line)

        if labels[i] in outputs:
            print()
            line_calc, = ax.plot([],[], label='Model output')
            lines_calculated.append(line_calc)


        ax.set_ylabel(ylabels[i])
        ax.set_ylim(ylimits[i])
        ax.set_xlabel('Time [s]')
        ax.set_xlim((0,n_plot/100))
        #ax.set_xticklabels([])

        ax.legend()

        ax.grid(animated=True)

        i += 1
    return fig, axs, lines, lines_calculated, plot_arrays, calculated_arrays

def animate(iter, lock, plot_arrays, lines, calculated_arrays, lines_calculated, axs, fig, queue_data, queue_calculated, use_csv=False, n_plot=1500 ,
            keys=('aInputTorque','aSensorAngle')):
        
    # update data from data base
        # if use_csv:
        #     start = time.perf_counter()
        #     headers = read_csvHeader('databuffer.csv', lock)
        #     data =  read_csvData('databuffer.csv', lock)
        #     plotstep_dict = create_dict_HeadersAndData(headers, data)
        #     stop = time.perf_counter()
        #     print(stop-start)
                
        # else:

    while not queue_data.empty():
        plotstep_dict = queue_data.get()

        # set data on line object

        if plot_arrays[0,-1] != plotstep_dict['aTime'][-1] or np.isnan(plot_arrays[0,-1]):
            
            plot_arrays[0,:] = np.concatenate((plot_arrays[0,:],plotstep_dict['aTime']))[-n_plot:]

            for i in range(len(keys)):
                plot_arrays[i+1,:] = np.concatenate((plot_arrays[i+1,:],plotstep_dict[keys[i]]))[-n_plot:]
                
                lines[i].set_data(plot_arrays[0,:], plot_arrays[i+1,:])

    while not queue_calculated.empty():

        calculated_step = queue_calculated.get()
        

        if calculated_arrays[0,-1] != calculated_step[0][-1] or np.isnan(calculated_arrays[0,-1]):
            

            calculated_arrays[0,:] = np.concatenate((calculated_arrays[0,:], calculated_step[0]))[-n_plot:]
        
            for i in range(len(lines_calculated)):
                calculated_arrays[i+1,:] = np.concatenate((calculated_arrays[i+1,:], calculated_step[i+1]))[-n_plot:]
                
                lines_calculated[i].set_data(calculated_arrays[0,:], calculated_arrays[i+1,:])

    #lines[i].set_data(dict_data['aDataCounter'][-50:iter], dict_data[keys[i]][-50:iter])
        

    # rescale axes
    rescale = False
    

    for ax, y in zip(axs, plot_arrays[1:,:]):
         

        max_y = np.nanmax(y[-round(n_plot*4/4):]) 
        min_y = np.nanmin(y[-round(n_plot*4/4):])
        range_y = max_y - min_y

        ax_min = ax.get_ylim()[0]
        ax_max = ax.get_ylim()[1]
        range_ax = ax_max - ax_min

         

        if max_y > ax_max - 0.05*range_ax:
              ax_max = max_y + 0.4*range_y
              #ax_min = min_y - 0.05*range_y
              ax.set_ylim(ax_min, ax_max)
              rescale = True

        if min_y < ax_min + 0.05*range_ax:
             ax_min = min_y - 0.4*range_y
             #ax_max = max_y + 0.05*range_y
             ax.set_ylim(ax_min, ax_max)
             rescale = True

        if min_y > ax_min + 0.1*range_ax:
            ax_min = min_y - 0.05*range_y
            #ax_max = max_y + 0.05*range_y
            ax.set_ylim(ax_min, ax_max)
            rescale = True

        if max_y < ax_max - 0.1*range_ax:
            ax_max = max_y + 0.05*range_y
            #ax_min = min_y - 0.05*range_y
            ax.set_ylim(ax_min, ax_max)
            rescale = True

        last_step = plot_arrays[0,-1]
        if  last_step > ax.get_xlim()[1] - 1:
             ax.set_xlim(last_step-round(n_plot/100*2/3), last_step+round(n_plot/100*1/3))
             #rescale = True

    if rescale:
        fig.canvas.draw()
        fig.canvas.flush_events()
            
        
        
    

        
        
    return lines_calculated
        
def plot_figure(fig, axs, lock, plot_arrays, lines, int, queue, use_csv=True):
    print(1)
    animation.FuncAnimation(fig=fig, func=animate, fargs=(lock,plot_arrays,lines, axs, queue, use_csv), blit=True, interval=int, repeat=False)
    print(2)
    


     



if __name__ == "__main__":
    fig,axs,lines, lines_calc, plot_arrays, calc_array=initiate_plot()
    from multithreading_module import make_lock
    lock = make_lock()

    fig,axs,lines,lines_calculated,plot_arrays,calculated_arrays = initiate_plot()
    #animation = plot_figure(fig, axs, lock, plot_arrays, lines, 100)
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
            

