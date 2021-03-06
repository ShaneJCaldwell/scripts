#!/usr/bin/env python

# Adapted from a script Hanlun gave me to filter through the top of his structures, including 
# total score and H-bonding interactions. Strip down to just bin on a single score.

import sys
import os

top_cutoff = 102 #define how many to take

fin = open(sys.argv[1],'r') # open the input file
poses = [] # array of every pose in scorefile


for line in fin.read().split('\n')[2:-1]: # for every line in the scorefile
  #print line
  poses.append([line,float(line.split()[1])])  # line, total to total list of poses
poses_top = sorted(poses, key=lambda x:x[1])[:top_cutoff] # make list of only the top ones
#print poses_top[99] # have a look
fin.close()


dirname = 'top{}'.format(top_cutoff) # make directory
os.system('mkdir '+dirname) 

fout = open(dirname+'/score.sc','w') # write out the reduced scorefile

for i in poses_top: # for all of the best poses
  
  # Write to a new scorefile
  fout.write('{}\n'.format(i[0])) 

  # Copy every file in the top list, that ends with pdb to the top__ directory
  # from the scorefile list, take the last string, then split and take the front before underscore 
  # to get the pdb filename root
  os.system('cp {}.pdb {}/'.format(i[0].split()[-1].split("_")[0], dirname)) 
fout.close()