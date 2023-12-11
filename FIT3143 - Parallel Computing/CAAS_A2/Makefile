ALL:	wsn.c
	mpicc -Wall -o Out wsn.c -lpthread -g

runcaas1:
	srun Out 3 3 3 24 1 2

runcaas2:
	srun Out 2 5 5 15 2 4

runsim1:
	mpirun -np 5 ./Out

runsim2:
	mpirun -np 7 ./Out
	

clean:
	/bin/rm -f out *.o
	/bin/rm -f log.txt
	/bin/rm -f station0_log.txt
	/bin/rm -f station1_log.txt
	/bin/rm -f station2_log.txt
	/bin/rm -f station3_log.txt
	/bin/rm -f station4_log.txt
	/bin/rm -f station5_log.txt
	/bin/rm -f station6_log.txt
	/bin/rm -f station7_log.txt
	/bin/rm -f station8_log.txt
	/bin/rm -f station9_log.txt

