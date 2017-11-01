#!/bin/bash

infile="$1"
outfile="${infile%.*}_sorted.${infile##*.}"

cut -f 2 $infile | sort -r >> $outfile