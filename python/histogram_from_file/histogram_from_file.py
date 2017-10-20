#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np

#converter = {0: lambda s: float(s.strip('"'))}
values = np.loadtxt('score.sc', skiprows=2, usecols=[8])

plt.hist(values, bins=50, range=(0.0, 1000.0))

plt.xlabel('x axis label')
plt.ylabel('y axis label')
plt.title('Plot Title')
plt.grid(False)
plt.savefig("output.png")
plt.show()