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
df_agg  = []
for ii in range(grid):
    for jj in range(grid):
        wrk         = f'part_{ii}_{jj}/'
        print(wrk)
        data_poat   = np.loadtxt(wrk + 'poat.dat', usecols=1, dtype=np.float)
        data_polg   = np.loadtxt(wrk + 'polg.dat', usecols=1, dtype=np.float)
        data        = np.column_stack((data_poat, data_polg))
        df          = pd.DataFrame(data, columns=['poat', 'polg'])
        df_sampled  = df.sample(frac=1.0)
        #kde         = sns.kdeplot(data=df_sampled, y='poat', x='polg', ax=axs, fill=True, cbar=False, color='teal', levels=4, alpha=0.75)
        df_agg.append(df_sampled)
df_agg      = pd.concat(df_agg)
print(df_agg.info)
kde         = sns.kdeplot(data=df_agg, y='poat', x='polg', ax=axs, fill=True, cbar=False, color='teal', levels=4, alpha=0.75)
kde.set(xlabel=r"$P-O_{lg}$", ylabel=r"$P-O_{att}$")
plt.savefig('cv_kde.png', dpi=200, transparent=True)