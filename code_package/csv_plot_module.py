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



def initiate_plot(rows=1, cols=2, labels=('input torque', 'sensor angle'), ylabels=('Input [T]','Sensor [rad]'), ylimits=([-20,20],[-0.2, 0.5])):
    fig, axs = plt.subplots(nrows=rows, ncols=cols, layout='constrained')
    i = 0
    lines = []
    for ax in axs:
         ax.set_ylabel(ylabels[i])
         ax.set_ylim(ylimits[i])

         line, = ax.plot([], [], label=labels[i])
         lines.append(line)

         ax.set_xlabel('Time [s]')
         ax.set_xlim([0,10])
         ax.set_xticklabels([])

         ax.legend()

         i += 1
    return fig, axs, lines









if __name__ == "__main__":

    # def data_gen():
    #     t = data_gen.t
    #     cnt = 0
    #     while cnt < 1000:
    #         cnt+=1
    #         t += 0.05
    #         y1 = np.sin(2*np.pi*t) * np.exp(-t/10.)
    #         y2 = np.cos(2*np.pi*t) * np.exp(-t/10.)
    #         # adapted the data generator to yield both sin and cos
    #         yield t, y1, y2

    # data_gen.t = 0

    # # create a figure with two subplots
    # fig, (ax1, ax2) = plt.subplots(2,1)

    # # intialize two line objects (one in each axes)
    # line1, = ax1.plot([], [], lw=2)
    # line2, = ax2.plot([], [], lw=2, color='r')
    # line = [line1, line2]

    # # the same axes initalizations as before (just now we do it for both of them)
    # for ax in [ax1, ax2]:
    #     ax.set_ylim(-1.1, 1.1)
    #     ax.set_xlim(0, 5)
    #     ax.grid()

    # # initialize the data arrays 
    # xdata, y1data, y2data = [], [], []
    # def run(data):
    #     # update the data
    #     t, y1, y2 = data
    #     xdata.append(t)
    #     y1data.append(y1)
    #     y2data.append(y2)

    #     # axis limits checking. Same as before, just for both axes
    #     for ax in [ax1, ax2]:
    #         xmin, xmax = ax.get_xlim()
    #         if t >= xmax:
    #             ax.set_xlim(xmin, 2*xmax)
    #             ax.figure.canvas.draw()

    #     # update the data of both line objects
    #     line[0].set_data(xdata, y1data)
    #     line[1].set_data(xdata, y2data)

    #     return line

    # ani = animation.FuncAnimation(fig, run, blit=True, interval=10, repeat=False)
    # plt.show()
    
    rows=1
    cols=2
    labels=('input torque', 'sensor angle')
    ylabels=('Input [T]','Sensor [rad]')
    ylimits=((-20,20),(-0.01, 0.31))

    fig, axs = plt.subplots(nrows=rows, ncols=cols, layout='constrained')
    i = 0
    lines = []
    for ax in axs:
         ax.set_ylabel(ylabels[i])
         ax.set_ylim(ylimits[i])

         line, = ax.plot([], [], label=labels[i])
         lines.append(line)

         ax.set_xlabel('Time [s]')
         ax.set_xlim(0,300)
         ax.set_xticklabels([])

         ax.legend()

         i += 1


    def animate(iter, keys=('aInputTorque','aSensorAngle')):
     
        headers = read_csvHeader('databuffer.csv')
        data =  read_csvData('databuffer.csv')

        dict_data = create_dict_HeadersAndData(headers, data)


        for i in range(len(lines)):
            lines[i].set_data(dict_data['aDataCounter'][-50:iter], dict_data[keys[i]][-50:iter])
            

        

        return lines



    ani = animation.FuncAnimation(fig=fig, func=animate, blit=True, interval=1)
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


