def manipulador():
	list_configs = ["2 1024 4 32 1 1" ,"2 1024 4 16 2 1" , "2 1024 4 8 4 1", "2 1024 4 4 8 1","2 1024 4 2 16 1","2 1024 4 1 32 1","2 1024 4 16 1 2","2 1024 4 8 2 2","2 1024 4 4 4 2","2 1024 4 2 8 2","2 1024 4 1 16 2","2 1024 4 8 1 4","2 1024 4 4 2 4","2 1024 4 2 4 4","2 1024 4 1 8 4","2 1024 4 4 1 8","2 1024 4 2 2 8","2 1024 4 1 4 8","2 1024 4 2 1 16","2 1024 4 1 2 16","2 1024 4 1 1 32"]
	for valor in list_configs:
		print valor
		p = subprocess.Popen('nvprof --metrics sm_efficiency ./gemm-cuda.exe 0 '+str(valor)+"512 512 512", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		for line in p.stdout.readlines():
			resultado = line,
			retval = p.wait()
			strg = "" + line
			if strg.find("Multiprocessor Activity") > -1:
				idx = strg.index("Multiprocessor Activity")
				subsrtg = strg[idx:].split("    ")
				substring = subsrtg[3]
				substring1 = substring.replace("%",'')
				metric_value = float(substring1)
				print "sm_efficiency: ", metric_value
		arquivo_csv = open("gemm-smefficiency-512-grid-2,1024,4,titanx-2tentativa.csv","a")
		arquivo_csv.write("gx,gy,gz,bx,by,bz,funcId,smefficiency \n")
		arquivo_csv.write(str(valor)+","+str(metric_value)+"\n")

if __name__ == '__main__':
	manipulador()