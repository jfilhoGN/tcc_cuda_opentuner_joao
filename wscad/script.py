import matplotlib.pyplot as plt
import re

def generated_list():
	list_achieved_occupancy = []
	expressao = re.compile(r'achieved_occupancy: .[0-9].[0-9]*')
	arquivo_nohup = open("/home/jfilhogn/Documentos/Git/tcc_cuda_opentuner_joao/wscad/sincoscuda-opentuner/nohub_backup-128.out","r")
	for linha in arquivo_nohup:
		match = expressao.findall(linha)
		if match:
			string = ''.join(match)
			string_replace = string.replace("achieved_occupancy:  ","")
			list_achieved_occupancy.append(string_replace)
	#print(list_achieved_occupancy)
	return list_achieved_occupancy

	
def generated_graphics():
	list_achieved_occupancy = generated_list()
	plt.plot(list_achieved_occupancy,linestyle='--', color='r', marker='s')
	plt.ylabel("Porcentagem Ocupância")
	plt.show()

if __name__ == '__main__':
	generated_list()
	generated_graphics()