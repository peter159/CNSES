# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from .lca import LCA

# columns = "influencer,consumidor_experiencias,comprometido,eco_urbano,tecnologico,amante_contenido,natura,cine,automocion,tecnologia,deportes,futbol,viajes,salud,perros"

# data = pd.read_csv("./racm-data-encoded.csv",
#                    nrows = 100000,
#                    usecols=columns)
# data = data[data.sum(axis=1)!=0]
# data.shape

# generate data
columns = ["C1","C2","C3","C4"]
true_theta = [
    [0.1,0.4,0.9,0.2],
    [0.5,0.9,0.1,0.1],
    [0.9,0.9,0.5,0.9]
]
true_weights = [0.1, 0.5, 0.4]
N = 10000

data = []
for tw,tt in zip(true_weights,true_theta):
    data.append(stats.bernoulli.rvs(p=tt, size=(int(tw*N),len(tt))).tolist())
    
data = np.concatenate(data)
__import__("ipdb").set_trace()  # FIXME BREAKPOINT

# applying lca algorithms
lca = LCA(n_components=5, tol=10e-4, max_iter=1000)
lca.fit(data)
lca.weight

# chart
_,ax = plt.subplots(figsize=(15,5))
ax.plot(lca.ll_[1:], linewidth=3)
ax.set_title("Log-Likelihod")
ax.set_xlabel("iteration")
ax.set_ylabel(r"p(x|$\theta$)")
ax.grid(True)

# plot result
_,axs = plt.subplots(nrows=lca.theta.shape[0], figsize=(15,lca.theta.shape[0]*10))
axs = axs.ravel()
for i,ax in enumerate(axs):
    ax.bar(range(len(columns)),lca.theta[i,:])
    ax.set_xticks(range(len(columns)))
    ax.set_xticklabels(columns, rotation="vertical")
plt.show()

res = lca.predict(data)

lca.bic

# model selection
ks = [2,3,4,5,6]
bics = []
for k in ks:
    lca = LCA(n_components=k, tol=10e-4, max_iter=1000)
    lca.fit(data)
    bics.append(lca.bic)

_,ax = plt.subplots(figsize=(15,5))
ax.plot(ks, bics, linewidth=3)
ax.grid(True)
