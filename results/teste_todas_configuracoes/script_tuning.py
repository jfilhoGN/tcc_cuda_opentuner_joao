#!/usr/bin/env python
import os
import subprocess
import re

def read_file_configs():
	#testar tambem com 512
	file_gemm = open('./configuracoes/saida-gemm-1024.txt','r')
	list_configs = []
	list_configs_correct = []
	for linha in file_gemm:
		list_configs.append(linha)
	for linha in list_configs:
		linha = str(linha)
		linha = linha.replace("'","").replace(",","").replace("\n","")
		list_configs_correct.append(linha)
	return list_configs_correct

def manipulador():
	list_configs = read_file_configs()
	count = 1
	for valor in list_configs:
		print str(count) + " de 21231"
		p = subprocess.Popen('nvprof --metrics sm_efficiency ./gemm-cuda.exe 0 '+str(valor), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		for line in p.stdout.readlines():
			resultado = line,
			retval = p.wait()
			strg = "" + line
			if strg.find("Multiprocessor Activity") > -1:
				idx = strg.index("Multiprocessor Activity")
				subsrtg = strg[idx:].split("    ")
				#print "substrg: ", subsrtg
				substring = subsrtg[3]
				substring1 = substring.replace("%",'')
				metric_value = float(substring1)
				print "sm_efficiency: ", metric_value
		valor = valor.replace(" ",",").replace(",1024,1024,1024","")
		arquivo_csv = open("gemm-smefficiency-1024-todas-conf-titanx.csv","a")
		arquivo_csv.write("gx,gy,gz,bx,by,bz,gpuId,smefficiency \n")
		arquivo_csv.write(str(valor)+",0,"+str(metric_value)+"\n")
		count += 1

if __name__ == '__main__':
	read_file_configs()
	manipulador()
