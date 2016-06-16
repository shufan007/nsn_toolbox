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

//=================================================
/***************************************************
 Global Defination
***************************************************/
#define RESOURCE_TYPE_NUM  2   //Codec; Rake;
#define CLOCK_PER_SEC (1000)

const int  Argc_C  =  6;

/***********************************************************/
const char ResourceTypeStr[RESOURCE_TYPE_NUM][MARK_LEN] = {"Codec", "Rake"};

const char TotalResourceTtiType [NumOfTotalResource_C][MARK_LEN] = {"2msTti", "10msTti", "2ms(OneHarq)"};

const float Benchmark_value = 1920;
const float Benchmark_mips  = 1920;
const float Benchmark_ce     = 192;

const int   TotalMips[RESOURCE_TYPE_NUM][NumOfTotalResource_C] = {
          /* 2msTti,  10msTti, 2msOneHarq*/
            {1920,       1920,        12800}, /* Codec,  12800 = 160*80 */
            {1920,       1920,         7680}}; /* Rake,    7680 = 96*80  */
            
            
const float TotalCEs[RESOURCE_TYPE_NUM][NumOfTotalResource_C] = {
          /* 2msTti,  10msTti, 2msOneHarq*/
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
void DataInit(TopList_T[] , TopList_T*);
void ResourceStatSort(ResourceStat_T* , const int );
void  CollectResourceInfo( const int );
void AdjustTotalResource();
void SwapResourceStats(ResourceStat_T* , ResourceStat_T* );
void TempTopListInit(TopList_T[]);
void TopListInit(TopList_T*);
void KnapsackInit();
void TopListMerge(TopList_T[], TopList_T*);
void TopListPrint(TopList_T * );
void FilesHeaderPrint(int);
void PrintCombinStat(CombinStat_T*);

/* ******************************************************************
    Main Function of Test Set Generator
    
******************************************************************** */
DataBase_T    g_DataBase;
Knapsack_T    knapsack[NumOfTti_C]; 
Service_T       service;
int                resourceType;
FILE *           topList_fp = NULL;
    
/******************************************************************** */
int main(int argc, char* argv[])
{
    int start = clock();
    
    if(Argc_C != argc)
    {
        UsageDisplay(argv[0]);
    }
    else
    {                       
        ServiceInit(argc, argv);
                  
        TestSetGeneratorMainFlow();   
        
        printf(" * Take Time: %f seconds.\n", (double)(clock()-start)/CLOCK_PER_SEC);    
    }
    
    return 0;
}


void ServiceInit(int argc, char** argv)
{
    int i;
    
    service.r99Service   = atoi(argv[1]);
    service.r99UeNum   = atoi(argv[2]);

    service.totalUeNum = 0;
    for (i = 0; i<NumOfTotalResource_C; i++)
    {
        service.numOfUpaUes[i] = atoi(argv[3+i]);
        assert(service.numOfUpaUes[i] < MaxNumOfUes_C);

        if (service.numOfUpaUes[i] >0)
        {
            service.totalUeNum += service.numOfUpaUes[i];
            service.validUeNum[i%NumOfTti_C] = service.numOfUpaUes[i];
            sprintf(service.serviceArray[i%NumOfTti_C], "%dxHSUPA%s", 
                    service.numOfUpaUes[i], TotalResourceTtiType[i]);           
        }
    }  
    assert(service.r99Service < sizeof(R99ServiceType)/(MARK_LEN*2));  
    
}
        

void TestSetGeneratorMainFlow()
{
    int i, ttiType;

    TopList_T   tempTopList[NumOfTti_C];    
    TopList_T   topList;         
    
    GetTopListFile();    
    
    for( resourceType = 0; resourceType<RESOURCE_TYPE_NUM; resourceType++)    // Codec, Rake
    {  
        DataInit(tempTopList, &topList);
    
        for (ttiType = 0; ttiType<NumOfTti_C; ttiType++)
        {                        
            CombinationSearch(&knapsack[ttiType], &tempTopList[ttiType]);  
            
            /*
            for(i = 0; i< tempTopList[ttiType].size; i++)
            {
                fprintf(topList_fp, " tempTopList[%d][%d]:%d\n", ttiType, i, tempTopList[ttiType].List[i]);
            }
            fprintf(topList_fp, "------------------------\n");
            */
        }

        TopListMerge(tempTopList, &topList);
       
        TopListPrint(&topList);
        
    }
    
    fclose(topList_fp);
}


void GetTopListFile()
{
    char topFileName[6*MARK_LEN]; 
    
    GetServiceStr();
    
    sprintf(topFileName, "Top%d_%s.txt", TOP_LIST_SIZE, service.ServiceStr);
    
    topList_fp = fopen(topFileName, "w"); 
    assert( topList_fp != NULL);
    fprintf(topList_fp, " * service: %s\n", service.ServiceStr);     
}

void GetServiceStr()
{
    int i;
    char TempStr[3*MARK_LEN] = {'\0'};
    service.ServiceStr[0] = '\0';
   
    for (i = 0; i<NumOfTti_C; i++)
    {
        if ('\0' != service.ServiceStr[0])
        {
            sprintf(TempStr, "+");
        }
        strcat(service.ServiceStr, TempStr);
        sprintf(TempStr, "%s", service.serviceArray[i]);
        strcat(service.ServiceStr, TempStr);    
    }

    if(service.r99UeNum>0)
    {
        sprintf(TempStr, "+%dx(%s)", service.r99UeNum, R99ServiceType[service.r99Service] );
        strcat(service.ServiceStr, TempStr);        
    }  
     
    printf("\n * service:  %s\n", service.ServiceStr);
    
}


void DataInit(TopList_T tempTopList[], TopList_T * topList)
{
    int  ttiType;
    
    AdjustTotalResource();
        
    for (ttiType = 0; ttiType<NumOfTotalResource_C; ttiType++)
    {
        if ( 0 != service.numOfUpaUes[ttiType]) 
        {
            CollectResourceInfo(ttiType);
        }
    }
    
    KnapsackInit();
    TopListInit(topList);
    TempTopListInit(tempTopList);    
}


/***********************************************************
AdjustTotalResource: Remove R99 Resource
************************************************************/
void AdjustTotalResource()
{
    int  i, ttiType;
    float  CE_Unit = R99CeUnits[service.r99Service];
    float  R99CE = CE_Unit * service.r99UeNum;
    int     totalMips, totalCE;

    if (R99CE - ((int)(R99CE /2))*2 >0)
    {
        //R99CE = ((int)(R99CE /2))*2 + 2;
        R99CE = ((int)(R99CE /2))*2;
    }

    memcpy(&g_DataBase.ResourceTypeMark, ResourceTypeStr[resourceType], MARK_LEN);
    
    for (i = 0; i<NumOfTotalResource_C; i++)
    {
        if (service.numOfUpaUes[i]>0)
        {
            ttiType = i%NumOfTti_C;

            g_DataBase.normalRate[ttiType].valueRate = Benchmark_value/TotalMips[resourceType][i];
            g_DataBase.normalRate[ttiType].mipsRate = Benchmark_mips/TotalMips[resourceType][i];
            g_DataBase.normalRate[ttiType].ceRate     = Benchmark_ce/TotalCEs[resourceType][i];
            
            totalMips = TotalMips[resourceType][i];
            totalCE = TotalCEs[resourceType][i];
            
            g_DataBase.totalCE[ttiType] = totalCE - (float)R99CE /g_DataBase.normalRate[ttiType].ceRate;
            g_DataBase.totalMips[ttiType] = (totalMips * g_DataBase.totalCE[ttiType])/totalCE; 

            //DivideTotalResource
            g_DataBase.totalCE[ttiType] = g_DataBase.totalCE[ttiType]*service.numOfUpaUes[i]/service.totalUeNum;
            g_DataBase.totalMips[ttiType] = g_DataBase.totalMips[ttiType]*service.numOfUpaUes[i]/service.totalUeNum; 
        }             
    }        
}



/********************************************************************
* CollectResourceInfo: preprocess of Resource metrix, 2 dimension -> 1 dimension
* return: resourceNum
*********************************************************************/
void CollectResourceInfo( const int ttiType)
{
    int  i;    
    int sfIndex, tbIndex;
    int ttiIndex = ttiType%NumOfTti_C;
    int resourceNum = 0;  
    ResourceStat_T ResourceStat[MaxNumOfBase_C];   
           
    for( sfIndex=0; sfIndex<MaxNumOfSf_C; sfIndex++)
    {
        for( tbIndex =0; tbIndex<MaxNumOfTbs_C; tbIndex++)
        {
            if (MipsMatrix[resourceType][ttiType][tbIndex][sfIndex] >0)   // if the value is non-zero, collect the values
            {
                ResourceStat[resourceNum].r_value = MipsMatrix[resourceType][ttiType][tbIndex][sfIndex];
                ResourceStat[resourceNum].c_value = ChannelElement[ttiIndex][sfIndex];
                ResourceStat[resourceNum].channel.sfIndex = sfIndex;
                ResourceStat[resourceNum].channel.tbIndex = tbIndex;
                ResourceStat[resourceNum].channel.ttiIndex = ttiIndex;
                resourceNum ++;
            }
        }
    }
    
    ResourceStatSort(ResourceStat, resourceNum);        
    g_DataBase.numOfChannelType[ttiIndex] = resourceNum;
    for( i=0; i<resourceNum; i++)
    {
        g_DataBase.MipsBase[ttiIndex][i] = ResourceStat[i].r_value;
        g_DataBase.CEBase[ttiIndex][i] = ResourceStat[i].c_value;
        memcpy(&g_DataBase.ChannelTable[ttiIndex][i], &ResourceStat[i].channel, sizeof(Channel_T));
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

void KnapsackInit()
{
    int  ttiType;               
    for (ttiType = 0; ttiType<NumOfTti_C; ttiType++)
    {
        knapsack[ttiType].caseNum = service.validUeNum[ttiType];
        knapsack[ttiType].caseKinds = g_DataBase.numOfChannelType[ttiType];
        memcpy(&knapsack[ttiType].Values, &g_DataBase.MipsBase[ttiType], sizeof(int)*MaxNumOfBase_C);
        memcpy(&knapsack[ttiType].Costs1, &g_DataBase.MipsBase[ttiType], sizeof(int)*MaxNumOfBase_C);
        memcpy(&knapsack[ttiType].Costs2, &g_DataBase.CEBase[ttiType], sizeof(float)*MaxNumOfBase_C);
        knapsack[ttiType].limitCost1 = g_DataBase.totalMips[ttiType];
        knapsack[ttiType].limitCost2 = g_DataBase.totalCE[ttiType];
                    
    } 
}

void TempTopListInit(TopList_T tempTopList[])
{   
    int ttiType;
    for (ttiType = 0; ttiType<NumOfTti_C; ttiType++)
    {                           
        TopListInit(&tempTopList[ttiType]);
    }
}

/***********************************************************
TopListInit: Initialize the topList Queueint
************************************************************/ 
void TopListInit(TopList_T* topList)
{
    memset(topList, 0, sizeof(TopList_T));

    topList->size = TOP_LIST_SIZE;   
}

void TopListMerge(TopList_T tempTopList[], TopList_T * topList)
{
    int i, ttiType; 
    int tempTopListIndex[NumOfTti_C] = {0};
    int index = 0;
    int maxIndex = 1;
    int combinListAddr;
    int updateFlag = 1;

    CombinStat_T tempCombinStat;
    
    for (ttiType = 0; ttiType<NumOfTti_C; ttiType++)
    {
        while (tempTopList[ttiType].size > 0 && tempTopList[ttiType].List[0].value <= 0)
        {
            HeapPop(&tempTopList[ttiType]);
        }          
        maxIndex *= tempTopList[ttiType].size;
    } 
        
    while(index < maxIndex) 
    {
        tempCombinStat.value = 0;        
        combinListAddr = 0;
        for (ttiType = 0; ttiType<NumOfTti_C; ttiType++)
        {
            tempCombinStat.value += (int)tempTopList[ttiType].List[tempTopListIndex[ttiType]].value * g_DataBase.normalRate[ttiType].valueRate;
            
            memcpy(&tempCombinStat.combinId[combinListAddr],
                        &tempTopList[ttiType].List[tempTopListIndex[ttiType]].combinId[0], 
                        sizeof(int)*service.validUeNum[ttiType]);
            
            combinListAddr += service.validUeNum[ttiType];    
        }
             
        if(tempCombinStat.value > topList->List[0].value)
        {
            HeapUpdateTop(topList, &tempCombinStat);
        }
        
        ttiType = 0;
        tempTopListIndex[ttiType] += 1;
                       
        if (tempTopListIndex[ttiType] == tempTopList[ttiType].size)
        {
            tempTopListIndex[ttiType] = 0;
            ttiType++;
            tempTopListIndex[ttiType] += 1;                        
        }
        
        index ++;
    }
    
}



void TopListPrint(TopList_T * topList)
{
    while (topList->size > 0 && topList->List[0].value <= 0)
    {
        HeapPop(topList);
    }

    FilesHeaderPrint(topList->size);
    printf("    Get The Top %d List. \n", topList->size);
    
    while (topList->size > 0 && topList->List[0].value >0)
    {    
        PrintCombinStat(&topList->List[0]);
        fprintf(topList_fp, "\n");
        
        HeapPop(topList);
    }    
}

void FilesHeaderPrint(int topListSize)
{  
    int i;  
    int ttiType;
    
    fprintf(topList_fp, "\n[ * %s *  Top %d List]\n", g_DataBase.ResourceTypeMark, topListSize);
    
    fprintf(topList_fp, "[Total Resource:] ", g_DataBase.ResourceTypeMark);    
    for (ttiType = 0; ttiType<NumOfTti_C; ttiType++)
    {
        fprintf(topList_fp, " %s -> Mips: %d, CE: %.1f; ", service.serviceArray[ttiType],
                g_DataBase.totalMips[ttiType], g_DataBase.totalCE[ttiType]); 
    }
    
    fprintf(topList_fp, "\n < SF Types -> ");
    for( i=0; i< MaxNumOfSf_C-1; i++)
    {
        fprintf(topList_fp, "%s, ", SfStringsTbl[i]);
    } 
    
    fprintf(topList_fp, "%s>\n", SfStringsTbl[MaxNumOfSf_C-1]);
}

void PrintCombinStat(CombinStat_T* CombinStatPtr)
{
    int  ttiType, i;
    int SfDistribution[NumOfTti_C][MaxNumOfSf_C] = {0};
    int Values[NumOfTti_C] = {0};
    float CEs[NumOfTti_C]   = {0};
    int  sfIndex;
    int combinListAddr = 0;

    fprintf(topList_fp, " Normalized value: %d ", CombinStatPtr->value);
    
    for (ttiType = 0; ttiType<NumOfTti_C; ttiType++)
    {           
        for( i= 0; i< service.validUeNum[ttiType]; i++)
        {
            sfIndex = g_DataBase.ChannelTable[ttiType][CombinStatPtr->combinId[combinListAddr+i]].sfIndex;  
            
            SfDistribution[ttiType][sfIndex]++;

            Values[ttiType] += knapsack[ttiType].Values[CombinStatPtr->combinId[combinListAddr+i]];
            CEs[ttiType]     += knapsack[ttiType].Costs2[CombinStatPtr->combinId[combinListAddr+i]];   

            //fprintf(topList_fp, "%d, ", knapsack[ttiType].Values[CombinStat->Combin[combinListAddr+i]]);
        }
        combinListAddr += service.validUeNum[ttiType];
    }
    
    for (ttiType = 0; ttiType<NumOfTti_C; ttiType++)
    {             
        fprintf(topList_fp, " [%s -> Mips: %d, CE: %.1f; ",  service.serviceArray[ttiType], Values[ttiType], CEs[ttiType] );
         
        fprintf(topList_fp, "Distribution(SF):");
            
        for( i=0; i< MaxNumOfSf_C; i++)
        {
            fprintf(topList_fp, " %d,",  SfDistribution[ttiType][i]);
        } 
        
        fprintf(topList_fp, "]");   
    }
        
    fprintf(topList_fp, "] Combination(ttiIndex; sfIndex; tbSize;) => ");
    
    combinListAddr = 0;
    for (ttiType = 0; ttiType<NumOfTti_C; ttiType++)
    {
        for( i= 0; i< service.validUeNum[ttiType]; i++)
        {
            fprintf(topList_fp, "%d; %d; %d; ",
            g_DataBase.ChannelTable[ttiType][CombinStatPtr->combinId[combinListAddr+i]].ttiIndex,
            g_DataBase.ChannelTable[ttiType][CombinStatPtr->combinId[combinListAddr+i]].sfIndex,
            TbSizesTbl[ttiType][g_DataBase.ChannelTable[ttiType][CombinStatPtr->combinId[combinListAddr+i]].tbIndex]);            
        }        
        combinListAddr += service.validUeNum[ttiType];
    }
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
    
    for(i=0; i<NumOfTotalResource_C; i++)
    {
        printf("    [%d] Number of UPA %s Ues\n", 3+i, TotalResourceTtiType[i]);
    }       
  
    printf(" * @Example: %s 0 0 10 20 0\n", exeFilePath);
    printf(" * Output: \n");
    printf("       A file named Topxxx.txt, the top list of the test set combinations.\n");
    printf("-------------------------------------------\n");
}




