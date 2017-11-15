#!/usr/bin/python

# Brian Coventry

import os, sys, subprocess

#Command line arguments:
# ./split_commands.py list_of_commands.list folder_to_use_as_work_dir

def cmd(command, wait=True):
    # print ""
    # print command
    the_command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if (not wait):
        return
    the_stuff = the_command.communicate()
    return the_stuff[0] + the_stuff[1]

folder = cmd("readlink -f %s"%sys.argv[2]).strip()
if (not os.path.exists(folder)):
    print("%s doesn't exist!!!"%folder)
    sys.exit(1)


to_open = sys.argv[1]

f = open(to_open)
lines = f.readlines()
f.close()

sets = []
this_set = []
for line in lines:
    line = line.strip()
    if (len(line) == 0):
        continue
    this_set.append(line)
    if (len(this_set) == 50): # This is how many jobs per set, change it to whatever you want
        sets.append(this_set)
        this_set = []

if (len(this_set) > 0):
    sets.append(this_set)

if (not os.path.exists("%s/logs"%folder)):
    os.mkdir("%s/logs"%folder)

if (not os.path.exists("%s/commands"%folder)):
    os.mkdir("%s/commands"%folder)


# To run these sbatches do this:
# cd commands
# for j in *.sh; do sbatch -p short/medium/backfill $j; done
############################## pick one ^^ ################

count = 0
for this_set in sets:
    f = open("%s/commands/command%i.sh"%(folder, count), "w")
    line = line.strip()
    count += 1
    f.write("#!/bin/bash\n")
    f.write("#SBATCH --mem=8gb\n")
    f.write("#SBATCH -n 1\n")
    f.write("#SBATCH -o %s/logs/log%i.loglog\n"%(folder, count))
    f.write("\n".join(this_set))
    f.close()




