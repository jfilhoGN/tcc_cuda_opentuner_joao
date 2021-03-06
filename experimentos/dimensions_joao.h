#include <stdio.h>

/* Tipo para o ponteiro de função. */
typedef int (*op_func) (void);

//---------------------------------------
// 1D_ (grid)
//---------------------------------------
// gx > 1 -> (32,1,1)(1,1,1)
__device__ int getGlobalIdx_grid_1D_x() {
    return blockIdx.x;
}

// gy > 1 -> (1,32,1)(1,1,1)
__device__ int getGlobalIdx_grid_1D_y() {
    return blockIdx.y;
}

// gz > 1 -> (1,1,32)(1,1,1)
__device__ int getGlobalIdx_grid_1D_z() {
    return blockIdx.z;
}

//---------------------------------------
// _1D (block)
//---------------------------------------
// bx > 1 -> (1,1,1)(32,1,1)
__device__ int getGlobalIdx_block_1D_x() {
    return threadIdx.x;
}

// by > 1 -> (1,1,1)(1,32,1)
__device__ int getGlobalIdx_block_1D_y() {
    return threadIdx.y;
}

// bz > 1 -> (1,1,1)(1,1,32)
__device__ int getGlobalIdx_block_1D_z() {
    return threadIdx.z;
}

//---------------------------------------
// 2D_ (grid)
//---------------------------------------
// gx,gy > 1 -> (32,32,1)(1,1,1)
__device__ int getGlobalIdx_grid_2D_xy() {
    
    return blockIdx.x + blockIdx.y * gridDim.x;
}

// gx,gz > 1 -> (32,1,32)(1,1,1)
__device__ int getGlobalIdx_grid_2D_xz() {
    
    return blockIdx.x + blockIdx.z * gridDim.x;
}

// gy,gz > 1 -> (1,32,32)(1,1,1)
__device__ int getGlobalIdx_grid_2D_yz() {
    
    return blockIdx.y + blockIdx.z * gridDim.y;
}

//---------------------------------------
// _2D (block)
//---------------------------------------
// bx,by > 1 -> (1,1,1)(32,32,1)
__device__ int getGlobalIdx_block_2D_xy() {
    
    return 0;
}

// bx,bz > 1 -> (1,1,1)(32,1,32)
__device__ int getGlobalIdx_block_2D_xz() {
    
    return 0;
}

// by,bz > 1 -> (1,1,1)(1,32,32)
__device__ int getGlobalIdx_block_2D_yz() {
    
    return 0;
}

//---------------------------------------
// 3D_ (grid)
//---------------------------------------
// gx,gy,gz > 1 -> (32,32,32)(1,1,1)
__device__ int getGlobalIdx_grid_3D_xyz() {
    
    return 0;
}

//---------------------------------------
// _3D (block)
//---------------------------------------
// bx,by,bz > 1 -> (1,1,1)(32,32,32)
__device__ int getGlobalIdx_block_3D_xyz() {
    
    return 0;
}

//---------------------------------------
// 1D_1D (grid and block)
//---------------------------------------
// gx e bx > 1 -> (32,1,1)(32,1,1)
__device__ int getGlobalIdx_grid_1D_x_block_1D_x() {
    return blockIdx.x * blockDim.x + threadIdx.x;
}

// gx e by > 1 -> (32,1,1)(1,32,1)
__device__ int getGlobalIdx_grid_1D_x_block_1D_y() {
    return blockIdx.x * blockDim.y + threadIdx.y;
}

// gx e bz > 1 -> (32,1,1)(1,1,32)
__device__ int getGlobalIdx_grid_1D_x_block_1D_z() {
    return blockIdx.x * blockDim.z + threadIdx.z;
}

// gy e bx > 1 -> (1,32,1)(32,1,1)
__device__ int getGlobalIdx_grid_1D_y_block_1D_x() {
    return blockIdx.y * blockDim.x + threadIdx.x;
}

// gy e by > 1 -> (1,32,1)(1,32,1)
__device__ int getGlobalIdx_grid_1D_y_block_1D_y() {
    return blockIdx.y * blockDim.y + threadIdx.y;
}

