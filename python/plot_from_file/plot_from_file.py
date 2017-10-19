#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np

values = np.loadtxt('calcs.txt')

x = values[:,0]
y = values[:,1]

plt.plot(x,y)

plt.xlabel('x axis label')
plt.ylabel('y axis label')
plt.title('Plot Title')
plt.grid(False)
plt.savefig("output.png")
plt.show()