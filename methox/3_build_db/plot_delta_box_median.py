import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

plt.rcParams.update({'font.sans-serif'  : 'Helvatica',
                    'font.family'       : "sans-serif",
                    'font.size'         : 12,
                    'font.weight'       : 'regular',
                    'xtick.labelsize'   : 12,
                    'ytick.labelsize'   : 10,
                    'axes.labelsize'    : 12,
                    'axes.linewidth'    : 1.5,
                    'legend.fontsize'   : 10,
                    'legend.loc'        : 'upper right'})

#-- constants --
num_solute_atoms    = 14
num_parts           = 11
num_frame_per_calc  = 500
data_base   = '/projectnb/cui-buchem/tanmoy/projects/ML_delta/methox/2_ad_map_sol/'


def load_energies(filename):
    energies = []
    for ii in range(num_parts):
        for jj in range(num_parts):
            wrk         = data_base + f'part_{ii}_{jj}/'
            energy = np.loadtxt(wrk + filename, dtype=np.float32)
            energies.append(energy)
    energies = np.array(energies)
    print("energies.shape:\t\t", energies.shape)
    return energies

def process_energies(en_high, en_low):
    high_min_idx    = np.argmin(en_high)
    en_dic      = {"base_high" : en_high[high_min_idx].astype(float), "base_low" : en_low[high_min_idx].astype(float)}
    en_hm       = en_high - en_high[high_min_idx]
    en_lm       = en_low  - en_low[high_min_idx]
    en_delta    = en_hm   - en_lm
    return en_delta

en_dft      = load_energies('en_dft.dat').reshape(num_parts * num_parts * num_frame_per_calc)
en_dftb     = load_energies('en_dftb.dat').reshape(num_parts * num_parts * num_frame_per_calc)
assert len(en_dft) == len(en_dftb), f"length of DFT energies: {len(en_dft)}, length of DFTB energies: {len(en_dftb)}\n"
en_delta    = process_energies(en_dft, en_dftb)
en_delta    = en_delta.reshape(num_parts * num_parts, num_frame_per_calc)
en_medians  = [np.median(en_delta[i]) for i in range(len(en_delta))]
en_medians_ascending_idx    = np.argsort(en_medians)
print(en_medians_ascending_idx)
en_delta_sorted = en_delta[en_medians_ascending_idx]

dfs = []
for ii in range(len(en_delta_sorted)):
    dic = {}
    dic['idx'] = str(ii)
    dic['energy'] = en_delta_sorted[ii] - np.median(en_delta_sorted[ii])
    dfs.append(pd.DataFrame(dic))

df = pd.concat(dfs)
print(df)

fig, axs = plt.subplots(1,1,figsize=(4, 9))
plt.xlim(-40,40)
#plt.title(" ")
bpl = sns.boxplot(data=df, ax=axs, x='energy', y='idx', linewidth=0.7, color='limegreen')
bpl.set(xlabel=r"$\Delta E \:(median\: subtracted)\: (kcal/mol)$")
axs.axes.yaxis.set_visible(False)
plt.savefig('box_delta_median.png', dpi=200, transparent=True)
plt.clf()
