/************************************************************************************
       Function:       Main of the LRC Resource Model Test set Generator
       Author:         Fan, Shuangxi (Nokia - CN/Hangzhou)
       Date:           2015-3-20
 ************************************************************************************/
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<assert.h>
#include<time.h>
#include "RMTTestSet.h"
#include "KnapsackCombinationSearch.h"

/***************************************************
 Global Defination
***************************************************/
#define RESOURCE_TYPE_NUM  2   //Codec; Rake;

#define CLOCK_PER_SEC (1000)

const int  minArgc   =  5;
const int  maxArgc  =  7;

/***********************************************************/
const char ResourceTypeStr[RESOURCE_TYPE_NUM][MARK_LEN] = {"Codec", "Rake"};

const char TtiType [NumOfTotalResource_C][MARK_LEN] = {"2msTti", "10msTti", "2ms(OneHarq)"};

const int   TotalMips[RESOURCE_TYPE_NUM][NumOfTotalResource_C] = {
          /* 2msTti,  10msTti, 2ms(OneHarq)*/
            {1920,       1920,        12800}, /* Codec,  12800 = 160*80 */
            {1920,       1920,         7680}}; /* Rake,    7680 = 96*80  */            
            
const float TotalCEs[RESOURCE_TYPE_NUM][NumOfTotalResource_C] = {
          /* 2msTti,  10msTti, 2ms(OneHarq)*/
            {192,       192,        1536}, /* Codec,  1536 = 192*8 */
            {192,       192,        1536}};/* Rake,   1536 = 192*8  */                 
            
/* Consumed Resource Units of R99 service, use R99Index to get the choice. */
const float R99CeUnits[] = {
            1.6,    //AMR(12.2kbps)
            2,        //UL UDI 32k + DL32k            
            4       //UL AMR12.2k + Packet(UL64k_DL64k)
                };

const char R99ServiceType [][MARK_LEN*2] = {
            "AMR(12.2k)",
            "UL_UDI32k+DL32k",                
            "UL_AMR12.2k+Packet(UL64k_DL64k)"
            };

const char *SfStringsTbl[MaxNumOfSf_C] =
          {"ccrs", "SF32", "SF16", "SF8", "SF4", "2xSF4", "2xSF2", "2xSF4+2xSF2"};

const int TbSizesTbl[NumOfTti_C][MaxNumOfTbs_C]={
          {0, 52,   132, 153, 292, 335,  699,   760, 1202, 1426, 2433, 2881,   4895,   5786,  7000,   8172,  11598}, // 2ms TTI
          {0, 172, 372, 426, 772, 881, 1572, 1790, 3608, 6120, 7240, 12270, 14484, 18780, 20000, 20001, 20002}}; // 10ms TTI


const float ChannelElement[NumOfTti_C][MaxNumOfSf_C] = {
    /* ccrs,  SF32, SF16, SF8,    SF4,   2xSF4,  2xSF2, 2xSF4+2xSF2*/
    {    0,      0,      0,     10,    19.2,     32,     64,      96 },  /* 2ms TTI */
    {    0,      2.4,   5,     10,    19.2,     32,     64,       0  },  /* 10ms TTI */
}; 

