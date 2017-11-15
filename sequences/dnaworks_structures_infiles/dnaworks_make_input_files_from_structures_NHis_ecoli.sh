#!/bin/bash

#DASM to translate heterodimers of repeat-proteins and miniprotein
#23/Sept/2017, Bakerlab
#dadriano@gmail.com, do not complain if it doesn't work for you

# Adapted and commented by S. Caldwell 2017.11.15
# Take pdb files, use another script for sequence files input

path="./"
input_pdb=$1 #This should be a PDB structure with two chains separated by a TER

# dnaworks can only handle really short names. Daniel has implemented a hash to get around this problem,
# but for now I will comment it out and make sure my filenames are very short.

#input_hash=`md5sum ${input_pdb} | awk '{print $1}'`
#tmp_out="${input_hash}.dnawj" #output to avoid DNAworks names too long problem
tmp_out="${input_pdb}.dnawj" # this outfile is the input for dnaworks. Write configuration here.
file=$(basename ${input_pdb})

#To extract sequences
seqA=$(/software/rosetta/main/source/scripts/python/public/pdb2fasta.py $input_pdb | grep -v ">" | sed -n 1p) #The sequenceA

nucl_RBS="GAAGGAGATGTCTAA"
nucl_StopCod="TAA"
nucl_StartCod="ATG"
#prot_CstrepTagII="GGGSAWSHPQFEKGGGSGGGSGGSAWSHPQFEK"
#prot_NhisTag="GSSHHHHHHSSG"
prot_NhisTag_Trp="GHHHHHHGGWGGSG"
TEVcut="GENLYFQG"

# The below all writes to an input file based on the pdb name for dnaworks

echo "solutions 5" > ${path}/${tmp_out}  # 5 runs per gene
echo "repeat 10" >> ${path}/${tmp_out}	# window of 10 nt used to search for repeats
echo "length 100" >> ${path}/${tmp_out} # length of oligos
#echo "MELTing 65" >> ${path}/${tmp_out}
echo "melting low 75" >> ${path}/${tmp_out} 
echo "LOGFILE \"${path}${tmp_out}.out\"" >> ${path}/${tmp_out}
echo "pattern" >> ${path}/${tmp_out} # exclude the below sequences
#echo "  SpeI  ACTAGT" >> ${path}/${tmp_out}
#echo "  EARI  CTCTTC" >> ${path}/${tmp_out}
#echo "  EARI  GAAGAG" >> ${path}/${tmp_out}
echo "  BamHI GGATCC" >> ${path}/${tmp_out}
echo "  NdeI CATATG" >> ${path}/${tmp_out} # NdeI
echo "  XhoI CTCGAG" >> ${path}/${tmp_out} # XhoI
#echo "  NheI GCTAGC" >> ${path}/${tmp_out} # NheI
#echo "  BsaI GGTCTC" >> ${path}/${tmp_out} # BsaI
#echo "  BsaI GAGACC" >> ${path}/${tmp_out} # BsaI
#echo "  Aarl  CACCTGC" >> ${path}/${tmp_out}
echo "  PolyA AAAAAA" >> ${path}/${tmp_out}
echo "  PolyG GGGGGG" >> ${path}/${tmp_out}
echo "  PolyT TTTTTT" >> ${path}/${tmp_out}
echo "  PolyC CCCCCC" >> ${path}/${tmp_out}
echo "//" >> ${path}/${tmp_out}
echo >> ${path}/${tmp_out}
#echo "codon E. coli" >> ${path}/${tmp_out}
echo "codon ecoli2" >> ${path}/${tmp_out}
#echo "codon s. cerevesiae" >> ${path}/${tmp_out}
echo "frequency threshold 5" >> ${path}/${tmp_out} # use codons above 5% abundance in target organism
echo "tbio" >> ${path}/${tmp_out} #thermodynamically balanced "inside-out" method

# Weight repeats up to prioritize the lack of repeats in the sequence.
echo "weight twt 1.0 cwt 1.0 rwt 2.0 mwt 1.0 gwt 1.0 awt 1.0 lwt 1.0 pwt 1.0 fwt 1.0" >> ${path}/${tmp_out}

tmp_query_line=""

# Outline the construct below
tmp_query_line=${tmp_query_line}"protein\n${prot_NhisTag_Trp}${TEVcut}${seqA}\n//\n"

# Add a stop codon if not using the vector tags
tmp_query_line=${tmp_query_line}"nucleotide\n${nucl_StopCod}\n//\n"
echo -e ${tmp_query_line} | awk -v max_fasta_line_len=80 '{for (i=1;i<=length($0);i+=max_fasta_line_len) print substr( $0, i, max_fasta_line_len )}' >> ${path}/${tmp_out}

# Do these in separate scripts to run it as an sbatch

#Execute the job
#/home/strauch/local/DNAWorks/dnaworks ${path}/${tmp_out}

#Assemble the monomer final seq
#cat ${path}/${tmp_out}.out | awk 'BEGIN{doprint=0;results[1]="";seqcount=0}{if($0 ~ /---------/){doprint-=1; next};if((doprint>1) && (length($0)>3)){results[seqcount]=results[seqcount] $2}else if(doprint>0){if (( $0 !~ /The oligonucleotide assembly/)&&(length($0)>3)){print $0 " " results[$1]}};if($0 ~ / #    Tm   Len  |    Score/){doprint=1};if(($0 ~ /The DNA sequence/)){doprint=3; seqcount+=1}}' | sort -nk 5 > ${path}/${tmp_out}_dnaworks_translations.dat 
#dnaSeq=`cat ${path}/${tmp_out}_dnaworks_translations.dat | head -n 1 | awk '{print $NF}'` 

#echo ${dnaSeq} > ${path}/${file}.ecoli_dna.seq

