##########################################################################################
#
# Define a function to take two chains, with defined start/end points,
# superpose them by lsq, and export the NCS transformation matrix in appropriate 
# format for input into SORTWATER CCP4 utility. 
#
# Writes a file - matrices.txt - in the working directory.  
# The contents can be manually copied into a SORTWATER script
#
# Modified from coot python source function single_manual_ncs_ghosts
# in the ncs.py module, Bernhard Lohkamp and Paul Emsley, University of York
# https://code.google.com/p/coot/source/browse/branches/release-0.7.x/python/ncs.py
#
# Shane Caldwell, McGill University, 2015.04.16
# 
##########################################################################################

###USAGE####

# print_ncs_matrix(imol, resno_start, resno_end, ref_chain, peer_chain)
# imol = the molecule number in coot, int
# resno_start = starting residue of two chains to be aligned, int
# resno_end = ending residue of two chains to be aligned, int
# ref_chain = static chain, to which the other chain is aligned, string
# peer_chain = moving chain, aligned to ref_chain, string

# eg. print_ncs_matrix(0, 1, 250, "A", "B")

############

def print_ncs_matrix(imol, resno_start, resno_end, ref_chain, peer_chain):

	#Make copy in order to superpose        
	imol_copy = copy_molecule(imol)
        clear_lsq_matches()
	#LSQ - reference then moving chain. Use all atoms
        add_lsq_match(resno_start, resno_end, ref_chain, 
                      resno_start, resno_end, peer_chain, 0) 
	#Calculate and export transformation matrix to rtop array        
	rtop = apply_lsq_matches(imol_copy, imol_copy)
	close_molecule(imol_copy) 

	#Separate out rotation and translation arrays, for clarity's sake
	rotation = rtop[0]
	translation = rtop[1]

	#Spit raw matrices to terminal, in un-transposed format
	print "NCS matrix for superposing %s onto %s in the form \
		[m11 m21 m31 m12 m22 m32 m13 m23 m33] [t1 t2 t3], at full precision" \
		%(peer_chain, ref_chain)
	print "%s" %(rtop[0])
	print "%s" %(rtop[1])

	#Open the output text file
	matrix_out_file = open("matrices.txt", "a+")
	
	#Title the output matrix
	print >> matrix_out_file, "#Transposed matrix for sortwater input, superposing %s onto %s"\
		 %(peer_chain, ref_chain)
	#Transposed format
	print >> matrix_out_file, "#Format is m11 m12 m13 m21 m22 m23 m31 m32 m33 t1 t2 t3"
	#SORTWATER input flag, note they are backwards from coot's with the mobile chain first
	print >> matrix_out_file, "NCS %s %s MATRIX" %(peer_chain, ref_chain),
	#Print matrix values, transposed with 6 digits precision, inline. 
	#Will handle translations up to 999.99 Angstroem
	print >> matrix_out_file, "%9.6f %9.6f %9.6f %9.6f %9.6f %9.6f %9.6f %9.6f %9.6f %10.6f %10.6f %10.6f" \
		%(rotation[0], rotation[3], rotation[6], \
		  rotation[1], rotation[4], rotation[7], \
		  rotation[2], rotation[5], rotation[8], \
		  translation[0], translation[1], translation[2])
	matrix_out_file.close()
	
	#Describe what was done
	print "Transformation matrix for chain %s onto %s written to file matrices.txt" %(peer_chain, ref_chain)

#NOTE: DUPLICATE AND EDIT THE FOLLOWING LINE AS NECESSARY TO RUN ALL OF YOUR NCS COMPARISONS
print_ncs_matrix( imol, start_residue, end_residue, "chainid_reference", "chainid_moving")

print "Completed calculating all NCS transformations for SORTWATER input."
print "Copy the contents of matrices.txt into your SORTWATER script"