const int MipsMatrix[RESOURCE_TYPE_NUM][NumOfTotalResource_C][MaxNumOfTbs_C][MaxNumOfSf_C]={
    /* DecoderMips */
    { 
          /* 2ms TTI */
          /*  ccrs,   SF32, SF16, SF8, SF4, 2xSF4, 2xSF2, 2xSF4+2xSF2*/
          { {   0,     0,       0,      0,     0,     0,       0,      0  }, //0
            {    0,     24,     0,      0,     0,     0,       0,      0  }, //52
            {    0,     0,     26,      0,     0,     0,       0,      0  }, //132
            {    0,     24,     0,      0,     0,     0,       0,      0  }, //153
            {    0,     0,      0,      96,    0,     0,       0,      0  }, //292
            {    0,     0,      26,     0,     0,     0,       0,      0  }, //335
            {    0,     0,      0,      96,   130,   0,       0,      0  }, //699
            {    0,     0,      0,      0,     130,   0,      0,      0  }, //760
            {    0,     0,      0,      0,     150,   0,      0,      0  }, //1202
            {    0,     0,      0,      0,     173,  173,    0,      0  }, //1426
            {    0,     0,      0,      0,     0,     193,    0,      0  }, //2433
            {    0,     0,      0,      0,     0,     223,   223,    0  }, //2881
            {    0,     0,      0,      0,     0,      0,     253,    0  }, //4895
            {    0,     0,      0,      0,     0,      0,     293,   293 }, //5786
            {    0,     0,      0,      0,     0,      0,       0,    323 }, //7000
            {    0,     0,      0,      0,     0,      0,       0,    353 }, //8172
            {    0,     0,      0,      0,     0,      0,       0,    383 }},//11598

            
          /* 10ms TTI */
          /*ccrs,  SF32, SF16, SF8, SF4, 2xSF4, 2xSF2, 2xSF4+2xSF2*/
        { {   0,     0,      0,     0,      0,     0,         0,       0 },//0
          {    0,     0,      0,     0,      0,     0,         0,       0 },//172
          {    0,    24,     0,     0,      0,     0,         0,       0 },//372
          {    0,     0,      0,     0,      0,     0,         0,       0 },//426
          {    0,     0,     24,     0,      0,     0,         0,      0 },//772
          {    0,    24,     0,     0,      0,     0,         0,       0 },//881
          {    0,     0,      0,    40,      0,     0,         0,      0 },//1572
          {    0,     0,     26,     0,     48,    0,         0,      0 },//1790
          {    0,     0,      0,    42,     50,    0,         0,      0 },//3608
          {    0,     0,      0,     0,     54,    0,         0,       0 },//6120
          {    0,     0,      0,     0,     58,    58,        0,      0 },//7240
          {    0,     0,      0,     0,      0,     68,       0,       0 },//12270
          {    0,     0,      0,     0,      0,     76,      76,      0 },//14484
          {    0,     0,      0,     0,      0,     0,        95,      0 },//18780
          {    0,     0,      0,     0,      0,     0,        110,      0 },//20000
          {    0,     0,      0,     0,      0,     0,         0,       0 },//20001
          {    0,     0,      0,     0,      0,     0,         0,       0 }},//20002       
        
          /* 2ms TTI (one harq)*/
          /*  ccrs,   SF32, SF16, SF8, SF4, 2xSF4, 2xSF2, 2xSF4+2xSF2*/
          { {   0,     0,       0,      0,     0,     0,       0,      0  }, //0
            {    0,     24,     0,      0,     0,     0,       0,      0  }, //52
            {    0,     0,     26,      0,     0,     0,       0,      0  }, //132
            {    0,     24,     0,      0,     0,     0,       0,      0  }, //153
            {    0,     0,      0,      96,    0,     0,       0,      0  }, //292
            {    0,     0,      26,     0,     0,     0,       0,      0  }, //335
            {    0,     0,      0,      96,   130,   0,       0,      0  }, //699
            {    0,     0,      0,      0,     130,   0,      0,      0  }, //760
            {    0,     0,      0,      0,     150,   0,      0,      0  }, //1202
            {    0,     0,      0,      0,     173,   0,      0,      0  }, //1426
            {    0,     0,      0,      0,     0,      0,       0,     0  }, //2433
            {    0,     0,      0,      0,     0,      0,       0,    0  }, //2881
            {    0,     0,      0,      0,     0,      0,       0,    0  }, //4895
            {    0,     0,      0,      0,     0,      0,       0,    0 }, //5786
            {    0,     0,      0,      0,     0,      0,       0,    0 }, //7000
            {    0,     0,      0,      0,     0,      0,       0,    0 }, //8172
            {    0,     0,      0,      0,     0,      0,       0,    0 }}//11598        
    },
  
/* ReceiverMips */
    {
          /* 2ms TTI */
          /*ccrs, SF32, SF16, SF8, SF4, 2xSF4, 2xSF2, 2xSF4+2xSF2*/
        { {   0,      0,     0,     0,    0,     0,         0,     0   },//0
          {    0,     46,    0,     0,    0,     0,         0,     0   },//52
          {    0,     0,    47,     0,    0,     0,         0,     0   },//132
          {    0,     46,    0,     0,    0,     0,         0,     0   },//153
          {    0,     0,     0,     60,   0,     0,         0,     0   },//292
          {    0,     0,    47,     0,    0,     0,         0,     0   },//335
          {    0,     0,     0,     60,  96,    0,         0,     0   },//699
          {    0,     0,     0,     0,    96,    0,         0,     0   },//760
          {    0,     0,     0,     0,    96,    0,         0,     0   },//1202
          {    0,     0,     0,     0,    96,   123,       0,    0   },//1426
          {    0,     0,     0,     0,     0,    123,      0,     0   },//2433
          {    0,     0,     0,     0,     0,    123,     225,   0   },//2881
          {    0,     0,     0,     0,     0,     0,       225,   0   },//4895
          {    0,     0,     0,     0,     0,     0,       225,   383 },//5786
          {    0,     0,     0,     0,     0,     0,         0,    383  },//7000
          {    0,     0,     0,     0,     0,     0,         0,    383  },//8172
          {    0,     0,     0,     0,     0,     0,         0,    383  }},//11598

          /* 10ms TTI */
          /*ccrs, SF32, SF16, SF8, SF4, 2xSF4, 2xSF2, 2xSF4+2xSF2*/
        { {  0,      0,      0,     0,    0,      0,        0,     0  },//0
          {   0,      0,      0,     0,    0,      0,        0,     0  },//172
          {   0,     24,     0,     0,    0,      0,        0,     0  },//372
          {   0,      0,      0,     0,    0,      0,        0,     0  },//426
          {   0,      0,     33,    0,    0,      0,        0,     0  },//772
          {   0,     24,     0,     0,    0,      0,        0,     0  },//881
          {   0,      0,      0,   48,    0,      0,        0,     0  },//1572
          {   0,      0,     33,    0,   60,     0,        0,     0  },//1790
          {   0,      0,      0,   48,   60,     0,        0,     0  },//3608
          {   0,      0,      0,    0,   60,      0,        0,     0  },//6120
          {   0,      0,      0,    0,   60,     80,       0,     0  },//7240
          {   0,      0,      0,    0,    0,      80,       0,     0  },//12270
          {   0,      0,      0,    0,    0,      80,      120,   0  },//14484
          {   0,      0,      0,    0,    0,      0,        120,    0  },//18780
          {   0,      0,      0,    0,    0,      0,        120,    0  },//20000
          {   0,      0,      0,    0,    0,      0,         0,     0  },//20001
          {   0,      0,      0,    0,    0,      0,         0,     0  }},//20002

          /* 2ms TTI (one harq)*/
          /*ccrs, SF32, SF16, SF8, SF4, 2xSF4, 2xSF2, 2xSF4+2xSF2*/
        { {   0,      0,     0,     0,    0,     0,         0,     0   },//0
          {    0,     46,    0,     0,    0,     0,         0,     0   },//52
          {    0,     0,    47,     0,    0,     0,         0,     0   },//132
          {    0,     46,    0,     0,    0,     0,         0,     0   },//153
          {    0,     0,     0,     60,   0,     0,         0,     0   },//292
          {    0,     0,    47,     0,    0,     0,         0,     0   },//335
          {    0,     0,     0,     60,  96,    0,         0,     0   },//699
          {    0,     0,     0,     0,    96,    0,         0,     0   },//760
          {    0,     0,     0,     0,    96,    0,         0,     0   },//1202
          {    0,     0,     0,     0,    96,    0,         0,     0   },//1426
          {    0,     0,     0,     0,     0,     0,         0,     0   },//2433
          {    0,     0,     0,     0,     0,     0,         0,     0   },//2881
          {    0,     0,     0,     0,     0,     0,         0,     0   },//4895
          {    0,     0,     0,     0,     0,     0,         0,     0 },//5786
          {    0,     0,     0,     0,     0,     0,         0,    0  },//7000
          {    0,     0,     0,     0,     0,     0,         0,    0  },//8172
          {    0,     0,     0,     0,     0,     0,         0,    0  }}//11598       
    }
};

