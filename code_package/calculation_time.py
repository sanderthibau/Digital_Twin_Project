
import control as ct
from control.matlab import ss
import numpy as np
import time
from collections import OrderedDict
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

# import matplotlib.font_manager as font_manager
# font_manager._rebuild()

# from matplotlib import rc
# rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
# #rc('text', usetex=True)

def create_random_matrix(rows, columns):
    M = 0.5*np.ones((rows,columns)) - np.random.rand(rows,columns)
    return M

contour_example = 0
if contour_example:
    fig = plt.figure(tight_layout=True)
    spec = gridspec.GridSpec(ncols=2, nrows=2, figure=fig)
    ax1 = fig.add_subplot(spec[0, 0])
    ax2 = fig.add_subplot(spec[0, 1])
    ax3 = fig.add_subplot(spec[1, 0])
    ax4 = fig.add_subplot(spec[1:2, 1:2])
    ax1.set_facecolor('white')
    fig.set_facecolor('white')
    x = np.arange(11)
    y =np.arange(11)
    xx, yy = np.meshgrid(x,y)
    z1 = xx*yy
    contour = ax1.contourf(x, y, z1, levels=10, cmap='turbo')
    scatter0 = ax1.scatter(xx, yy, s=10, marker=".", c='k')

    cbar = plt.colorbar(contour, label='z', ax=ax1)
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_title('Contour plot with $z = x * y$')
    ax1.set_aspect('equal')

    

    
    
    z2 = xx*yy**2


    #contour = plt.contourf(x, y, z, levels=10)
    im = ax2.pcolor(x, y, z2)
    cbar = plt.colorbar(im, label='z', ax=ax2)
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    ax2.set_title('Contour plot with $z = x * y^2$')
    ax2.set_aspect('equal')


    z3 = xx**2*yy
    scatter1 = ax3.scatter(xx, yy, s = 30, c=z3, cmap='turbo')

    cbar = plt.colorbar(scatter1, label='z', ax=ax3)
    ax3.set_xlabel('x')
    ax3.set_ylabel('y')
    ax3.set_title('Contour plot with $z = x^2 * y$')
    ax3.set_aspect('equal')
   
    scatter2 = ax4.scatter(xx, yy, s=z3/3, marker='.', c='k', cmap='turbo')
    
    ax4.set_xlabel('x')
    ax4.set_ylabel('y')
    ax4.set_title('Contour plot with $z = x^2 * y$')

    ax4.scatter([],[], marker='.', s=z3[1,1]/3, c='k', label=f'{z3[1,1]} s')
    ax4.scatter([],[], marker='.', s=z3[10,10]/3, c='k', label=f'{z3[10,10]} s')
    ax4.legend(loc='upper left', bbox_to_anchor=(1.05,1.05), title='z proportional \nto marker size')

    ax4.set_aspect('equal')
    ax4.grid()

    plt.show()

discrete_bool = False
#discrete_bool = True

"""
ranges for extra = -3:
n_inputs_range = [1, 4, 16, 64]
n_outputs_range = [1, 4, 16, 64]
n_states_range = [2, 8, 32, 128]

time to create matrices = 5 seconds
"""


n_inputs_range = [4] + [40,60, 80] + [120] #[40*i for i in range(1, 4)]

n_outputs_range = [4] + [40,80,120] #[40*i for i in range(1, 4)]

n_states_range = [4] + [40,60, 80] + [100, 120] #[40*i for i in range(1, 4)]      # [2*4**i for i in range(7+extra)]



timestep_range = [0.004,0.0025, 0.001, 0.00025] #[10**-i for i in range(2+limit, 4+limit)]

duration_range = [0.02] + [0.4,0.8,1.2,1.6,2]#[i/10 for i in range(1,6)] #+ [0.5] + [2] + [5] + [10] #*i for i in range(1,6)]

np.savez('ranges',  inputs=np.array(n_inputs_range), outputs=np.array(n_outputs_range), states=np.array(n_states_range),
                    steps=np.array(timestep_range), dur=np.array(duration_range))

#ranges = np.asanyarray(ranges)
#np.save('ranges', ranges)


print(f'inputs = {n_inputs_range}')
print(f'outputs = {n_outputs_range}')
print(f'states = {n_states_range}')
print(f'timesteps = {timestep_range}')
print(f'duration = {duration_range}')



"""
timestep_range = [0.01, 0.001, 0.0001]
duration_range = [0.02, 0.08, 0.32, 1.28, 5.12]
"""

i_r = len(n_inputs_range)
o_r = len(n_outputs_range)
s_r = len(n_states_range)

t_r = len(timestep_range)
d_r = len(duration_range)

multi_array = np.zeros((i_r, o_r, s_r, t_r, d_r))
"""
This array allows to store all time data with a dimension for every parameter
"""

