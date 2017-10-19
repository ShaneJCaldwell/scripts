#!/bin/bash

# For every file in a folder with given (eg. pdb) extension
for i in $(ls *.pdb)
do 
	# Copy any lines containing this filename (i) from this file to that file
	grep $i sourcefile.txt >> destinationfile.txt
done