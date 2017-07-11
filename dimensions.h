#include <stdio.h>

/* Tipo para o ponteiro de função. */
typedef int (*op_func) (void);

/* Tabela de funções para chamada parametrizada. */
__device__ op_func getGlobalIdFunc[9] = { getGlobalIdx_1D_1D, getGlobalIdx_1D_2D, getGlobalIdx_1D_3D, 
                      getGlobalIdx_2D_1D, getGlobalIdx_2D_2D, getGlobalIdx_2D_3D,
                      getGlobalIdx_3D_1D, getGlobalIdx_3D_2D, getGlobalIdx_3D_3D};


__device__ int getGlobalIdx_1D_1D_x() {
    // Operações -> multiply: 1 add: 1 (2 FLOPs).
    // printf("getGlobalIdx_1D_1D.\n");
    return blockIdx.x * blockDim.x + threadIdx.x;
}

__device__ int getGlobalIdx_1D_1D_y() {
    // Operações -> multiply: 1 add: 1 (2 FLOPs).
    // printf("getGlobalIdx_1D_1D.\n");
    return blockIdx.y * blockDim.y + threadIdx.y;
}

__device__ int getGlobalIdx_1D_1D_z() {
    // Operações -> multiply: 1 add: 1 (2 FLOPs).
    // printf("getGlobalIdx_1D_1D.\n");
    return blockIdx.z * blockDim.z + threadIdx.z;
}

__device__ int getGlobalIdx_1D_2D_x() {
    // Operações -> multiply: 3 add: 2 (5 FLOPs).
    // printf("getGlobalIdx_1D_2D.\n");
    return blockIdx.x * blockDim.x * blockDim.y + threadIdx.y * blockDim.x
            + threadIdx.x;
}

__device__ int getGlobalIdx_1D_2D_y() {
    // Operações -> multiply: 3 add: 2 (5 FLOPs).
    // printf("getGlobalIdx_1D_2D.\n");
    return blockIdx.y * blockDim.y * blockDim.x + threadIdx.x * blockDim.y
            + threadIdx.y;
}

__device__ int getGlobalIdx_1D_2D_z() {
    // Operações -> multiply: 3 add: 2 (5 FLOPs).
    // printf("getGlobalIdx_1D_2D.\n");
    return blockIdx.z * blockDim.z * blockDim.x + threadIdx.x * blockDim.z
            + threadIdx.z;
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
