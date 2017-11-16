
#Script to model random drift of receptors on a membrane and ligands in a box on top of that membrane. 
#Binding events will be modelled with a kon and koff value. 
#Activation/deactivation probability of bound receptors. 
#Substrate lives in box on opposite side, can bind activated receptors
#Bound substrate can be modified, which changes the dissociation rate
#Free substrate that is modified can dimerize
#will report when dimer reaches the edge of the box
#ARGH. Accidentally deleted earlier iteration scripts with simpler structures. Rebuild them from this one?
#Lesson: git from the start!
#later: add counters to extract statistics for binding and relative proportions, etc.

#Shane J Caldwell

import numpy as np
import matplotlib.pyplot as plt

#define limits of box
edge = 200
zheight = 10
zdepth = 50

#define time
cycles = 200

#binding range cutoff
binding_distance = 3.

#binding parameters (will be time dependent!!)
kbind = 0.7  #probability of ligand within binding range successfully docking to its target
krelease = 0.1 #probability of ligand dissociating in a given cycle
activation_prob = 0.01	#probability of receptor activating when bound to ligand in a given cycle
deactivation_prob = 0.0001 #probability of a receptor spontaneously deactivating in a cycle
#krelease_activated = 0.00001 #probability of ligand dissociating from an activated receptor == not used yet
substr_binding_prob = 0.9 #probability of substrate within binding range successfully docking to its target
substr_relase_prob = 0.0001 #probability of unmodified substrate dissociating in a given cycle
substr_mod_prob = 0.1 #probability docked substrate being modified in a given cycle
mod_substr_release_prob = 0.05 #probability of modified substrate (product) dissociating in a given cycle
substr_decay_prob = 0.01 #probability substrate loses its modification and returns to ground state
dimer_prob = 0.7 #probability that colliding substrates will succesfully dimerize

### Receptors ###
#number of particles in simulation = n_receptor
n_receptor = 3
#randomize receptor particle position
x = np.random.rand(n_receptor) * edge
y = np.random.rand(n_receptor) * edge
#set boolean variable to track if ligand is bound to receptor, if receptor is active or not
rec_bound = [False] * n_receptor
rec_active = [False] * n_receptor
#receptor mobility
rec_mobility =10


### Extracellular Ligands ###
#number of ligands in simulation = n_lig
n_lig = 50
#define one mobility for ligand
lig_mobility = 10
#randomize ligand particle position
xlig = np.random.rand(n_lig) * edge
ylig = np.random.rand(n_lig) * edge
zlig = np.random.rand(n_lig) * zheight
#set boolean variable to track if ligand is bound to receptor
#variable to track which receptor ligand is boung to to keep coords the same
lig_bound = [False] * n_lig
lig_receptor_id = [-1] * n_lig


### Intracellular Substrate ###
#number of substrates in simulation = n_sub
n_sub = 3
#define one mobility for substrate
sub_mobility = 10

#randomize ligand particle position
xsub = np.random.rand(n_sub) * edge
ysub = np.random.rand(n_sub) * edge
zsub = np.random.rand(n_sub) * zdepth * (-1)

#set boolean variable to track if ligand is bound to receptor
#variable to track which receptor ligand is boung to
#boolean if substrate is modified or not
sub_bound = [False] * n_sub
sub_receptor_id = [-1] * n_sub
sub_mod = [False] * n_sub
sub_binding_partner = [-1] * n_sub
sub_dimerized = [False] * n_sub


def twoD_diffuse(x, y, edge, mobility):

	#randomize direction and magnitude of displacement
	direction = np.random.rand() * 2 * np.pi
	distance = np.random.rand() * mobility

	#print "receptor %s" %(i + 1)			
	x = x + (distance * np.cos(direction))
	y = y + (distance * np.sin(direction))

	#keep inside boundaries
	if x > edge:
		x = x - edge
	if x < 0:
		x = x + edge
	if y > edge:
		y = y - edge
	if y < 0:
		y = y + edge

	return (x,y)

