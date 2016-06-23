/************************************************************************************
       Function:       Searching Algorithm for Resource Model Test set Generator
       Author:         Fan, Shuangxi (Nokia - CN/Hangzhou)
       History:
       
       0.8           (2015 -3 -20)   Implement the algorithm
       1.0           (2015 -5 -7 )    Resconsitution, 
 ************************************************************************************/
//#pragma once

#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<assert.h>
#include "RMTTestSet.h"

/***************************************************
 Global Definations
***************************************************/
//#define __DEBUE__

#define SEARCH_TRACE    "SearchingTrace"
#define MAX_SEARCH      1000000

#define GLO_TRUE       1
#define GLO_FALSE      0

#define  EPS                0.001     // used for judge the equality of float type
#define STR_LEN         50

/*  operators of tree struct, for heap process  */
#define PARENT(i) (((i+1)>>1)-1)
#define LEFT(i)      ((i<<1)+1)
#define RIGHT(i)   ((i<<1)+2)

/* *******************************************
    Custom structure definitions 
    ******************************************** */
typedef struct{
    int     depth;
    int     value;
    int     cost1;
    float  cost2;
}BranchRoot_T; 


typedef struct{
    int     caseNum;
    int     depth;
    int     currentMinValue;
    int     searchNum;
    int     updateNum;    
    BranchRoot_T BranchRoot;    
    CombinStat_T Combin;
}AllocInfo_T; 


/* ******************************************************************
    Function prototypes
    
******************************************************************** */
void CombinationSearchCommonInit(Knapsack_T*);
void AllocInfoInit();
void TraceFileInit();
void PrintSearchedStatisticsInfo();
void AllocateProcess();
void AllocDownStep();
void NextAllocationControlProcess();
void AllocRollbackOneStep();
void AllocRollbackToBranchRoot();
void SearchingLogTrace();
void PrintArrayToFile(FILE*, int*, int);
void TopListUpdate(TopList_T*);
void HeapUpdateTop(TopList_T*, CombinStat_T*);
void MinHeapify(TopList_T*, int);
void HeapPop(TopList_T*);
void HeapPush(TopList_T* , CombinStat_T*);
void SwapCombinStats(CombinStat_T* , CombinStat_T*);

/******************************************************************************

    Main process function of the combination search algorithm 

******************************************************************************/ 
FILE             * trace_fp         = NULL;
static int         g_count          = 0;
Knapsack_T*   knapsackPtr;
AllocInfo_T      allocInfo;

/******************************************************************************
[Problem Description:]
 - Combinatorial optimization problem --> resource allocation model
 
    *  Properties of Knapsack_T: 
        caseNum:         number of cases
        caseKinds:        kind number of cases
        Values: {v_j }   value of the cases
        Costs1: {c1_j}  cost1 of the cases
        Costs2: {c2_j}  cost2 of the cases
        limitCost1:  limit value of total cost1
        limitCost2:  limit value of total cost2
        x_i:                 resource consumption of user  i
        (Here,  caseNum and caseKinds indicate the input size of the problem.)

    * Constraint Equation:
        object:  max(Sum(v_i)) (i = 1 ,2,......, caseNum)
            s.t
        Sum(c1_i)<= limitCost1  (for c1_i in Costs1)
        Sum(c2_i)<= limitCost2  (for c2_i in Costs2)
        (The object can also be the top K list)

[Algorithm Description:]
* Technical points:
    1. Tree structure is used in the searching process;
    2. Arrange combinations in order;
    3. Greedy search;
    4. Backtracking;
    5. Effcient control process.
* Allocate process:
    * Growth Rules:
        - down:  child <= parent 
        - right: right child < left child
         * this 2 attribute can Make sure the combinations in order in the allocation process.
        - up (backtracking): current value cant't update the top list
         * discard the right branch, back to choose the next valid branch.
        * Greedy Rules: Always choose the biggest valid value.
         * searching always near the optimum combination.

- The allocated rule: the value of the child should no big than the parent's.
- The create process start from first level, if this allocate success, 
  it point to current node level, else it back to its parent level
*  Combinatorial Search: greedy allocate, search near the optimum value.
* If the priority_queue is full and this allocate can't update the priority_queue, then call back.
 - DOWN: New node value allocate only between the parent value and the biggest value;
 - UP(recall): (Trying) Change the parent value to the value of the next index,then go to downward.

[Attributes:] 
    * Fast
    * Not sensitive to the input size
    
* Input: knapsackPtr
* Output: topList
**********************************************************************************/

