
objects = RMTTestSet.o KnapsackCombinationSearch.o 
RMTTestSetGenerator: $(objects)
	cc -o RMTTestSetGenerator $(objects)
KnapsackCombinationSearch.o: KnapsackCombinationSearch.c KnapsackCombinationSearch.h
	cc -c KnapsackCombinationSearch.c
RMTTestSet.o: RMTTestSet.c RMTTestSet.h KnapsackCombinationSearch.h
	cc -c RMTTestSet.c

#gcc -O2 KnapsackCombinationSearch.c RMTTestSet.c -o RMTTestSetGenerator

## Clean built files
clean:
	rm *.o *.exe