// gy e bz > 1 -> (1,32,1)(1,1,32)
__device__ int getGlobalIdx_grid_1D_y_block_1D_z() {
    return blockIdx.y * blockDim.z + threadIdx.z;
}

// gz e bx > 1 -> (1,1,32)(32,1,1)
__device__ int getGlobalIdx_grid_1D_z_block_1D_x() {
    return blockIdx.z * blockDim.x + threadIdx.x;
}

// gz e by > 1 -> (1,1,32)(1,32,1)
__device__ int getGlobalIdx_grid_1D_z_block_1D_y() {
    return blockIdx.z * blockDim.y + threadIdx.y;
}

// gz e bz > 1 -> (1,1,32)(1,1,32)
__device__ int getGlobalIdx_grid_1D_z_block_1D_z() {
    return blockIdx.z * blockDim.z + threadIdx.z;
}

//---------------------------------------
// 1D_2D
//---------------------------------------
// gx e bx,by > 1 -> (32,1,1)(32,32,1)
__device__ int getGlobalIdx_grid_1D_x_block_2D_xy() {
    
    return blockIdx.x * blockDim.x * blockDim.y + threadIdx.x + threadIdx.y;
}

// gx e bx,bz > 1 -> (32,1,1)(32,1,32)
__device__ int getGlobalIdx_grid_1D_x_block_2D_xz() {
    
    return blockDim.x * blockDim.z * blockIdx.x + threadIdx.x + threadIdx.z;
}

// gx e by,bz > 1 -> (32,1,1)(1,32,32)
__device__ int getGlobalIdx_grid_1D_x_block_2D_yz() {
    
    return blockDim.y * blockDim.z * blockIdx.x + threadIdx.y + threadIdx.z;
}

// gy e bx,by > 1 -> (1,32,1)(32,32,1)
__device__ int getGlobalIdx_grid_1D_y_block_2D_xy() {
    
    return blockDim.x * blockDim.y * blockIdx.y + threadIdx.x + threadIdx.y;
}

// gy e bx,bz > 1 -> (1,32,1)(32,1,32)
__device__ int getGlobalIdx_grid_1D_y_block_2D_xz() {
    
    return blockDim.x * blockDim.z * blockIdx.y + threadIdx.x + threadIdx.z;
}

// gy e by,bz > 1 -> (1,32,1)(1,32,32)
__device__ int getGlobalIdx_grid_1D_y_block_2D_yz() {
    
    return blockDim.y * blockDim.z * blockIdx.y + threadIdx.y + threadIdx.z;
}

// gz e bx,by > 1 -> (1,1,32)(32,32,1)
__device__ int getGlobalIdx_grid_1D_z_block_2D_xy() {
    
    return blockDim.x * blockDim.y * blockIdx.z + threadIdx.x + threadIdx.y;
}

// gz e bx,bz > 1 -> (1,1,32)(32,1,32)
__device__ int getGlobalIdx_grid_1D_z_block_2D_xz() {
    .
    return blockDim.x * blockDim.z * blockIdx.z + threadIdx.x + threadIdx.z;
}

// gz e by,bz > 1 -> (1,1,32)(1,32,32)
__device__ int getGlobalIdx_grid_1D_z_block_2D_yz() {
    
    return blockDim.y * blockDim.z * blockIdx.z + threadIdx.y + threadIdx.z;
}

//---------------------------------------
// 1D_3D
//---------------------------------------
// gx e bx,by,bz > 1 -> (32,1,1)(16,32,2)
__device__ int getGlobalIdx_grid_1D_x_block_3D_xyz() {
    // TODO
    return blockIdx.x * blockDim.x * blockDim.y * blockDim.z
            + threadIdx.z * blockDim.y * blockDim.x + threadIdx.y * blockDim.x
            + threadIdx.x;
}

// gy e bx,by,bz > 1 -> (1,32,1)(16,32,2)
__device__ int getGlobalIdx_grid_1D_y_block_3D_xyz() {
    
    return blockIdx.y * blockDim.x * blockDim.y * blockDim.z
            + threadIdx.z * blockDim.y * blockDim.x + threadIdx.y * blockDim.x
            + threadIdx.x;
}

