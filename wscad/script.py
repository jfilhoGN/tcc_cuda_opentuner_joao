import matplotlib.pyplot as plt
import re


def generated_list():
	list_metrics = []
	expressao = re.compile(r'achieved_occupancy: .[0-9].[0-9]*')
	arquivo_nohup = open("/home/jfilhogn/Documentos/Git/tcc_cuda_opentuner_joao/wscad/polybench/ATAX/results_gtx/nohup-224.out","r")
	for linha in arquivo_nohup:
		match = expressao.findall(linha)
		if match:
			string = ''.join(match)
			string_replace = string.replace("achieved_occupancy:  ","")
			list_metrics.append(string_replace)
	print(list_metrics)
	return list_metrics

	
def generated_graphics():
	list_metrics = generated_list()
	list_plot = []
	for i in range(0,100):
		list_plot.append(list_metrics[i])
	plt.plot(list_plot, color='green')
	plt.ylabel("Média de Warps Ativos por execução")
	#plt.show()
	plt.savefig('atax-512-occ-gtx.png')

if __name__ == '__main__':
	generated_list()
	generated_graphics()