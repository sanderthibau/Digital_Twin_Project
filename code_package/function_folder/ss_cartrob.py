
import control as ct
from control.matlab import ss
import matplotlib.pyplot as plt
import numpy as np
import time

start_time = time.time()
K = 2*10**6
m = 50
J = 0.05
R = 0.0098
bs = 50
b1= 0.01

#State Space Cartesian Robot system
A = [[0,0,1,0],[0,0,0,1],[-K/m,K*R/m,0,0],[K*R/J,-K*R*R/J,0,0]]

B = [[0],[0],[0],[1/J]]

C = [0,1,0,0]

D = 0

sysCR = ss(A,B,C,D)


Time = np.linspace(0,1,10)
U = np.sin(3*Time)-Time/30
X0 = [0,0,0,0]
start_time = time.time()
t, yout, xout = ct.forced_response(sysCR,Time, U, X0, return_x=True)
print("--- %s seconds ---" % (time.time() - start_time))

#print(len(Time)-len(xout[1,:]))
#plt.plot(Time,yout)
#plt.show()

