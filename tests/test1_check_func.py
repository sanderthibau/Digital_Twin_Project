import numpy as np
import matplotlib.pyplot as plt

plt.figure(1)
plt.hist([1,2,3],[1,2,3])
plt.show

x = np.linspace(-10,10)
y = np.sin(x)/x
b = 2
def f(a):
    return a + b
plt.figure(2)
plt.plot(x,y)

plt.plot([1,2,3])
plt. ylabel('sin(x)/x')
plt.xlabel('x')
plt.show()