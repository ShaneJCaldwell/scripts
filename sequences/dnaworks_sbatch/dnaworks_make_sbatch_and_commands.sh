#!/bin/bash

# Script to generate batch of slurm runs (dnaworks)

# Name the batchfile once
batchfile="sbatch.sh"
commands="commands.cmd"

# Location of dnaworks binary
dnaworks="/home/strauch/local/DNAWorks/dnaworks"

# Slurm stuff
queue="short"
n_processors="8" # 8 or less to keep things under 64g memory
memory=$((8*$n_processors)) #fairly intensive memory requirement

# Create batchfile
touch $batchfile
touch $commands

# Make executable
chmod +x $batchfile

# Write this block of text to the batchfile, some default SLURM settings (Leave N=1)

cat << EOF >> $batchfile
#!/bin/bash
#SBATCH -p $queue
#SBATCH -n $n_processors
#SBATCH -N 1
#SBATCH --mem=${memory}g
#SBATCH -o slurm.log
cat $commands | parallel -j$n_processors
EOF

# For every input file, write a new line into the commands file
for i in $(ls *.dnawj);
do
		echo "$dnaworks $i" >> $commands

done;