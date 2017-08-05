/**
 * atax.cu: This file is part of the PolyBench/GPU 1.0 test suite.
 *
 *
 * Contact: Scott Grauer-Gray <sgrauerg@gmail.com>
 * Louis-Noel Pouchet <pouchet@cse.ohio-state.edu>
 * Web address: http://www.cse.ohio-state.edu/~pouchet/software/polybench/GPU
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <assert.h>
#include <unistd.h>
#include <sys/time.h>
#include <cuda.h>
#include "../../dimensions.h"
#include "../common/polybenchUtilFuncts.h"
#include "../common/polybench.c"

#include <cuda_runtime.h>

#include "../../../dimensions.h"


//define the error threshold for the results "not matching"
#define PERCENT_DIFF_ERROR_THRESHOLD 0.5

#define GPU_DEVICE 0

#ifndef M_PI
#define M_PI 3.14159
#endif

/* Can switch DATA_TYPE between float and double */
typedef float DATA_TYPE;

void init_array(DATA_TYPE *x, DATA_TYPE *A, int NX, int NY)
{
	int i, j;

	for (i = 0; i < NX; i++)
	{
		x[i] = i * M_PI;
		for (j = 0; j < NY; j++)
		{
			A[i*NY + j] = ((DATA_TYPE) i*(j)) / NX;
		}
	}
}


void compareResults(DATA_TYPE *z, DATA_TYPE *z_outputFromGpu, int NY)
{
	int i, fail;
	fail = 0;

	for (i=0; i<NY; i++)
	{
		if (percentDiff(z[i], z_outputFromGpu[i]) > PERCENT_DIFF_ERROR_THRESHOLD)
		{
			fail++;
		}		
	}
	
	// print results
	printf("Non-Matching CPU-GPU Outputs Beyond Error Threshold of %4.2f Percent: %d\n", PERCENT_DIFF_ERROR_THRESHOLD, fail);
}


void GPU_argv_init()
{
	cudaDeviceProp deviceProp;
	cudaGetDeviceProperties(&deviceProp, GPU_DEVICE);
	printf("setting device %d with name %s\n",GPU_DEVICE,deviceProp.name);
	cudaSetDevice( GPU_DEVICE );
}


__global__ void atax_kernel1(DATA_TYPE *A, DATA_TYPE *x, DATA_TYPE *tmp, int NX, int NY, funcId)
{
	int i = getGlobalIdFunc[funcId]();

	if (i < NX)
	{
		int j;
		for(j=0; j < NY; j++)
		{
			tmp[i] += A[i * NY + j] * x[j];
		}
	}
}

__global__ void atax_kernel2(DATA_TYPE *A, DATA_TYPE *y, DATA_TYPE *tmp, int NX, int NY, int funcId)
{
	int j = getGlobalIdFunc[funcId]();
	
	if (j < NY)
	{
		int i;
		for(i=0; i < NX; i++)
		{
			y[j] += A[i * NY + j] * tmp[i];
		}
	}
}


void atax_cpu(DATA_TYPE* A, DATA_TYPE* x, DATA_TYPE* y, DATA_TYPE* tmp, int NX, int NY)
{
	int i,j;
	
	for (i= 0; i < NY; i++)
	{
    	y[i] = 0;
	}
  
	for (i = 0; i < NX; i++)
 	{
      	tmp[i] = 0;

      	for (j = 0; j < NY; j++)
		{
			tmp[i] = tmp[i] + A[i*NY + j] * x[j];
		}
		
      	for (j = 0; j < NY; j++)
		{
			y[j] = y[j] + A[i*NY + j] * tmp[i];
		}
    }
}


