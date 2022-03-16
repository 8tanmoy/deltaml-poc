import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from schnetpack.data import AtomsData


import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

energy      = np.loadtxt('en_delta.dat', dtype=np.float)
cv          = np.loadtxt('cv.dat', dtype=float)
print(len(energy))
print(len(cv))
polg        = cv[:,0]
poat        = cv[:,1]
df          = pd.DataFrame({'poat' : poat, 'polg' : polg, 'energy' : energy})

fig         = px.scatter_3d(df, x='polg', y='poat', z='energy', color='energy', 
    labels={'polg' : 'P-Olg', 'poat' : 'P-Oatt', 'energy' : "dE (kcal/mol)"})
fig.update_layout()
fig.write_html('3dscatter_cv_delta.html')