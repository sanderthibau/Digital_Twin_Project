import numpy as np
import matplotlib.pyplot as plt

from labellines import labelLines
from matplotlib.lines import Line2D
import matplotlib.gridspec as gridspec

from matplotlib import rcParams
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = 'cmr10'
plt.rcParams['mathtext.fontset'] = 'cm'
rcParams['axes.unicode_minus'] = False
rcParams['axes.formatter.use_mathtext'] = True

multi_array = np.load('multi_array.npy')
ranges = np.load('ranges.npz')

def two_dimension_slicer(i,j, array, heavy_duty=1):
    """
    Selects all values of dimenson i and j,
    while fixing the other dimensions at their element 0 or -1 (heavy_duty)
    
    """
    constant_index = 0
    if heavy_duty:
        constant_index = -1
    index_list = []
    for n in range(array.ndim):
        
        if n == i or n== j:
            index_list.append(slice(None))
        else:
            index_list.append(constant_index)
    return array[tuple(index_list)]




n_inputs_range = list(ranges['inputs'])
n_outputs_range = list(ranges['outputs'])
n_states_range = list(ranges['states'])


timestep_range = list(ranges['steps'])
duration_range = list(ranges['dur'])

ranges_title = ['Input dimension', 'Output dimension', 'State dimension', 'Length of timestep', 'Simulated time']
ranges_list = [ranges[key] for key in ranges]
ranges_unity = ['n', 'n', 'n', 'sec', 'sec']


print(f'inputs = {n_inputs_range}')
print(f'outputs = {n_outputs_range}')
print(f'states = {n_states_range}')
print(f'timesteps = {timestep_range}')
print(f'duration = {duration_range}')



i_r = len(n_inputs_range)
o_r = len(n_outputs_range)
s_r = len(n_states_range)

t_r = len(timestep_range)
d_r = len(duration_range)


plot_duration = 1
plot_percentage = 1
plot_states = 1
contours = 1

## PLOTS CALCULATION TIME as function of SIMULATED TIME (duration)
if plot_duration:
        
    fig1 = plt.figure(figsize=(8,6))

    for a in range(i_r):
        
        time_for_calc = multi_array[a, -1, -1, -1, :]
        plt.plot(duration_range, time_for_calc, 'g*--', linewidth=0.7, ms=4, 
                    label=f'{n_inputs_range[a]}')
        
    for b in range(o_r):
        
        time_for_calc = multi_array[-1, b, -1, -1, :]
        plt.plot(duration_range, time_for_calc, 'kx--', linewidth=0.7, ms=4, 
                    label=f'{n_outputs_range[b]}')
    
    for c in range(s_r):
        
        time_for_calc = multi_array[-1, -1, c, -1, :]
        plt.plot(duration_range, time_for_calc, 'b.--', linewidth=0.7, ms=4, 
                    label=f'{n_states_range[c]}')
        
    for d in range(t_r):
        
        time_for_calc = multi_array[-1, -1, -1, d, :]
        #print(f'time step difference: {time_for_calc}')
        plt.plot(duration_range, time_for_calc, 'r+--', linewidth=0.7, ms=4, 
                    label=f'{timestep_range[d]}')



    lines = plt.gca().get_lines()
    labelLines(lines, zorder=2.5)
    plt.title('Calculation time with varying parameters while others held constant')
    plt.xlabel('Simulated time [sec]')
    plt.ylabel('Calculated time [sec]')

    colors = ('g','k','b','r')
    markers = ('*','x','.','+')
    lines = [Line2D([0], [0], marker=m, color=c, linewidth=0.7, linestyle='--') for c,m in zip(colors,markers)]
    labels = [f'Input dimension = {n_inputs_range}', f'Output dimension = {n_outputs_range}', f'State dimension = {n_states_range}', f'Lenght of timestep = {timestep_range}']
    plt.grid()
    ax = plt.gca()
    ax.set_facecolor('white')
    fig1.patch.set_facecolor('white')
    plt.legend(lines, labels, title='Parameters held constant at: (I, O, S, L) = (120, 120, 120, 0.00025)')
    plt.savefig('calctimegraph_duration')
    