/* ******************************************************************
    Function prototypes
    
******************************************************************** */
void UsageDisplay(char* );
void ServiceInit(int , char** );
void TestSetGeneratorMainFlow();
void GetTopListFile();
void GetServiceStr();
void DataInit(Knapsack_T*, TopList_T* );
void ResourceStatSort(ResourceStat_T* , const int );
void CollectResourceInfo();
void AdjustTotalResource();
void SwapResourceStats(ResourceStat_T* , ResourceStat_T* );
void KnapsackInit(Knapsack_T*);
void TopListInit(TopList_T* );
void TopListPrint(TopList_T*);
void PrintHeaderInfo(int);
void PrintCombinStat(const CombinStat_T* );

/* ******************************************************************
    Main Function of Test Set Generator
    
******************************************************************** */

DataBase_T     g_DataBase;
Service_T        service;
int                 resourceType;

FILE *            topList_fp = NULL;

/******************************************************************** */
int main(int argc, char* argv[])
{  
    if((minArgc != argc) && (maxArgc != argc))
    {
        UsageDisplay(argv[0]);
    }
    else
    {        
        int start;
        
        ServiceInit(argc, argv);            
        
        while(service.upaUeNum <= service.upaUeNumEnd) 
        {            
            start = clock();
            
            TestSetGeneratorMainFlow();   
            
            printf(" * Take Time: %f seconds.\n", (double)(clock()-start)/CLOCK_PER_SEC);
            
            service.upaUeNum += service.upaUeNumStep;
        }      
    }
    
    return 0;
}


