
# Adam's script to screen for docking locations for symmetric ligands. Adapted and documented from Ralph's iteration. A lot cut out to fit the specifics of the
# dirhodium problem, including allowing binding at both ASP and GLU residues

import sys,os
import math
import pyrosetta
from argparse import ArgumentParser


# Customize this process to the specific geometry case being studied.
def check_alignment(pose, i):

    #angle between the vertical and the vector of two atoms specified here
    angle_error = pyrosetta.rosetta.numeric.angle_degrees(pyrosetta.rosetta.numeric.xyzVector_double_t(0,0,0),
                                                          pyrosetta.rosetta.numeric.xyzVector_double_t(0,0,1),
                                                          pose[i].atom('V1').xyz(),
                                                          pose[i].atom('V2').xyz())
    #I think this is to find the squared distance between two atoms on the XY plane as a proxy for vertical?
    #Oh, it's the distance of each atom from the z-axis.
    distance_error1 = pyrosetta.rosetta.numeric.xyzVector_double_t(0,0,pose[i].atom('V1').xyz().z).distance_squared(pose[i].atom('V1').xyz())
    distance_error2 = pyrosetta.rosetta.numeric.xyzVector_double_t(0,0,pose[i].atom('V2').xyz().z).distance_squared(pose[i].atom('V2').xyz())
    # dihedral1 = pyrosetta.rosetta.numeric.dihedral_degrees(pose[-1].atom('').xyz(),pose[-1].atom('').xyz(),pose[i].atom('').xyz(),pose[i].atom('').xyz())
    # angle1 = pyrosetta.rosetta.numeric.angle_degrees(pose[-1].atom('').xyz(),pose[-1].atom('').xyz(),pose[i].atom('').xyz())
    # chi2 = pyrosetta.rosetta.numeric.dihedral_degrees(pose[i].atom('').xyz(),pose[i].atom('').xyz(),pose[i].atom('').xyz(),pose[i].atom('').xyz())
                                                      
    return angle_error, distance_error1, distance_error2 #, dihedral1, angle1, chi2

    
def main(argv):
    parser = ArgumentParser()
    parser.add_argument('-s',type=str) # Allow for input file to be specified at initialization
    args=parser.parse_args()
    input_pdb=args.s
    pdbfile=str(input_pdb) #duplicated string?
    pdb = os.path.split(str( pdbfile ))[-1]
    pdbname=str((pdb).split('.',)[0])
    print (str(pdbname))

    #initialize pyrosetta. output virtual atoms as they are the hack to centre the ligand params files specific to situation
    pyrosetta.init('-extra_res_fa DRD.params DRE.params -out:file:output_virtual true')

    
    pose = pyrosetta.pose_from_file(input_pdb)
    sf = pyrosetta.get_score_function()
    
    surface_selector = pyrosetta.rosetta.core.select.residue_selector.LayerSelector()
    surface_selector.set_layers(False, False, True)
    surface_residue_indexes = pyrosetta.rosetta.core.select.get_residues_from_subset(surface_selector.apply(pose))
    print(surface_residue_indexes)

    #For both modified amino acids
        #For each surface residue
            #For each rotamer
                
    for h in 'DRD', 'DRE':
        ncaa = h

        print "Residue ", h

        # Iterating all residue position indexes
        for i in surface_residue_indexes:
            pose_clone = pose.clone()
            
            # Mutate to target residue
            pyrosetta.rosetta.protocols.simple_moves.MutateResidue(i, ncaa).apply(pose_clone)
            # Set native rotamers - needed?
            # if ncaa == 'DRD':
            # 	pose_clone.set_chi(1, i, 170.459) # Update for Asp
            # 	pose_clone.set_chi(2, i, -89.397)
            # elif ncaa == 'DRE':
            # 	pose_clone.set_chi(1, i, 170.459) # Update for Glu
            # 	pose_clone.set_chi(2, i, -89.397)
            # 	pose_clone.set_chi(3, i, 180.000)
            
            trm = pyrosetta.rosetta.protocols.protein_interface_design.movers.TryRotamers(resnum=i, scorefxn=sf, explosion=0, jump_num=0, clash_check=True, solo_res=False, include_current=True)
            trm.setup_rotamer_set(pose_clone)
            rotamer_set = trm.rotamer_set()
        	
            #print trm
            #print rotamer_set
            #print(rotamer_set.num_rotamers())
            
            #For every rotamer that doesn't clash
            for j in pyrosetta.rrange(int(rotamer_set.num_rotamers())):
                pose_clone2 = pose_clone.clone()
                pose_clone2.replace_residue(i, rotamer_set.rotamer(j), True)
                
                angle_error, distance_error1, distance_error2 = check_alignment(pose_clone2, i) # ,dihedral1,angle1,chi2
                if (angle_error < 4 or angle_error > 176) and distance_error1 < 0.5 and distance_error2 < 0.5: #and abs(dihedral1)>30 and abs(dihedral1)<120 and angle1>90 and angle1<125 and abs(chi2)>45:
                    #print "Hit found!"
                    hitlist = open("output/hitlist.txt", "a")
                    print >>hitlist, str(pdbname) + " residue " + str(i) + " rotamer " + str(j) + " of " + str(h)
                    hitlist.close()

                    #print "pdb " + str(pdbname) + " residue " + str(i) + " rotamer " + str(j) + " supports residue " + str(h) + " in the appropriate position"

                    pose_clone3 = pose_clone2.clone()
                    sfsm_c4 = pyrosetta.rosetta.protocols.simple_moves.symmetry.SetupForSymmetryMover('./C4_Z.sym')
                    sfsm_c4.apply(pose_clone3)
               
               # export a pdb file of the symmetric molecule
                    pose_clone3.dump_pdb('output/' + str(pdbname) + '_' + str(h) + '_' + str(i) + '_' + str(j) + '.pdb')

# Run main                
if __name__ == '__main__':
    main(sys.argv)
