ALL:	Serial Parallel

Serial:	string_pattern_match.c
	gcc -Wall -o spm string_pattern_match.c 
	
Parallel:	parallel_string_pattern_match.c
	gcc -Wall -o pspm parallel_string_pattern_match.c  -fopenmp
	
runm:
	./spm MOBY_DICK.txt output_M.txt 215724
	
runl:	
	./spm LITTLE_WOMEN_MOBY_DICK.txt output_L.txt 411191
	
runs:	
	./spm SHAKESPEARE.txt output_S.txt 965465
	
runp4:	
	export OMP_NUM_THREADS=4 && ./pspm
	
runp8:	
	export OMP_NUM_THREADS=8 && ./pspm
	
runp16:	
	export OMP_NUM_THREADS=16 && ./pspm 
	

clean:
	/bin/rm -f spm *.o
	/bin/rm -f pspm *.o
	/bin/rm -f output_L.txt
	/bin/rm -f output_M.txt
	/bin/rm -f output_S.txt
