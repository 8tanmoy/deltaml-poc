import plotly.graph_objects as go
import numpy as np
from schnetpack.data import AtomsData


import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
plt.rcParams.update({'font.sans-serif'  : 'Helvatica',
                    'font.family'       : "sans-serif",
                    'font.size'         : 12,
                    'font.weight'       : 'regular',
                    'xtick.labelsize'   : 12,
                    'ytick.labelsize'   : 12,
                    'axes.labelsize'    : 12,
                    'axes.linewidth'    : 1.5,
                    'legend.fontsize'   : 10,
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
sns.scatterplot(data=df, x='polg', y='poat', hue='energy', hue_norm=(-40,40), palette='Spectral', s=4)
plt.xlabel(r"$P-O_{lg} (\AA)$")
plt.ylabel(r"$P-O_{att} (\AA)$")
plt.legend(bbox_to_anchor=(0.95, 1), loc='upper left', borderaxespad=0)
plt.savefig('scatter_cv_delta.png', dpi=200, transparent=True)
plt.clf()


