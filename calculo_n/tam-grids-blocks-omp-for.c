#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#ifdef _OPENMP
#include <omp.h>
#else
#define omp_get_thread_num() 0
#define omp_get_num_threads() 1
#define omp_get_num_procs()                                                    \
  (system("cat /proc/cpuinfo | grep 'processor' | wc -l"))
#endif

#define MAX_BLOCK_X 1024
#define MAX_BLOCK_Y 1024
#define MAX_BLOCK_Z 1024
#define MAX_GRID_X 2147483647
#define MAX_GRID_Y 65535
#define MAX_GRID_Z 65535
#define min(x,y) ((x)<(y)?(x):(y))

int main(int argc, char const *argv[]){
    unsigned long long int gx, gy, gz, bx, by, bz, confBlock;
    unsigned long long int confGrid, config, countConfig;
    unsigned int iteracoes;
    unsigned int n_threads;
    int id;
    iteracoes = atoi(argv[1]);
    n_threads = atoi(argv[2]);
    confBlock = 0;
    confGrid = 0;
    config = 0;
    countConfig = 0;

    #pragma omp parallel num_threads(n_threads) private(id) firstprivate(confGrid, confBlock, config)
    {
      id = omp_get_thread_num();
      printf("Thread[%d][%lu]: Threading starting...\n", id, (long int)pthread_self());
      #pragma omp for private(bz, by, bx, gx, gy, gz) schedule(guided,32) reduction(+:countConfig)
      for(bz = 1; bz <= min(iteracoes, MAX_BLOCK_Z); bz++){
       	for(by = 1; by <= min((iteracoes / bz), MAX_BLOCK_Y); by++){
       		for(bx = 1; bx < min(((iteracoes / bz)/ by), MAX_BLOCK_X); bx++){
       			for(gx = 1; gx <= min((((iteracoes / bz ) / by ) / bx),MAX_GRID_X); gx++){
       				for(gy = 1; gy <= min(((((iteracoes/ bz)/ by)/ bx) / gx),MAX_GRID_Y);gy++){
       					for(gz =1; gz <= min((((((iteracoes / bz )/by)/ bx)/ gx)/ gy),MAX_GRID_Z); gz++){
       						confBlock = bx * by * bz;
       						confGrid = gx * gy * gz;
       						config = confBlock * confGrid;
       						if((confBlock <= 1024) && (config == iteracoes) && (confBlock% 32 ==0)){
       							// printf("(%4d,%4d,%4d,%4d,%4d,%4d ) \n", gx, gy, gz, bx, by,bz);
       							countConfig++;
       							// printf("Thread[%d][%lu]: Generating config[%lu] (%lu,%lu,%lu,%lu,%lu,%lu).\n", id, (long int)pthread_self(), countConfig, gx, gy, gz, bx, by, bz); 
       						}
       					}
       				}
       			}
       		}
       	}
      }
    }

    printf("Thread[%d][%lu]: iteracoes: %d, count: %lld\n", omp_get_thread_num(),
         (long int)pthread_self(), iteracoes, countConfig);

    return(0);
}
