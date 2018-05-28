#!/usr/bin/env python
#
# Autotune flags to g++ to optimize the performance of apps/raytracer.cpp
#
# This is an extremely simplified version meant only for tutorials
#
import adddeps  # fix sys.path
import math
import re
import sys

import opentuner
from opentuner import ConfigurationManipulator
from opentuner import EnumParameter
from opentuner import IntegerParameter
from opentuner import MeasurementInterface
from opentuner import Result

# Formato de entrada
# nvprof --metrics gld_efficiency ./gem-cuda kernel gx gy gz bx by bz ni nj nk funcId

BLOCO_PARAMETROS = [
	('kernel', 0, 0), 
	('ni', int(sys.argv[2]),int(sys.argv[2])),
	('nj', int(sys.argv[2]),int(sys.argv[2])),
	('nk', int(sys.argv[2]),int(sys.argv[2])),
	('gpuId', 1, 1)  
]

BLOCO_PARAMETROS_CONFIGS = [ 'config' ]

def read_file_configs():
	file_gemm = open('/home/joao/Documentos/tcc_cuda_opentuner_joao/benchmarks/gen-configs/saida_gemm-'+str(sys.argv[2])+'.txt','r')
	list_configs = []
	for linha in file_gemm:
		list_configs.append(linha)
	#print list_configs
	return list_configs