def threeD_diffuse_asymm_bounded(x, y, z, edge, height, mobility, topology):

	#randomize direction and magnitude of displacement in 2d
	direction = np.random.rand() * 2 * np.pi
	distance = np.random.rand() * mobility
	#randomize z displacement. in future switch to full 3d via euler angles
	zdispl = (np.random.rand() - 0.5) * 2 * mobility
			
	x = x + (distance * np.cos(direction))
	y = y + (distance * np.sin(direction))
	z = z + (zdispl)
	
	#keep inside boundaries
	if x > edge:
		x = x - edge
	if x < 0:
		x = x + edge
	if y > edge:
		y = y - edge
	if y < 0:
		y = y + edge
		
	#can't pass through membrane, let it stop, don't bounce		
	if z * topology < 0:
		z = 0
	#if exceeds max height, let it go, replace it with a new particle at the upper boundary 
	#(maintains concentration, but loses stochastisity). As long as box is big enough, should be np)
	elif z * topology > height:
		x = np.random.rand() * edge
		y = np.random.rand() * edge
		z = height * topology

	return (x,y,z)

def binding_check(x1, y1, x2, y2, z2, bound1, bound2, distance, prob, t, rec_id, lig_id):
	#troubleshooting - had trouble passing none to variables
#	print (lig_bound[j], rec_bound[i], xlig[j], ylig[j], lig_receptor_id[j])
	if np.sqrt((x1 - x2)**2 + (y1 - y2)**2) < distance and z2 < distance and bound1 == False and bound2 == False:
		print "Cycle %s: Encounter between receptor %s and ligand %s" %(t+1,rec_id,lig_id)
		rolldice = np.random.rand()
		if rolldice < prob:
			print "    Successfully bound receptor %s and ligand %s" %(rec_id,lig_id)
			return (True, True, x1, y1, rec_id)
		else:
			print "    Receptor %s did not bind ligand %s" %(rec_id,lig_id)
			return (False, False, x2, y2, -1)
	else:
		return (lig_bound[j], rec_bound[i], x2, y2, lig_receptor_id[j])
	


def unbinding_check(prob, t, rec_id, lig_id):
	rolldice = np.random.rand()
	print "unbind test for cycle %s" %(t)
	if rolldice < krelease:
		print "Cycle %s: Receptor %s has released ligand %s" %(t+1,rec_id,lig_id)
		return (False, False, -1)
	else:
		print "Cycle %s: r %s still grabbing onto ligand %s" %(t+1,rec_id,lig_id)
		return (True, True, rec_id)


