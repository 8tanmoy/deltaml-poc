from cProfile import label
from turtle import position
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import sys
import os

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
fig, axs = plt.subplots(1,1,figsize=(5.5, 5))
plt.title(" ")
sns.set_palette("pastel")
plt.xlim(1.5, 3.5)
plt.ylim(1.5, 3.5)

grid = 11
for ii in range(grid):
    for jj in range(grid):
        wrk         = f'part_{ii}_{jj}/'
        print(wrk)
        data_poat   = np.loadtxt(wrk + 'poat.dat', usecols=1, dtype=np.float)
        data_polg   = np.loadtxt(wrk + 'polg.dat', usecols=1, dtype=np.float)
        data        = np.column_stack((data_poat, data_polg))
        df          = pd.DataFrame(data, columns=['poat', 'polg'])
        #df_sampled  = df.sample(frac=0.2)
        plt.scatter(df['polg'], df['poat'], alpha=1, color='teal', marker='s', s=4)
plt.xlabel(r"$P-O_{lg}$")
plt.ylabel(r"$P-O_{att}$")
plt.savefig('cv_scatter.png', dpi=200, transparent=True)