## PLOTS calculation time as function STATES ##
if plot_states:
    fig2 = plt.figure(figsize=(8,6))

    for a in range(i_r):
        
        time_for_calc = multi_array[a, -1, :, -1, -1]
        plt.plot(n_states_range, time_for_calc, 'g*--', linewidth=0.7, ms=4, 
                    label=f'{n_inputs_range[a]}')
        
    for b in range(o_r):
        
        time_for_calc = multi_array[-1, b, :, -1, -1]
        plt.plot(n_states_range, time_for_calc, 'kx--', linewidth=0.7, ms=4, 
                    label=f'{n_outputs_range[b]}')
    
    for d in range(t_r):
        
        time_for_calc = multi_array[-1, -1, :, d, -1]
        plt.plot(n_states_range, time_for_calc, 'b.--', linewidth=0.7, ms=4, 
                    label=f'{timestep_range[d]}')
        
    for e in range(d_r):
        
        time_for_calc = multi_array[-1, -1, :, -1, e]
        #print(f'time step difference: {time_for_calc}')
        plt.plot(n_states_range, time_for_calc, 'r+--', linewidth=0.7, ms=4, 
                    label=f'{duration_range[e]}')



    lines = plt.gca().get_lines()
    labelLines(lines, zorder=2.5)
    plt.title('Calculation time with varying parameters while others held constant')
    plt.xlabel('State dimension')
    plt.ylabel('Calculated time [sec]')

    colors = ('g','k','b','r')
    markers = ('*','x','.','+')
    lines = [Line2D([0], [0], marker=m, color=c, linewidth=0.7, linestyle='--') for c,m in zip(colors,markers)]
    labels = [f'Input dimension = {n_inputs_range}', f'Output dimension = {n_outputs_range}', f'Lenght of timestep = {timestep_range}', f'Duration simulated = {duration_range}']
    plt.grid()
    ax = plt.gca()
    ax.set_facecolor('white')
    fig2.patch.set_facecolor('white')
    plt.legend(lines, labels, title='Parameters held constant at: (I, O, L, D) = (120, 120, 0.00025 s, 2 s)')
    plt.savefig('calctimegraph_states')
    
## PLOTS INFLUENCE OF PARAMETERS ON CALCULATION TIME AGAINST EACH OTHER ##

if contours:
    n = len(ranges)
    h_d = 1
    # fig = plt.figure(tight_layout=True, figsize=(9,7))
    # fig = plt.figure(figsize=(9,7))
    # spec = gridspec.GridSpec(n, n, hspace=0.07, wspace=0.07, figure=fig)
    
    
    fig = plt.figure(figsize=(12,8))
    spec = gridspec.GridSpec(n, n, hspace=0.06, wspace=0.06, figure=fig)

    for i in range(n):
        for j in range(n):

            ax = fig.add_subplot(spec[i,j])
            ax.tick_params('x', rotation=35)
            ax.margins(0.1, 0.1)
            

            if i == j: # diagonal
                print(ranges_title[i])
                if i == 0:
                    ax.set_yticks(ranges_list[i])
                if i == n - 1:
                    ax.scatter([],[], marker='o', s=multi_array[1,1,1,1,1]*30, c='k', label=f'{round(multi_array[1,1,1,1,1],2)} sec')
                    ax.scatter([],[], marker='o', s=multi_array[-1,-1,-1,-1,-1]*30, c='k', label=f'{round(multi_array[-1,-1,-1,-1,-1],2)} sec') 

                    ax.set_xticks(ranges_list[i])

                ax.text(sum(ax.get_xlim())/2, sum(ax.get_ylim())/2, ranges_title[i]+'\n'+f'[{ranges_unity[i]}]', verticalalignment='center', horizontalalignment='center', fontsize=10, fontweight='bold')

                if i < n - 1:
                    ax.set_xticks([])
                if j > 0:
                    ax.set_yticks([])
            else:

                x = ranges_list[j]
                y = ranges_list[i]
                xx, yy = np.meshgrid(x,y)


                
                if i < j:
                    zz = two_dimension_slicer(i, j, multi_array, h_d)
                else:
                    zz = two_dimension_slicer(i, j, multi_array, h_d).T

                ax.scatter(xx, yy, marker='o', c='k', s=zz*30)
                ax.set_xticks(ranges_list[j])
                ax.set_yticks(ranges_list[i])
                


                if j > 0:
                    ax.set_yticks([])
                if i < n - 1:
                    ax.set_xticks([])

                #ax.grid()
    
        
    fig.legend(bbox_to_anchor=(0.30,1), title='Simulated time proportional \nto marker size:')
    fig.suptitle("Scatterplot Matrix", fontsize=17)
                 