void ServiceInit(int argc, char** argv)
{  
    service.r99Service        = atoi(argv[1]);
    service.r99UeNum        = atoi(argv[2]);    
    service.upaTtiType       = atoi(argv[3]);
    service.upaUeNumStart = atoi(argv[4]);
    service.upaUeNum        = service.upaUeNumStart;
    service.upaUeNumEnd   = service.upaUeNumStart;   
    service.upaUeNumStep  = 1;  

    if (maxArgc == argc)
    {
        service.upaUeNumStep = atoi(argv[5]);
        service.upaUeNumEnd  = atoi(argv[6]);
    }
  
    assert(service.upaTtiType < NumOfTotalResource_C);
    assert(service.r99Service < sizeof(R99ServiceType)/(MARK_LEN*2));
    assert(service.upaUeNumStart <= MaxNumOfUes_C);
    assert(service.upaUeNumEnd <= MaxNumOfUes_C);  
    
}

void TestSetGeneratorMainFlow()
{
    Knapsack_T   knapsack;
    TopList_T      topList;

    GetTopListFile();
        
    for( resourceType = 0; resourceType<RESOURCE_TYPE_NUM; resourceType++)
    {
        DataInit(&knapsack, &topList); 

        KnapsackCombinationSearch(&knapsack, &topList);

        TopListPrint(&topList);
    } 
    
    fclose(topList_fp);
}


void GetTopListFile()
{
    char topFileName[6*MARK_LEN]; 
    
    GetServiceStr();
    
    sprintf(topFileName, "Top%d_%s.txt",  TOP_LIST_SIZE, service.ServiceStr);
    
    topList_fp = fopen(topFileName, "w"); 
    assert( topList_fp != NULL);
    
  
}

void GetServiceStr()
{
    char TempStr[3*MARK_LEN] = {'\0'}; 
    
    sprintf(service.ServiceStr, "%dxHSUPA%s", service.upaUeNum, TtiType[service.upaTtiType]);

    if(service.r99UeNum>0)
    {
        sprintf(TempStr, "+%dx(%s)", service.r99UeNum, R99ServiceType[service.r99Service] );
        strcat(service.ServiceStr, TempStr);
    }
           
    printf("\n * service:  %s\n\n", service.ServiceStr);
}



/***************************************************************************
* GlobalDataStatInit: preprocess of the Resource data before put them into the Searching process
*  - Init Resource Base and MipsInfo
****************************************************************************/
void DataInit(Knapsack_T* knapsack, TopList_T*  topList)
{
    
    AdjustTotalResource();     
        
    CollectResourceInfo();

    KnapsackInit(knapsack);
    
    TopListInit(topList);    
}


