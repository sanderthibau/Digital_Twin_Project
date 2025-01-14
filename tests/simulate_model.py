import control as ct
from control.matlab import ss
import numpy as np
import matplotlib.pyplot as plt
import math
import time

K = 1*10**6
m = 5
J = 0.05
R = 0.0098
bs = 50

fric_BOOL = 1
fric_x = 0.1 * fric_BOOL
fric_T = 0.01 * fric_BOOL


A = np.array([[0,0,1,0], [0,0,0,1], [-K/m, K*R/m, -fric_x/m, 0], [K*R/J, -K*R*R/J, 0, -fric_T/J]])

B = np.array([[0],[0],[0],[1/J]])

C = np.array([0,1,0,0])

D = np.array([0])

sysCR = ss(A,B,C,D)

N = 2
period = 0.01
timesteps = np.linspace(0,period,N)



inputs = 0 * np.ones(N)

def sys_response(ssys, timesteps_input, u_input, initial_state=[[0],[0],[0],[0]]):

    time, yout, xout = ct.forced_response(ssys, timesteps_input, u_input, initial_state, return_x=True)
    return time, yout, xout

t, y, x = sys_response(sysCR, timesteps, inputs)

#print(t)
#print(y)
#print(x)
#print(x[0,-1])


if __name__ == "__main__":
    start_time = time.time()
    initial = [[0],[0],[0],[0]]
    #reference_pos = 0.1
    iter = 0
    gain_P = 710
    gain_D = 110
    max_input = 30

    noise_sigma = 0.001
    noise_mean = 0

    pos_x = np.array(initial[0])
    amount_iterations = 1000
    buffer_size = 100

    D_BOOL = 1


    while iter < amount_iterations:
        iter += 1

        reference_pos =  0.1 * math.ceil(10*iter/amount_iterations)
        
        t, y, x = sys_response(sysCR, timesteps[-N:], inputs[-N:], initial)


        noise_pos = np.random.normal(noise_mean,noise_sigma, N-1)

        pos_iter = np.add(x[0,1:], noise_pos)


        pos_x = np.concatenate((pos_x,pos_iter))
        error = pos_iter[-1] - reference_pos

        next_input = -gain_P * error

        inputs_next = next_input * np.ones(N)

        if D_BOOL:
            velocity_end_iter = x[2,-1]
            
            inputs_next = np.add(inputs_next, -gain_D*velocity_end_iter)
        
        timesteps_next = np.add(timesteps[-(N-1):], period)
        
        if iter < amount_iterations:
            
            timesteps = np.concatenate((timesteps, timesteps_next))

            inputs_next = np.sign(inputs_next[0]) * min(abs(inputs_next[0]), max_input) * np.ones_like(inputs_next)

            inputs = np.concatenate((inputs[:-1], inputs_next))

        initial = x[:,-1]

    stairs_down = 1

    if stairs_down:
        # last_input = inputs[-1]
        # last_pos_x = pos_x[-1]
        # last_timestep = timesteps[-1]

        # inputs = np.concatenate((inputs, np.add(-inputs, last_input)))
        # pos_x = np.concatenate((pos_x, np.add(-pos_x, last_pos_x)))
        # timesteps = np.concatenate((timesteps, np.add(timesteps, last_timestep)))
        iter = 0
        while iter < amount_iterations:
            iter += 1

            reference_pos =  1 - 0.1 * math.ceil(10*iter/amount_iterations)
            
            t, y, x = sys_response(sysCR, timesteps[-N:], inputs[-N:], initial)


            noise_pos = np.random.normal(noise_mean,noise_sigma, N-1)

            pos_iter = np.add(x[0,1:], noise_pos)


            pos_x = np.concatenate((pos_x,pos_iter))
            error = pos_iter[-1] - reference_pos

            next_input = -gain_P * error

            inputs_next = next_input * np.ones(N)

            if D_BOOL:
                velocity_end_iter = x[2,-1]
                
                inputs_next = np.add(inputs_next, -gain_D*velocity_end_iter)
            
            timesteps_next = np.add(timesteps[-(N-1):], period)

            timesteps = np.concatenate((timesteps, timesteps_next))
            inputs_next = np.sign(inputs_next[0]) * min(abs(inputs_next[0]), max_input) * np.ones_like(inputs_next)

            inputs = np.concatenate((inputs[:-1], inputs_next))
            if iter < amount_iterations:
                pass
                
                

                

            initial = x[:,-1]

    
        amount_iterations *= 2





    print(f"Iteration took {time.time() - start_time} seconds")
    total = 1 + (N-1)*amount_iterations
    simtime = amount_iterations*period
    print(f"Total amount of timesteps = {total}, N = {N-1} (steps per iteration), Iterations = {amount_iterations}, Period [s]= {period}, Simulated time [s] = {simtime}")



    


    send_to_TC = 1
    
    if send_to_TC:

        """
        In TwinCat:

        PROGRAM MAIN
        VAR	

        fInputArray : ARRAY [1..total_steps] OF REAL;
        fSensorArray : ARRAY [1..total_steps] OF REAL;

        END_VAR
        """
        start_time = time.time()
        import pyads
        AMSNETID = "192.168.0.3.1.1" #local netid

        plc = pyads.Connection(AMSNETID, pyads.PORT_TC3PLC1)
        plc.open()
        print(f"Connected?: {plc.is_open}") #debugging statement, optional
        print(f"Local Address? : {plc.get_local_address()}") #debugging statement, optional


        #write var
        plc.write_by_name('MAIN.fInputArray', inputs, pyads.PLCTYPE_REAL * total)
        plc.write_by_name('MAIN.fSensorArray', pos_x, pyads.PLCTYPE_REAL * total)
        
        
        #bool to let twincat wait on data
        plc.write_by_name('MAIN.data_received', True, pyads.PLCTYPE_BOOL)
        


        
        """
        #read to test
        sensor_array = plc.read_by_name('MAIN.fSensorArray', pyads.PLCTYPE_REAL * total)
        print(sensor_array)
        """

        plc.close()
        print(f"Sending data took {time.time() - start_time} seconds")

        




    


    
    
show_figures = 0
block_figure = True
if show_figures:

    plt.figure(1)
    plt.plot(timesteps,100* pos_x, label='position x [0.01 * m]')
    plt.plot(timesteps, inputs, label='input T [Nm]')
    plt.xlabel('time [s]')
    plt.legend()
    plt.show(block=block_figure)   


    