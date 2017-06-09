all: seq omp

seq:
	gcc tam_grids_blocks.c -o tam_grids_blocks.exe
	
omp:
	gcc -fopenmp tam-grids-blocks-omp-for.c -o tam-grids-blocks-omp-for.exe

clean:
	rm *.exe

