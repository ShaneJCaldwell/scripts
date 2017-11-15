#!/bin/bash

# Script to generate batch of rosetta_scripts runs

# script run files
batchfile="sbatch.sh"
commands_design="commands.sh"

# input scripts - can be in a central location
flagsfile="flags.flags" 
xmlfile="file.xml"

# rosetta
rosetta="/software/rosetta/latest/bin/rosetta_scripts"
nstruct="10"	# number of structures per batch design run
cycles="10"		# number of batches, use to split out to multiple processors

#input
sourcefiles="location/of/pdb/files"
cstfile="/location/of/constraints/file"
symfile="/location/of/symmdef/file"
paramsfile="/location/of/params/file"
resfile="resfile.res" 	# usually local

#slurm
n_processors="10"
memory="60"
queue="medium"

# Create files
touch $batchfile
touch $commands_design
mkdir output

# Make executable
chmod +x $batchfile
chmod +x $commands_design #executable to test interactively, comment out to disable


# Write this block of text to the batchfile, some default SLURM settings (Leave N=1)

cat << EOF >> $batchfile
#!/bin/bash
#SBATCH -p $queue
#SBATCH -n $n_processors
#SBATCH -N 1
#SBATCH --mem=${memory}g
#SBATCH -o design.log
cd $(echo $(pwd))
cat $commands_design | parallel -j$n_processors
EOF

# can put out a flags file each time or comment this out 
# to use a single one. This is what a flags file is for, anyway

# cat << EOF >> $flagsfile
# -symmetry:symmetry_definition $symfile
# -beta
# -parser:script_vars symmetry=$symfile
# -in:file:extra_res_fa $paramsfile
# -output_virtual true
# -packing:ex1:level 6
# -packing:ex2:level 6
# -out:path:all ./output/
# EOF

# cycles cycles of nstruct designs each for each pdb in directory

for j in $(seq 1 $cycles);
do
	for i in $(find $sourcefiles  -type f -name "*.pdb");
	do
			echo "$rosetta \
			-parser:protocol $xmlfile \
			@$flagsfile \
			-parser:script_vars constraints=$cstfile \
			-parser:script_vars resfile=$resfile \
			-nstruct $nstruct \
			-s $i \
			-out:file:scorefile score.sc \
			-out:suffix _batch$(printf "%02d" "$j")" >> $commands_design

	done;
done;