void CombinationSearch(Knapsack_T* inKnapsack, TopList_T*  topList) 
{
    CombinationSearchCommonInit(inKnapsack);

    /*************************************************
    *  main searching process
    allocInfo.depth: to indicate the point to be spread,  
    when depth back to -1 means the allocate process complete
    **************************************************/      
    while (allocInfo.depth >= 0)
    {
        AllocateProcess();

        if (allocInfo.depth == allocInfo.caseNum)
        {  
            TopListUpdate(topList);
        }
            
#ifdef __DEBUE__
        SearchingLogTrace();
#endif      
        if (allocInfo.searchNum >= MAX_SEARCH)
        {
            printf(" *** Hit the max search number: %d !\n", MAX_SEARCH);
            break;
        }
      
        NextAllocationControlProcess();          
    }
    
    PrintSearchedStatisticsInfo();

}//----------------------------------------------------------------------------------


void CombinationSearchCommonInit(Knapsack_T* inKnapsack)
{
    g_count++; 

    knapsackPtr = inKnapsack;

   AllocInfoInit();

#ifdef __DEBUE__
    TraceFileInit();    
#endif

}

void AllocInfoInit()
{
    memset(&allocInfo, 0, sizeof(AllocInfo_T));
    
    allocInfo.caseNum = knapsackPtr->caseNum;

    memset(allocInfo.Combin.combinId, 0, sizeof(int)*(allocInfo.caseNum+1));   
    allocInfo.Combin.combinId[0] = knapsackPtr->caseKinds -1; // init the first value 
}


void TraceFileInit()
{
    char fileName[STR_LEN];
    
    sprintf(fileName, "%s_%d.txt", SEARCH_TRACE, g_count);
    
    trace_fp  = fopen(fileName, "w");
    assert(trace_fp != NULL);
    
    fprintf(trace_fp, "\n case Kinds: %d\n case number: %d\n limitCost1: %d\n limitCost2: %d\n", 
        knapsackPtr->caseKinds, knapsackPtr->caseNum, knapsackPtr->limitCost1, knapsackPtr->limitCost2);
    fprintf(trace_fp, " \"==>\": input topList\n");
    fprintf(trace_fp, "------------------------------------\n");
}

void PrintSearchedStatisticsInfo()
{    
    printf( "   Search: %d, Update: %d\n", allocInfo.searchNum, allocInfo.updateNum);
    
    if (NULL != trace_fp)
    {
        fprintf(trace_fp, "\n [ * Search: %d, Update: %d ]\n", allocInfo.searchNum, allocInfo.updateNum);
        fclose(trace_fp);
    }    
}


/***********************************************************
Module Function: Allocate this branch
    *  if all conditions match, then this branch can be allocated successfully,
        else, it will keep track of the current records, then break
************************************************************/
void AllocateProcess()
{
    int maxPermitValue;

    while ((allocInfo.Combin.combinId[allocInfo.depth] >= 0) && (allocInfo.depth < allocInfo.caseNum))
    {
        maxPermitValue = allocInfo.Combin.value + knapsackPtr->Values[allocInfo.Combin.combinId[allocInfo.depth]]*(allocInfo.caseNum - allocInfo.depth);    

        if (maxPermitValue > allocInfo.currentMinValue)
        { 
            AllocDownStep();
        }
        else    /* If can't allocate anymore, save the current value to the index of caseNum, then break */
        {
            allocInfo.Combin.combinId[allocInfo.caseNum] = allocInfo.Combin.combinId[allocInfo.depth];            
            break;
        }
    }
    
    allocInfo.searchNum ++;
     
}


