import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as FF
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
#plotly.tools.set_credentials_file(username='jfilhoGN', api_key='rYs9TLQRKfgmXeAaMIDI')

df = pd.read_csv('gemm-gld_efficiency-160.csv',names=['kernel','gx','gy','gz','bx','by','bz','gpuId','gld_efficiency'])
#resultado = df.sort_values("sm_efficiency",ascending=True)
#print(resultado)

new_df = df[['gx','gy','gz','bx','by','bz','gld_efficiency']]
new_df['configuration'] = df[['gx','gy','gz','bx','by','bz']].apply(lambda x: ','.join(x), axis=1)
new_df['configuration'] = new_df['configuration'].astype('str')

# plt.plot(new_df['gld_efficiency'])
# plt.show()

trace = go.Scatter(x = new_df['configuration'],y = new_df['gld_efficiency'],
                  name='Porcentagem da métrica gld_efficiency', mode='markers')
layout = go.Layout(showlegend=True)
fig = go.Figure(data=[trace], layout=layout)

plot(fig, filename='gld-gemm-titan-160', image='png')
