import pandas as pd

df = pd.read_csv('gemm-smefficiency-512-todas-conf-gtx780.csv', names=['gx', 'gy', 'gz', 'bx', 'by', 'bz','gpuId', 'smefficiency'])

lista = df.sort_values(by='smefficiency', ascending=True)

lista_linha = []
for index, row in lista.iterrows():
 	lista_linha.append(row)

for i,value1 in enumerate(lista_linha[:-1]):
	linha = value1
	gx = linha[0]
	gy = linha[1]
	gz = linha[2]
	#print "parentes"
	for i, value2 in enumerate(lista_linha[:-1]):
		if (value2[0] == gx) and (value2[1] == gy) and (value2[2] == gz):
			# print gx
			# print gy
			# print gz
			print value2[0]+","+value2[1]+","+value2[2]+","+value2[3]+","+value2[4]+","+value2[5]+","+value2[6]+","+value2[7]
		if (value2[0] == gy) and (value2[1] == gz) and (value2[2] == gx):
			print value2[0]+","+value2[1]+","+value2[2]+","+value2[3]+","+value2[4]+","+value2[5]+","+value2[6]+","+value2[7]
		if (value2[0] == gz) and (value2[1] == gx) and (value2[2] == gy):
			print value2[0]+","+value2[1]+","+value2[2]+","+value2[3]+","+value2[4]+","+value2[5]+","+value2[6]+","+value2[7]

# 	# if(lista_linha[i][7] < lista_linha[i+1][7]):
#  # 		if(lista_linha[i][0] != lista_linha[i+1][0]):
#  # 			gx += 1
#  # 		if(lista_linha[i][1] != lista_linha[i+1][1]):
#  # 			gy += 1
#  # 		if(lista_linha[i][2] != lista_linha[i+1][2]):
#  # 			gz += 1
#  # 		if(lista_linha[i][3] != lista_linha[i+1][3]):
#  # 			bx += 1
#  # 		if(lista_linha[i][4] != lista_linha[i+1][4]):
#  # 			by += 1
#  # 		if(lista_linha[i][5] != lista_linha[i+1][5]):
#  # 			bz += 1

# print("gx: ", gx)
# print("gy: ", gy)
# print("gz: ", gz)
# print("bx: ", bx)
# print("by: ", by)
# print("bz: ", bz)

