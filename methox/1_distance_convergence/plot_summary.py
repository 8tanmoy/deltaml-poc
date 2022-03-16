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


experiment_names    = ['1_fixed_solute', '2_flexible_solute', '3_free_solute'] #, '4_very_free_solute']
legend_names        = {'1_fixed_solute' : 'frozen solute', 
    '2_flexible_solute' : 'umbrella on at Hill',
    '3_free_solute' : 'umbrella off',
    '4_very_free_solute' : 'umbrella off | dihedral off'}

#plt.ylim(-2.5, 2.5)
plt.title(" ")
for experiment in experiment_names:
    df  = pd.read_csv(os.path.join(experiment, 'convergence.csv'), header=0)
    sns.lineplot(data=df, x='r', y='energy', label=legend_names[experiment])
plt.ylabel(r"$\Delta E$ (kcal/mol)")
plt.xlabel(r"r ($\AA$)")
plt.legend(loc='center right')
plt.tight_layout()
plt.savefig('convergence_summary.png', dpi=200, transparent=True)

plt.clf()
fig, axs = plt.subplots(1,1,figsize=(5.5, 5))
for experiment in experiment_names:
    df  = pd.read_csv(os.path.join(experiment, 'convergence.csv'), header=0)
    df_at12 = df[df['r']==12.0]
    sns.kdeplot(data=df_at12, x='energy', label=legend_names[experiment], ax=axs, shade=True)
plt.title(r"$r=12\AA$ from P")
plt.ylabel(r"Probability")
plt.xlabel(r"$\Delta E$ (kcal/mol)")
plt.tight_layout()
plt.legend(loc='upper right')
plt.savefig('delta_at12A.png', dpi=200, transparent=True)
