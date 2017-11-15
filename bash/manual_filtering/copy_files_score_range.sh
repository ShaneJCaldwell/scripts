#!/bin/bash

# S. Caldwell 2017.11.14

# This script will take a pool of pdb files and the scorefile 
# that they had generated and based upon a value, only copy if the
# model fell within a specific range default lower limit is zero, 
# but could be higher if binning, other things possible.

# Set the thresholds, upper and lower
upper=300
lower=0
directory=/path/to/directory

# Send every line in scorefile - starting at 3 - to awk, make i the score of interest (in this case fa_rep of a default scorefunction)
# and last (pdb filename) space-delimited items
for i in $(tail -n +3 ../score.sc | awk '{print $9 "," $NF}')
do 
	#fa_rep is column 9 in this file. read it and filter based on cutoff
	score=$(echo $i | awk -F"," '{print $1}')
	PDB=$(echo $i | awk -F"," '{print $2}' | awk -F'_' '{print $1}').pdb 
	
	#echo $PDB "has score of" $score	
	
	if [ $(echo $score'<='$upper | bc -l) -eq 1 ]
	then
		echo $PDB "has score of" $score	
		echo "$PDB passes the score <= $upper filter"
		if [ $(echo $score'>'$lower | bc -l) -eq 1 ]
		then
			echo "$PDB is also above the lower threshold of $lower"
			echo "Copying to current directory"
			cp $directory/$PDB .

			# Specialized case where I also wanted to filter based on a filesize cutoff as well. 
			# if [ $(wc -c $directory/$PDB | awk '{print $1}') -le 50000 ] # if wordcount is less than 50 000 it is a truncated model
			# then
			# 	echo "... but ... the filesize is too small and corresponds to a truncated intermediate model"
			# 	echo "Skipping this file."
			# else
			#	echo "Copying to current directory"
		 	#	cp $directory/$PDB .
		 	# fi
		else
			echo "$PDB is too good! better than lower filter"
			echo "File skipped"
		fi
	fi
done