#!/bin/bash

# S Caldwell 2017.11.14

# Use this script to copy lines from an origin file to a new file
# Originally used to pull lines from a reindexing log into a new log as the 
# pdb files the index was based on was filtered down.

# For every file in a folder with given (eg. pdb) extension
for i in $(ls *.pdb)
do 
	# Copy any lines containing this filename (i) from this file to that file
	grep $i sourcefile.txt >> destinationfile.txt
done