class gemmTuner(MeasurementInterface):

	def manipulator(self):
		"""Define the search space by creating a
		ConfigurationManipulator
		"""
		list_configs = []
		list_configs = read_file_configs()
		manipulator = ConfigurationManipulator()
		print "Executing manipulator"
		for param, mini, maxi in BLOCO_PARAMETROS:
			#print "param: ", param, " mini: ", mini, " maxi: ", maxi
			manipulator.add_parameter(IntegerParameter(param, mini, maxi))

		# E preciso gerar as configuracoes validas com o run.c.
		# manipulator.add_parameter(EnumParameter(param, [ 'gx:1024, gy:1, gz:1, bx:1, by:1, bz:1, ', 'gx:32, gy:32, gz:1, bx:1, by:1, bz:1, ' ]))
		for param in BLOCO_PARAMETROS_CONFIGS:
			manipulator.add_parameter(EnumParameter(param,list_configs))
		return manipulator
		
	def run(self, desired_result, input, limit):
		"""
		Compile and run a given configuration then
		return performance
		"""
		# cfg = desired_result.configuration.data

		while True:
			# Configuration:  {'kernel': 0, 'gpuId': 0, 'config': 'gx:1024, gy:1, gz:1, bx:1, by:1, bz:1, ', 'funcId': 7}
			configuration = desired_result.configuration.data
			print "Configuration: ", configuration
			cfg = { match.group(1):match.group(2) for match in re.finditer(r"([^:]+):(\S+)\s*,[ \n]", configuration['config'])}
			print "CFG: ", cfg
			confBlock = int(cfg['bx']) * int(cfg['by']) * int(cfg['bz'])
			confGrid =  int(cfg["'gx"]) * int(cfg['gy']) * int(cfg['gz'])
			config = confBlock * confGrid
			print "ConfBlock "+ str(confBlock)
			print "ConfGrid " + str(confGrid)
			if((confBlock <= 1024) and (confBlock % 32 == 0) and (config == n)):
				break
			else:
				return Result(time=FAIL_PENALTY)

		# print "desired: " + str(desired_result.configuration.data)
		# print "CFG: ", cfg
		print "compiled: ", 'true' if compiled else 'false'
		if not compiled:
			print "Compiling the program..."
			gcc_cmd = 'nvcc -I /usr/local/cuda/include -L /usr/local/cuda/lib64 -ccbin=g++-6 gemm.cu -lcuda -lm -o gemm-cuda.exe'
			compile_result = self.call_program(gcc_cmd)
			assert compile_result['returncode'] == 0
			print " OK.\n"
			global compiled
			compiled = not compiled
		run_cmd = 'nvprof --metrics achieved_occupancy ./gemm-cuda.exe'

		# print "Antes do IF"
		# if((confBlock <= 1024) and (confBlock % 32 == 0) and (config == n)):
		# 	dimBlock = 0
		# 	dimGrid = 0
		# 	# Test of quantity of block dimensions are used.
		# 	# a if test else b
		# 	dimBlock += 1 if(int(cfg['bx']) > 1) else 0
		# 	dimBlock += 1 if(int(cfg['by']) > 1) else 0
		# 	dimBlock += 1 if(int(cfg['bz']) > 1) else 0
		# 	if(dimBlock == 0):
		# 		dimBlock = 1

		# 	# Test of quantity of grid dimensions are used.
		# 	dimGrid += 1 if(int(cfg["'gx"]) > 1) else 0
		# 	dimGrid += 1 if(int(cfg['gy']) > 1) else 0
		# 	dimGrid += 1 if(int(cfg['gz']) > 1) else 0
		# 	if(dimGrid == 0):
		# 		dimGrid = 1
			
		# 	if(dimGrid == 1):
		# 		cfg['funcId'] =  dimGrid + dimBlock - 2
		# 	if(dimGrid == 2):
		# 		cfg['funcId'] =  dimGrid + dimBlock + 0
		# 	if(dimGrid == 3):
		# 		cfg['funcId'] =  dimGrid + dimBlock + 2
		kernel = ' {0}'.format(configuration['kernel'])	
		gpuId =  ' {0}'.format(configuration['gpuId'])
		run_cmd += ' {0}'.format(configuration['kernel'])
		run_cmd += ' {0}'.format(cfg["'gx"])
		run_cmd += ' {0}'.format(cfg['gy'])
		run_cmd += ' {0}'.format(cfg['gz'])
		run_cmd += ' {0}'.format(cfg['bx'])
		run_cmd += ' {0}'.format(cfg['by'])
		run_cmd += ' {0}'.format(cfg['bz'])
		run_cmd += ' {0}'.format(configuration['ni'])
		run_cmd += ' {0}'.format(configuration['nj'])
		run_cmd += ' {0}'.format(configuration['nk'])
		run_cmd += ' {0}'.format(configuration['gpuId'])

		print "Running command line: ", run_cmd
		#print "CFG->funcId: " +  str(cfg['funcId'])

		run_result = self.call_program(run_cmd)
		if run_result['returncode'] != 0:
			return Result(time=FAIL_PENALTY)
		else:
			val = self.get_metric_from_app_output(run_result['stderr'], cfg, kernel,gpuId)
			return Result(time=val)
		# else:
		# 	print "Invalid configuration, return penalty."
		# 	return Result(time=FAIL_PENALTY)

	def get_metric_from_app_output(self, app_output, configuration, kernel, gpuId):
		"""Returns the metric value from output benchmark"""
		metric_value = 0.0
		lines = app_output.split("\n")
		for current_line in lines:
			strg = "" + current_line
			if strg.find("Occupancy") > -1:
				idx = strg.index("Occupancy")
				subsrtg = strg[idx:].split("    ")
				print "substrg: ", subsrtg
				metric_value = float(subsrtg[3])
				print "achieved_occupancy: ", metric_value
		configuration = str(configuration)
		configuration = configuration.replace("{",str(kernel)+",").replace(":","").replace("}","")
		configuration = configuration.replace("'gx","").replace("'gy'","").replace("'gz'","").replace("'bx'","").replace("'by'","").replace("'bz'","").replace("'","").replace("\"","")
		resultado = metric_value
		arquivo_csv = open("/home/joao/Documentos/tcc_cuda_opentuner_joao/results/gtx1070/gemm-occupancy-"+str(sys.argv[2])+".csv","a")
		arquivo_csv.write("Kernel,gx,gy,gz,bx,by,bz,gpuId,occupancy \n")
		arquivo_csv.write(str(configuration)+","+str(gpuId)+","+str(resultado)+"\n")
		return metric_value

	def save_final_config(self, configuration):
		"""called at the end of tuning"""
		print "Optimal block size written to gemmcuda_final_config.json:", configuration.data
		self.manipulator().save_to_file(configuration.data, 'gemmcuda_final_config-'+str(sys.argv[2])+'.json')

if __name__ == '__main__':
	FAIL_PENALTY = 9999999999
	compiled = False
	ni = int(sys.argv[2])
	nj = int(sys.argv[2])
	nk = int(sys.argv[2])
	n = ni * nj
	argparser = opentuner.default_argparser()
	read_file_configs()
	gemmTuner.main(argparser.parse_args())
