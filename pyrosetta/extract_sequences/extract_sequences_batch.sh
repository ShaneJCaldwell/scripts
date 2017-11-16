#!/bin/bash

for i in $(find /path/to/files -type f -name "*.pdb")
do
	echo $i;
	/software/rosetta/main/source/scripts/python/public/pdb2fasta.py $i >> sequences.fas
done;