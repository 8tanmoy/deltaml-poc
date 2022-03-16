from cv2 import rotate
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import sys

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

def collate_energy(fname) -> pd.DataFrame:
    df_en   = []
    for ii in range(5, 65, 1):
        print(ii)
        file_frag   = f"part_{ii}/{fname}"
        en_frag     = np.loadtxt(file_frag, dtype=np.float32)
        df_en.append(pd.DataFrame({'r': 0.2 * ii, 'energy': en_frag}))
    df_en = pd.concat(df_en)
    return df_en

df_dft  = collate_energy('en_dft_70.dat')
df_dftb = collate_energy('en_dftb_70.dat')

ref_idx = 0
df_dft['energy'] = df_dft['energy'] - df_dft['energy'].iloc[ref_idx]
df_dftb['energy'] = df_dftb['energy'] - df_dftb['energy'].iloc[ref_idx]
delta_ref = df_dft['energy'].iloc[ref_idx] - df_dftb['energy'].iloc[ref_idx]
df_delta = pd.DataFrame()
df_delta['r'] = df_dft['r']
df_delta['energy'] = df_dft['energy'] - df_dftb['energy']
print(df_delta)

fig, axs = plt.subplots(2,1,figsize=(6, 8))

axs[0].set_title(r"QM/MM DFT(B3LYP/aug-cc-pVDZ), DFTB(3OB))]", fontsize=14)
ax_bar = sns.boxplot(x='r', y='energy', data=df_delta, ax=axs[0])
ax_bar.set(xlabel=r"$R_{cutoff}(\AA)$", xticklabels=[], ylabel=r"$\Delta E(kcal/mol)$")

df_mean = df_delta.groupby('r').mean().reset_index()
print(df_mean)
axs[1].hlines(y=delta_ref, xmin=np.min(df_mean['r']), xmax=np.max(df_mean['r']), color='grey')
axs[1].plot(df_mean['r'] ,df_mean['energy'], color='orange')
axs[1].scatter(df_mean['r'] ,df_mean['energy'] , color='red', s=20)
axs[1].set_xlabel(r"$R_{cutoff}(\AA)$")
axs[1].set_ylabel(r"$\Delta E (kcal/mol)$")
plt.tight_layout()
plt.savefig('convergence.png', dpi=200)