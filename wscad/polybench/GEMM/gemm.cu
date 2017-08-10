/**
 * gemm.cu: This file is part of the PolyBench/GPU 1.0 test suite.
 *
 *
 * Contact: Scott Grauer-Gray <sgrauerg@gmail.com>
 * Louis-Noel Pouchet <pouchet@cse.ohio-state.edu>
 * Web address: http://www.cse.ohio-state.edu/~pouchet/software/polybench/GPU
 */

 // FALTA SO CHAMAR AS DIMENSOES E ARRUMAR NO KERNEL

#include <unistd.h>
#include <stdio.h>
#include <time.h>
#include <sys/time.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include <cuda.h>
#include "../../../dimensions.h"
#include "../common/polybenchUtilFuncts.h"
#include "../common/polybench.c"


#define GPU_DEVICE 0

//define the error threshold for the results "not matching"
#define PERCENT_DIFF_ERROR_THRESHOLD 0.05


/* Declared constant values for ALPHA and BETA (same as values in PolyBench 2.0) */
#define ALPHA 32412.0f
#define BETA 2123.0f

/* Can switch DATA_TYPE between float and double */
typedef float DATA_TYPE;

void gemm(DATA_TYPE *A, DATA_TYPE *B, DATA_TYPE *C, int NI, int NJ, int NK)
{
	int i,j,k;
	
	for (i = 0; i < NI; i++)
	{
    	for (j = 0; j < NJ; j++)
    	{
			C[i*NJ + j] *= BETA;
	
			for (k = 0; k < NK; ++k)
			{
	  			C[i*NJ + j] += ALPHA * A[i*NK + k] * B[k*NJ + j];
			}
      	}
	}
}


void init(DATA_TYPE *A, DATA_TYPE *B, DATA_TYPE *C, int NI, int NJ, int NK)
{
	int i, j;

  	for (i = 0; i < NI; i++)
	{
    	for (j = 0; j < NK; j++)
		{
      		A[i*NK + j] = ((DATA_TYPE) i*j) / NI;
		}
	}

  	for (i = 0; i < NK; i++)
	{
    	for (j = 0; j < NJ; j++)
		{
      		B[i*NJ + j] = ((DATA_TYPE) i*j + 1) / NJ;
		}
	}

  	for (i = 0; i < NI; i++)
	{
    	for (j = 0; j < NJ; j++)
		{
      		C[i*NJ + j] = ((DATA_TYPE) i*j + 2) / NJ;
		}
	}
}


void compareResults(DATA_TYPE* C, DATA_TYPE* C_outputFromGpu, int NI, int NJ)
{
	int i, j, fail;
	fail = 0;
	
	// Compare C1 and C2
	for (i=0; i < NI; i++) 
	{
		for (j=0; j < NJ; j++) 
		{
			if (percentDiff(C[i*NJ + j], C_outputFromGpu[i*NJ + j]) > PERCENT_DIFF_ERROR_THRESHOLD) 
			{
				fail++;
			}
		}
	}
	
	// Print results
	printf("Non-Matching CPU-GPU Outputs Beyond Error Threshold of %4.2f Percent: %d\n", PERCENT_DIFF_ERROR_THRESHOLD, fail);
}


void GPU_argv_init()
{
	cudaDeviceProp deviceProp;
	cudaGetDeviceProperties(&deviceProp, GPU_DEVICE);
	printf("setting device %d with name %s\n",GPU_DEVICE,deviceProp.name);
	cudaSetDevice( GPU_DEVICE );
}


__global__ void gemm_kernel(DATA_TYPE *a, DATA_TYPE *b, DATA_TYPE *c, int NI, int NJ, int NK, int funcId)
{
	int j = getGlobalIdFunc[funcId]();
	int i = getGlobalIdFunc[funcId]();

	if ((i < NI) && (j < NJ))
	{	
		c[i * NJ + j] *= BETA;
		int k;
		for(k=0; k < NK; k++)
		{
			c[i * NJ + j] += ALPHA * a[i * NK + k] * b[k * NJ +j];
		}
	}
}
	

