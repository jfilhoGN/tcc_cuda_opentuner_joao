#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <malloc.h>
 
#ifndef DATA_TYPE
#define DATA_TYPE float
#endif

DATA_TYPE N = 1024;

__device__ int getGlobalIdx_1D_1D() {
    // Operações -> multiply: 1 add: 1 (2 FLOPs).
    // printf("getGlobalIdx_1D_1D.\n");
    return blockIdx.x * blockDim.x + threadIdx.x;
}
__device__ int getGlobalIdx_1D_2D() {
    // Operações -> multiply: 3 add: 2 (5 FLOPs).
    // printf("getGlobalIdx_1D_2D.\n");
    return blockIdx.x * blockDim.x * blockDim.y + threadIdx.y * blockDim.x
            + threadIdx.x;
}
__device__ int getGlobalIdx_1D_3D() {
    // Operações -> multiply: 6 add: 3 (9 FLOPs).
    // printf("getGlobalIdx_1D_3D.\n");
    return blockIdx.x * blockDim.x * blockDim.y * blockDim.z
            + threadIdx.z * blockDim.y * blockDim.x + threadIdx.y * blockDim.x
            + threadIdx.x;
}
__device__ int getGlobalIdx_2D_1D() {
    // Operações -> multiply: 2 add: 2 (4 FLOPs).
    // printf("getGlobalIdx_2D_1D.\n");
    int blockId = blockIdx.y * gridDim.x + blockIdx.x;
    int threadId = blockId * blockDim.x + threadIdx.x;
    return threadId;
}
__device__ int getGlobalIdx_2D_2D() {
    // Operações -> multiply: 4 add: 3 (7 FLOPs).
    // printf("getGlobalIdx_2D_2D.\n");
    int blockId = blockIdx.x + blockIdx.y * gridDim.x;
    int threadId = blockId * (blockDim.x * blockDim.y)
            + (threadIdx.y * blockDim.x) + threadIdx.x;
    return threadId;
}
__device__ int getGlobalIdx_2D_3D() {
    // Operações -> multiply: 7 add: 4 (11 FLOPs).
    // printf("getGlobalIdx_2D_3D.\n");
    int blockId = blockIdx.x + blockIdx.y * gridDim.x;
    int threadId = blockId * (blockDim.x * blockDim.y * blockDim.z)
    + (threadIdx.z * (blockDim.x * blockDim.y)) + (threadIdx.y * blockDim.x)
            + threadIdx.x;
    return threadId;
}
__device__ int getGlobalIdx_3D_1D() {
    // Operações -> multiply: 4 add: 3 (7 FLOPs).
    // printf("getGlobalIdx_3D_1D.\n");
    int blockId = blockIdx.x + blockIdx.y * gridDim.x
            + gridDim.x * gridDim.y * blockIdx.z;
    int threadId = blockId * blockDim.x + threadIdx.x;
    return threadId;
}
__device__ int getGlobalIdx_3D_2D() {
    // Operações -> multiply: 6 add: 4 (10 FLOPs).
    // printf("getGlobalIdx_3D_2D.\n");
    int blockId = blockIdx.x + blockIdx.y * gridDim.x
            + gridDim.x * gridDim.y * blockIdx.z;
    int threadId = blockId * (blockDim.x * blockDim.y)
            + (threadIdx.y * blockDim.x) + threadIdx.x;
    return threadId;
}
__device__ int getGlobalIdx_3D_3D() {
    // Operações -> multiply: 9 add: 5 (14 FLOPs).
    // printf("getGlobalIdx_3D_3D.\n");
    int blockId = blockIdx.x + blockIdx.y * gridDim.x
            + gridDim.x * gridDim.y * blockIdx.z;
    int threadId = blockId * (blockDim.x * blockDim.y * blockDim.z)
            + (threadIdx.z * (blockDim.x * blockDim.y))
            + (threadIdx.y * blockDim.x) + threadIdx.x;
    return threadId;
}

__global__ void vecAdd(DATA_TYPE *a, DATA_TYPE *b, DATA_TYPE *c, int n){
    //Thread ID
    int id = blockIdx.x*blockDim.x+threadIdx.x;
 
    if (id < n)
        c[id] = a[id] + b[id];
}
 
int main(int argc, char **argv){
 	
 	int blockSize, gridSize;
 	//Tamanho do block size será passado pelo opentuner
    // Numero de threads por block
    blockSize = atoi(argv[1]);

    // Host entrada vetor
    int *h_a;
    int *h_b;

    //Host saida vetor
    int *h_c;
 
    // Device entrada vetor
    int *d_a;
    int *d_b;

    //Device saida vetor
    int *d_c;
 
    // Tamanho, em bytes
    size_t bytes = N*sizeof(int);
 
    // Alocando o tamanho do vetor
    h_a = (int*)malloc(bytes);
    h_b = (int*)malloc(bytes);
    h_c = (int*)malloc(bytes);
 
    // Alocando memoria para a GPU
    cudaMalloc(&d_a, bytes);
    cudaMalloc(&d_b, bytes);
    cudaMalloc(&d_c, bytes);
 
    int i;
    // Inicializa vetor e adicionando valores
    for( i = 0; i < N; i++ ) {
        h_a[i] = i;
        h_b[i] = i;
    }
 
    // Copia do vetor Host para o vetor Device
    cudaMemcpy( d_a, h_a, bytes, cudaMemcpyHostToDevice);
    cudaMemcpy( d_b, h_b, bytes, cudaMemcpyHostToDevice);

    // Numero de thread blocks na grid
    gridSize = (int)ceil((float)N/blockSize);
 
    // Executa o kernel
    vecAdd<<<gridSize, blockSize>>>(d_a, d_b, d_c, N);
 
    // Copia array de volta para o host
    cudaMemcpy( h_c, d_c, bytes, cudaMemcpyDeviceToHost );
 
    for(i=0; i<N; i++){
    	printf("resultado: %d\n", h_c[i]);
    }
    
    cudaFree(d_a);
    cudaFree(d_b);
    cudaFree(d_c);
 
    free(h_a);
    free(h_b);
    free(h_c);
 
    return 0;
}
