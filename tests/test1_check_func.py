import numpy as np
import matplotlib.pyplot as plt
import csv

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from matplotlib import rcParams
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = 'cmr10'
plt.rcParams['mathtext.fontset'] = 'cm'
rcParams['axes.unicode_minus'] = False
rcParams['axes.formatter.use_mathtext'] = True

# Generate example data
np.random.seed(42)
weight = np.random.uniform(1500, 4000, 100)
turning_circle = np.random.uniform(30, 50, 100)
displacement = np.random.uniform(100, 300, 100)
horsepower = np.random.uniform(50, 250, 100)
gas_tank_size = np.random.uniform(10, 25, 100)

# Combine data into a dictionary
data = {
    "Weight": weight,
    "Turning Circle": turning_circle,
    "Displacement": displacement,
    "Horsepower": horsepower,
    "Gas Tank Size": gas_tank_size,
}

variables = list(data.keys())
values = list(data.values())
print(values)
n = len(variables)

# Create the figure
fig = plt.figure(figsize=(12, 12))
gs = gridspec.GridSpec(n, n, wspace=0.1, hspace=0.1)

# Create the scatter plot matrix
for i in range(n):
    for j in range(n):
        ax = fig.add_subplot(gs[i, j])
        
        if i == j:
            # Diagonal: plot a histogram
            ax.hist(values[i], bins=15, color='lightblue', edgecolor='black')
            if i < n - 1:
                ax.set_xticks([])
            if j > 0:
                ax.set_yticks([])
        else:
            # Off-diagonal: scatter plot
            ax.scatter(values[j], values[i], alpha=0.7, s=15, color='blue')
            if j > 0:
                ax.set_yticks([])
            if i < n - 1:
                ax.set_xticks([])

        # Add labels for the outermost axes
        if i == n - 1:
            ax.set_xlabel(variables[j], fontsize=10)
        if j == 0:
            ax.set_ylabel(variables[i], fontsize=10)
            

# Add a title
fig.suptitle("Scatterplot Matrix", fontsize=16, y=0.92)

# Show the plot
plt.show()

inp = [e for e in [1]]
print(inp)



# plt.figure(1)
# plt.hist([1,2,3],[1,2,3])
# plt.show

# x = np.linspace(-10,10)
# y = np.sin(x)/x
# b = 2
# def f(a):
#     return a + b
# plt.figure(2)
# plt.plot(x,y)

# plt.plot([1,2,3])
# plt. ylabel('sin(x)/x')
# plt.xlabel('x')
# plt.show()