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

# constants
natoms = 9
nframes = 140 * 50

wrk = '/projectnb/cui-buchem/tanmoy/projects/ML/ad_map_malon/md_sol/'
en_file_dftb = wrk + 'dftb/' + 'en_dftb.dat'
f_file_dftb = wrk + 'dftb/' + 'f_dftb.dat'
en_file_dft = wrk + 'dft/' + 'en_dft.dat'
f_file_dft = wrk + 'dft/' + 'f_dft.dat'
traj_file = wrk + 'md_frames.pdb'

#-- load structures --
frames      = read(traj_file, index=':')
nframes = len(frames)
print('nframes=', nframes)

en_dftb = np.loadtxt(en_file_dftb)
cv  = np.arange(-3.5, 3.5, 0.05)

en_l = en_dftb[:nframes]

en_dft = np.loadtxt(en_file_dft)
en_h = en_dft[:nframes]

print("en_l.shape = ", en_l.shape)
print("en_h.shape = ", en_h.shape)

#h_min   = np.argmin(en_h)
h_min   = 3995
en_hm    = en_h - en_h[h_min]
en_lm    = en_l - en_l[h_min]

endata  = en_hm - en_lm

f_h = np.loadtxt(f_file_dft)
f_h = f_h.reshape(nframes, natoms, 3)

f_l = np.loadtxt(f_file_dftb)
f_l = f_l.reshape(nframes, natoms, 3)

print(f_h.shape)
print(f_l.shape)

fdata = -(f_h - f_l)

property_list = []

for ii in range(nframes):
    property_list.append(
        {
            'energy' :  np.array([endata[ii]]),
            'forces' :  np.array(fdata[ii])
        }
    )
print('len property list', len(property_list))
#----
dbname		= 'admap_md_malon.db'
if Path(dbname).is_file():
    Path(dbname).unlink()
#----
print('making new db')
new_dataset = AtomsData(dbname, available_properties=['energy', 'forces'])
print('adding systems')
new_dataset.add_systems(frames, property_list)
#---- non-essential ----
print('Available properties:')
for p in new_dataset.available_properties:
    print('-', p)
#-----
print(new_dataset.get_properties(0))