int main(int argc, char** argv)
{
	double t_start, t_end;

	int NX = 0;
	int NY = 0;
	int kernel = 0;
	int funcId = 0;
	int i = 0;

	if (argc != 11) {
        printf("Uso: %s <kernel> <g.x> <g.y> <g.z> <b.x> <b.y> <b.z> <nx> <ny> \n", argv[0]);
        /*printf("     funcId:\n");
        printf("     0: 1D_1D, 1: 1D_2D, 2: 1D_3D\n");
        printf("     3: 2D_1D, 4: 2D_2D, 5: 2D_3D\n");
        printf("     6: 3D_1D, 7: 3D_2D, 8: 3D_3D\n");*/
        return 0;
    }
    else{
        printf("#argumentos (argc): %d\n", argc);
        for (i = 0; i < argc; ++i) {
           printf(" argv[%d]: %s\n", i, argv[i]);
        }
    
        kernel = atoi(argv[1]);
        NX = atoi(argv[8]);
        NY = atoi(argv[9]);
        //funcId = atoi(argv[10]);
        printf("Executando: %s atax_kernel_%d grid(%d, %d, %d) block(%d, %d, %d) %d\n", argv[0], kernel, atoi(argv[2]), atoi(argv[3]), atoi(argv[4]), atoi(argv[5]), atoi(argv[6]), atoi(argv[7]));
    }
  
    /* Recuperar as informações da GPU. */
    printf("%s Starting...\n", argv[0]);

	DATA_TYPE* A;
	DATA_TYPE* x;
	DATA_TYPE* y;
	DATA_TYPE* y_outputFromGpu;
	DATA_TYPE* tmp;

	A = (DATA_TYPE*)malloc(NX*NY*sizeof(DATA_TYPE));
	x = (DATA_TYPE*)malloc(NY*sizeof(DATA_TYPE));
	y = (DATA_TYPE*)malloc(NY*sizeof(DATA_TYPE));
	y_outputFromGpu = (DATA_TYPE*)malloc(NY*sizeof(DATA_TYPE));
	tmp = (DATA_TYPE*)malloc(NX*sizeof(DATA_TYPE));

	init_array(x, A, NX, NY);

	GPU_argv_init();
	DATA_TYPE *A_gpu;
	DATA_TYPE *x_gpu;
	DATA_TYPE *y_gpu;
	DATA_TYPE *tmp_gpu;

	cudaMalloc((void **)&A_gpu, sizeof(DATA_TYPE) * NX * NY);
	cudaMalloc((void **)&x_gpu, sizeof(DATA_TYPE) * NY);
	cudaMalloc((void **)&y_gpu, sizeof(DATA_TYPE) * NY);
	cudaMalloc((void **)&tmp_gpu, sizeof(DATA_TYPE) * NX);
	
	cudaMemcpy(A_gpu, A, sizeof(DATA_TYPE) * NX * NY, cudaMemcpyHostToDevice);
	cudaMemcpy(x_gpu, x, sizeof(DATA_TYPE) * NY, cudaMemcpyHostToDevice);
	cudaMemcpy(y_gpu, y, sizeof(DATA_TYPE) * NY, cudaMemcpyHostToDevice);
	cudaMemcpy(tmp_gpu, tmp, sizeof(DATA_TYPE) * NX, cudaMemcpyHostToDevice);
	
	if (kernel == 0){
		dim3 block(atoi(argv[5]), atoi(argv[6]), atoi(argv[7]));
		dim3 grid1(atoi(argv[2]), atoi(argv[3]), atoi(argv[4]));
		funcId = calculateFunctionId(grid, block);
  		printf("funcId: %d\n", funcId);
		t_start = rtclock();
		atax_kernel1<<< grid1, block >>>(A_gpu,x_gpu,tmp_gpu, NX, NY, funcId);
		cudaThreadSynchronize();
		t_end = rtclock();
		fprintf(stdout, "GPU Runtime: %0.6lfs\n", t_end - t_start);
		cudaMemcpy(y_outputFromGpu, y_gpu, sizeof(DATA_TYPE) * NX, cudaMemcpyDeviceToHost);
		cudaFree(A_gpu);
		cudaFree(x_gpu);
		cudaFree(y_gpu);
		cudaFree(tmp_gpu);
	}else{
		dim3 block(atoi(argv[5]), atoi(argv[6]), atoi(argv[7]));
		dim3 grid2(atoi(argv[2]), atoi(argv[3]), atoi(argv[4]));
		funcId = calculateFunctionId(grid, block);
  		printf("funcId: %d\n", funcId);
		t_start = rtclock();
		atax_kernel2<<< grid2, block >>>(A_gpu,y_gpu,tmp_gpu, NX, NY, funcId);
		cudaThreadSynchronize();
		t_end = rtclock();
		fprintf(stdout, "GPU Runtime: %0.6lfs\n", t_end - t_start);
		cudaMemcpy(y_outputFromGpu, y_gpu, sizeof(DATA_TYPE) * NX, cudaMemcpyDeviceToHost);
		cudaFree(A_gpu);
		cudaFree(x_gpu);
		cudaFree(y_gpu);
		cudaFree(tmp_gpu);
	}
	
	t_start = rtclock();
	atax_cpu(A, x, y, tmp, NX, NY);
	t_end = rtclock();
	fprintf(stdout, "CPU Runtime: %0.6lfs\n", t_end - t_start);

	compareResults(y, y_outputFromGpu, NY);

	free(A);
	free(x);
	free(y);
	free(y_outputFromGpu);
	free(tmp);

  	return 0;
}

