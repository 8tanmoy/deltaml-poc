import os
from pathlib import Path
from matplotlib.colors import Colormap
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import numpy as np
import pickle
from ase.units import kcal, mol
from ase.io import read, write
import schnetpack as spk
from schnetpack import AtomsData
import sys
import json

from torch import float32

# constants
num_solute_atoms    = 14
num_parts           = 11
num_frame_per_calc  = 500
fixed_atom_index    = 0

data_base   = '/projectnb/cui-buchem/tanmoy/projects/ML_delta/methox/2_ad_map_sol/'

#-- go through pdbs and get num_waters --
num_atoms   = []
f_dft       = []
f_dftb      = []
for ii in range(num_parts):
    for jj in range(num_parts):
        wrk             = data_base + f'part_{ii}_{jj}/'
        print(wrk)
        f_dft_part      = np.loadtxt(wrk + f'forces_dft.dat', dtype=np.float32)
        f_dftb_part     = np.loadtxt(wrk + f'forces_dftb.dat', dtype=np.float32)
        count           = 0
        num_atoms_part  = []
        for kk in range(num_frame_per_calc):
            frame   = read(wrk + f'frames/frame_{kk}.pdb', parallel=True)
            natoms  = len(frame)
            beg     = count
            count   = count + natoms
            temp_dft = np.array([f_dft_part[beg:count]])
            temp_dftb = np.array([f_dftb_part[beg:count]])
            f_dft.append(temp_dft)
            f_dftb.append(temp_dftb)
            num_atoms_part.append(natoms)
        min_part    = min(num_atoms_part)
        num_atoms.append(min_part)
    #print(count)
min_num_atoms   = min(num_atoms)
print("expected forces length:\t\t", num_frame_per_calc * num_parts * num_parts)
print("dft forces length:\t\t", len(f_dft))
print("dftb forces length:\t\t", len(f_dftb))

#print('dft forces shape:\t\t', f_dft.shape)
#print('dftb forces shape:\t\t', f_dftb.shape)

#-- write forces pickle --
with open('forces_dft.pkl','wb') as ffile_dft:
    pickle.dump(f_dft, ffile_dft)

with open('forces_dftb.pkl','wb') as ffile_dftb:
    pickle.dump(f_dftb, ffile_dftb)

#-- write results -- 
log_dict    = {'min_num_atoms' : min_num_atoms,
    'min_num_waters' : (min_num_atoms - num_solute_atoms)/3}
json_string = json.dumps(log_dict, indent=4)
print(json_string)
with open('1_scan_structures.json','w') as logfile:
    logfile.write(json_string)
