import pandas as pd
import numpy as np

df = pd.read_csv('sincos-smefficiency-320-todas-conf-funcid-titanx-kerrnel.csv',names=['kernel','gx','gy','gz','bx','by','bz','funcId','smefficiency'])
resultado = df.sort_values("smefficiency",ascending=True)
print(resultado)
	