int main(int argc, char *argv[])
{
	double t_start, t_end;

	int NJ = 0;
	int NI = 0;
	int NK = 0;
    int kernel = 0;
    int funcId = 0;
    int i = 0;
    if (argc != 11) {
        printf("Uso: %s <kernel> <g.x> <g.y> <g.z> <b.x> <b.y> <b.z> <ni> <nj> <nk> \n", argv[0]);
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
        NI = atoi(argv[8]);
        NJ = atoi(argv[9]);
        NK = atoi(argv[10]);
        //funcId = atoi(argv[11]);
        //printf("Executando: %s gemm_kernel_%d grid(%d, %d, %d) block(%d, %d, %d) %d\n", argv[0], kernel, atoi(argv[2]), atoi(argv[3]), atoi(argv[4]), atoi(argv[5]), atoi(argv[6]), atoi(argv[7]));
    }
  
    /* Recuperar as informações da GPU. */
    printf("%s Starting...\n", argv[0]);

	DATA_TYPE* A;
	DATA_TYPE* B;  
	DATA_TYPE* C;  
	DATA_TYPE* C_outputFromGpu; 

	A = (DATA_TYPE*)malloc(NI*NK*sizeof(DATA_TYPE)); 
	B = (DATA_TYPE*)malloc(NK*NJ*sizeof(DATA_TYPE));   
	C = (DATA_TYPE*)malloc(NI*NJ*sizeof(DATA_TYPE)); 
	C_outputFromGpu = (DATA_TYPE*)malloc(NI*NJ*sizeof(DATA_TYPE)); 


	DATA_TYPE *A_gpu;
	DATA_TYPE *B_gpu;
	DATA_TYPE *C_gpu;

	cudaMalloc((void **)&A_gpu, sizeof(DATA_TYPE) * NI * NK);
	cudaMalloc((void **)&B_gpu, sizeof(DATA_TYPE) * NK * NJ);
	cudaMalloc((void **)&C_gpu, sizeof(DATA_TYPE) * NI * NJ);

	init(A, B, C, NI, NJ, NK);
	
	GPU_argv_init();
	
	cudaMemcpy(A_gpu, A, sizeof(DATA_TYPE) * NI * NK, cudaMemcpyHostToDevice);
	cudaMemcpy(B_gpu, B, sizeof(DATA_TYPE) * NK * NJ, cudaMemcpyHostToDevice);
	cudaMemcpy(C_gpu, C, sizeof(DATA_TYPE) * NI * NJ, cudaMemcpyHostToDevice);
	
	dim3 block(atoi(argv[5]), atoi(argv[6]), atoi(argv[7]));
	dim3 grid(atoi(argv[2]), atoi(argv[3]), atoi(argv[4]));
	
	if (kernel==0){
		funcId = calculateFunctionId(grid, block);
		t_start = rtclock();
		gemm_kernel<<< grid, block >>>(A_gpu, B_gpu, C_gpu, NI, NJ, NK, funcId);
		cudaThreadSynchronize();

		t_end = rtclock();
		fprintf(stdout, "GPU Runtime: %0.6lfs\n", t_end - t_start);

		cudaMemcpy(C_outputFromGpu, C_gpu, sizeof(DATA_TYPE) * NI * NJ, cudaMemcpyDeviceToHost);    
	
		cudaFree(A_gpu);
		cudaFree(B_gpu);
		cudaFree(C_gpu);
	}
	

	t_start = rtclock();	
	gemm(A, B, C, NI, NJ, NK);
	t_end = rtclock();
	fprintf(stdout, "CPU Runtime: %0.6lfs\n", t_end - t_start);
	
	compareResults(C, C_outputFromGpu, NI, NJ);

	free(A);
	free(B);  
	free(C);  
	free(C_outputFromGpu); 

    return 0;
}

