import pandas as pd
import numpy as np

df = pd.read_csv('sincos-ipc-320.csv',names=['kernel','gx','gy','gz','bx','by','bz','gpuId','ipc'])
resultado = df.sort_values("ipc",ascending=True)
print(resultado)
	