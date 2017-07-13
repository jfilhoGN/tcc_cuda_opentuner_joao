#include <cuda_runtime.h>
#include <stdio.h>
#include "dimensions.h"


__global__ void checkIndex(int funcId) {
  /*printf("threadIdx:(%2d, %2d, %2d) blockIdx:(%2d, %2d, %2d) blockDim:(%2d, %2d, %2d) "
         "gridDim:(%2d, %2d, %2d) -> id: %2d\n",
         threadIdx.x, threadIdx.y, threadIdx.z, blockIdx.x, blockIdx.y,
         blockIdx.z, blockDim.x, blockDim.y, blockDim.z, gridDim.x, gridDim.y,
         gridDim.z, getGlobalIdFunc[funcId]());*/
    printf("gridDim:(%2d, %2d, %2d) blockDim:(%2d, %2d, %2d) blockIdx:(%2d, %2d, %2d) "
         "threadIdx:(%2d, %2d, %2d) -> id: %2d\n", gridDim.x, gridDim.y,
         gridDim.z, blockDim.x, blockDim.y, blockDim.z, blockIdx.x, blockIdx.y,
         blockIdx.z, threadIdx.x, threadIdx.y, threadIdx.z, getGlobalIdFunc[funcId]());
    
}

int main(int argc, char **argv) {

  if (argc != 8) {
        printf("Uso: %s <g.x> <g.y> <g.z> <b.x> <b.y> <b.z> <gpuId>\n", argv[0]);
        return 0;
    }
  /* Definição do arranjo de threads em blocos do grid. */
  dim3 grid(atoi(argv[1]), atoi(argv[2]), atoi(argv[3]));
  dim3 block(atoi(argv[4]), atoi(argv[5]), atoi(argv[6]));

  /*
     grid(gx,gy,gx) block(bx,by,bz)
     funcId é escolhida com base nos valores de [gx,gy,gx,bx,by,bz]
     Cada valor irá contribuir com uma parcela para o cálculo do índice da função:
     [gx > 1, gy > 1, gx > 1, bx > 1, by > 1, bz > 1]
     Exemplo: grid(32,1,1) block(32,1,1)
              [1,0,0,1,0,0] -> [32,16,8,4,2,1] = [32 + 4] = 36
              A função getGlobalIdFunc(36) será:
              // 36: 100 100 getGlobalIdx_grid_1D_x_block_1D_x 
  */

  int funcId = 0;

  funcId += (grid.x > 1) ? 32 : 0;
  funcId += (grid.y > 1) ? 16 : 0;
  funcId += (grid.z > 1) ? 8 : 0;
  funcId += (block.x > 1) ? 4 : 0;
  funcId += (block.y > 1) ? 2 : 0;
  funcId += (block.z > 1) ? 1 : 0;

  int gpuId =  atoi(argv[8]);

  /* Define the gpu id to work */
  cudaSetDevice(gpuId);

  // check grid and block dimension from host side
  printf("config(gx: %d, gy: %d, gz: %d, bx: %d, by: %d, bz: %d)\n", grid.x, grid.y, grid.z, block.x, block.y, block.z);
  
  printf("gridDim:( x,  y,  z) blockDim:( x,  y,  z) blockIdx:( x,  y,  z) threadIdx:( x,  y,  z)\n");
  // check grid and block dimension from device side
  checkIndex<<<grid, block>>>(funcId);
  
  // reset device before you leave
  cudaDeviceReset();
  return (0);
}
