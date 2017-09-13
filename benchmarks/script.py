import matplotlib.pyplot as plt
import re


def generated_list():
	list_metrics = []
	list_occupancy = []
	expressao_command = re.compile(r'Running command line: (.*)\n')
	expressao_occupancy = re.compile(r'achieved_occupancy: .[0-9].[0-9]*')
	arquivo_nohup = open("/home/jfilhogn/Documentos/Git/ajuste-dimensoes-kernels-wscad-2017/sincoscuda-opentuner/results_gtx/nohup-224.out","r")
	for linha in arquivo_nohup:
		match = expressao_command.findall(linha)
		if match:
			string = ''.join(match)
			string_replace1 = string.replace("Running command line:  ","")
			string_replace2 = string_replace1.replace("nvprof --metrics achieved_occupancy ./sincosc-cuda ","  ")
			list_metrics.append(string_replace2)
	#print(list_metrics)
	arquivo_nohup1 = open("/home/jfilhogn/Documentos/Git/ajuste-dimensoes-kernels-wscad-2017/sincoscuda-opentuner/results_gtx/nohup-224.out","r")
	for linha1 in arquivo_nohup1:
		match1 = expressao_occupancy.findall(linha1)
		if match1:
			string1 = ''.join(match1)
			string_replace3 = string1.replace("achieved_occupancy:  ","")
			list_occupancy.append(string_replace3)
	#print(list_occupancy)
	#print(len(list_occupancy))
	arquivo_novo_nohup = open("/home/jfilhogn/Documentos/Git/ajuste-dimensoes-kernels-wscad-2017/sincoscuda-opentuner/results_gtx/nohup-224.out_novo.csv","w")
	arquivo_novo_nohup.write("Kernel,gx,gy,gz,bx,by,bz,nx,ny,nz,gpuId,occupancy \n")
	for i,j in zip(list_metrics, list_occupancy):
		arquivo_novo_nohup.write(i+" "+j+"\n")
	arquivo_novo_nohup.close()
		

if __name__ == '__main__':
	generated_list()
