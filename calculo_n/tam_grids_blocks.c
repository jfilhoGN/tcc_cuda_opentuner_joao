#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define MAX_BLOCK_X 1024
#define MAX_BLOCK_Y 1024
#define MAX_BLOCK_Z 1024
#define MAX_GRID_X 2147483647
#define MAX_GRID_Y 65535
#define MAX_GRID_Z 65535
#define min(x,y) ((x)<(y)?(x):(y))

int main(int argc, char const *argv[]){
	unsigned long long int gx, gy, gz, bx, by, bz, confBlock;
	unsigned long long int confGrid, config, contConfig;
	unsigned int iteracoes;
	iteracoes = atoi(argv[1]);
	confBlock = 0;
	confGrid = 0;
	config = 0;
	contConfig = 0;
	for(bz = 1; bz <= min(iteracoes, MAX_BLOCK_Z); bz++){
		for(by = 1; by <= min((iteracoes / bz), MAX_BLOCK_Y); by++){
			for(bx = 1; bx < min(((iteracoes / bz)/ by), MAX_BLOCK_X); bx++){
				for(gx = 1 ;gx <= min((((iteracoes / bz ) / by ) / bx),MAX_GRID_X); gx++){
					for(gy = 1 ;gy <= min(((((iteracoes/ bz)/ by)/ bx) / gx),MAX_GRID_Y);gy++){
						for(gz =1; gz <= min((((((iteracoes / bz )/by)/ bx)/ gx)/ gy),MAX_GRID_Z); gz++){
							confBlock = bx * by * bz;
							confGrid = gx * gy * gz;
							config = confBlock * confGrid;
							if((confBlock <= 1024) && (config == iteracoes) && (confBlock% 32 ==0)){
								//printf("(%4d,%4d,%4d,%4d,%4d,%4d ) \n", gx, gy, gz, bx, by,bz);
								contConfig++;
							}

						}
					}
				}
			}
		}
		
	}
	printf("iteracoes: %d, count: %lld\n", iteracoes, contConfig);
	return(0);
}
