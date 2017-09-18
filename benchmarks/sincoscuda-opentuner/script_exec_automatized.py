#!/usr/bin/env python
import os

lista_ns = [96,128,160,192,224,256,288,320,352]
for i in lista_ns:
	print(i)
	os.system('python sincoscuda.py --n '+str(i))