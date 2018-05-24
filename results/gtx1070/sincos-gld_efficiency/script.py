import pandas as pd
import numpy as np

df = pd.read_csv('sincos-smefficiency-executed-352.csv',names=['kernel','gx','gy','gz','bx','by','bz','gpuId','sm_eficiency'])
resultado = df.sort_values("sm_eficiency",ascending=True)
print(resultado)
	