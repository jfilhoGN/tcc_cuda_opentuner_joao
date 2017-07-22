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

#define MAX_BLOCK_X 1024
#define MAX_BLOCK_Y 1024
#define MAX_BLOCK_Z 64
#define MAX_GRID_X 2147483647
#define MAX_GRID_Y 65535
#define MAX_GRID_Z 65535

#for(bz = 1; bz <= min(iterations,MAX_BLOCK_Z); bz++) {
#    for(by = 1; by <= min((iterations / bz),MAX_BLOCK_Y); by++) {
#      for(bx = 1; bx <= min(((iterations / bz) / by),MAX_BLOCK_X); bx++) {
#        for(gx = 1; gx <= min((((iterations / bz) / by) / bx),MAX_GRID_X); gx++) {
#          for(gy = 1; gy <= min(((((iterations / bz) / by) / bx) / gx),MAX_GRID_Y); gy++) {
#            for(gz = 1; gz <= min((((((iterations / bz) / by) / bx) / gx) / gy),MAX_GRID_Z); gz++)

# parameters: <kernel> <g.x> <g.y> <g.z> <b.x> <b.y> <b.z> <nx> <ny> <nz> <funcId> <gpuId>

# Configs
# (name, min, max)
BLOCK_GRID_PARAMS = [
  ('kernel', 0, 3),
  ('gx', 1, 65535),
  ('gy', 1, 65535),
  ('gz', 1, 65535),
  ('bx', 1, 1024),
  ('by', 1, 1024),
  ('bz', 1, 64),
  ('nx', 357, 357),
  ('ny', 357, 357),
  ('nz', 357, 357),
  ('funcId', 0, 9), # Retirar.
  ('gpuId', 0, 0)  
]
# Test para 2 1 1 64 1 1 1 64 64 64 0 0 

class SincosCudaTuner(MeasurementInterface):

  def manipulator(self):
    """
    Define the search space by creating a
    ConfigurationManipulator
    """
    manipulator = ConfigurationManipulator()

    print "Executing manipulator"
    
    for param, mini, maxi in BLOCK_GRID_PARAMS:
      print "param: ", param, " mini: ", mini, " maxi: ", maxi, " iterations: ", iterations
      dimensions = {'bx', 'by', 'bz', 'gx', 'gy', 'gz'}
      if param in dimensions:
        value = min(iterations, maxi)
      else:
        value = maxi
      manipulator.add_parameter(IntegerParameter(param, mini, value))

    return manipulator

# --------------------------------------------------------------------
  def run(self, desired_result, input, limit):
    """
    Compile and run a given configuration then
    return performance
    """
    cfg = desired_result.configuration.data
    
    print "CFG: ", cfg
    
    print "compiled: ", 'true' if compiled else 'false'

    if not compiled:
      print "Compiling the program..."
      gcc_cmd = 'nvcc -I/usr/local/cuda/include -L/usr/local/cuda/lib64 -ccbin=g++ src/sincosc.cu -lcuda -lm -o sincosc-cuda.bin'    
      compile_result = self.call_program(gcc_cmd)
      assert compile_result['returncode'] == 0
      print " OK.\n"
      global compiled
      compiled = not compiled

    #  for(bz = 1; bz <= min(iterations,MAX_BLOCK_Z); bz++) {
    #    for(by = 1; by <= min((iterations / bz),MAX_BLOCK_Y); by++) {
    #      for(bx = 1; bx <= min(((iterations / bz) / by),MAX_BLOCK_X); bx++) {
    #        for(gx = 1; gx <= min((((iterations / bz) / by) / bx),MAX_GRID_X); gx++) {
    #          for(gy = 1; gy <= min(((((iterations / bz) / by) / bx) / gx),MAX_GRID_Y); gy++) {
    #            for(gz = 1; gz <= min((((((iterations / bz) / by) / bx) / gx) / gy),MAX_GRID_Z); gz++)
    # ./sincosc-cuda <kernel> <g.x> <g.y> <g.z> <b.x> <b.y> <b.z> <nx> <ny> <nz> <funcId> <gpuId>
    # nvprof --metrics achieved_occupancy ./sincosc-cuda 2 1 1 64 1 1 1 64 64 64 0 0
    run_cmd = 'nvprof --metrics achieved_occupancy ./sincosc-cuda.bin'
    for param, min, max in BLOCK_GRID_PARAMS:
      print "Param: ", param, " ", cfg[param]
      run_cmd += ' {1}'.format(param, cfg[param])

    print "Generated command line: ", run_cmd

    confBlock = cfg['bx'] * cfg['by'] * cfg['bz']
    confGrid =  cfg['gx'] * cfg['gy'] * cfg['gz']
    config = confBlock * confGrid

    print "confBlock: ", confBlock
    print "confGrid: ", confGrid
    print "config: ", config
    print "iterations: ", iterations

    # Evict kernel divergence, blocks with multiply warp size.
    print "Test: ", "True" if((confBlock <= 1024) and (config == iterations) and (confBlock % 32 == 0)) else "False"

    if((confBlock <= 1024) and (config == iterations) and (confBlock % 32 == 0)):
      dimBlock = 0
      dimGrid = 0
      # Test of quantity of block dimensions are used.
      # a if test else b
      dimBlock += 1 if(cfg['bx'] > 1) else 0
      dimBlock += 1 if(cfg['by'] > 1) else 0
      dimBlock += 1 if(cfg['bz'] > 1) else 0
      if(dimBlock == 0):
        dimBlock = 1
                
      # Test of quantity of grid dimensions are used.
      dimGrid += 1 if(cfg['gx'] > 1) else 0
      dimGrid += 1 if(cfg['gy'] > 1) else 0
      dimGrid += 1 if(cfg['gz'] > 1) else 0
      if(dimGrid == 0):
        dimGrid = 1
                
      countConfig += 1
      print "Running command line: ", run_cmd
      run_result = self.call_program(run_cmd)
      # assert run_result['returncode'] == 0
      # print(run_result)
      # return Result(time=run_result['time'])
      # return Result(occupancy=run_result['occupancy'])
      # return Result(time=run_result['time'])
      if run_result['returncode'] != 0:
        return Result(time=FAIL_PENALTY)
      else:
        val = self.get_metric_from_app_output(run_result['stderr'])
        return Result(time=val)
    else:
      print "Invalid configuration, return penalty."
      return Result(time=FAIL_PENALTY)

# --------------------------------------------------------------------
  def get_metric_from_app_output(self, app_output):
    """Returns the metric value from output benchmark"""
    metric_value = 0.0
    #buf = StringIO.StringIO(app_output)
    #lines = buf.readlines()
    lines = app_output.split("\n")
    for current_line in lines:
        # print "Bla: ", current_line
        strg = "" + current_line
        # print strg
        if strg.find("Occupancy") > -1:
          # print "contains"
          # print "Bla: ", strg
          idx = strg.index("Occupancy")
          subsrtg = strg[idx:].split("    ")
          print "substrg: ", subsrtg
          metric_value = float(subsrtg[3])
          print "achieved_occupancy: ", metric_value
    return (1.0 - metric_value)

# --------------------------------------------------------------------
  def save_final_config(self, configuration):
    """called at the end of tuning"""
    print "Optimal block size written to sincoscuda_final_config.json:", configuration.data
    self.manipulator().save_to_file(configuration.data,
                                    'sincoscuda_final_config.json')

# --------------------------------------------------------------------
if __name__ == '__main__':
  FAIL_PENALTY = 9999999999
  compiled = False
  iterations = 1 * 357 * 357

  argparser = opentuner.default_argparser()
  SincosCudaTuner.main(argparser.parse_args())
