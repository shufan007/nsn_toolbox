
objects = LRC_RMTTestSet_Mixed.o SearchAlgorithm.o 
RMTTestSetGenerator: $(objects)
	cc -o RMTTestSetGenerator_Mixed $(objects)
SearchAlgorithm.o: SearchAlgorithm.c RMTTestSet.h
	cc -c SearchAlgorithm.c
LRC_RMTTestSet_DCHType.o: LRC_RMTTestSet_Mixed.c RMTTestSet.h
	cc -c LRC_RMTTestSet_Mixed.c

#gcc -O2 SearchAlgorithm.c LRC_RMTTestSet_DCHType.c -o RMTTestSetGenerator

## Clean built files
clean:
	rm *.o *.exe