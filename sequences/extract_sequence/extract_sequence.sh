#!/bin/bash

# S. Caldwell 2017.11.15
# After running dnascripts to optimize codons and reduce redundancy, take output .out files and make 
# dat and seq files containing the relevant sequence. Taken from dadriano's master script, but do this afterward to 
# run things in parallel first.

path="./"

for i in $(ls *.pdb)
do
	tmp_out="${i}.dnawj"

	#Assemble the monomer final seq
	cat ${path}${tmp_out}.out | awk 'BEGIN{doprint=0;results[1]="";seqcount=0}{if($0 ~ /---------/){doprint-=1; next};if((doprint>1) && (length($0)>3)){results[seqcount]=results[seqcount] $2}else if(doprint>0){if (( $0 !~ /The oligonucleotide assembly/)&&(length($0)>3)){print $0 " " results[$1]}};if($0 ~ / #    Tm   Len  |    Score/){doprint=1};if(($0 ~ /The DNA sequence/)){doprint=3; seqcount+=1}}' | sort -nk 5 > ${path}/${tmp_out}_dnaworks_translations.dat 
	dnaSeq=`cat ${path}/${tmp_out}_dnaworks_translations.dat | head -n 1 | awk '{print $NF}'` 

	echo ${dnaSeq} > ${path}/${i}.ecoli_dna.seq

done