void AllocDownStep()
{
    int     minPermitCost1;
    float  minPermitCost2;
    
    minPermitCost1 = allocInfo.Combin.cost1 + knapsackPtr->Costs1[allocInfo.Combin.combinId[allocInfo.depth]] 
                             + knapsackPtr->Costs1[0]*(allocInfo.caseNum - allocInfo.depth-1);
    minPermitCost2 = allocInfo.Combin.cost2 + knapsackPtr->Costs2[allocInfo.Combin.combinId[allocInfo.depth]]
                             + knapsackPtr->Costs2[0]*(allocInfo.caseNum - allocInfo.depth-1); 
    
    if((minPermitCost1 <= knapsackPtr->limitCost1) && ((minPermitCost2 -knapsackPtr->limitCost2) <= EPS)) 
    {
        allocInfo.Combin.value += knapsackPtr->Values[allocInfo.Combin.combinId[allocInfo.depth]];            
        allocInfo.Combin.cost1 += knapsackPtr->Costs1[allocInfo.Combin.combinId[allocInfo.depth]];
        allocInfo.Combin.cost2 += knapsackPtr->Costs2[allocInfo.Combin.combinId[allocInfo.depth]];
        allocInfo.Combin.combinId[allocInfo.depth+1] = allocInfo.Combin.combinId[allocInfo.depth];
        allocInfo.depth ++;
    }
    else
    {
        allocInfo.Combin.combinId[allocInfo.depth] --;
    }
}


/*************************************************************
Module Function: check the value of this allocatation, update the Queue
    *  if this branch being successfully allocated, update the Queue if need, 
        and keep track of the current status
*************************************************************/
void TopListUpdate(TopList_T* topListPtr)
{
    allocInfo.Combin.combinId[allocInfo.caseNum] = -1; // -1 is update flag    
    allocInfo.updateNum++;
    
    //update Top List
    HeapUpdateTop(topListPtr, &allocInfo.Combin);    
    allocInfo.currentMinValue = topListPtr->List[0].value; 
}


/*************************************************************
    Module Function: The main control process for next turn of allocation
    1. Track back: track back from last depth
        If last allocation update the Queue success, track back 1 step
    2. Then, we use"drop" to avoid the non valid value
        - For "drop", if not "drop", it means this allocation can't update last value,
           so, keep track back until drop != 0
**************************************************************/
void NextAllocationControlProcess()
{    
    if (-1 == allocInfo.Combin.combinId[allocInfo.caseNum])
    {
        AllocRollbackOneStep();    
    }
    else    /* update allocInfo by BranchRoot */
    {
        AllocRollbackToBranchRoot();      
    }
        
    while(allocInfo.depth>=0)
    {                
        /* if the "drop" is true, go to next allocation, else roll back.
            (here, the value at caseNum saved the value of last allocate depth) */
        if(allocInfo.Combin.combinId[allocInfo.depth]> allocInfo.Combin.combinId[allocInfo.caseNum])
        {
            break;
        }
        
        AllocRollbackOneStep(); 
    } 
 
    //keep the records of current branch root
    allocInfo.BranchRoot.depth = allocInfo.depth;
    allocInfo.BranchRoot.value = allocInfo.Combin.value;
    allocInfo.BranchRoot.cost1 = allocInfo.Combin.cost1;
    allocInfo.BranchRoot.cost2 = allocInfo.Combin.cost2;

}

