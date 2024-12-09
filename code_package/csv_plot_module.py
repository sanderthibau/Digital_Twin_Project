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


def read_csvHeader(csvFile):
    with open(csvFile, 'r') as file:
          reader = csv.reader(file)
          for row in reader:
               headers = row
               break
    return headers

def read_csvData(csvFile, header=True):
    with open(csvFile, 'r') as file:
            reader = csv.reader(file)
            if header:
                next(reader, None)
            buffer_array = np.empty((0,4)) 
            for line in reader:
                floats = [float(e) for e in line]
                buffer_array = np.append(buffer_array, np.array([floats]), axis=0)
    return buffer_array

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
         ax.set_xlim((0,10))
         ax.set_xticklabels([])

         ax.legend()

         i += 1
    return fig, axs, lines, plot_arrays






if __name__ == "__main__":

    fig,a,lines, plot_arrays=initiate_plot()

    dict_data = None

    def animate(iter, dict_data, n_plot=500, n_step=10 , keys=('aInputTorque','aSensorAngle')):
        iter += 1
        print(iter)
        # update data from data base
        if iter == 1:
            headers = read_csvHeader('databuffer.csv')
            data =  read_csvData('databuffer.csv')
            dict_data = create_dict_HeadersAndData(headers, data)
            
            
            
            

        buffer_length = dict_data['aTime'].shape[0]
        step_amount = np.around(buffer_length/n_step)
        plotstep_dict = {}

        if iter == step_amount:

            for key in keys:
                plotstep_dict[key] = dict_data[key][(iter-1)*n_step:]
                plotstep_dict['aTime'] = dict_data['aTime'][(iter-1)*n_step:]
            iter = 0

        else:
            for key in keys:
                plotstep_dict[key] = dict_data[key][(iter-1)*n_step:iter*n_step]
                plotstep_dict['aTime'] = dict_data['aTime'][(iter-1)*n_step:iter*n_step]
            

        # set data on line object
        plot_arrays[0,:] = np.concatenate((plot_arrays[0,:],plotstep_dict['aTime']))[-n_plot:]
        print(plotstep_dict['aTime'])
        for i in range(len(lines)):
             lines[i].set_data(plot_arrays[0,:], plot_arrays[i,:])



            #lines[i].set_data(dict_data['aDataCounter'][-50:iter], dict_data[keys[i]][-50:iter])
        """

        # rescale axes
        rescale = False

        for ax, y, t in zip(axs, ydata, tdata):
             if y < ax.get_ylimit()[0]:
                  ax.set_limits(y, ax.get_limit()[1])
            

        """
        
        return lines



    ani = animation.FuncAnimation(fig=fig, func=animate, fargs=(dict_data,), blit=True, interval=1000, repeat=False)
    plt.show()


    
    
    
    
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