#run number of cycles t
for t in range (0,cycles):
	#print "Cycle %s" %(t + 1)

	#Move receptor by random displacement
	for i in range (0, n_receptor):	
		(x[i],y[i]) = twoD_diffuse(x[i],y[i],edge,rec_mobility)

	#Move ligand by random displacement if unbound
	for i in range (0, n_lig):
	
		#unbound ligand diffuses freely, wraparound in xy, closed lower and open upper boundary		
		if lig_bound[i] == False:
			(xlig[i], ylig[i], zlig[i]) = threeD_diffuse_asymm_bounded(xlig[i], ylig[i], zlig[i], edge, zheight, lig_mobility, 1)
	
		# for ligand that stays bound to receptor, coordinates of ligand should be same as the receptor				
		elif lig_bound[i] == True:
			xlig[i] = x[lig_receptor_id[i]]
			ylig[i] = y[lig_receptor_id[i]]
			#leave zlig[i] unchanged


	#Move substrate by random displacement if unbound, keep dimeric particles together
	for i in range (0, n_sub):
		#print "substrate %s" %(i + 1)	
		if sub_bound[i] == False:	
			(xsub[i], ysub[i], zsub[i]) = threeD_diffuse_asymm_bounded(xsub[i], ysub[i], zsub[i], edge, zdepth, sub_mobility, -1)		
	
		# for substrate that stays bound to receptor, coordinates of substrate should be same as the receptor		
		elif sub_bound[i] == True:
			xsub[i] = x[sub_receptor_id[i]]
			ysub[i] = y[sub_receptor_id[i]]
			#leave zsub[i] unchanged
	
		#if dimerized, copy coordinates from higher index partner
		#probably not ideal solution yet
		if sub_dimerized[i] == True:
			if i < sub_binding_partner[i]:
				xsub[i] = xsub[sub_binding_partner[i]]
				ysub[i] = ysub[sub_binding_partner[i]]
				zsub[i] = zsub[sub_binding_partner[i]]

	#test for ligand binding any receptor within defined binding distance
	for i in range (0, n_receptor):
		for j in range (0, n_lig):
			#print "i=%s" %(i)
			#print "j=%s" %(j)
			(lig_bound[j], rec_bound[i], xlig[j], ylig[j], lig_receptor_id[j]) = \
			binding_check(x[i], y[i], xlig[j], ylig[j], zlig[j], lig_bound[j], \
			rec_bound[i], binding_distance, kbind, t, i, j)
			#print (lig_bound[j], rec_bound[i], xlig[j], ylig[j], lig_receptor_id[j])


	#unbinding check for bound receptors - there must be a more efficient way!
	for i in range (0, n_receptor):
		for j in range (0, n_lig):
			if lig_bound[j] == True and rec_bound[i] == True and lig_receptor_id[j] == i: 
				(lig_bound[j], rec_bound[i], lig_receptor_id[j]) = unbinding_check(krelease, t, i, j)
				if lig_bound[j] == False:
					print "unbound. Brownian kick to get rid of ligand"				
					ligdirection = np.random.rand() * 2 * np.pi
					ligdistance = np.random.rand() * lig_mobility
					ligzdispl = (np.random.rand() - 0.5) * 2 * lig_mobility
					xlig[j] = xlig[j] + (ligdistance * np.cos(ligdirection))
					ylig[j] = ylig[j] + (ligdistance * np.sin(ligdirection))
					zlig[j] = zlig[j] + (ligzdispl)		
			

	#activation check - receptors with bound ligand have a %chance of becoming active per cycle	
	for i in range (0, n_receptor):
		if rec_bound[i] == True and rec_active[i] == False:
			#print "ligand is bound to receptor %s" %(i)
			rolldice = np.random.rand()
			if rolldice < activation_prob:
				rec_active[i] = True
				print "Cycle %s: Receptor %s has become active" %(t+1,i)
		elif rec_bound[i] == True and rec_active[i] == True:
			rolldice = np.random.rand()
			if rolldice < deactivation_prob:
				rec_active[i] = False
				print "Cycle %s: Receptor %s has deactivated" %(t+1,i)


	#test for substrate binding activated receptor in defined binding distance
	#have not defined a limit for substrate docking yet. potentially many could bind
	for i in range (0, n_receptor):
		for j in range (0, n_sub):
			if np.sqrt(np.square(x[i] - xsub[j]) + np.square(y[i] - ysub[j])) < binding_distance \
			and zsub[j] * (-1) < binding_distance \
			and sub_bound[j] == False \
			and rec_active[i] == True:
				print "Cycle %s: Encounter between activated receptor %s and substrate %s" %(t+1,i,j)
				rolldice = np.random.rand()
				if rolldice < substr_binding_prob:
					print "    Docked substrate %s onto receptor %s" %(j,i)
					xsub[j] = x[i]
					ysub[j] = y[i]
					sub_bound[j] = True
					rec_bound[i] = True
					sub_receptor_id[j] = i
				else:
					print "    Receptor %s did not bind substrate %s" %(i,j)

	#unbinding check for substrates bound to substrate
	for i in range (0, n_receptor):
		for j in range (0, n_sub):
			if sub_bound[j] == True and sub_mod[j] == False and sub_receptor_id[j] == i:
				rolldice = np.random.rand()
				if rolldice < substr_relase_prob:
					print "Cycle %s: Receptor %s has released substrate %s unmodified" %(t+1,i,j)
					subdirection = np.random.rand() * 2 * np.pi
					subdistance = np.random.rand() * sub_mobility
					subzdispl = (np.random.rand() - 0.5) * 2 * sub_mobility
					xsub[j] = xsub[j] + (subdistance * np.cos(subdirection))
					ysub[j] = ysub[j] + (subdistance * np.sin(subdirection))
					zsub[j] = zsub[j] + (subzdispl)
					sub_bound[j] = False
			elif sub_bound[j] == True and sub_mod[j] == True and sub_receptor_id[j] == i:
				rolldice = np.random.rand()
				if rolldice < mod_substr_release_prob:
					print "Cycle %s: Modified substrate %s has dissociated from receptor %s" %(t+1,j,i)					
					subdirection = np.random.rand() * 2 * np.pi
					subdistance = np.random.rand() * sub_mobility
					subzdispl = (np.random.rand() - 0.5) * 2 * sub_mobility
					xsub[j] = xsub[j] + (subdistance * np.cos(subdirection))
					ysub[j] = ysub[j] + (subdistance * np.sin(subdirection))
					zsub[j] = zsub[j] + (subzdispl)
					sub_bound[j] = False					
					

	#catalysis check - possibly modify bound unmodified substrate	
	for i in range (0, n_sub):
		if sub_bound[i] == True and sub_mod[i] == False:
			#print "substrate is bound to receptor %s" %(i)
			rolldice = np.random.rand()
			if rolldice < substr_mod_prob:
				sub_mod[i] = True
				print "Cycle %s: Substrate %s has been modified" %(t+1,i)

	#substrate deactivation check - substrate can spontaneously deactivate	
	for i in range (0, n_sub):
		if sub_bound[i] == False and sub_mod[i] == True:
			rolldice = np.random.rand()
			if rolldice < substr_decay_prob:
				sub_mod[i] = False
				print "Cycle %s: Substrate %s has lost its modification" %(t+1,i)

	#activated substrate collision check
	for i in range (0, n_sub):
		for j in range (i+1, n_sub):
			#print "Comparing sub %s with sub %s" %(i,j)
			if sub_mod[i] == True and sub_mod[j] == True and sub_dimerized[i] == False and sub_dimerized[j] == False:
				d = np.sqrt((xsub[i]-xsub[j])**2 + (ysub[i]-ysub[j])**2 + (zsub[i]-zsub[j])**2)
				if d < binding_distance:
					print "Cycle %s: Modified substrate %s and %s have collided!" %(t+1,i,j)
					rolldice = np.random.rand()
					if rolldice < dimer_prob:
						print "    Substrates %s and %s have formed a productive dimer" %(i,j)
						sub_dimerized[i] = True
						sub_dimerized[j] = True
						sub_binding_partner[i] = j
						sub_binding_partner[j] = i
						xsub[i] = xsub[j]
						ysub[i] = ysub[j]
						zsub[i] = zsub[j]
					else:
						print "    Substrates %s and %s did not bind" %(i,j)

	for i in range (0, n_sub):
		if zsub[i] < (zdepth * (-1)) + binding_distance and sub_dimerized[i] == True:
			print "Dimer containing substrate %s has reached the lower limit" %(i)
			#reset to recycle. not a final model
			sub_dimerized[i] = False
			sub_mod[i] = False

	#tally molecule states
	bound_receptors = 0
	active_receptors = 0
	for i in range (0, n_receptor):
		if rec_bound[i] == True:
			bound_receptors = bound_receptors + 1
		if rec_active[i] == True:
			active_receptors = active_receptors + 1
