#!/bin/bash

# S. Caldwell 2017.11.15 extract fasta sequence from .seq files made from 
# dnaworks pipeline. Put it in a single fasta file to send places or do bioinformatics

orderfile=name_of_fas_file.fas

for i in *.seq # each seq file
do 
	#echo $i
	echo ">"$(echo $i | awk -F. '{print $1}') >> $orderfile # fasta format >name without extensions from seqfile
	cat $i >> $orderfile	# contents of seqfile
	echo "" >> $orderfile	# lazy newline
done

# Send this right to clustal or other analysis that reads fasta format