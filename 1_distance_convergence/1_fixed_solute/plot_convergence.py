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

list1 = []
list2 = []
dist  = []
mean  = []
fig, axs = plt.subplots(2, 1,figsize=(6, 8))
for ii in range(5,70,1):
    print(ii)
    file_dft    = f"part_{ii}/en_dft_70.dat"
    file_dftb   = f"part_{ii}/en_dftb_70.dat"
    diff        = np.loadtxt(file_dft, dtype=np.float32) - np.loadtxt(file_dftb, dtype=np.float32)
    list1 = np.append(list1, np.repeat(ii * 0.2, len(diff)))
    list2 = np.append(list2, diff)
    dist.append(ii * 0.2)
    mean.append(np.mean(diff))
    
print(list1.shape, list2.shape)
dic = {'idx' : list1, 'delta' : list2}
df  = pd.DataFrame.from_dict(dic)
print(df)

#-- set delta at lowest distance to be the baseline --
baseline = df['delta'].iloc[0]
print(f'baseline {baseline}')
df['delta'] = df['delta'] - baseline

axs[0].set_title(r"QM/MM DFT(B3LYP/aug-cc-pVDZ), DFTB(3OB))]", fontsize=14)
ax_bar = sns.boxplot(x='idx', y='delta', data=df, ax=axs[0])
ax_bar.set(xlabel=r"$R_{cutoff}(\AA)$", xticklabels=[], ylabel=r"$\Delta E(kcal/mol)$")

axs[1].hlines(y=0.0, xmin=min(dist), xmax=max(dist), color='grey')
axs[1].plot(dist ,mean - mean[0], color='orange')
axs[1].scatter(dist ,mean - mean[0], color='red', s=20)
axs[1].set_xlabel(r"$R_{cutoff}(\AA)$")
axs[1].set_ylabel(r"$\Delta E (kcal/mol)$")
plt.tight_layout()
plt.savefig('convergence.png', dpi=200)