#	print "At cycle %s, %s receptors bound of %s" %(t + 1, bound_receptors, n_receptor)
#	print "At cycle %s, %s receptors active of %s" %(t + 1, active_receptors, n_receptor)

	bound_lig = 0
	for i in range (0, n_lig):
		if lig_bound[i] == True:
			bound_lig = bound_lig + 1
#	print "At cycle %s, %s ligands bound of %s" %(t + 1, bound_lig, n_lig)

	docked_sub = 0
	mod_sub = 0
	dimer_sub = 0
	for i in range (0, n_sub):
		if sub_bound[i] == True:
			docked_sub = docked_sub + 1
		if sub_mod[i] == True:
			mod_sub = mod_sub + 1
		if sub_dimerized[i] == True:
			dimer_sub = dimer_sub + 1
#	print "At cycle %s, %s substrates docked of %s" %(t + 1, docked_sub, n_sub)
#	print "At cycle %s, %s substrates modified of %s" %(t + 1, mod_sub, n_sub)
#	print "At cycle %s, %s substrates dimerized of %s" %(t + 1, dimer_sub, n_sub)


##### Plotting #####


	#plot unbound receptor as green, bound inactive as blue, active as red
	for i in range (0, n_receptor):
		if rec_active[i] == True:
			plt.scatter(x[i],y[i], c="red")	
		elif rec_bound[i] == True and rec_active[i] == False:
			plt.scatter(x[i],y[i], c="blue")
		else:
			plt.scatter(x[i],y[i], c="green")

	#plot bound substrate as orange, modified as black, free unmodified as purple
	for i in range (0, n_sub):
		if sub_dimerized[i] == True:
			plt.scatter(xsub[i], ysub[i], c="white")
		elif sub_bound[i] == True:
			plt.scatter(xsub[i], ysub[i], c="orange")
		elif sub_mod[i] == True:
			plt.scatter(xsub[i], ysub[i], c="black")
#		else:
#			plt.scatter(xsub[i], ysub[i], c="purple")

'''
	#plot ligand as pink if within binding distance of plane else yellow
	for i in range (0, n_lig):
		if zlig[i] < binding_distance:
			plt.scatter(xlig[i], ylig[i], c="pink")
		else:
			plt.scatter(xlig[i], ylig[i], c="yellow")
'''

plt.show()
#plt.savefig("png.png", bbox_inched="tight")
