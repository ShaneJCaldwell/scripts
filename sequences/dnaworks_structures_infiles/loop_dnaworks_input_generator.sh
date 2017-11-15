#!/bin/bash

for i in $(ls *.pdb)
do
	./dnaworks_structures_ecoli.sh $i
done