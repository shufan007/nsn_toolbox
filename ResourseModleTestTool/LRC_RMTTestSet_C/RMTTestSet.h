/************************************************************************************
       [Header File:] Header File
       Function:       Common definations for Resource Model Test set
       Author:         Fan, Shuangxi (Nokia - CN/Hangzhou)
       Date:           2015-3-14

 ************************************************************************************/

/***************************************************
 Constant definitions
***************************************************/

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


