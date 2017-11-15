#!/bin/bash

# S Caldwell, 2017.11.14

# This script will make a new scorefile using only the score and name terms to compare more easily. 

# Send every line in scorefile - starting at 3 - to awk, 
# make i the score of interest (in this case total score)
# and last (pdb filename) space-delimited items

infile=$1
outfile="${infile%.*}_condensed.${infile##*.}"

echo -e "score \t name" >> $outfile

for i in `tail -n +3 $infile | awk '{print $2 "," $NF}'`
do 
	score=$(echo $i | awk -F"," '{print $1}')
	PDB=$(echo $i | awk -F"," '{print $2}') 
	
	echo $score" "$PDB >> $outfile
	
done