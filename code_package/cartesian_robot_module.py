"""
This ontains the functions related to the cartesian robot model
"""
import control as ct
from control.matlab import ss, bode
import numpy as np

K = 1*10**6
m = 5
J = 0.05
R = 0.0098
bs = 50
fric_x = 0.1
fric_T = 0.1


A = [[0,0,1,0], [-K/m, -(bs+fric_x)/m, K*R/m, bs*R/m], [0,0,0,1], [K*R/J,bs*R/J, -K*R*R/J,-(bs*R*R+fric_T)/J]]

B = [[0],[0],[0],[1/J]]

C = [1,0,0,0]

D = 0

sysCR = ss(A,B,C,D)



def forced_response(ssystem, timesteps_input, u_input, initial_state=[[0],[0],[0],[0]] ):
    """
    This function returns the output of a system (state space)
    given the inputs at certain timesteps and the initial condition
    """
    time, yout, xout = ct.forced_response(ssystem, timesteps_input, u_input, initial_state, return_x=True)

    return xout

def friction_feedforward(cart_velocity, coulomb=0.1, static=0.20, viscous=0.06, stiction_ref=0.2):
    F_f = np.sign(cart_velocity)*(coulomb + (static-coulomb)*np.exp(-np.abs(cart_velocity/stiction_ref))) + viscous*cart_velocity
    return F_f





if __name__ == "__main__":
    import matplotlib.pyplot as plt
    t = np.linspace(0,10,100)
    T = 0.1 * np.ones_like(t) #*np.sin(0.5*t)
    v = 3*np.sin(t)
    v1 = t - 5
    fric = friction_feedforward(v)
    fric1  = friction_feedforward(v1)
    x,xdot,phi,phidot = forced_response(sysCR, t, T)
    print(x)

    #bode(sysCR)
    #plt.show()




    plt.figure(2)
    plt.plot(v1, fric1)
    plt.xlabel('velocity [m/s]')
    plt.ylabel('friction [T]')
    plt.show()

    plt.figure(3)
    plt.plot(t,fric, label = 'friction')
    plt.plot(t,v, label = 'velocity')
    plt.xlabel('time [s]')
    plt.legend()
    plt.show()

