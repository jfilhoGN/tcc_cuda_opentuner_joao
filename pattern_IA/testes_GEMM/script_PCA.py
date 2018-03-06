# -*- coding: utf-8 -*-
import numpy as np
#import seaborn.apionly as seaborn
import matplotlib.pyplot as plt
from pandas import read_csv
from sklearn.decomposition import PCA
from pandas import DataFrame

df = read_csv('./gemm-smefficiency/gemm-smefficiency-512.csv', index_col='smefficiency')

def z_score(x):
    """Remove a média e normaliza os pelo desvio padrão"""
    #print((x - x.mean()) / x.std())
    return (x - x.mean()) / x.std()

pca = PCA(n_components=None)
pca.fit(df.apply(z_score).T)
loadings = DataFrame(pca.components_.T)
loadings.index = ['PC %s' % pc for pc in loadings.index + 1]
loadings.columns = ['TS %s' % pc for pc in loadings.columns + 1]
print(loadings)
PCs = np.dot(loadings.values.T, df)
marker = dict(linestyle='none', marker='o', markersize=7, color='blue', alpha=0.5)

fig, ax = plt.subplots(figsize=(7, 2.75))
ax.plot(PCs[0], np.zeros_like(PCs[0]),
        label="Scores", **marker)
[ax.text(x, y, t) for x, y, t in zip(PCs[0], loadings.values[1, :], df.columns)]

ax.set_xlabel("PC1")

_ = ax.set_ylim(-1, 1)
marker = dict(linestyle='none', marker='o', markersize=7, color='blue', alpha=0.5)

#ax = seaborn.corrplot(df, annot=True, diag_names=False)

fig, ax = plt.subplots(figsize=(7, 2.75))
ax.plot(PCs[0], PCs[1], label="Scores", **marker)

ax.set_xlabel("PC1")
ax.set_ylabel("PC2")

text = [ax.text(x, y, t) for x, y, t in
        zip(PCs[0], PCs[1]+0.5, df.columns)]

perc = pca.explained_variance_ratio_ * 100

perc = DataFrame(perc, columns=['Percentage explained ratio'], index=['PC %s' % pc for pc in np.arange(len(perc)) + 1])
ax = perc.plot(kind='bar')


TS1 = loadings['TS 1']
TS1.index = df.index
ax = TS1.plot(kind='bar')


marker = dict(linestyle='none', marker='o', markersize=7, color='blue', alpha=0.5)

fig, ax = plt.subplots(figsize=(7, 7))
ax.plot(loadings.iloc[0], loadings.iloc[1], label="Loadings", **marker)
ax.set_xlabel("non-projected PC1")
ax.set_ylabel("non-projected PC2")
ax.axis([-1, 1, -1, 1])
text = [ax.text(x, y, t) for
        x, y, t in zip(loadings.iloc[0], loadings.iloc[1], df.index)]
