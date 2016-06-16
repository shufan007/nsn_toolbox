
objects = LRC_RMTTestSet_DCHType.o SearchAlgorithm.o 
RMTTestSetGenerator: $(objects)
	cc -o RMTTestSetGenerator $(objects)
SearchAlgorithm.o: SearchAlgorithm.c RMTTestSet.h
	cc -c SearchAlgorithm.c
LRC_RMTTestSet_DCHType.o: LRC_RMTTestSet_DCHType.c RMTTestSet.h
	cc -c LRC_RMTTestSet_DCHType.c

#gcc -O2 SearchAlgorithm.c LRC_RMTTestSet_DCHType.c -o RMTTestSetGenerator

## Clean built files
clean:
	rm *.o *.exe