void AllocRollbackOneStep()
{
    allocInfo.depth --;

    if (allocInfo.depth >=0)
    {
        allocInfo.Combin.value -= knapsackPtr->Values[allocInfo.Combin.combinId[allocInfo.depth]];
        allocInfo.Combin.cost1 -= knapsackPtr->Costs1[allocInfo.Combin.combinId[allocInfo.depth]];
        allocInfo.Combin.cost2 -= knapsackPtr->Costs2[allocInfo.Combin.combinId[allocInfo.depth]]; 
                   
        allocInfo.Combin.combinId[allocInfo.depth] --; 
    } 
}

void AllocRollbackToBranchRoot()
{
    allocInfo.depth            = allocInfo.BranchRoot.depth;
    allocInfo.Combin.value = allocInfo.BranchRoot.value;
    allocInfo.Combin.cost1 = allocInfo.BranchRoot.cost1;
    allocInfo.Combin.cost2 = allocInfo.BranchRoot.cost2;
          
    allocInfo.Combin.combinId[allocInfo.depth] --;        
}


void SearchingLogTrace()
{
    int printNum;
    
    if ( -1 == allocInfo.Combin.combinId[allocInfo.caseNum])
    {
        printNum = allocInfo.caseNum;
        fprintf(trace_fp, "\n ==>");     
    }
    else
    {
        printNum = allocInfo.depth+1;
        fprintf(trace_fp, "\n    "); 
    }    
    fprintf(trace_fp, " [value:%d; cost1:%d; cost2:%.1f] ", allocInfo.Combin.value, allocInfo.Combin.cost1, allocInfo.Combin.cost2);  
    PrintArrayToFile(trace_fp, allocInfo.Combin.combinId, printNum);
}

void PrintArrayToFile(FILE* fp, int array[], int printLen)
{
    int i;
    for ( i=0; i<printLen; i++) 
    {
        fprintf(fp, "%d ", array[i]);
    }    
    //fprintf(fp, "\n");
}


void HeapUpdateTop(TopList_T* topList, CombinStat_T* Obj)
{
    memcpy(&topList->List[0], Obj, sizeof(CombinStat_T));
    MinHeapify(topList, 0);
}

/***********************************************************
Realize smallest priority queue with the element type is CombinStat_T
************************************************************/
void MinHeapify(TopList_T* topList, int current)
{
    int LeftChild;
    int RightChild;
    int smallest = current;

    LeftChild = LEFT(current);
    RightChild = RIGHT(current);

    if ((LeftChild < topList->size) && (topList->List[current].value > topList->List[LeftChild].value))
    {
        smallest = LeftChild;
    }

    if ((RightChild < topList->size) && (topList->List[smallest].value > topList->List[RightChild].value))
    {
        smallest = RightChild;
    }

    if(current != smallest)
    {
        SwapCombinStats(&topList->List[current], &topList->List[smallest]);

        MinHeapify(topList, smallest);
    }
}


void HeapPop(TopList_T* topList)
{
    memcpy(&topList->List[0], &topList->List[topList->size-1], sizeof(CombinStat_T));
    topList->size --;
    MinHeapify(topList, 0);
}

void HeapPush(TopList_T* topList, CombinStat_T* Obj)
{
    int current;
    int parent;
    memcpy(&topList->List[topList->size], Obj, sizeof(CombinStat_T));
    topList->size ++;

    current = topList->size -1;
    while(current >= 1)
    {
        parent = PARENT(current);
        if (topList->List[current].value < topList->List[parent].value)
        {
            SwapCombinStats(&topList->List[current], &topList->List[parent]);
            current = parent;
        }
        else
        {
            break;
        }
    }
}

/***********************************************************
Swap combinId Status
************************************************************/
void SwapCombinStats(CombinStat_T* Obj1, CombinStat_T* Obj2)
{
    CombinStat_T Temp;
    memcpy(&Temp, Obj1, sizeof(CombinStat_T));
    memcpy(Obj1, Obj2, sizeof(CombinStat_T));
    memcpy(Obj2, &Temp, sizeof(CombinStat_T));
}




