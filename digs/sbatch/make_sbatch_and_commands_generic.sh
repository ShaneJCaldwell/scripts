#!/bin/bash

# Script to generate batch of slurm runs (generic)

# Name the batchfile once
batchfile="sbatch.sh"
commands="commands.cmd"

#slurm
n_processors="10"
memory="60"
queue="medium"

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
for i in $(ls *.extension);
do
		echo "command $i" >> $commands

done;