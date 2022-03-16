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


def trim_frames_forces(frame, trim_to : int):
    '''
    trims frames and forces to desired number of atoms
    frame : ase.atoms object
    trim_to : integer
    '''
    center_atom_index   = 0
    center_atom_symbol  = 'P'
    #print("center atom is: ", frame[center_atom_index].symbol)
    assert frame[center_atom_index].symbol == center_atom_symbol, 'center atom does not match'
    natoms                  = len(frame)
    solute_atoms_idx        = list(range(num_solute_atoms))
    solvent_atoms_idx       = list(range(num_solute_atoms,natoms))

    #-- get the indices of first --
    solvent_oxygens_idx     = [atom.index for atom in frame if ((atom.symbol == 'O') and (atom.index in solvent_atoms_idx))]
    solvent_oxygens_dist    = frame.get_distances(center_atom_index, solvent_oxygens_idx)
    zip_idx_dist            = np.column_stack([solvent_oxygens_idx, solvent_oxygens_dist])
    zip_min_dist            = zip_idx_dist[zip_idx_dist[:,1].argsort()][:trim_to]
    
    #-- get only oxygen indices --
    nearest_oxygens_idx     = np.sort(zip_min_dist[:,0].astype(int)).tolist()

    #-- get whole water indices --
    nearest_waters_idx      = []
    for oxy in nearest_oxygens_idx:
        nearest_waters_idx.append(oxy)
        nearest_waters_idx.append(oxy + 1)
        nearest_waters_idx.append(oxy + 2)

    #print("nearest oxygen indices\n", nearest_oxygens_idx)
    #print("nearest waters indices\n", nearest_waters_idx)

    #-- finally slice the frame --
    idx_solute_oxygens      = solute_atoms_idx + nearest_oxygens_idx
    idx_solute_waters       = solute_atoms_idx + nearest_waters_idx

    return idx_solute_oxygens, idx_solute_waters

def load_forces(fpath):
    with open(fpath, "rb") as file:
        forces = pickle.load(file)
    return forces

def write_frames_db(frames, name):
    if Path(name).is_file():
        Path(name).unlink()
    with connect(name, type='db') as db:
        for frame in frames:
            db.write(frame)
    return

def write_pickle(forces, name):
    if Path(name).is_file():
        Path(name).unlink()
    with open(name, "wb") as fpickle:
        pickle.dump(forces, fpickle)
    return

if __name__ == '__main__':
    forces_dft  = load_forces('forces_dft.pkl')     #shape nframes x (1, natoms, 3)
    forces_dftb = load_forces('forces_dftb.pkl')    #shape nframes x (1, natoms, 3)
    assert len(forces_dft) == len(forces_dftb), "forces dft dftb unequal length"

    trimmed_forces_dft_oxy  = []
    trimmed_forces_dftb_oxy = []
    trimmed_forces_dft_wat  = []
    trimmed_forces_dftb_wat = []
    frames_oxy  = []
    frames_wat  = []

    count   = 0
    for ii in range(num_parts):
        for jj in range(num_parts):
            wrk         = data_base + f'part_{ii}_{jj}/frames/'
            print(wrk)
            for kk in range(num_frame_per_calc):
                frame           = read(wrk + f'frame_{kk}.pdb', parallel=True)
                f_dft_temp      = forces_dft[count][0]
                f_dftb_temp     = forces_dftb[count][0]

                assert len(frame) == len(f_dft_temp) == len(f_dftb_temp), f"coordinate and force length mismatch\
                    {len(frame)}, {f_dft_temp.shape}, {f_dftb_temp.shape}"

                idx_solute_oxygens, idx_solute_waters   = trim_frames_forces(frame, min_num_waters)

                trimmed_frame_oxy       = frame[idx_solute_oxygens]
                trimmed_frame_wat       = frame[idx_solute_waters]
                frames_oxy.append(trimmed_frame_oxy)
                frames_wat.append(trimmed_frame_wat)

                temp_forces_dft_oxy  = f_dft_temp[idx_solute_oxygens]
                temp_forces_dftb_oxy = f_dftb_temp[idx_solute_oxygens]
                temp_forces_dft_wat  = f_dft_temp[idx_solute_waters]
                temp_forces_dftb_wat = f_dftb_temp[idx_solute_waters]

                trimmed_forces_dft_oxy.append(  temp_forces_dft_oxy )
                trimmed_forces_dftb_oxy.append( temp_forces_dftb_oxy)
                trimmed_forces_dft_wat.append(  temp_forces_dft_wat )
                trimmed_forces_dftb_wat.append( temp_forces_dftb_wat)

                count += 1
    trimmed_forces_dft_oxy  = np.array(trimmed_forces_dft_oxy )
    trimmed_forces_dftb_oxy = np.array(trimmed_forces_dftb_oxy)
    trimmed_forces_dft_wat  = np.array(trimmed_forces_dft_wat )
    trimmed_forces_dftb_wat = np.array(trimmed_forces_dftb_wat)

    '''
    print(trimmed_forces_dft_oxy.shape)
    print(trimmed_forces_dftb_oxy.shape)
    print(trimmed_forces_dft_wat.shape)
    print(trimmed_forces_dftb_wat.shape)
    '''

    #-- write database for trimmed frames --
    print("hello", len(frames_oxy))
    write_frames_db(frames_oxy, 'frames_oxy.db')
    write_frames_db(frames_wat, 'frames_wat.db')

    #-- write pickles for forces --
    write_pickle(trimmed_forces_dft_oxy  , 'forces_dft_oxy.pkl')
    write_pickle(trimmed_forces_dftb_oxy , 'forces_dftb_oxy.pkl')
    write_pickle(trimmed_forces_dft_wat  , 'forces_dft_wat.pkl')
    write_pickle(trimmed_forces_dftb_wat , 'forces_dftb_wat.pkl')
