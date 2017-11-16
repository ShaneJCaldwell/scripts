import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = fig.gca(projection='3d')


turns = 3				#number of turns of primary helix. 
incline = 25			# incline of primary helix in degrees
resolution = 50000		# number of points to calculate
frequency = 90

phi = np.pi/180*incline	# phi = incline angle in radians

a = 1				# a = radius of primary helix
b = frequency*np.cos(phi) 					# b = frequency turns secondary helix/primary helix
c = 0.4				# c = radius of secondary helix



#define range. 6 pi = 3 full cycles
t = np.linspace(0, turns * 2 * np.pi/np.cos(phi), resolution)

#incline due to pitch of first helix plus change due to secondary helix
z = t*np.sin(phi) + c*np.cos(phi)*np.cos(b*t) 

#polar coords, main radius + change due to secondary helix radius
r = a*(1+ c*np.sin(b*t))

# polar coords, normal progression + displacement because of incline
theta = t*np.cos(phi) - c*np.sin(phi)*np.cos(b*t) 


x = r * np.cos(theta) #convert polar coords to xyz
y = r * np.sin(theta)

mpl.pyplot.autoscale(False) # autoscale distorts the curve
ax.plot(x, y, z, label='superhelix')
ax.legend()

plt.show()
