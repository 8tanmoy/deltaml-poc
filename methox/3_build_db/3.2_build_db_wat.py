import os
from pathlib import Path
from matplotlib.colors import Colormap
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import numpy as np
import pickle
import sys
import json

from ase.units import kcal, mol
from ase.io import read, write
from ase.db import connect

import schnetpack as spk
from schnetpack import AtomsData


#-- constants --
num_solute_atoms    = 14
num_parts           = 11
num_frame_per_calc  = 500

data_base   = '/projectnb/cui-buchem/tanmoy/projects/ML_delta/methox/2_ad_map_sol/'

#-- read json output from before --
with open('1_scan_structures.json', 'r') as json_file:
    read_dict   = json.load(json_file)
    print("reading saved json from 1_scan_structures\n", read_dict)
min_num_atoms   = int(read_dict['min_num_atoms'])
min_num_waters  = int(read_dict['min_num_waters'])

def load_energies(filename):
    energies = []
    for ii in range(num_parts):
        for jj in range(num_parts):
            wrk         = data_base + f'part_{ii}_{jj}/'
            energy = np.loadtxt(wrk + filename, dtype=np.float32)
            #print(energy.shape)
            energies.append(energy)
    energies = np.array(energies)
    print("energies.shape:\t\t", energies.shape)
    return energies

def process_energies(en_high, en_low):
    high_min_idx    = np.argmin(en_high)
    en_dic      = {"base_high" : en_high[high_min_idx].astype(float), "base_low" : en_low[high_min_idx].astype(float)}
    en_hm       = en_high - en_high[high_min_idx]
    en_lm       = en_low  - en_low[high_min_idx]
    en_delta    = en_hm   - en_lm
    json_string = json.dumps(en_dic)
    with open('3_build_db.json','w') as logfile:
        logfile.write(json_string)
    return en_delta

def load_forces(fpath):
    with open(fpath, "rb") as file:
        forces = pickle.load(file)
    return forces

def process_forces(f_high, f_low):
    f_delta = f_high - f_low
    return f_delta

def load_frames(fpath):
    frames = read(fpath, index=":")
    return frames

if __name__ == '__main__':
    en_dft      = load_energies('en_dft.dat').reshape(num_parts * num_parts * num_frame_per_calc)
    en_dftb     = load_energies('en_dftb.dat').reshape(num_parts * num_parts * num_frame_per_calc)
    assert len(en_dft) == len(en_dftb), f"length of DFT energies: {len(en_dft)}, length of DFTB energies: {len(en_dftb)}\n"
    en_delta    = process_energies(en_dft, en_dftb)

    #-- make sure en_delta is in good range --
    good_en_delta_idx   = [idx for idx in range(len(en_delta)) if (en_delta[idx] > -40.0 and en_delta[idx] < 60.0)]
    en_delta_good       = en_delta[good_en_delta_idx]
    np.savetxt('en_delta.dat', en_delta_good)

    include_type        = 'wat'
    forces_high_name    = 'forces_dft_' + include_type + '.pkl'
    forces_low_name     = 'forces_dftb_' + include_type + '.pkl'
    forces_dft          = load_forces(forces_high_name)
    forces_dftb         = load_forces(forces_low_name)
    assert len(forces_dft) == len(forces_dftb), f"length of DFT energies: {len(forces_dft)}, length of DFTB energies: {len(forces_dftb)}\n"
    forces_delta        = process_forces(forces_dft, forces_dftb)
    forces_delta_good   = forces_delta[good_en_delta_idx]

    frames              = load_frames('frames_'+ include_type +'.db')
    frames_good         = [frames[kk] for kk in good_en_delta_idx]

    #-- build db for SchNetPack
    dbname		= 'methox_'+ include_type +'.db'

    if Path(dbname).is_file():
        Path(dbname).unlink()

    property_list = []
    for ii in range(len(frames_good)):
        property_list.append(
            {
                'energy' :  np.array([en_delta_good[ii]]),
                'forces' :  np.array(forces_delta_good[ii])
            }
        )
    print('len property list', len(property_list))
    new_dataset = AtomsData(dbname, available_properties=['energy', 'forces'])
    new_dataset.add_systems(frames_good, property_list)
    print('Available properties:')
    for p in new_dataset.available_properties:
        print('-', p)
    print(new_dataset.get_properties(0))