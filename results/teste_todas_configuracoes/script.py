import pandas as pd
import numpy as np

df = pd.read_csv('gemm-smefficiency-512.csv',names=['kernel','gx','gy','gz','bx','by','bz','gpuId','sm_efficiency'])
resultado = df.sort_values("sm_efficiency",ascending=True)
print(resultado)
	