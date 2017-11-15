#!/bin/bash

# Script to generate batch of pyrosetta runs (for filtering for good residue rotamers)

# Name the batchfile once
batchfile="sbatch.sh"
commands="commands"

# Create batchfile
touch $(batchfile)

# Make executable
chmod +x $(batchfile)

# Write this block of text to the batchfile, some default SLURM settings (Leave N=1)
# Source pyrosetta
# Make an output directory for files
# In this case, two outputs in symmetric and asymmetric pdb files
# Create a file to track some outputs

cat << EOF >> $(batchfile)
#!/bin/bash
#SBATCH -p medium
#SBATCH -n 20
#SBATCH -N 1
#SBATCH --mem=64g
#SBATCH -o log
source /software/pyrosetta2/setup.sh
mkdir output
mkdir output/asymmetric
mkdir output/symmetric
touch output/hitlist.txt
cd /home/scald/projects/dirhodium_TIM/screen_loop_built/
cat $(commands) | parallel -j20
EOF

# For every input pdb file, write a new line into the commands file
for i in $(find /pdb/source/directory/ -type f -name "startname*.pdb");
do
		echo "python script.py -s $i" >> $(commands)

done;