/***********************************************************
AdjustTotalResource: Remove R99 Resource
************************************************************/
void AdjustTotalResource()
{
    float  CE_Unit = R99CeUnits[service.r99Service];
    float  R99CE = CE_Unit * service.r99UeNum;
    int     totalMips;
    float   totalCE;

    if (R99CE - ((int)(R99CE /2))*2 >0)
    {
        //R99CE = ((int)(R99CE /2))*2 + 2;
        R99CE = ((int)(R99CE /2))*2;
    }
       
    totalMips = TotalMips[resourceType][service.upaTtiType];
    totalCE = TotalCEs[resourceType][service.upaTtiType];
    
    g_DataBase.totalCE = totalCE - R99CE;
    g_DataBase.totalMips = (totalMips * (totalCE - R99CE))/totalCE;   
    
    memcpy(&g_DataBase.ResourceTypeMark, ResourceTypeStr[resourceType], MARK_LEN);

}

/********************************************************************
* CollectResourceInfo: preprocess of Resource metrix, 2 dimension -> 1 dimension
*********************************************************************/
void CollectResourceInfo()
{
    int  i;    
    int sfIndex, tbIndex;
    int ttiIndex = service.upaTtiType % NumOfTti_C;     
    int resourceNum = 0;
    ResourceStat_T ResourceStat[MaxNumOfBase_C];   
          
    for( sfIndex=0; sfIndex<MaxNumOfSf_C; sfIndex++)
    {
        for( tbIndex =0; tbIndex<MaxNumOfTbs_C; tbIndex++)
        {
            if (MipsMatrix[resourceType][service.upaTtiType][tbIndex][sfIndex] >0)   // if the value is non-zero, collect the values
            {
                ResourceStat[resourceNum].r_value = MipsMatrix[resourceType][service.upaTtiType][tbIndex][sfIndex];
                ResourceStat[resourceNum].c_value = ChannelElement[ttiIndex][sfIndex];
                ResourceStat[resourceNum].channel.sfIndex = sfIndex;
                ResourceStat[resourceNum].channel.tbIndex = tbIndex;
                ResourceStat[resourceNum].channel.ttiIndex = ttiIndex;
                resourceNum ++;
            }
        }
    }

    ResourceStatSort(ResourceStat, resourceNum);        
    g_DataBase.numOfChannelType = resourceNum;
    
    for( i=0; i<resourceNum; i++)
    {
        g_DataBase.MipsBase[i] = ResourceStat[i].r_value;
        g_DataBase.CEBase[i] = ResourceStat[i].c_value;
        memcpy(&g_DataBase.ChannelTable[i], &ResourceStat[i].channel, sizeof(Channel_T));
    }
    
}


/***********************************************************
ResourceStat Sort: sort the 1 dimensional Resource Base
************************************************************/
void ResourceStatSort(ResourceStat_T* ResourceStat, const int size)
{
    int i, j;
    int swapFlag;

    for( i=1; i<size; i++)
    {
        swapFlag = 0;
        for( j=0; j<size-i; j++)
        {
            if (ResourceStat[j].r_value > ResourceStat[j+1].r_value)
            {
                SwapResourceStats(&ResourceStat[j], &ResourceStat[j+1]);
                swapFlag = 1;
            }
        }
        
        if (swapFlag == 0)
        {
            break;
        }
    }
}

/***********************************************************
Swap ResourceBaseStats
************************************************************/
void SwapResourceStats(ResourceStat_T* Obj1, ResourceStat_T* Obj2)
{
    ResourceStat_T Temp;
    memcpy(&Temp, Obj1, sizeof(ResourceStat_T));
    memcpy(Obj1, Obj2, sizeof(ResourceStat_T));
    memcpy(Obj2, &Temp, sizeof(ResourceStat_T));
}

void KnapsackInit(Knapsack_T* knapsack)
{
    knapsack->caseNum = service.upaUeNum;
    knapsack->caseKinds = g_DataBase.numOfChannelType;
    memcpy(&knapsack->Values, &g_DataBase.MipsBase, sizeof(int)*MaxNumOfBase_C);
    memcpy(&knapsack->Costs1, &g_DataBase.MipsBase, sizeof(int)*MaxNumOfBase_C);
    memcpy(&knapsack->Costs2, &g_DataBase.CEBase, sizeof(float)*MaxNumOfBase_C);
    knapsack->limitCost1 = g_DataBase.totalMips;
    knapsack->limitCost2 = g_DataBase.totalCE;
}

