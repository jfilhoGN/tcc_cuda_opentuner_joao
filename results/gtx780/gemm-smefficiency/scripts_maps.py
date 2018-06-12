import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as FF
plotly.tools.set_credentials_file(username='jfilhoGN', api_key='rYs9TLQRKfgmXeAaMIDI')

df = pd.read_csv('gemm-smefficiency-64.csv',names=['kernel','gx','gy','gz','bx','by','bz','gpuId','sm_efficiency'])

new_df = df[['gx','gy','gz','bx','by','bz','sm_efficiency']]
new_df['configuration'] = df[['gx','gy','gz','bx','by','bz']].apply(lambda x: ','.join(x), axis=1)
new_df['configuration'] = new_df['configuration'].astype('str')

plt.plot(new_df['sm_efficiency'])
plt.show()


# usando plotly
# trace = go.Scatter(x = new_df['configuration'], y = new_df['gld_efficiency'],
#                   name='Porcentagem da métrica gld_efficiency')
# layout = go.Layout(title='Busca da melhor configuração pela métrica gld_efficiency - GPU - GTX780',
#                    plot_bgcolor='rgb(230, 230,230)', 
#                    showlegend=True)
# fig = go.Figure(data=[trace], layout=layout)

# py.iplot(fig, filename='gld_efficiency-64-sincos-gtx780')



#