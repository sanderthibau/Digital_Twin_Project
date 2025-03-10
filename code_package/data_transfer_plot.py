import matplotlib.pyplot as plt
import numpy as np

from matplotlib import rcParams
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = 'cmr10'
plt.rcParams['mathtext.fontset'] = 'cm'
rcParams['axes.unicode_minus'] = False
rcParams['axes.formatter.use_mathtext'] = True


parameters = np.load('parameters.npz')
DataSizes = parameters['DataSizes']

types = ['multiprocessing', 'multithreading', 'manager_queue']



indicator = 0
type = types[indicator]

struc = 1
if struc:
    type = type+'_struct'

load = 1
if load:
    type = 'L_'+ type
print(type)

transfer_times = np.load('transfer_times'+f'_{type}'+'.npz')
read_time = transfer_times['TimeRead']
put_time = transfer_times['TimePut']*10**-9
get_time = np.load('get_times'+f'_{type}'+'.npy')*10**-9

#print(transfer_time)
plt.figure(1)
plt.plot(DataSizes, read_time[:, 0], label='Average transfer time', color='royalblue')
plt.fill_between(DataSizes, read_time[:,3], read_time[:,4], label='90 percent confidence interval',alpha=0.2, color='royalblue')
plt.scatter(DataSizes, read_time[:, 1], label='Minimal and maximal transfer time', color='grey', marker='+', s=15)
plt.scatter(DataSizes, read_time[:, 2], color='grey', marker='+', s=15)


plt.title('Time to read an array from TwinCat with pyads in function of array size\n(every array size tested 100 times)')
plt.ylabel('Data transfer time [sec]')
plt.xlabel('Number of array elements')
plt.legend()



plt.figure(2)
plt.plot(DataSizes, put_time[:, 0], label='Average time to put array in queue', color='royalblue')
plt.fill_between(DataSizes, put_time[:,3], put_time[:,4], label='90 percent confidence interval',alpha=0.2, color='royalblue')
plt.scatter(DataSizes, put_time[:, 1], label='Minimal and maximal time to put in queue', color='grey', marker='+', s=15)
plt.scatter(DataSizes, put_time[:, 2], color='grey', marker='+', s=15)


plt.title('Time to put an array in a queue in function of array size\n(every array size tested 100 times)')
plt.ylabel('Time to put array in queue [sec]')
plt.xlabel('Number of array elements')
plt.legend()

plt.figure(3)
plt.plot(DataSizes, get_time[:, 0], label='Average time to get array from queue', color='royalblue')
plt.fill_between(DataSizes, get_time[:,3], get_time[:,4], label='90 percent confidence interval',alpha=0.2, color='royalblue')
plt.scatter(DataSizes, get_time[:, 1], label='Minimal and maximal time to get from queue', color='grey', marker='+', s=15)
plt.scatter(DataSizes, get_time[:, 2], color='grey', marker='+', s=15)


plt.title('Time to get an array from a queue in function of array size\n(every array size tested 100 times)')
plt.ylabel('Time to get array from queue [sec]')
plt.xlabel('Number of array elements')
plt.legend()


plt.show()