do_test = not(contour_example)
if do_test:

    start0 = time.perf_counter()
    for a in range(i_r):
        print(a)
        n_inputs = n_inputs_range[a]

        for b in range(o_r):
            n_outputs = n_outputs_range[b]

            for c in range(s_r):
                n_states = n_states_range[c]

                A = create_random_matrix(n_states, n_states)
                B = create_random_matrix(n_states, n_inputs)

                C = create_random_matrix(n_outputs, n_states)
                D = create_random_matrix(n_outputs, n_inputs)

                state_space_model = ss(A, B, C, D, discrete_bool)
                

                for d in range(t_r):
                    timestep = timestep_range[d]

                    for e in range(d_r):
                        duration = duration_range[e]

                        number_steps = int(duration/timestep)
                        time_points = np.linspace(0,duration,number_steps)
                        #time_points = np.arange(0,duration,timestep)
                        u_inputs = create_random_matrix(n_inputs, number_steps)
                        initial_state = create_random_matrix(n_states, 1)

                        if (a,b,c,d,e) == (0,0,0,0,0):
                            
                            T, yout, xout = ct.forced_response(state_space_model, time_points, u_inputs, initial_state, return_x=True)

                        # the thing we want to time: #
                        start = time.perf_counter()
                        T, yout, xout = ct.forced_response(state_space_model, time_points, u_inputs, initial_state, return_x=True)
                        calc_time = time.perf_counter() - start

                        multi_array[a,b,c,d,e] = calc_time

    np.save('multi_array', multi_array)
    calc_time_tot = time.perf_counter() - start0

    print(f'total time = {calc_time_tot} sec')
    print(f'max calculation time = {np.max(multi_array)}')
    
    print(calc_time)


    # plotting = 0
    # contours = 0
    # if plotting:
        
    #     fig1 = plt.figure(1)

    #     for a in range(i_r):
            
    #         time_states = multi_array[a, 0, 0, 1, :]
    #         plt.plot(duration_range, time_states, 'g*--', linewidth=0.7, ms=4, 
    #                  label=f'{n_inputs_range[a]}')
            
    #     for b in range(o_r):
            
    #         time_states = multi_array[0, b, 0, 1, :]
    #         plt.plot(duration_range, time_states, 'kx--', linewidth=0.7, ms=4, 
    #                  label=f'{n_outputs_range[b]}')
        
    #     for c in range(s_r):
            
    #         time_states = multi_array[0, 0, c, 1, :]
    #         plt.plot(duration_range, time_states, 'b.--', linewidth=0.7, ms=4, 
    #                  label=f'{n_states_range[c]}')
            
    #     for d in range(t_r):
            
    #         time_states = multi_array[0, 0, 0, d, :]
    #         #print(f'time step difference: {time_states}')
    #         plt.plot(duration_range, time_states, 'r+--', linewidth=0.7, ms=4, 
    #                  label=f'{timestep_range[d]}')



    #     lines = plt.gca().get_lines()
    #     labelLines(lines, zorder=2.5)
    #     plt.title('Calculation time with varying parameters while others held constant')
    #     plt.xlabel('Simulated time [sec]')
    #     plt.ylabel('Calculated time [sec]')

    #     colors = ('g','k','b','r')
    #     markers = ('*','x','.','+')
    #     lines = [Line2D([0], [0], marker=m, color=c, linewidth=0.7, linestyle='--') for c,m in zip(colors,markers)]
    #     labels = [f'Input dimension = {n_inputs_range}', f'Output dimension = {n_outputs_range}', f'State dimension = {n_states_range}', f'Lenght of timestep = {timestep_range}']
    #     plt.grid()
    #     ax = plt.gca()
    #     ax.set_facecolor('white')
    #     fig1.patch.set_facecolor('white')
    #     plt.legend(lines, labels, title='Parameters held constant at: (I, O, S, L) = (4, 4, 4, 0.001)')
    #     plt.savefig('calctimegraph')

    #     if contours:
    #         plt.figure(2)
    #         states = n_states_range
    #         timesteps = timestep_range

    #         time_calculated = multi_array[0,0,:,:,2].T
    #         #print(time_calculated)
    #         contour = plt.contourf(states, timesteps, time_calculated, levels=10)

    #         cbar = plt.colorbar(contour, label='calculated time')
    #         plt.xlabel('amount of states')
    #         plt.ylabel('length of timestep')
    #         plt.title('Contour plot with inputs (2), outputs (2) and simulated time (0.32s) constant')

    #         plt.figure(3)
    #         states = n_states_range
    #         inputs = n_inputs_range

    #         time_calculated = multi_array[:,0,:,1,2].T
    #         #print(time_calculated)
    #         contour = plt.contourf(states, inputs, time_calculated, levels=10)

    #         cbar = plt.colorbar(contour, label='calculated time')
    #         plt.xlabel('number of states')
    #         plt.ylabel('number of inputs')
    #         plt.title('Contour plot with outputs (2), step length (0.025s) and simulated time (0.32s) constant')

    #         plt.figure(4)
    #         timesteps = timestep_range
    #         sim_duration = duration_range

    #         time_calculated = multi_array[0,0,1,:,:].T
            
    #         #print(time_calculated)
    #         contour = plt.contourf(timesteps, sim_duration, time_calculated, levels=10)

    #         cbar = plt.colorbar(contour, label='calculated time')
    #         plt.xlabel('length of timestep')
    #         plt.ylabel('simulated time')
    #         plt.title('Contour plot with inputs (2), outputs (2) and states (8) constant')

    #     plt.show()
