// gz e bx,by,bz > 1 -> (1,1,32)(16,32,2)
__device__ int getGlobalIdx_grid_1D_z_block_3D_xyz() {
    
    return blockIdx.z * blockDim.x * blockDim.y * blockDim.z
            + threadIdx.z * blockDim.y * blockDim.x + threadIdx.y * blockDim.x
            + threadIdx.x;
}

//---------------------------------------
// 2D_1D
//---------------------------------------
// gx,gy e bx > 1 -> (32,32,1)(32,1,1)
__device__ int getGlobalIdx_grid_2D_xy_block_1D_x() {
    
    int blockId = blockIdx.y * blockDim.x + blockIdx.x;
    int threadId = blockId * blockDim.x + threadIdx.x;
    return threadId;
}

// gx,gy e by > 1 -> (32,32,1)(1,32,1)
__device__ int getGlobalIdx_grid_2D_xy_block_1D_y() {
    
    int blockId = blockIdx.y * blockDim.y + blockIdx.x;
    int threadId = blockId * blockDim.y + threadIdx.y;
    return threadId;
}

// gx,gy e bz > 1 -> (32,32,1)(1,1,32)
__device__ int getGlobalIdx_grid_2D_xy_block_1D_z() {
    
    int blockId = blockIdx.y * blockDim.z + blockIdx.x;
    int threadId = blockId * blockDim.z + threadIdx.z;
    return threadId;
}

// gx,gz e bx > 1 -> (32,1,32)(32,1,1)
__device__ int getGlobalIdx_grid_2D_xz_block_1D_x() {
    
    int blockId = blockIdx.z * blockDim.x + blockIdx.x;
    int threadId = blockId * blockDim.x + threadIdx.x;
    return threadId;
}

// gx,gz e by > 1 -> (32,1,32)(1,32,1)
__device__ int getGlobalIdx_grid_2D_xz_block_1D_y() {
    
    int blockId = blockIdx.z * blockDim.y + blockIdx.x;
    int threadId = blockId * blockDim.y + threadIdx.y;
    return threadId;
}

// gx,gz e bz > 1 -> (32,1,32)(1,1,32)
__device__ int getGlobalIdx_grid_2D_xz_block_1D_z() {
    
    int blockId = blockIdx.z * blockDim.z + blockIdx.x;
    int threadId = blockId * blockDim.z + threadIdx.z;
    return threadId;
}

// gy,gz e bx > 1 -> (1,32,32)(32,1,1)
__device__ int getGlobalIdx_grid_2D_yz_block_1D_x() {
    
    int blockId = blockIdx.z * blockDim.x + blockIdx.y;
    int threadId = blockId * blockDim.x + threadIdx.x;
    return threadId;
}

// gy,gz e by > 1 -> (1,32,32)(1,32,1)
__device__ int getGlobalIdx_grid_2D_yz_block_1D_y() {
    
    int blockId = blockIdx.z * blockDim.y + blockIdx.y;
    int threadId = blockId * blockDim.x + threadIdx.y;
    return threadId;
}

// gy,gz e bz > 1 -> (1,32,32)(1,1,32)
__device__ int getGlobalIdx_grid_2D_yz_block_1D_z() {
    
    int blockId = blockIdx.z * blockDim.z + blockIdx.y;
    int threadId = blockId * blockDim.z + threadIdx.z;
    return threadId;
}

//---------------------------------------
// 2D_2D
//---------------------------------------
// gx,gy e bx,by > 1 -> (32,32,1)(32,32,1)
__device__ int getGlobalIdx_grid_2D_xy_block_2D_xy() {
    
    int blockId = blockIdx.x + blockIdx.y * blockDim.x;
    int threadId = blockId * (blockDim.x * blockDim.y)
            + (threadIdx.y * blockDim.x) + threadIdx.x;
    return threadId;
}

