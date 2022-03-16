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

grid = 5
df_agg  = []
for ii in range(grid):
    for jj in range(grid):
        wrk         = f'part_{ii}_{jj}/'
        print(wrk)
        data_poat   = np.loadtxt(wrk + 'poat.dat', usecols=1, dtype=np.float)
        data_polg   = np.loadtxt(wrk + 'polg.dat', usecols=1, dtype=np.float)
        data        = np.column_stack((data_poat, data_polg))
        df          = pd.DataFrame(data, columns=['poat', 'polg'])
        df_agg.append(df)
df_agg      = pd.concat(df_agg)
#plt.hist2d(df_agg['polg'], df_agg['poat'], bins=100, density=True, range=[[1.5, 3.5], [1.5, 3.5]], cmap='GnBu')
hst = sns.histplot(data=df_agg, y='poat', x='polg', ax=axs, fill=True, palette='pastel')
hst.set(xlabel=r"$P-O_{lg}$", ylabel=r"$P-O_{att}$")
plt.savefig('cv_hist2d.png', dpi=200, transparent=True)