import pandas as pd

df = pd.read_csv('gemm-smefficiency-512-todas-conf-gtx780.csv', names=['gx', 'gy', 'gz', 'bx', 'by', 'bz','gpuId', 'smefficiency'])

#criei um subset
df1 = df[(df['smefficiency'] >= '98')]
lista = df1.sort_values(by='smefficiency', ascending=True)

print lista
lista_linha = []
for index, row in lista.iterrows():
	lista_linha.append(row)

gx = 0
gy = 0
gz = 0
bx = 0
by = 0
bz = 0
for i,value in enumerate(lista_linha[:-1]):
	if(lista_linha[i][7] < lista_linha[i+1][7]):
 		if(lista_linha[i][0] != lista_linha[i+1][0]):
 			gx += 1
 		if(lista_linha[i][1] != lista_linha[i+1][1]):
 			gy += 1
 		if(lista_linha[i][2] != lista_linha[i+1][2]):
 			gz += 1
 		if(lista_linha[i][3] != lista_linha[i+1][3]):
 			bx += 1
 		if(lista_linha[i][4] != lista_linha[i+1][4]):
 			by += 1
 		if(lista_linha[i][5] != lista_linha[i+1][5]):
 			bz += 1

print("gx: ", gx)
print("gy: ", gy)
print("gz: ", gz)
print("bx: ", bx)
print("by: ", by)
print("bz: ", bz)

