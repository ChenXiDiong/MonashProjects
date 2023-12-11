ALL:	openmp.c sequential.c
	gcc -Wall -o seq sequential.c -fopenmp
	gcc -Wall -o omp openmp.c -fopenmp

run:
	./seq
	./omp
	
clean:
	/bin/rm -f seq *.o
	/bin/rm -f omp *.o
	/bin/rm -f seq_output.txt
	/bin/rm -f par_output.txt