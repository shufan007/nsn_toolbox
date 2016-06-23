/************************************************************************************
       [Header File:] Header File
       Function:       Common definations for Knapsack Combination Search
       Author:         Fan, Shuangxi (Nokia - CN/Hangzhou)
       Date:           2015-3-14

 ************************************************************************************/

/***************************************************
 Constant definitions
***************************************************/
#define TOP_LIST_SIZE    60     // set your TOP_LIST_SIZE

#define MaxCaseKinds      17*8   // set your MaxCaseKinds

//#define MaxCaseKinds      100   // set your MaxCaseKinds
#define MaxCaseNum       100   // set your MaxCaseNum

/***************************************************/

//struct of Combination Status
typedef struct {
   int    value; 
   int    cost1;  
   float cost2;  
   int    combinId[MaxCaseNum+1]; 
}CombinStat_T;

typedef struct {
   int size;
   CombinStat_T List[TOP_LIST_SIZE]; 
}TopList_T; 

        
typedef struct{
    int    caseNum;  
    int    caseKinds;    
    int    Values[MaxCaseKinds]; 
    int    Costs1[MaxCaseKinds]; 
    float Costs2[MaxCaseKinds];
    int    limitCost1;
    int    limitCost2;    
}Knapsack_T;


/* ******************************************************************
    Function prototypes
    
******************************************************************** */

void HeapPop(TopList_T* );

/*********************************************************************
[Problem Description:]
 - Combinatorial optimization problem --> resource allocation model
    *  Properties of Knapsack_T: 
        caseNum:         number of cases
        caseKinds:        kind number of cases
        Values: {v_j }   value of the cases
        Costs1: {c1_j}  cost1 of the cases
        Costs2: {c2_j}  cost2 of the cases
        limitOfTotalCost1:  limit value of total cost1
        limitOfTotalCost2:  limit value of total cost2
        x_i:                 resource consumption of user  i
        (Here,  caseNum and caseKinds indicate the input size of the problem.)

    * Constraint Equation:
        object:  max(Sum(v_i)) (i = 1 ,2,......, caseNum)
            s.t
        Sum(c1_i)<= limitOfTotalCost1  (for c1_i in Costs1)
        Sum(c2_i)<= limitOfTotalCost2  (for c2_i in Costs2)
        (The object can also be the top K list)
**********************************************************************/
void KnapsackCombinationSearch(const Knapsack_T*, TopList_T*);

//=====================================================