## PLOTS calculation time/simulated time ##
if plot_percentage:
        
    fig = plt.figure(figsize=(8,6))

    for i in range(d_r):
        multi_array[:,:,:,:,i] = multi_array[:,:,:,:,i]/duration_range[i]*100

    for a in range(i_r):
        
        time_for_calc = multi_array[a, -1, -1, -1, :]
        plt.plot(duration_range, time_for_calc, 'g*--', linewidth=0.7, ms=4, 
                    label=f'{n_inputs_range[a]}')
        
    for b in range(o_r):
        
        time_for_calc = multi_array[-1, b, -1, -1, :]
        plt.plot(duration_range, time_for_calc, 'kx--', linewidth=0.7, ms=4, 
                    label=f'{n_outputs_range[b]}')
    
    for c in range(s_r):
        
        time_for_calc = multi_array[-1, -1, c, -1, :]
        plt.plot(duration_range, time_for_calc, 'b.--', linewidth=0.7, ms=4, 
                    label=f'{n_states_range[c]}')
        
    for d in range(t_r):
        
        time_for_calc = multi_array[-1, -1, -1, d, :]
        #print(f'time step difference: {time_for_calc}')
        plt.plot(duration_range, time_for_calc, 'r+--', linewidth=0.7, ms=4, 
                    label=f'{timestep_range[d]}')



    lines = plt.gca().get_lines()
    labelLines(lines, zorder=2.5)
    plt.title('Calculation percentage with varying parameters while others held constant')
    plt.xlabel('Simulated time [sec]')
    plt.ylabel('Calculated time/simulated time [%]')

    colors = ('g','k','b','r')
    markers = ('*','x','.','+')
    lines = [Line2D([0], [0], marker=m, color=c, linewidth=0.7, linestyle='--') for c,m in zip(colors,markers)]
    labels = [f'Input dimension = {n_inputs_range}', f'Output dimension = {n_outputs_range}', f'State dimension = {n_states_range}', f'Lenght of timestep = {timestep_range}']
    plt.grid()
    ax = plt.gca()
    ax.set_facecolor('white')
    fig.patch.set_facecolor('white')
    plt.legend(lines, labels, title='Parameters held constant at: (I, O, S, L) = (120, 120, 120, 0.00025)')
    plt.savefig('calctimegraph_percentage')

plt.show()

    # plt.figure()

    # states = n_states_range
    # timesteps = timestep_range

    # time_calculated = multi_array[0,0,:,:,2].T
    # #print(time_calculated)
    # contour = plt.contourf(states, timesteps, time_calculated, levels=10)

    # cbar = plt.colorbar(contour, label='calculated time')
    # plt.xlabel('amount of states')
    # plt.ylabel('length of timestep')
    # plt.title('Contour plot with inputs (2), outputs (2) and simulated time (0.32s) constant')

    # plt.figure()
    # states = n_states_range
    # inputs = n_inputs_range

    # time_calculated = multi_array[:,0,:,1,2].T
    # #print(time_calculated)
    # contour = plt.contourf(states, inputs, time_calculated, levels=10)

    # cbar = plt.colorbar(contour, label='calculated time')
    # plt.xlabel('number of states')
    # plt.ylabel('number of inputs')
    # plt.title('Contour plot with outputs (2), step length (0.025s) and simulated time (0.32s) constant')

    # plt.figure()
    # timesteps = timestep_range
    # sim_duration = duration_range

    # time_calculated = multi_array[0,0,1,:,:].T
    
    # #print(time_calculated)
    # contour = plt.contourf(timesteps, sim_duration, time_calculated, levels=10)

    # cbar = plt.colorbar(contour, label='calculated time')
    # plt.xlabel('length of timestep')
    # plt.ylabel('simulated time')
    # plt.title('Contour plot with inputs (2), outputs (2) and states (8) constant')