void TopListInit(TopList_T*  topList)
{
    memset(topList, 0, sizeof(TopList_T));

    topList->size = TOP_LIST_SIZE;    
}

void TopListPrint(TopList_T* topList)
{
    while (topList->size > 0 && topList->List[0].value <= 0)
    {
        HeapPop(topList);
    }
    
    printf("    Get The Top %d List. \n\n", topList->size);
    
    PrintHeaderInfo(topList->size);  
    
    while (topList->size > 0 && topList->List[0].value >0)
    {
        PrintCombinStat(&topList->List[0]);        
        HeapPop(topList);
    } 
}

void PrintHeaderInfo(int topListSize)
{  
    int i;  
    
    fprintf(topList_fp, " * Service: %s\n", service.ServiceStr);   
    
    fprintf(topList_fp, "\n[ * %s *  Top %d List ] [Total Resource -> Mips: %d, CE: %.1f]\n", 
        g_DataBase.ResourceTypeMark, topListSize, g_DataBase.totalMips, g_DataBase.totalCE);
    
    fprintf(topList_fp, "  < SF Types ->  ");
    for( i=0; i< MaxNumOfSf_C-1; i++)
    {
        fprintf(topList_fp, "%s, ", SfStringsTbl[i]);
    } 
    fprintf(topList_fp, "%s >\n", SfStringsTbl[MaxNumOfSf_C-1]);
}

void PrintCombinStat(const CombinStat_T* CombinStat)
{
    int i;
    int ttiIndex = service.upaTtiType % NumOfTti_C;
    int SfDistribution[MaxNumOfSf_C] = {0};

    for( i=0; i< service.upaUeNum; i++)
    {
        SfDistribution[g_DataBase.ChannelTable[CombinStat->combinId[i]].sfIndex]++;
    }     

    fprintf(topList_fp, "[Mips: %d; CE: %.1f; ", CombinStat->value, CombinStat->cost2);
    fprintf(topList_fp, "Distribution(SF):");
        
    for( i=0; i< MaxNumOfSf_C; i++)
    {
        fprintf(topList_fp, " %d,",  SfDistribution[i]);
    } 
    
    fprintf(topList_fp, "] Combination(ttiIndex; sfIndex; tbSize;) => ");

    for( i=0; i< service.upaUeNum; i++)
    {
        fprintf(topList_fp, "%d; %d; %d; ",
        g_DataBase.ChannelTable[CombinStat->combinId[i]].ttiIndex,
        g_DataBase.ChannelTable[CombinStat->combinId[i]].sfIndex,
        TbSizesTbl[ttiIndex][g_DataBase.ChannelTable[CombinStat->combinId[i]].tbIndex]);
    }
    
    fprintf(topList_fp, "\n"); 
}


void UsageDisplay(char* exeFilePath)
{
    int i;
    
    printf("\n----------------- Usage: ------------------\n"); 
    printf(" * [Function:] RMT test set generator.\n");
    printf(" * Input:\n");
    printf("    [1] R99 service:\n");
    for(i=0; i<sizeof(R99ServiceType)/(MARK_LEN*2); i++)
    {
        printf("          %d   %s\n", i, R99ServiceType[i]);
    }  
    printf("    [2] Number of R99 Ues\n");     
    printf("    [3] HSUPA Tti Type:\n");
    
    for(i=0; i<NumOfTotalResource_C; i++)
    {
        printf("          %d   %s\n", i, TtiType[i]);
    }       
    printf("    [4] Start Number of UPA Ues\n");
    printf("    [5] Step of UPA Ues (optional)\n"); 
    printf("    [6] End Number of UPA Ues (optional)\n");       
    
    printf(" * Note: The input parameters can be first %d, or all %d. \n", minArgc-1, maxArgc-1);
    printf(" * @Example: %s 0 40 0 30\n", exeFilePath);
    printf(" * @Example: %s 0 40 0 10 10 80\n", exeFilePath);
    printf(" * Output: \n");
    printf("       A file named Topxxx.txt, the top list of the test set combinations.\n");
    printf("-------------------------------------------\n");
}





