
import control as ct
from control.matlab import ss
import numpy as np
import time
import matplotlib.pyplot as plt

def create_random_matrix(rows, columns):
    M = np.random.rand(rows,columns)
    return M

discrete_bool = False
#discrete_bool = True

"""
ranges for extra = -3:
n_inputs_range = [1, 4, 16, 64]
n_outputs_range = [1, 4, 16, 64]
n_states_range = [2, 8, 32, 128]

time to create matrices = 5 seconds
"""
extra = -3
n_inputs_range = [2*4**i for i in range(7+extra)]
n_outputs_range = [2*4**i  for i in range(7+extra)]
n_states_range = [4*4**i for i in range(7+extra)]

limit = 0
timestep_range = [10**-i for i in range(3+limit, 4+limit)]
duration_range = [0.02 * 8**i for i in range(0, 3+limit)]

print(f'inputs = {n_inputs_range}')
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


do_test = 1
if do_test:

    start0 = time.perf_counter()
    for a in range(i_r):
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
                        time_points = np.arange(0,duration,timestep)
                        u_inputs = create_random_matrix(n_inputs, number_steps)
                        initial_state = create_random_matrix(n_states, 1)

                        # the thing we want to time: #
                        start = time.perf_counter()
                        T, yout, xout = ct.forced_response(state_space_model, time_points, u_inputs, initial_state, return_x=True)
                        calc_time = time.perf_counter() - start

                        multi_array[a,b,c,d,e] = calc_time


    calc_time = time.perf_counter() - start0

    print(calc_time)


    plotting = 1
    if plotting:
        
        b, d, e = -1, -1, -1

        for a in range(i_r):
            
            time_states = multi_array[a, b, :, d, e]
            plt.plot(n_states_range, time_states, label=f'#inputs = {n_inputs_range[a]}')



        plt.title('Calculation time with increasing number of states and inputs')
        plt.xlabel('number of states')
        plt.legend()
        plt.show()
















