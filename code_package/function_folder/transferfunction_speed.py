import control as ct
from control.matlab import *
import matplotlib.pyplot as plt
import time


## reading out data from twincat with pyads
U = [1,-1,1] #read out input data
X0 = 0 #read out current state
T = [0.1,0.2,0.3] #time steps

Keff = 2*10**6
mL = 5
Jm = 0.05
r = 0.0098
bs = 50
b1= 0.01

rigid_part = tf([1],[Jm+mL*r**2, b1, 0])
flexible_part = tf([mL, bs, Keff], [Jm*mL/(Jm+mL*r**2), bs, Keff])

twomass = series(rigid_part, flexible_part)

start_time = time.time()
t, result = ct.forced_response(twomass,T=T, U=U, X0=X0)
print("--- %s seconds ---" % (time.time() - start_time))

print(result)
print(t)


phi, t= step(twomass, 1)
plt.plot(t, phi)
plt.show()