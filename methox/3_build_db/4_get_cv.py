import plotly.graph_objects as go
import numpy as np
from schnetpack.data import AtomsData


available_properties = ['energy', 'forces']
data        = AtomsData('methox_oxy.db', available_properties=available_properties, subset=None, load_only=['energy'])
frames      = [data.get_atoms(i) for i in range(len(data))]

#energies    = [data.get_properties(i)[1]['energy'].item() for i in range(len(data))]

poat = []
polg = []
for frame in frames:
    xpoat = frame.get_distance(0,4)
    xpolg = frame.get_distance(0,9)
    poat.append(xpoat)
    polg.append(xpolg)

poat = np.array(poat)
polg = np.array(polg)
cv   = np.column_stack((polg, poat))
np.savetxt('cv.dat', cv)