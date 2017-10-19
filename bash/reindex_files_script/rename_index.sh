#!/bin/bash

handle="handle"

# Create logfile
touch file_renaming_index.log
echo "Renaming pdb files to cut down the filename length. Storing the index here of what duplicate files correspond to which parental ones." >> file_renaming_index.log

# Count the number of files and name them sequentially. Start at zero for cases where the first one is parental to the rest
count=0

# Zero-pad to 6 digits in this case
countout=$(printf "%06d" "$count")

# Loop through all files in the directory, recursively if necessary
for i in $(find /path/to/files -type f -name "*.extension")
do
	echo "$handle$countout.extension comes from $i" >> file_renaming_index.log # Write to index file
	cp $i ./$handle$countout\.extension # Copy the file
	((count++)) # Increment counter
	countout=$(printf "%06d" "$count") # Zero pad
done