#!/bin/bash

# S Caldwell 2017.11.14

# for every file in a directory, 
# copy a parental file from a central location and make it locally 
# with the name of a local file.
# originally used to make a resfile for each pdb model in one place but 
# could be adapted for many things

for file in *
do 
	resfile=$(echo $file | awk -F"." '{print $1}')
	cp ../../template/resfile_TIM.res $resfile.res
done