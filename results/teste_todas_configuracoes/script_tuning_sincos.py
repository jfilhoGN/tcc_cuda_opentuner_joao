#!/usr/bin/env python
import os
import signal
import subprocess
import re

def read_file_configs():
	#testar tambem com 512
	file_gemm = open('./configuracoes/saida-gemm-320-funcid.txt','r')
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
		print count
		# # Kernel 0
		p = subprocess.Popen('nvprof --metrics sm_efficiency ./sincosc-cuda.exe 0 '+str(valor), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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
				print "sm_efficiency_0: ", metric_value
		valor1 = valor.replace(" ",",").replace(",320,320,320","")
		print str(valor1)+","+str(metric_value)
		p.stdout.close()
		arquivo_csv = open("sincos-smefficiency-320-todas-conf-funcid-titanx-kerrnel.csv","a")
		arquivo_csv.write("kernel,gx,gy,gz,bx,by,bz,funcId,smefficiency \n")
		arquivo_csv.write("0,"+str(valor1)+","+str(metric_value)+"\n")
		
		# # Kernel 1
		q = subprocess.Popen('nvprof --metrics sm_efficiency ./sincosc-cuda.exe 1 '+str(valor), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		for line in q.stdout.readlines():
			resultado = line,
			retval = q.wait()
			strg = "" + line
			if strg.find("Multiprocessor Activity") > -1:
				idx = strg.index("Multiprocessor Activity")
				subsrtg = strg[idx:].split("    ")
				#print "substrg: ", subsrtg
				substring = subsrtg[3]
				substring1 = substring.replace("%",'')
				metric_value = float(substring1)
				print "sm_efficiency_1: ", metric_value
		valor2 = valor.replace(" ",",").replace(",320,320,320","")
		print str(valor2)+","+str(metric_value)
		q.stdout.close()
		#arquivo_csv = open("sincos-smefficiency-320-todas-conf-funcid-titanx.csv","a")
		arquivo_csv.write("1,"+str(valor2)+","+str(metric_value)+"\n")
		count+=1

		# Kernel 2
		r = subprocess.Popen('nvprof --metrics sm_efficiency ./sincosc-cuda.exe 2 '+str(valor), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		arquivo_saida = open("sincos-todas-kernel2-320.csv","a")
		for line in r.stdout.readlines():
			resultado = line,
			retval = r.wait()
			strg = "" + line
			if strg.find("======== Error: CUDA device error.") > -1:
				print "Nao rodou"
				arquivo_saida.write("Nao Rodou\n")
				metric_value = 0
			elif strg.find("Multiprocessor Activity") > -1:
				idx = strg.index("Multiprocessor Activity")
				subsrtg = strg[idx:].split("    ")
				#print "substrg: ", subsrtg
				substring = subsrtg[3]
				substring1 = substring.replace("%",'')
				metric_value = float(substring1)
				print "sm_efficiency_2: ", metric_value
		valor3 = valor.replace(" ",",").replace(",320,320,320","")
		print str(valor3)+","+str(metric_value)
		arquivo_saida.write("2,"+str(valor3)+","+str(metric_value)+"\n")
		r.stdout.close()

		# kernel 3
		t = subprocess.Popen('nvprof --metrics sm_efficiency ./sincosc-cuda.exe 3 '+str(valor), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		for line in t.stdout.readlines():
			resultado = line,
			retval = t.wait()
			strg = "" + line
			if strg.find("Multiprocessor Activity") > -1:
				idx = strg.index("Multiprocessor Activity")
				subsrtg = strg[idx:].split("    ")
				#print "substrg: ", subsrtg
				substring = subsrtg[3]
				substring1 = substring.replace("%",'')
				metric_value = float(substring1)
				print "sm_efficiency_3: ", metric_value
		valor4 = valor.replace(" ",",").replace(",320,320,320","")
		print str(valor3)+str(metric_value)
		arquivo_saida.write("3,"+str(valor4)+","+str(metric_value)+"\n")
		t.stdout.close()
		count += 1


if __name__ == '__main__':
	read_file_configs()
	manipulador()