// gx,gy e bx,bz > 1 -> (32,32,1)(32,1,32)
__device__ int getGlobalIdx_grid_2D_xy_block_2D_xz() {
    
    int blockId = blockIdx.x + blockIdx.y * blockDim.x;
    int threadId = blockId * (blockDim.x * blockDim.z)
            + (threadIdx.z * blockDim.x) + threadIdx.x;
    return threadId;
}

// gx,gy e by,bz > 1 -> (32,32,1)(1,32,32)
__device__ int getGlobalIdx_grid_2D_xy_block_2D_yz() {
    
    int blockId = blockIdx.x + blockIdx.y * blockDim.y;
    int threadId = blockId * (blockDim.y * blockDim.z)
            + (threadIdx.z * blockDim.y) + threadIdx.y;
    return threadId;
}

// gx,gz e bx,by > 1 -> (32,1,32)(32,32,1)
__device__ int getGlobalIdx_grid_2D_xz_block_2D_xy() {
    
    int blockId = blockIdx.x + blockIdx.z * blockDim.x;
    int threadId = blockId * (blockDim.x * blockDim.y)
            + (threadIdx.y * blockDim.x) + threadIdx.x;
    return threadId;
}

// gx,gz e bx,bz > 1 -> (32,1,32)(32,1,32)
__device__ int getGlobalIdx_grid_2D_xz_block_2D_xz() {
    
    int blockId = blockIdx.x + blockIdx.z * blockDim.x;
    int threadId = blockId * (blockDim.x * blockDim.z)
            + (threadIdx.z * blockDim.x) + threadIdx.x;
    return threadId;
}

// gx,gz e by,bz > 1 -> (32,1,32)(1,32,32)
__device__ int getGlobalIdx_grid_2D_xz_block_2D_yz() {
    
    int blockId = blockIdx.x + blockIdx.z * blockDim.x;
    int threadId = blockId * (blockDim.y * blockDim.z)
            + (threadIdx.y * blockDim.z) + threadIdx.y;
    return threadId;
}

// gy,gz e bx,by > 1 -> (1,32,32)(32,32,1)
__device__ int getGlobalIdx_grid_2D_yz_block_2D_xy() {
    
    int blockId = blockIdx.y + blockIdx.z * blockDim.x;
    int threadId = blockId * (blockDim.x * blockDim.y)
            + (threadIdx.y * blockDim.x) + threadIdx.x;
    return threadId;
}

// gy,gz e bx,bz > 1 -> (1,32,32)(32,1,32)
__device__ int getGlobalIdx_grid_2D_yz_block_2D_xz() {
    
    int blockId = blockIdx.y + blockIdx.z * blockDim.x;
    int threadId = blockId * (blockDim.x * blockDim.z)
            + (threadIdx.z * blockDim.x) + threadIdx.x;
    return threadId;
}

// gy,gz e by,bz > 1 -> (1,32,32)(1,32,32)
__device__ int getGlobalIdx_grid_2D_yz_block_2D_yz() {
    
    int blockId = blockIdx.y + blockIdx.z * blockDim.y;
    int threadId = blockId * (blockDim.y * blockDim.z)
            + (threadIdx.z * blockDim.y) + threadIdx.y;
    return threadId;
}

//---------------------------------------
// 2D_3D
//---------------------------------------
// gx,gy e bx,by,bz > 1 -> (32,32,1)(32,32,32)
__device__ int getGlobalIdx_grid_2D_xy_block_3D_xyz() {
    
    int blockId = blockIdx.x + blockIdx.y * blockDim.x;
    int threadId = blockId * (blockDim.x * blockDim.y * blockDim.z)
    + (threadIdx.z * (blockDim.x * blockDim.y)) + (threadIdx.y * blockDim.x)
            + threadIdx.x;
    return threadId;
}

// gx,gz e bx,by,bz > 1 -> (32,1,32)(32,32,32)
__device__ int getGlobalIdx_grid_2D_xz_block_3D_xyz() {
    
    int blockId = blockIdx.x + blockIdx.z * blockDim.x;
    int threadId = blockId * (blockDim.x * blockDim.y * blockDim.z)
    + (threadIdx.z * (blockDim.x * blockDim.y)) + (threadIdx.y * blockDim.x)
            + threadIdx.x;
    return threadId;
}

