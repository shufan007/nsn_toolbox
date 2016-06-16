/************************************************************************************
       [Header File:] Header File
       Function:       Common definations for Resource Model Test set
       Author:         Fan, Shuangxi (Nokia - CN/Hangzhou)
       Date:           2015-3-14

 ************************************************************************************/

/***************************************************
 Constant definitions
***************************************************/
#define TOP_LIST_SIZE        60

#define NumOfTti_C              2      //2msTti, 10msTti
#define NumOfTotalResource_C  3  //2msTti, 10msTti, 2ms(OneHarq)

#define MaxNumOfTbs_C      17
#define MaxNumOfSf_C         8
#define MaxNumOfBase_C    (MaxNumOfTbs_C * MaxNumOfSf_C)
#define MaxNumOfUes_C      80

#define MARK_LEN               20

/***************************************************/
typedef struct{
    int r99Service;
    int r99UeNum;    
    int upaTtiType;
    int upaUeNum;
    int upaUeNumStart;   
    int upaUeNumStep;
    int upaUeNumEnd;
    char ServiceStr[5*MARK_LEN];
}Service_T;


typedef struct {
   int sfIndex;
   int tbIndex;
   int ttiIndex;
} Channel_T;


//struct of Combination Status
typedef struct {
   int    value; 
   int    cost1;  
   float cost2;  
   int    combinId[MaxNumOfUes_C+1]; 
}CombinStat_T;

typedef struct {
   int size;
   CombinStat_T List[TOP_LIST_SIZE]; 
}TopList_T; 

typedef struct {
   int              r_value;  //resource value
   float           c_value;  //constraint value
   Channel_T   channel; 
}ResourceStat_T;


typedef struct {
    char          ResourceTypeMark[MARK_LEN];
    int            MipsBase[MaxNumOfBase_C];
    float         CEBase[MaxNumOfBase_C];
    Channel_T ChannelTable[MaxNumOfBase_C];
    int            numOfChannelType;
    int            totalMips;
    float         totalCE;
}DataBase_T;

        
typedef struct{
    int    caseNum;  
    int    caseKinds;    
    int    Values[MaxNumOfBase_C]; 
    int    Costs1[MaxNumOfBase_C]; 
    float Costs2[MaxNumOfBase_C];
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
void CombinationSearch(const Knapsack_T*, TopList_T*);

//=====================================================


