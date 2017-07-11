#include <cuda_runtime.h>
#include <stdio.h>
// #include "dimensions.h"

__global__ void checkIndex(int funcId) {
  /*printf("threadIdx:(%d, %d, %d) blockIdx:(%d, %d, %d) blockDim:(%d, %d, %d) "
         "gridDim:(%d, %d, %d) -> id: %d\n",
         threadIdx.x, threadIdx.y, threadIdx.z, blockIdx.x, blockIdx.y,
         blockIdx.z, blockDim.x, blockDim.y, blockDim.z, gridDim.x, gridDim.y,
         gridDim.z, getGlobalIdFunc[funcId]());*/
    printf("threadIdx:(%d, %d, %d) blockIdx:(%d, %d, %d) blockDim:(%d, %d, %d) "
         "gridDim:(%d, %d, %d) -> id: %d\n",
         threadIdx.x, threadIdx.y, threadIdx.z, blockIdx.x, blockIdx.y,
         blockIdx.z, blockDim.x, blockDim.y, blockDim.z, gridDim.x, gridDim.y,
         gridDim.z);
}

int main(int argc, char **argv) {

  if (argc != 9) {
        printf("Uso: %s <g.x> <g.y> <g.z> <b.x> <b.y> <b.z> <funcId> <gpuId>\n", argv[0]);
        printf("     funcId:\n");
        printf("     0: 1D_1D, 1: 1D_2D, 2: 1D_3D\n");
        printf("     3: 2D_1D, 4: 2D_2D, 5: 2D_3D\n");
        printf("     6: 3D_1D, 7: 3D_2D, 8: 3D_3D\n");
        return 0;
    }
  /* Definição do arranjo de threads em blocos do grid. */
  dim3 grid(atoi(argv[1]), atoi(argv[2]), atoi(argv[3]));
  dim3 block(atoi(argv[4]), atoi(argv[5]), atoi(argv[6]));

  int funcId = atoi(argv[7]);
  int gpuId =  atoi(argv[8]);

  /* Define the gpu id to work */
  cudaSetDevice(gpuId);

  // check grid and block dimension from host side
  printf("grid.x %d grid.y %d grid.z %d\n", grid.x, grid.y, grid.z);
  printf("block.x %d block.y %d block.z %d\n", block.x, block.y, block.z);
  
  // check grid and block dimension from device side
  checkIndex<<<grid, block>>>(funcId);
  
  // reset device before you leave
  cudaDeviceReset();
  return (0);
}