// gy,gz e bx,by,bz > 1 -> (1,32,32)(32,32,32)
__device__ int getGlobalIdx_grid_2D_yz_block_3D_xyz() {
    
    int blockId = blockIdx.x + blockIdx.y * blockDim.x;
    int threadId = blockId * (blockDim.x * blockDim.y * blockDim.z)
    + (threadIdx.z * (blockDim.x * blockDim.y)) + (threadIdx.y * blockDim.x)
            + threadIdx.x;
    return threadId;
}

//---------------------------------------
// 3D_1D
//---------------------------------------
// gx,gy,gz e bx > 1 -> (32,32,32)(32,1,1)
__device__ int getGlobalIdx_grid_3D_xyz_block_1D_x() {
    int blockId = blockIdx.x + blockIdx.y * gridDim.x
            + gridDim.x * gridDim.y * blockIdx.z;
    int threadId = blockId * blockDim.x + threadIdx.x;
    return threadId;
}

// gx,gy,gz e by > 1 -> (32,32,32)(1,32,1)
__device__ int getGlobalIdx_grid_3D_xyz_block_1D_y() {
    
    int blockId = blockIdx.x + blockIdx.y * gridDim.x
            + gridDim.x * gridDim.y * blockIdx.z;
    int threadId = blockId * blockDim.y + threadIdx.y;
    return threadId;
}

// gx,gy,gz e bz > 1 -> (32,32,32)(1,1,32)
__device__ int getGlobalIdx_grid_3D_xyz_block_1D_z() {
    
    int blockId = blockIdx.x + blockIdx.y * gridDim.x
            + gridDim.x * gridDim.y * blockIdx.z;
    int threadId = blockId * blockDim.z + threadIdx.z;
    return threadId;
}

//---------------------------------------
// 3D_2D
//---------------------------------------
// gx,gy,gz e bx,by > 1 -> (32,32,32)(16,32,1)
__device__ int getGlobalIdx_grid_3D_xyz_block_2D_xy() {
    int blockId = blockIdx.x + blockIdx.y * blockDim.x
            + blockDim.x * blockDim.y * blockIdx.z;
    int threadId = blockId * (blockDim.x * blockDim.y)
            + (threadIdx.y * blockDim.x) + threadIdx.x;
    return threadId;
}

// gx,gy,gz e bx,bz > 1 -> (32,32,32)(16,1,32)
__device__ int getGlobalIdx_grid_3D_xyz_block_2D_xz() {
    
    int blockId = blockIdx.x + blockIdx.y * blockDim.x
            + blockDim.x * blockDim.z * blockIdx.z;
    int threadId = blockId * (blockDim.x * blockDim.z)
            + (threadIdx.x * blockDim.z) + threadIdx.z;
    return threadId;
}

// gx,gy,gz e by,bz > 1 -> (32,32,32)(1,16,32)
__device__ int getGlobalIdx_grid_3D_xyz_block_2D_yz() {
    
    int blockId = blockIdx.x + blockIdx.y * blockDim.y
            + blockDim.z * blockDim.y * blockIdx.z;
    int threadId = blockId * (blockDim.y * blockDim.z)
            + (threadIdx.z * blockDim.z) + threadIdx.y;
    return threadId;
}

//---------------------------------------
// 3D_3D
//---------------------------------------
__device__ int getGlobalIdx_grid_3D_xyz_block_3D_xyz() {
    // Operações -> multiply: 9 add: 5 (14 FLOPs).
    // printf("getGlobalIdx_3D_3D.\n");
    int blockId = blockIdx.x + blockIdx.y * gridDim.x
            + gridDim.x * gridDim.y * blockIdx.z;
    int threadId = blockId * (blockDim.x * blockDim.y * blockDim.z)
            + (threadIdx.z * (blockDim.x * blockDim.y))
            + (threadIdx.z * blockDim.x) + threadIdx.y;
    return threadId;
}


