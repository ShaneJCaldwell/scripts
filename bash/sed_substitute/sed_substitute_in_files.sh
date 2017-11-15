#!/bin/bash

# S. Caldwell 2017.11.14

# For every file in parent folder with given (eg. pdb) extension
for i in $(ls ../*.pdb)
do
	# copy files from parent directory here
	echo "Copying $i into working directory"
	cp $i .
done


for i in $(ls *.pdb)
do 
	echo "file $i"
	# Find and replace DRE with GLU
	# don't bother with backup because these files were already copied right above.
	sed -i '' 's/DRE/GLU/g' $i
done