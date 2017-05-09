#Codigo para opentuner soma de vetor
import adddeps  # fix sys.path

import opentuner
from opentuner import ConfigurationManipulator
from opentuner import IntegerParameter
from opentuner import MeasurementInterface
from opentuner import Result

class SumVectorCudaTuner(MeasurementInterface):
	
	def manipulator(self):
		manipulator = ConfigurationManipulator()
		manipulator.add_parameter(
			IntegerParameter('BLOCK_SIZE', 1, 1024))
		return manipulator


	def run(self, desired_result, input, limit):
		cfg = desired_result.configuration.data
		print "Compilando..."
		gcc_cmd = 'nvcc -I/usr/local/cuda/include -L/usr/local/cuda/lib64 -ccbin=g++-4.7 ./src/sumvector.cu -lcuda -lm -o sumvector-cuda.bin' 
		compile_result = self.call_program(gcc_cmd)
		assert compile_result['returncode'] == 0
		
		run_cmd = './sumvector-cuda.bin'
		run_cmd += ' {1}'.format('BLOCK_SIZE',cfg['BLOCK_SIZE'])

		print "Gerado seguinte comando: ", run_cmd
		run_result = self.call_program(run_cmd)
		assert run_result['returncode'] == 0
		return Result(time=run_result['time'])


	def save_final_config(self, configuration):

		print "Adicionado otimo BLOCK_SIZE para sumvector_final_config.json:", configuration.data
		self.manipulator().save_to_file(configuration.data,
			'sumvector_final_config.json')



if __name__ == '__main__':
	argumentos = opentuner.default_argparser()
	SumVectorCudaTuner.main(argumentos.parse_args())