__device__ op_func getGlobalIdFunc[63] = {getGlobalIdx_grid_1D_x, getGlobalIdx_grid_1D_y, getGlobalIdx_grid_1D_z, getGlobalIdx_block_1D_x, getGlobalIdx_block_1D_y, getGlobalIdx_block_1D_z, getGlobalIdx_grid_2D_xy, getGlobalIdx_grid_2D_xz, getGlobalIdx_grid_2D_yz, getGlobalIdx_block_2D_xy, getGlobalIdx_block_2D_xz, getGlobalIdx_block_2D_yz, getGlobalIdx_grid_3D_xyz, getGlobalIdx_block_3D_xyz, getGlobalIdx_grid_1D_x_block_1D_x, getGlobalIdx_grid_1D_x_block_1D_y, getGlobalIdx_grid_1D_x_block_1D_z, getGlobalIdx_grid_1D_y_block_1D_x, getGlobalIdx_grid_1D_y_block_1D_y, getGlobalIdx_grid_1D_y_block_1D_z, getGlobalIdx_grid_1D_z_block_1D_x, getGlobalIdx_grid_1D_z_block_1D_z, getGlobalIdx_grid_1D_x_block_2D_xy, getGlobalIdx_grid_1D_x_block_2D_xz, getGlobalIdx_grid_1D_x_block_2D_yz, getGlobalIdx_grid_1D_y_block_2D_xy, getGlobalIdx_grid_1D_y_block_2D_xz, getGlobalIdx_grid_1D_y_block_2D_yz, getGlobalIdx_grid_1D_z_block_2D_xy, getGlobalIdx_grid_1D_z_block_2D_xz, getGlobalIdx_grid_1D_z_block_2D_yz, getGlobalIdx_grid_1D_x_block_3D_xyz, getGlobalIdx_grid_1D_y_block_3D_xyz, getGlobalIdx_grid_1D_z_block_3D_xyz, getGlobalIdx_grid_2D_xy_block_1D_x, getGlobalIdx_grid_2D_xy_block_1D_y, getGlobalIdx_grid_2D_xy_block_1D_z, getGlobalIdx_grid_2D_xz_block_1D_x, getGlobalIdx_grid_2D_xz_block_1D_y, getGlobalIdx_grid_2D_xz_block_1D_z, getGlobalIdx_grid_2D_yz_block_1D_x, getGlobalIdx_grid_2D_yz_block_1D_y, getGlobalIdx_grid_2D_yz_block_1D_z, getGlobalIdx_grid_2D_xy_block_2D_xy, getGlobalIdx_grid_2D_xy_block_2D_xz, getGlobalIdx_grid_2D_xy_block_2D_yz, getGlobalIdx_grid_2D_xz_block_2D_xy, getGlobalIdx_grid_2D_xz_block_2D_xz, getGlobalIdx_grid_2D_xz_block_2D_yz, getGlobalIdx_grid_2D_yz_block_2D_xy, getGlobalIdx_grid_2D_yz_block_2D_xz, getGlobalIdx_grid_2D_yz_block_2D_yz, getGlobalIdx_grid_2D_xy_block_3D_xyz, getGlobalIdx_grid_2D_xz_block_3D_xyz, getGlobalIdx_grid_2D_yz_block_3D_xyz, getGlobalIdx_grid_3D_xyz_block_1D_x, getGlobalIdx_grid_3D_xyz_block_1D_y, getGlobalIdx_grid_3D_xyz_block_1D_z, getGlobalIdx_grid_3D_xyz_block_2D_xy, getGlobalIdx_grid_3D_xyz_block_2D_xz, getGlobalIdx_grid_3D_xyz_block_2D_yz, getGlobalIdx_grid_3D_xyz_block_3D_xyz }


/*// Fontes. ESSE AQUI A GENTE VAI USAR?

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
}*/

/* Tabela de funções para chamada parametrizada. */
/*__device__ op_func getGlobalIdFunc[9] = { getGlobalIdx_1D_1D, getGlobalIdx_1D_2D, getGlobalIdx_1D_3D, 
                      getGlobalIdx_2D_1D, getGlobalIdx_2D_2D, getGlobalIdx_2D_3D,
                      getGlobalIdx_3D_1D, getGlobalIdx_3D_2D, getGlobalIdx_3D_3D};
*/


