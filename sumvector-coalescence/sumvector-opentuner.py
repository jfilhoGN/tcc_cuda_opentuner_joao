#!/usr/bin/env python
#
# Autotune flags to g++ to optimize the performance of apps/raytracer.cpp
#
# This is an extremely simplified version meant only for tutorials
#
import adddeps  # fix sys.path
import math

import opentuner
from opentuner import ConfigurationManipulator
from opentuner import EnumParameter
from opentuner import IntegerParameter
from opentuner import MeasurementInterface
from opentuner import Result

# Formato de entrada
# ./sumvector-cuda 0 1024 1024 1 42 1 1 44040192 3 0

BLOCO_PARAMETROS = [
	('kernel', 0, 0), 
	('gx', 1, 2147483647),
	('gy', 1, 65535),
	('gz', 1, 65535),
	('bx', 1, 1024),
	('by', 1, 1024),
	('bz', 1, 64),
	('n', 1, ),
	('funcId', 0, 9),
	('gpuId', 0, 0)  
]

class SumVectorTuner(MeasurementInterface):
	

	def manipulator(self):
		pass

	def run()