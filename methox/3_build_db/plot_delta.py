import plotly.graph_objects as go
import numpy as np
from schnetpack.data import AtomsData


import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
plt.rcParams.update({'font.sans-serif'  : 'Helvatica',
                    'font.family'       : "sans-serif",
                    'font.size'         : 14,
                    'font.weight'       : 'regular',
                    'xtick.labelsize'   : 10,
                    'ytick.labelsize'   : 10,
                    'axes.labelsize'    : 10,
                    'axes.linewidth'    : 1.5,
                    'legend.fontsize'   : 11,
                    'legend.loc'        : 'upper right'})

energy      = np.loadtxt('en_delta.dat', dtype=np.float)
cv          = np.loadtxt('cv.dat', dtype=float)
print(len(energy))
print(len(cv))
polg        = cv[:,0]
poat        = cv[:,1]
df          = pd.DataFrame({'poat' : poat, 'polg' : polg, 'energy' : energy})

fig, axs = plt.subplots(1,1,figsize=(5.5, 5))
plt.title(" ")
sns.histplot(data=df, x='energy', color='orange', ax=axs, kde=True)
plt.xlabel(r"$\Delta E$")
plt.savefig('hist_energies.png', dpi=200, transparent=True)
plt.clf()


