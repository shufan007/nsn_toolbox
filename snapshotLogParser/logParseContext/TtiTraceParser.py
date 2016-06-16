# -*- coding: utf-8 -*-
# ##############################################################################
# class TtiTrace():
# [Function]:  class for Tti Trace Decode
#       Author:         Fan, Shuangxi (NSN - CN/Hangzhou)
#       draft:          2014-10-14 
#       modify(split):  2015-11-20
#*      description:   
# ##############################################################################
#!/usr/bin/python

import os

from utils.common import CThread, creat_dictionary, debugLogSetup
from utils.CHexStrProcess import *
from utils.CBinDataConvert import *
from utils.CDictionaryFormatAdjust import *
from utils.CSyntaxParse import *
from utils.CSaveDataToXls import *
    
'''
# ##############################################################################
TODO:

1. add enum info to Tti Trace parsed data  
2. performance optimization:
   - use mmap, use slicing to read from the file
   - set struct and save the structs ectected from source file
   - record the modify time of the source file 
   - flush file
   - use array to instand some list

# ##############################################################################
'''

###################################################################   
#*  global variables defination
#  - TTI Trace Decoder paras
#  - TTI Trace Struct Name Map
###################################################################

DSP_Path = r"C_Application\SC_UP\DSP"
Time_field = ['year', 'month', 'day', 'hour', 'minute', 'second', 'millisec']

# Macro define files
DOpenIUBCommonDefs = r"I_Interface\Application_Env\Definitions\DOpenIUBCommonDefs.h"
UTxQe  = os.path.join(DSP_Path, r"ss_wcdmaenginedrivers\cp_l1transmission_nyquist\UTxQe.h")
CodecGlobalDefinitions  = r"C_Application\SC_UP\Include\Definitions\CodecGlobalDefinitions.h"

# common struct define files
STtiTraceCommonHeader =  os.path.join(DSP_Path, r"include\definitions\STtiTraceCommonHeader.h")
SSppemsgHeaderTypes =  os.path.join(DSP_Path, r"include\w1pltx_env\definitions\SSppemsgHeaderTypes.h")
TAC_msgHeaderTypes =  os.path.join(DSP_Path, r"ss_wcdmaenginedrivers\cp_l1transmission_nyquist\TAC_msgHeaderTypes.h")

# TtiTrace Files
StructFile_L1tra   = os.path.join(DSP_Path, r"SS_WcdmaEngineDrivers\CP_L1Transmission_Nyquist\L1Tra_BrowserTtiTrace.c")
StructFile_Decoder = os.path.join(DSP_Path, r"include\Codec_Env\Definitions\UDecDecoderRakeL2Trace.h")
StructFile_Encoder = os.path.join(DSP_Path, r"ss_codec\cp_codecbrowser\EncBrowser.c")
StructFile_FP      = os.path.join(DSP_Path, r"ss_commondsp\cp_tupframeprotocol\Fp_TtiTrace.h")

TtiTraceFiles = [
    
    CodecGlobalDefinitions, 
    DOpenIUBCommonDefs,
    UTxQe,
    
    STtiTraceCommonHeader,
    SSppemsgHeaderTypes,
    TAC_msgHeaderTypes,
        
    StructFile_L1tra,
    StructFile_Decoder,
    StructFile_Encoder,
    StructFile_FP   
]

# Tti_Trace DumpId

Dec_dumpId          = 4
Enc_dumpId          = 5
FP_dumpId           = 6
L1TraNonHs_dumpId   = 19
L1TraHs_dumpId      = 20

Tti_Trace_DumpId = [
    Dec_dumpId, 
    Enc_dumpId, 
    FP_dumpId, 
    L1TraNonHs_dumpId, 
    L1TraHs_dumpId]

#dumpHD_segment = [16,16]

TtiTraceTypeFlag_offset  = 2
TtiTraceTypeFlag_segment = [5, 27]

# ***********************************************
#   L1Tra_TTI_TRACE 
#  - L1Tra_NonHs, Encoder
# ***********************************************

# Dic: TtiTraceTypeFlag
ETtiTraceTypeFlag = {
    11:'ENonHsTtiTrace_L1tra',
    12:'EAgchTtiTrace_L1tra',
    13:'EHichRgchTtiTrace_L1tra',
    
    14:'EHsPdschTtiTrace_L1tra',
    15:'EHsScchTtiTrace_L1tra',
    16:'EHsPdschTtiTrace_encoder',
    17:'EHsScchTtiTrace_encoder',
    
    18:'EDchFachPchTtiTrace_encoder'
    }


L1Tra_TtiTrace_Struct_Map = {
    'ENonHsTtiTrace_L1tra':         'SBitFieldNonHs',
    'EAgchTtiTrace_L1tra':          'SBitFieldAgch',
    'EHichRgchTtiTrace_L1tra':      'SBitFieldRgHi',
    
    'EHsPdschTtiTrace_L1tra':       'SBitFieldHspdsch',
    'EHsScchTtiTrace_L1tra':        'SBitFieldHsScch',
    'EHsPdschTtiTrace_encoder':     'SBitFieldHsdpaEnc',
    'EHsScchTtiTrace_encoder':      None,               # not find yet!
    
    'EDchFachPchTtiTrace_encoder':  'SBitFieldEncDchFachPchTrch'
    }

# L1Tra_TtiTrace_Enum Files:
STtiTraceCommonHeader = os.path.join(DSP_Path,r"include\definitions\STtiTraceCommonHeader.h")
ETtiTraceProtocol     = os.path.join(DSP_Path,r"include\definitions\ETtiTraceProtocol.h")
#EPhysicalChannelType.h (d:\userdata\shufan\lrc_trunk\c_application\sc_up\include\definitions)

L1Tra_TtiTrace_Enum_Map = {
    'protocol'             : 'ETtiTraceProtocol',
    #'pad':  '',
    'TtiTraceTypeFlag'     : 'ETtiTraceTypeFlag',
    'chanType'             : '',
    'physicalChannelType'  : 'EPhysicalChannelType',
    'TtiTraceTypeFlag'     : '',
    
    'cmType'               : '',
    'trchType'             : '',
    'diversityMode'        : ''
    }


# ***************************************************
#              Decoder_TTI_TRACE 
# ***************************************************
userTypeData_offset = 2
# userType(2), hour(5), minute(6), second(6), sfn(12), pad(1) 
userType_segment = [2, 5, 6, 6, 12, 1]
userType_num = 3

ETtiTraceUserType = {
    0: 'dchTrace',   # 'EUserDCH'
    1: 'edchTrace',  # 'EUserEDCH'
    2: 'rachTrace',  # 'EUserRACH'
    3: 'EUserTypeNum'
    }


Dec_TtiTrace_Struct_Map = {
    'dchTrace':         'SDecDecoderTraceDch',
    'edchTrace':        'SDecDecoderTraceEdch',
    'rachTrace':        'SDecDecoderTraceRach'
    }


# ***************************************************
#              FP_TTI_TRACE 
# ***************************************************
ETrChnType = {
    0:'ETrChnType_Undefined',
    1:'ETrChnType_DCH',
    2:'ETrChnType_FACH',
    3:'ETrChnType_PCH',
    4:'ETrChnType_RACH',    
    5:'ETrChnType_CCH',
    6:'ETrChnType_HSDSCH',
    7:'ETrChnType_EDCH'   
    }

ELinkDirection = {
    0:'ELinkDirection_Downlink',
    1:'ELinkDirection_Uplink',
    2:'ELinkDirection_Error'    
    }

ETracePoint = {
    0:'EDlRecvTracePoint',
    1:'EDlSendToEncoderTracePoint',
    2:'EUlSendToPlatTracePoint'    
    }

EEdchDataType = {
    0:'EdchTypeOne',
    1:'EdchTypeTwo',
    2:'EdchTypeTwoForCellFach'    
    }

EFrameType = {
    0:'FRAME_TYPE_DATA',
    1:'FRAME_TYPE_CONTROL'   
    }

'''
 * Taken from 3GPP TS 25.425 for Common Transport Channel, beware that there
 * are different control frame types defined for different channels.

enum FrameType
{
    FrameType_DownlinkNodeSync              = 0x06,
    FrameType_UplinkNodeSync                = 0x07,
    FrameType_HsDschCapacityRequest         = 0xA,
    FrameType_HsDschCapacityAllocationType1 = 0xB,
    FrameType_HsDschCapacityAllocationType2 = 0xC
};
'''

EFpCchCtrlFrameType = {
    1:'EFpCchCtrlFrameType_OuterLoopPowerControl', 
    2:'EFpCchCtrlFrameType_TimingAdjustment',
    3:'EFpCchCtrlFrameType_DlSynchronisation',
    4:'EFpCchCtrlFrameType_UlSynchronisation',
                                                #   /* 5 is reserved*/
    6:'EFpCchCtrlFrameType_DlNodeSynchronisation',
    7:'EFpCchCtrlFrameType_UlNodeSynchronisation',
    8:'EFpCchCtrlFrameType_DynamicPuschAssignment',
    9:'EFpCchCtrlFrameType_TimingAdvance',
    10:'EFpCchCtrlFrameType_HsDschCapacityRequest',
    11:'EFpCchCtrlFrameType_HsDschCapacityAllocationType1',
    12:'EFpCchCtrlFrameType_HsDschCapacityAllocationType2',
    13:'EFpCchCtrlFrameType_MaxNumOfCtrlFrameType'
    }

EFpDchCtrlFrameType = {
    1:'EFpDchCtrlFrameType_OuterLoopPowerControl', 
    2:'EFpDchCtrlFrameType_TimingAdjustment',
    3:'EFpDchCtrlFrameType_DlSynchronisation',
    4:'EFpDchCtrlFrameType_UlSynchronisation',
                                                 #  /* 5 is reserved*/
    6:'EFpDchCtrlFrameType_DlNodeSynchronisation',
    7:'EFpDchCtrlFrameType_UlNodeSynchronisation',
    8:'EFpDchCtrlFrameType_RxTimingDeviation',
    9:'EFpDchCtrlFrameType_RadioInterParamUpdate',
    10:'EFpDchCtrlFrameType_TimingAdvance',
    11:'EFpDchCtrlFrameType_TnlCongestionIndication',
    12:'EFpDchCtrlFrameType_MaxNumOfCtrlFrameType'
    }

'''
typedef enum EDspUlChannelEvent
{
    EDspUlChannelEvent_NoAction       = 0,
    EDspUlChannelEvent_Delete         = 1,
    EDspUlChannelEvent_ReconfigCommit = 2,
    EDspUlChannelEvent_Activate       = 3
}EDspUlChannelEvent;


typedef enum{    
    EdchTypeOne,
    EdchTypeTwo,
    EdchTypeTwoForCellFach
}EEdchDataType;

'''

# split union to DCH, CCH, EDCH
DataTable_Map = {
    'DCH': ( 'SFpTtiTraceDchDlDataFrame',
             'SFpTtiTraceDchDlToEncoderDataFrame',
             'SFpTtiTraceDchUlDataFrame',
             'SFpTtiTraceDchDlCtrlFrame',
             'SFpTtiTraceDchUlCtrlFrame'
             ),
    
    'CCH': ( 'SFpTtiTraceFachDataFrame',
             'SFpTtiTraceFachToEncoderDataFrame',
             'SFpTtiTracePchDataFrame',
             'SFpTtiTracePchToEncoderDataFrame',
             'SFpTtiTraceRachDataFrame',
             'SFpTtiTraceCchDlCtrlFrame',
             'SFpTtiTraceCchUlCtrlFrame'
             ),
    
    'EDCH': ( 'SFpTtiTraceEdchDataFrame',
              'SFpTtiTraceEdchDlCtrlFrame'
              )    
    }


FP_Union_Split_Map = {
    'UFpTtiTraceChannelCommon':   ( 'SFpTtiTraceDchCommon',
                                    'SFpTtiTraceCchCommon',
                                    'SFpTtiTraceEdchCommon')
    
    }


FP_Union_Name = 'UFpTtiTrace'


UFpTtiTrace_Map = {
    0:  'SFpTtiTraceCommon',
    
    1:  'SFpTtiTraceDchDlDataFrame',
    2:  'SFpTtiTraceDchDlToEncoderDataFrame',
    3:  'SFpTtiTraceDchUlDataFrame',
    4:  'SFpTtiTraceDchDlCtrlFrame',
    5:  'SFpTtiTraceDchUlCtrlFrame',
    
    6:  'SFpTtiTraceFachDataFrame',
    7:  'SFpTtiTraceFachToEncoderDataFrame',
    8:  'SFpTtiTracePchDataFrame',
    9:  'SFpTtiTracePchToEncoderDataFrame',
    10: 'SFpTtiTraceRachDataFrame',
    11: 'SFpTtiTraceCchDlCtrlFrame',
    12: 'SFpTtiTraceCchUlCtrlFrame',
    
    13: 'SFpTtiTraceEdchDataFrame',
    14: 'SFpTtiTraceEdchDlCtrlFrame'   
    }


# [chanType, direction, tracepoint, frameType]
FP_HD_Info_offset = 2
FP_HD_Info_segment = (4,1,4,1)


# FpTtiTrace_Info_Map: [chanType, direction, tracepoint, frameType]
FpTtiTrace_Info_Map = {
    0:  None,         # 'SFpTtiTraceCommon',
    
    1:  [1, 0,  0,      0   ],    # 'SFpTtiTraceDchDlDataFrame',
    2:  [1, 0,  1,      0   ],    # 'SFpTtiTraceDchDlToEncoderDataFrame',
    3:  [1, 1,  2,      0   ],    # 'SFpTtiTraceDchUlDataFrame',
    4:  [1, 0,  0,      1   ],    # 'SFpTtiTraceDchDlCtrlFrame',
    5:  [1, 1,  2,      1   ],    # 'SFpTtiTraceDchUlCtrlFrame',
    
    6:  [2, 0,  0,      None],    # 'SFpTtiTraceFachDataFrame',
    7:  [2, 0,  1,      None],    # 'SFpTtiTraceFachToEncoderDataFrame',
    8:  [3, 0,  0,      None],    # 'SFpTtiTracePchDataFrame',
    9:  [3, 0,  1,      None],    # 'SFpTtiTracePchToEncoderDataFrame',
    10: [4, 1,  None,   None],    # 'SFpTtiTraceRachDataFrame',
    11: [5, 0,  0,      1   ],    # 'SFpTtiTraceCchDlCtrlFrame',
    12: [5, 1,  None,   1   ],    # 'SFpTtiTraceCchUlCtrlFrame',
    
    13: [7, 1,  2,      0   ],    # 'SFpTtiTraceEdchDataFrame',
    14: [7, 0,  0,      1   ]     # 'SFpTtiTraceEdchDlCtrlFrame'   
    }
################################################################### 
       
            
# ##############################################################################
# class TtiTrace():
# [Function]:  class for Tti Trace Decode
#  1. read structs from source files 
#  2. paser all kinds of TTi Trace
#    such as: L1TraNonHs Trace;
#             L1TraHs Trace;
#             Encoder Trace;
#             Decoder Trace;
#             FP Trace
# [Methods]:
# * __init__: init all data paras being used
# * split_Common: split Trace Data by Trace Type Flag only
#   - for L1TraNonHs, L1TraHs
# * split_Encoder: split Trace Data by dumpId only
#   - for  Enc
# * split_FP:  split Trace Data by Fp TtiTrace header Info  
# * TraceData_Split: split Trace Data by header Info and Trace Type 
#   - main function to split all Tti trace data
# * get_FP_CommonStruct: get FP common struct
#   - SFpTtiTraceCommon: SFpTtiTraceDchCommon, SFpTtiTraceCchCommon, SFpTtiTraceEdchCommon   
# * get_FP_Struct: get finial FP TtiTrace Struct and Aligned Segments according to Data
#   - FP_TraceId 0 ~ 14
# * Parse_blockData: paese block data
# * Tti_Trace_Parse_All: parse all tti trace     
#   - the main function to tti trace parse
# * save_Pasered_Data: function for data saving
#   - save parsed data to .xls file 
# 
# ##############################################################################
class TtiTrace():
    
    def __init__(self, Tti_Trace_Data, dumpblock_Data_len, RTLDumpId, SourcePath, ParsedDataDir, __DEBUG_LOG__):
        self.ParsedDataDir = ParsedDataDir
        self.SourcePath = SourcePath
              
        global TtiTraceFiles
        TempFileDir = os.path.join(self.ParsedDataDir, 'temp') 
        if os.path.isdir(TempFileDir) == False:
            os.mkdir(TempFileDir)          
        self.TempFileDir = TempFileDir   
        self.__DEBUG_LOG__ = __DEBUG_LOG__   

        self.hexStr_obj = CHexStrProcess()
        self.cstructPro_obj = CStructProcess()
        # --------------- control paramaters---------------
        self.printLevel_1 = True
        self.printLevel_2 = False
        # ------------------------------------------------- 
        self.TraceData          = Tti_Trace_Data        
        self.dumpblock_Data_len = dumpblock_Data_len

        self.TtiTracedumpId = []
        self.dumpName       = []
        for i in range(0, len(self.TraceData)):
            self.TtiTracedumpId.append(int(self.TraceData[i][0][8:],16))
            self.dumpName.append(RTLDumpId[self.TtiTracedumpId[i]][RTLDumpId[self.TtiTracedumpId[i]].find('_')+1:]) 
        
        self.L1TraNonHs_TraceNum = 3
        self.L1TraNonHs_data        = [[] for i in range(0, self.L1TraNonHs_TraceNum)]
        
        self.L1TraHs_TraceNum = 4
        self.L1TraHs_data       = [[] for i in range(0, self.L1TraHs_TraceNum)]
        
        self.Enc_TraceNum = 1
        #self.Enc_data = [[] for i in range(0, Enc_TraceNum)]
        self.Enc_data       = []        
        self.Enc_Items      = []
        self.Enc_Parse_data = []
        
        self.Dec_TraceNum = 3
        self.Dec_data       = [[] for i in range(0, self.Dec_TraceNum)]
        
        self.FP_TraceNum = 15
        self.FP_data        = [[] for i in range(0, self.FP_TraceNum)]
        
        # ----------- get All struct Dic  --------------
        
        '''
        ##################################################################
        TODO:
        1. add enum info to parsed data
        2. save last pased struct
        3. save history record
           save timestemp of last files, check the timestemp of source file
           if file changed, get new struct
                       
        ##################################################################
        '''                
        for i in range(0, len(TtiTraceFiles)):
            TtiTraceFiles[i] = os.path.join(self.SourcePath, TtiTraceFiles[i])
               
        cs = CStructExtract(TtiTraceFiles, self.TempFileDir)
        cs.get_Struct_Map()
        cs.print_MapedStructDic([L1Tra_TtiTrace_Struct_Map, Dec_TtiTrace_Struct_Map])       
        
        self.All_Struct_Dic   = cs.struct_Dic
        self.All_Union_Dic    = cs.union_Dic
        
        self.L1Tra_Struct_Dic = cs.get_UnfoldStructMapbyDic(L1Tra_TtiTrace_Struct_Map)
        self.Dec_Struct_Dic   = cs.get_UnfoldStructMapbyDic(Dec_TtiTrace_Struct_Map)

        self.FP_CommonStruct_Dch  = []
        self.FP_CommonStruct_Cch  = []        
        self.FP_CommonStruct_Edch = []

        self.FP_AlignedSegment_Dch  = []
        self.FP_AlignedSegment_Cch  = []        
        self.FP_AlignedSegment_Edch = []

        self.get_FP_CommonStruct()
        
    # ###################################################################
    # split Trace Data by Trace Type  Flag only
    # for L1TraNonHs, L1TraHs
    # ###################################################################
    def split_Common(self, Data, dumpblock_Data_len):
        indx = 0
        blockNr = 0            
        while indx < len(Data)-1:
            '''
            dumpHD_str = Data[indx].strip()
            dumpId = self.hexStr_obj.word_split(dumpHD_str, dumpHD_segment, 'Little')[1]
            dumpblock_Data_len = self.dumpblock_Data_len[dumpId]
            '''
            TypeFlag_datastr = Data[indx + TtiTraceTypeFlag_offset].strip()
            TtiTraceTypeFlag = self.hexStr_obj.word_split(TypeFlag_datastr, TtiTraceTypeFlag_segment, 'Little')[0]
            
            if TtiTraceTypeFlag >= 11 and TtiTraceTypeFlag <= 13:
                self.L1TraNonHs_data[TtiTraceTypeFlag - 11].extend(Data[indx: indx + dumpblock_Data_len[blockNr]])                
            elif TtiTraceTypeFlag >= 14 and TtiTraceTypeFlag <= 17:
                self.L1TraHs_data[TtiTraceTypeFlag - 14].extend(Data[indx: indx + dumpblock_Data_len[blockNr]])
                
            indx += dumpblock_Data_len[blockNr]
            blockNr += 1
        
    # ###################################################################
    # split Trace Data by dumpId only
    # for  Enc
    # ###################################################################
    def split_Encoder(self, Data, dumpblock_Data_len):
        indx = 0
        blockNr = 0
        if self.printLevel_1 == True:
            self.__DEBUG_LOG__.debug("   Encoder Trace total data length:%d, dumpblocks data len: %s"%\
                            (len(Data), dumpblock_Data_len))

        while indx < len(Data)-1:
            self.Enc_data.extend(Data[indx: indx + dumpblock_Data_len[blockNr]])                
            indx += dumpblock_Data_len[blockNr]
            blockNr += 1
              
    # ###################################################################
    # split Trace Data by Trace Type  Flag only
    # for  Dec
    # ###################################################################
    def split_Decoder(self, Data, dumpblock_Data_len):
        
        indx = 0
        blockNr = 0
        global userTypeData_offset
        global userType_segment
        global userType_num
        
        if self.printLevel_1 == True:
            self.__DEBUG_LOG__.debug("   Decoder Trace total data length:%d, dumpblocks data len: %s"%\
                            (len(Data), dumpblock_Data_len))
            
        while indx < len(Data)-1:
            '''
            dumpHD_str = Data[indx].strip()
            dumpId = self.hexStr_obj.word_split(dumpHD_str, dumpHD_segment, 'Little')[1]
            dumpblock_Data_len = self.dumpblock_Data_len[dumpId]
            '''
            userType_datastr = Data[indx + userTypeData_offset].strip()
            userType = self.hexStr_obj.word_split(userType_datastr, userType_segment, 'Little')[0]
           
            if self.printLevel_1 == True:
                self.__DEBUG_LOG__.debug("  userType:%d"% userType) 
                
            if userType >= 0 and userType <= userType_num:                
                self.Dec_data[userType].extend(Data[indx: indx + dumpblock_Data_len[blockNr]])               
                
            indx += dumpblock_Data_len[blockNr]
            blockNr += 1
                       
    # ######################################################
    # split_FP: split Trace Data by Fp TtiTrace header Info 
    # ######################################################
    def split_FP(self, Data, dumpblock_Data_len):       
        indx = 0
        blockNr = 0
        while indx < len(Data)-1:
            dumpHD_str = Data[indx].strip()
            HD_lineInfo = self.hexStr_obj.word_split(dumpHD_str, dumpHD_segment, 'Big')
            data_len = int(HD_lineInfo[0]/4)
            dumpId = HD_lineInfo[1]
            dumpblock_Data_len = self.dumpblock_Data_len[dumpId]

            HD_Info_datastr = Data[indx + FP_HD_Info_offset].strip()
            HD_Info_data = self.hexStr_obj.word_split(HD_Info_datastr, FP_HD_Info_segment, 'Little')
            HDInfo = "   data_len: %d(u32), dumpId: %d, HD_Info_data: %s\n"% (data_len, dumpId, HD_Info_data)
            if self.printLevel_2 == True:
                self.__DEBUG_LOG__.debug(HDInfo)
            
            for i in range(0, self.FP_TraceNum):
                match_Flag = None
                if FpTtiTrace_Info_Map[i] != None:
                    #print " * FpTtiTrace_Info_Map[%d]: %s"% (i, FpTtiTrace_Info_Map[i])                    
                    for j in range(0,len(HD_Info_data)):
                        if FpTtiTrace_Info_Map[i][j] != None and HD_Info_data[j] != FpTtiTrace_Info_Map[i][j]:
                            match_Flag = 0
                            break
                    if match_Flag != 0 and j == len(HD_Info_data)-1:
                        match_Flag = 1
                if match_Flag == 1:
                    break

            matchInfo = "   FpTtiTrace_Info_Map[%02d]: %s, "% (i, FpTtiTrace_Info_Map[i])
            
            if match_Flag == 1:
                # for the dumpBlock
                #self.FP_data[i].append(Data[indx: indx + dumpblock_Data_len[blockNr]])
                # for the piece of data                
                self.FP_data[i].extend(Data[indx: indx + data_len + 1])
                matchInfo += "   FP Trace block matched.\n"                                    
            else:            
                matchInfo +=  " ** Here find one FP Trace block not match any struct!"
                matchInfo +=  "     data Indx: %d\n"% (indx)               

            if self.printLevel_2 == True:
                self.__DEBUG_LOG__.debug(matchInfo)
        
            #indx += dumpblock_Data_len[blockNr]
            indx += (data_len + 1)                                       
            #blockNr += 1        
        
    # ######################################################            
    # split Trace Data by header Info and Trace Type
    # ######################################################
    def TraceData_Split(self):
        global Dec_dumpId 
        global Enc_dumpId 
        global FP_dumpId 
        global L1TraNonHs_dumpId 
        global L1TraHs_dumpId 

        for i in range(0, len(self.TtiTracedumpId)):
            dumpId = self.TtiTracedumpId[i]
            Data = self.TraceData[i]
            if dumpId == Dec_dumpId:
                self.split_Decoder(Data, self.dumpblock_Data_len[dumpId])
            elif dumpId == Enc_dumpId:
                self.split_Encoder(Data, self.dumpblock_Data_len[dumpId])               
            elif dumpId in [L1TraNonHs_dumpId, L1TraHs_dumpId]:
                self.split_Common(Data, self.dumpblock_Data_len[dumpId])
            elif dumpId == FP_dumpId:
                self.split_FP(Data, self.dumpblock_Data_len[dumpId])
            else:
                self.__DEBUG_LOG__.warning("** dumpId error! dumpId is: %d"% dumpId)
        
    # ###################################################################
    # get FP common struct
    # SFpTtiTraceCommon,
    # SFpTtiTraceDchCommon, SFpTtiTraceCchCommon, SFpTtiTraceEdchCommon
    # ##################################################################
    def get_FP_CommonStruct(self):
        
        FP_CommonStruct = self.All_Struct_Dic['SFpTtiTraceCommon'][0:-2]        
        FP_AlignedSegment_Common = self.cstructPro_obj.get_u32SegmentFromStruct(FP_CommonStruct)
        
        FP_CommonStruct.extend(self.All_Struct_Dic['SFpTtiTraceDlCommon'])        
        FP_AlignedSegment_Common.extend(self.cstructPro_obj.get_u32SegmentFromStruct(self.All_Struct_Dic['SFpTtiTraceDlCommon']))

        AlignedSegments = self.cstructPro_obj.get_UnionAlignedSegment(self.All_Union_Dic, self.All_Struct_Dic, 'UFpTtiTraceChannelCommon')
        
        self.FP_CommonStruct_Dch.extend(FP_CommonStruct)
        self.FP_AlignedSegment_Dch.extend(FP_AlignedSegment_Common)        
        self.FP_CommonStruct_Dch.extend(self.All_Struct_Dic['SFpTtiTraceDchCommon'])
        self.FP_AlignedSegment_Dch.extend(AlignedSegments[1])
        
        self.FP_CommonStruct_Cch.extend(FP_CommonStruct)
        self.FP_AlignedSegment_Cch.extend(FP_AlignedSegment_Common)        
        self.FP_CommonStruct_Cch.extend(self.All_Struct_Dic['SFpTtiTraceCchCommon'])
        self.FP_AlignedSegment_Cch.extend(AlignedSegments[2])
        
        self.FP_CommonStruct_Edch.extend(FP_CommonStruct)
        self.FP_AlignedSegment_Edch.extend(FP_AlignedSegment_Common)        
        self.FP_CommonStruct_Edch.extend(self.All_Struct_Dic['SFpTtiTraceEdchCommon'])
        self.FP_AlignedSegment_Edch.extend(AlignedSegments[3])
        
    # ###################################################################
    # get finial FP TtiTrace Struct and Aligned Segments according to Data
    # FP_TraceId 0 ~ 14
    # ###################################################################
    def get_FP_Struct(self, FP_TraceId, Data):       
        Out_Struct = []
        Out_AlignedSegments = []
        FP_Struct_getInfo = ''
        struct_section = []

        # out put initialization
        if FP_TraceId >= 1 and FP_TraceId <= 5:
            Out_Struct.extend(self.FP_CommonStruct_Dch)
            Out_AlignedSegments.extend(self.FP_AlignedSegment_Dch)            
        elif FP_TraceId >= 6 and FP_TraceId <= 12:
            Out_Struct.extend(self.FP_CommonStruct_Cch)
            Out_AlignedSegments.extend(self.FP_AlignedSegment_Cch)            
        elif FP_TraceId >= 13 and FP_TraceId <= 14:
            Out_Struct.extend(self.FP_CommonStruct_Edch)
            Out_AlignedSegments.extend(self.FP_AlignedSegment_Edch)            
        if FP_TraceId >= 1 and FP_TraceId <= 3:            
            struct_section = self.All_Struct_Dic[UFpTtiTrace_Map[FP_TraceId]][1:]                
            Out_Struct.extend(struct_section)                       
            SegmentList = self.cstructPro_obj.get_u32SegmentFromStruct(struct_section)            
            Out_AlignedSegments.extend(SegmentList)
                           
        elif FP_TraceId == 4:
            controlFrameType_field = self.All_Struct_Dic[UFpTtiTrace_Map[FP_TraceId]][1]
            Out_Struct.append(controlFrameType_field)
            Out_AlignedSegments.append([controlFrameType_field[2]])
            (data_indx, lastSegment, lastValue) = \
                        self.cstructPro_obj.get_LastStructSegmentValueFromData(Data[1:], Out_Struct, Out_AlignedSegments)            
            controlFrameType_value =  lastValue            
            #print "     - Out_Struct: %s"% (Out_Struct)            
            FP_Struct_getInfo += "   FP_TraceId: %d, controlFrameType_value: %d"% \
                                 ( FP_TraceId, controlFrameType_value)            
            FP_Struct_getInfo += "   data_indx = %d, lastSegment = %s\n"% (data_indx, lastSegment)            
            AlignedSegments = self.cstructPro_obj.get_UnionAlignedSegment(self.All_Union_Dic, self.All_Struct_Dic, 'UFpTtiTraceDchDlCtrlFrameInfo') 
            if controlFrameType_value == 1:
                Out_Struct.extend(self.All_Struct_Dic['SFpTtiTraceDchOuterLoopPowerControl'])
                Out_AlignedSegments.extend(AlignedSegments[1])
            elif controlFrameType_value == 3:
                Out_Struct.extend(self.All_Struct_Dic['SFpTtiTraceDchDlSync'])
                Out_AlignedSegments.extend(AlignedSegments[2])                
            elif controlFrameType_value == 9:
                Out_Struct.extend(self.All_Struct_Dic['SFpTtiTraceDchRadioInterfaceParameterUpdate'])
                Out_AlignedSegments.extend(AlignedSegments[3])                
            else:
                # for temp test
                #Out_Struct.extend(self.All_Struct_Dic['SFpTtiTraceDchDlSync'])
                Out_AlignedSegments.extend(DchDlCtrl_AlignedSegments[0])                
                FP_Struct_getInfo += " ** Invalid controlFrameType value find when FP_TraceId = 4 !\n"
                                                    
        elif FP_TraceId == 5:            
            controlFrameType_field = self.All_Struct_Dic[UFpTtiTrace_Map[FP_TraceId]][1]
            Out_Struct.append(controlFrameType_field)
            Out_AlignedSegments.append([controlFrameType_field[2]])
            (data_indx, lastSegment, lastValue) = \
                        self.cstructPro_obj.get_LastStructSegmentValueFromData(Data[1:], Out_Struct, Out_AlignedSegments)            
            controlFrameType_value =  lastValue            
            #print "     - Out_Struct: %s"% (Out_Struct)            
            FP_Struct_getInfo += "   FP_TraceId: %d, controlFrameType_value: %d"% (FP_TraceId, controlFrameType_value)
            FP_Struct_getInfo += "   data_indx = %d, lastSegment = %s\n"% (data_indx, lastSegment)
            
            AlignedSegments = self.cstructPro_obj.get_UnionAlignedSegment(self.All_Union_Dic, self.All_Struct_Dic, 'UFpTtiTraceDchUlCtrlFrameInfo')            
            if controlFrameType_value == 2:
                Out_Struct.extend(self.All_Struct_Dic['SFpTtiTraceDchTimingAdjustment'])
                Out_AlignedSegments.extend(AlignedSegments[1])                
            elif controlFrameType_value == 4:
                Out_Struct.extend(self.All_Struct_Dic['SFpTtiTraceDchUlSync'])              
                Out_AlignedSegments.extend(AlignedSegments[2])                 
            else:
                # for temp test                
                #Out_Struct.extend(self.All_Struct_Dic['SFpTtiTraceDchUlSync'])
                Out_AlignedSegments.extend(AlignedSegments[0])                 
                FP_Struct_getInfo += " ** Invalid controlFrameType value find when FP_TraceId = 5 !\n"
            
        elif FP_TraceId >= 6 and FP_TraceId <= 10:                      
            struct_section = self.All_Struct_Dic[UFpTtiTrace_Map[FP_TraceId]][1:]          
            Out_Struct.extend(struct_section)                       
            SegmentList = self.cstructPro_obj.get_u32SegmentFromStruct(struct_section)            
            Out_AlignedSegments.extend(SegmentList)
            
        elif FP_TraceId == 11:
            controlFrameType_field = self.All_Struct_Dic[UFpTtiTrace_Map[FP_TraceId]][1]
            Out_Struct.append(controlFrameType_field)
            Out_AlignedSegments.append([controlFrameType_field[2]])
            (data_indx, lastSegment, lastValue) = \
                        self.cstructPro_obj.get_LastStructSegmentValueFromData(Data[1:], Out_Struct, Out_AlignedSegments)
            controlFrameType_value =  lastValue
            #print "     - Out_Struct: %s"% (Out_Struct)            
            FP_Struct_getInfo += "   FP_TraceId: %d, controlFrameType_value: %d"% (FP_TraceId, controlFrameType_value)
            FP_Struct_getInfo += "   data_indx = %d, lastSegment = %s\n"% (data_indx, lastSegment)            
            AlignedSegments = self.cstructPro_obj.get_UnionAlignedSegment(self.All_Union_Dic, self.All_Struct_Dic, 'UFpTtiTraceCchDlCtrlFrameInfo')            
            # ** Pay Attation: controlFrameType should be conform !!            
            if controlFrameType_value == 3:
                Out_Struct.append(self.All_Struct_Dic['SFpTtiTracePchDlSync'])
                Out_AlignedSegments.extend(AlignedSegments[1])                
            else:
                Out_Struct.append(self.All_Struct_Dic['SFpTtiTraceNonPchDlSync'])             
                Out_AlignedSegments.extend(AlignedSegments[2])
                
        elif FP_TraceId == 12:
            controlFrameType_field = self.All_Struct_Dic[UFpTtiTrace_Map[FP_TraceId]][1]
            Out_Struct.append(controlFrameType_field)
            Out_AlignedSegments.append([controlFrameType_field[2]])
            (data_indx, lastSegment, lastValue) = \
                        self.cstructPro_obj.get_LastStructSegmentValueFromData(Data[1:], Out_Struct, Out_AlignedSegments)
            controlFrameType_value =  lastValue            
            #print "     - Out_Struct: %s"% (Out_Struct)            
            FP_Struct_getInfo += "   FP_TraceId: %d, controlFrameType_value: %d"% (FP_TraceId, controlFrameType_value)
            FP_Struct_getInfo += "   data_indx = %d, lastSegment = %s\n"% (data_indx, lastSegment)
            AlignedSegments = self.cstructPro_obj.get_UnionAlignedSegment(self.All_Union_Dic, self.All_Struct_Dic, 'UFpTtiTraceCchUlCtrlFrameInfo')
            # ** Pay Attation: controlFrameType should be conform !!            
            if controlFrameType_value == 2:
                Out_Struct.extend(self.All_Struct_Dic['SFpTtiTracePchTimingAdjustment'])
                Out_AlignedSegments.extend(AlignedSegments[1])                
            elif controlFrameType_value == 4:
                Out_Struct.extend(self.All_Struct_Dic['SFpTtiTracePchUlSync'])
                Out_AlignedSegments.extend(AlignedSegments[2])                
            elif controlFrameType_value == 7:
                Out_Struct.extend(self.All_Struct_Dic['SFpTtiTraceNonPchUlSync'])
                Out_AlignedSegments.extend(AlignedSegments[3])                
            elif controlFrameType_value == 9:
                Out_Struct.extend(self.All_Struct_Dic['SFpTtiTraceNonPchTimingAdjustment'])
                Out_AlignedSegments.extend(AlignedSegments[4])                
            else:
                Out_AlignedSegments.extend(AlignedSegments[0])                
                FP_Struct_getInfo += " ** Invalid controlFrameType value find when FP_TraceId = 12 !\n"
        elif FP_TraceId == 13:
            struct_section = self.All_Struct_Dic[UFpTtiTrace_Map[FP_TraceId]][1:-2]          
            Out_Struct.extend(struct_section)                       
            SegmentList = self.cstructPro_obj.get_u32SegmentFromStruct(struct_section)            
            Out_AlignedSegments.extend(SegmentList)            
            StructValues = self.cstructPro_obj.get_StructValues(Data, Out_Struct, Out_AlignedSegments)           
            edchDataType_value = StructValues[-7]            
            #numOfSubFrame_value = StructValues[-5]
            FP_Struct_getInfo += " * edchDataType_value: %d, \n"% (edchDataType_value)
            EdchCom_AlignedSegments = self.cstructPro_obj.get_UnionAlignedSegment(self.All_Union_Dic, self.All_Struct_Dic, 'UFpTtiTraceEdchComInfo')
            EdchSubFrame_AlignedSegments = self.cstructPro_obj.get_UnionAlignedSegment(self.All_Union_Dic, self.All_Struct_Dic, 'UFpTtiTraceEdchSubFrameInfo')           
            # ** Pay Attation: controlFrameType should be conform !!
            if edchDataType_value == 0:
                #Out_Struct.extend(self.All_Struct_Dic['SFpTtiTraceEdchTypeOneComInfo'])    # not use
                Out_Struct.extend(self.All_Struct_Dic['SFpTtiTraceEdchTypeOneSubFrameInfo'])                
                Out_AlignedSegments.extend(EdchCom_AlignedSegments[0]) 
                Out_AlignedSegments.extend(EdchSubFrame_AlignedSegments[1])                
            elif edchDataType_value == 1:
                Out_Struct.extend(self.All_Struct_Dic['SFpTtiTraceEdchTypeTwoComInfo'])                
                Out_Struct.extend(self.All_Struct_Dic['SFpTtiTraceEdchTypeTwoSubFrameInfo'])                
                Out_AlignedSegments.extend(EdchCom_AlignedSegments[1]) 
                Out_AlignedSegments.extend(EdchSubFrame_AlignedSegments[2])                                
            elif edchDataType_value == 2:
                Out_Struct.extend(self.All_Struct_Dic['SFpTtiTraceEdchTypeTwoForCellFachComInfo'])
                Out_Struct.extend(self.All_Struct_Dic['SFpTtiTraceEdchTypeTwoForCellFachSubFrameInfo'])

                Out_AlignedSegments.extend(EdchCom_AlignedSegments[2]) 
                Out_AlignedSegments.extend(EdchSubFrame_AlignedSegments[3])                 
            else:
                # if not match, use the bigger struct
                #Out_Struct.extend(self.All_Struct_Dic['SFpTtiTraceEdchTypeTwoForCellFachComInfo'])
                #Out_Struct.extend(self.All_Struct_Dic['SFpTtiTraceEdchTypeOneSubFrameInfo'])                
                Out_AlignedSegments.extend(EdchCom_AlignedSegments[0]) 
                Out_AlignedSegments.extend(EdchSubFrame_AlignedSegments[0])                
                FP_Struct_getInfo += " ** Invalid controlFrameType value find when FP_TraceId = 13 !\n"            
                                  
        elif FP_TraceId == 14:
            controlFrameType_field = self.All_Struct_Dic[UFpTtiTrace_Map[FP_TraceId]][1]
            Out_Struct.append(controlFrameType_field)
            Out_AlignedSegments.append([controlFrameType_field[2]])
            (data_indx, lastSegment, lastValue) = \
                        self.cstructPro_obj.get_LastStructSegmentValueFromData(Data[1:], Out_Struct, Out_AlignedSegments)
            controlFrameType_value =  lastValue            
            #print "     - Out_Struct: %s"% (Out_Struct)            
            FP_Struct_getInfo += "   FP_TraceId: %d, controlFrameType_value: %d"% ( FP_TraceId, controlFrameType_value)
            FP_Struct_getInfo += "   data_indx = %d, lastSegment = %s\n"% (data_indx, lastSegment)
            AlignedSegments = self.cstructPro_obj.get_UnionAlignedSegment(self.All_Union_Dic, self.All_Struct_Dic,'UFpTtiTraceEdchDlCtrlFrameInfo') 
            # ** Pay Attation: controlFrameType should be conform !!            
            if controlFrameType_value == 1:
                Out_Struct.extend(self.All_Struct_Dic['SFpTtiTraceEdchOuterLoopPowerControl'])
                Out_AlignedSegments.extend(AlignedSegments[1])                
            elif controlFrameType_value == 11:
                Out_Struct.extend(self.All_Struct_Dic['SFpTtiTraceEdchTnlCongestionIndication'])
                Out_AlignedSegments.extend(AlignedSegments[2])                
            else:
                Out_AlignedSegments.extend(AlignedSegments[0])                
                FP_Struct_getInfo += " ** Invalid controlFrameType value find when FP_TraceId = 14 !\n" 
        if self.printLevel_1 == True:
            FP_Struct_getInfo += "   FP_TraceId = %d,  struct_section: %s\n"% (FP_TraceId, struct_section)
            FP_Struct_getInfo += "   FP_TraceId = %d,  Out_AlignedSegments: %s\n"% (FP_TraceId, Out_AlignedSegments)

        if self.printLevel_1 == True:
            self.__DEBUG_LOG__.debug(FP_Struct_getInfo) 

        return (Out_Struct, Out_AlignedSegments)

    # ######################################################
    # paese block data
    # ######################################################
    def Parse_blockData(self, blockData, Struct, SegmentList = None):        
        ParseData = []
        if SegmentList == None:
            SegmentList = self.cstructPro_obj.get_u32SegmentFromStruct(Struct)
            
        StructWord_len = len(SegmentList)
        if self.printLevel_1 == True:        
            self.__DEBUG_LOG__.debug("   len(blockData) = %s, StructWord_len = %d"% (len(blockData), StructWord_len))
        
        indx = 0        
        while indx + StructWord_len< len(blockData):
            TraceWord_len = int(blockData[indx][2:6],16)/4
            #print "TraceWord_len = %d, StructWord_len = %d" % (TraceWord_len, StructWord_len)            
            indx += 1
            if TraceWord_len >= StructWord_len:
                This_parse_data = self.cstructPro_obj.get_StructValues(blockData[indx: indx + TraceWord_len], Struct, SegmentList)
                #print "This_parse_data: %s"% This_parse_data                
                ParseData.append(This_parse_data)
                
            elif TraceWord_len < StructWord_len:
                self.__DEBUG_LOG__.warning("  Here find TraceWord_len(%d) < StructWord_len(%d)! \n"% (TraceWord_len, StructWord_len))
                
            indx += TraceWord_len

        return ParseData

    def ItemsValuesCommonAdpat(self, keys, values):
        key_pattern = 'Ptr'
        dic_format_obj = CDictionaryFormatAdjust(keys, values)
        dic_format_obj.RemoveItemByKeyPattern("reserve")
        dic_format_obj.AdjustFormatByKeyPattern("Ptr", "0x%08x")
        global Time_field
        dic_format_obj.TimeFormatAdjust(Time_field)
        (adjusttKeys, adjusttValues) = dic_format_obj.get_AdjustedItems()
        return (adjusttKeys, adjusttValues)
            
    # ###################################################################      
    # the main function to tti trace parse
    # parse all tti trace  
    # ###################################################################
    def Tti_Trace_Parse_All(self):

        self.TraceData_Split()        
        self.__DEBUG_LOG__.info(" * TtiTracedumpId: %s"% self.TtiTracedumpId)
        
        threads = []       
        for i in range(0, len(self.TtiTracedumpId)):
            dumpId = self.TtiTracedumpId[i]          
            #blockData = self.TraceData[i]            
            if dumpId == Dec_dumpId:               
                t = CThread(self.DecTraceParse, (), '')
                t.setDaemon(True)
                threads.append(t)                 
            elif dumpId == Enc_dumpId:
                t = CThread(self.EncTraceParse, (), '')
                t.setDaemon(True)
                threads.append(t)                                    
            elif dumpId == L1TraNonHs_dumpId:
                t = CThread(self.L1TraNonHsTraceParse, (), '') 
                t.setDaemon(True)
                threads.append(t)                             
            elif dumpId == L1TraHs_dumpId: 
                t = CThread(self.L1TraHsTraceParse, (), '') 
                t.setDaemon(True)
                threads.append(t)                
            elif dumpId == FP_dumpId:
                t = CThread(self.FPTraceParse, (), '') 
                t.setDaemon(True)
                threads.append(t) 
                
        for i in range(0, len(threads)):
            threads[i].start()
            threads[i].join()             
             
        self.__DEBUG_LOG__.info(" * Tti Trace parser finish!")    
        

    def DecTraceParse(self):            
        sheetNameList  = []
        itemsList      = []
        parseData      = []
        for j in range(0, self.Dec_TraceNum):
            if self.Dec_data[j]:
                self.__DEBUG_LOG__.info(" * %s TTI Trace Parsing ..."% ETtiTraceUserType[j])
                sheetNameList.append(ETtiTraceUserType[j])
                                             
                StructName = Dec_TtiTrace_Struct_Map[ETtiTraceUserType[j]]
                Struct = self.Dec_Struct_Dic[StructName]                        
                keys = self.cstructPro_obj.get_Items_from_Struct(Struct)
                #SegmentList = self.cstructPro_obj.get_u32SegmentFromStruct(Struct)
                values = self.Parse_blockData(self.Dec_data[j], Struct)                        
                (adjusttKeys, adjusttValues) = self.ItemsValuesCommonAdpat(keys, values)                        
                # add keys and values to parsed data
                itemsList.append(adjusttKeys)                          
                parseData.append(adjusttValues)
                
                if self.printLevel_2 == True:                            
                    self.__DEBUG_LOG__.debug("   Dec_data[%d](len:%d): %s\n  [Struct:] %s\n  values(len:%d): %s"%\
                                   (j, len(self.Dec_data[j]), self.Dec_data[j], Struct, len(values), values))   
        
        fileName = 'Decoder_TTI_Trace'
        self.__DEBUG_LOG__.info(" * %s parsed data saving..."% fileName)                  
        fileName = os.path.join(self.ParsedDataDir, fileName)                
        CSaveDataToXls(fileName, sheetNameList, itemsList, parseData, ['sequenceNo'])                 

    def EncTraceParse(self):       
        sheetNameList  = []
        itemsList      = []
        parseData      = []
        
        if self.Enc_data:
            sheetNameList.append(ETtiTraceTypeFlag[18][1:-8]) 
            StructName = L1Tra_TtiTrace_Struct_Map[ETtiTraceTypeFlag[18]]
            Struct = self.L1Tra_Struct_Dic[StructName] 
            #print Struct                   
            keys = self.cstructPro_obj.get_Items_from_Struct(Struct)
            values = self.Parse_blockData(self.Enc_data, Struct)          
            (adjusttKeys, adjusttValues) = self.ItemsValuesCommonAdpat(keys, values)
            itemsList.append(adjusttKeys) 
            parseData.append(adjusttValues)   
            
            fileName = 'Encoder_TTI_Trace'
            self.__DEBUG_LOG__.info(" * %s parsed data saving..."% fileName)            
            fileName = os.path.join(self.ParsedDataDir, fileName)                                          
            CSaveDataToXls(fileName, sheetNameList, itemsList, parseData, ['sequenceNo'])                               
            
    def L1TraNonHsTraceParse(self):               
        sheetNameList  = []
        itemsList      = []
        parseData      = []               
        for j in range(0, self.L1TraNonHs_TraceNum):
            if self.L1TraNonHs_data[j]:
                self.__DEBUG_LOG__.info(" * %s TTI Trace Parsing ..."% ETtiTraceTypeFlag[j+11])               
                sheetNameList.append(ETtiTraceTypeFlag[j+11][1:-6])                   
                StructName = L1Tra_TtiTrace_Struct_Map[ETtiTraceTypeFlag[j+11]]
                Struct = self.L1Tra_Struct_Dic[StructName]
                keys = self.cstructPro_obj.get_Items_from_Struct(Struct)
                #SegmentList = self.cstructPro_obj.get_u32SegmentFromStruct(Struct)
                values = self.Parse_blockData(self.L1TraNonHs_data[j], Struct)                        
                (adjusttKeys, adjusttValues) = self.ItemsValuesCommonAdpat(keys, values)                        
                itemsList.append(adjusttKeys) 
                parseData.append(adjusttValues) 
                
                if self.printLevel_2 == True:                            
                    self.__DEBUG_LOG__.debug("   L1TraNonHs_data[%d](len:%d): %s\n   Struct: %s\n  values(len:%d): %s"%\
                                   (j, len(self.L1TraNonHs_data[j]), self.L1TraNonHs_data[j], Struct, len(values), values))

        fileName = 'L1tra_NonHs_TTI_Trace'
        self.__DEBUG_LOG__.info(" * %s parsed data saving..."% fileName)        
        fileName = os.path.join(self.ParsedDataDir, fileName)                
        CSaveDataToXls(fileName, sheetNameList, itemsList, parseData, ['sequenceNo'])    
            
    def L1TraHsTraceParse(self):         
        sheetNameList  = []
        itemsList      = []
        parseData      = []   
        for j in range(0, self.L1TraHs_TraceNum):                        
            if self.L1TraHs_data[j]:
                sheetNameList.append(ETtiTraceTypeFlag[j+11][1:-6])
                StructName = L1Tra_TtiTrace_Struct_Map[ETtiTraceTypeFlag[j+14]]
                Struct = self.L1Tra_Struct_Dic[StructName]                          
                keys = self.cstructPro_obj.get_Items_from_Struct(Struct)
                #values = self.Parse_blockData(self.L1TraHs_data[j], Struct, AlignedSegments)
                values = self.Parse_blockData(self.L1TraHs_data[j], Struct)                        
                (adjusttKeys, adjusttValues) = self.ItemsValuesCommonAdpat(keys, values)                        
                itemsList.append(adjusttKeys) 
                parseData.append(adjusttValues) 
                
        fileName = 'L1tra_NonHs_TTI_Trace'
        self.__DEBUG_LOG__.info(" * %s parsed data saving..."% fileName)        
        fileName = os.path.join(self.ParsedDataDir, fileName)                
        CSaveDataToXls(fileName, sheetNameList, itemsList, parseData, ['sequenceNo'])             
            
    def FPTraceParse(self):               
        sheetNameList  = []
        itemsList      = []
        parseData      = []         
        for j in range(0, self.FP_TraceNum):                        
            if self.FP_data[j]:                       
                FP_FrameName = UFpTtiTrace_Map[j][1:-6]
                (Struct, AlignedSegments) = self.get_FP_Struct(j, self.FP_data[j])
                if Struct: 
                    sheetNameList.append(UFpTtiTrace_Map[j][1:-5])                   
                    self.__DEBUG_LOG__.info(" * %s TTI Trace Parsing ..."% sheetNameList[-1])                        
                    if self.printLevel_1 == True: 
                        self.__DEBUG_LOG__.debug("   len(FP_data[%d]): %d"% (j, len(self.FP_data[j])))                    
                                                                      
                    keys = self.cstructPro_obj.get_Items_from_Struct(Struct)                           
                    values = self.Parse_blockData(self.FP_data[j], Struct, AlignedSegments)
                    (adjusttKeys, adjusttValues) = self.ItemsValuesCommonAdpat(keys, values)
                    itemsList.append(adjusttKeys) 
                    parseData.append(adjusttValues) 
                    
                    if self.printLevel_2 == True:                            
                        self.__DEBUG_LOG__.debug("   AlignedSegments(len:%d): %s\n  values[0]: %s"%\
                                       (len(AlignedSegments), AlignedSegments, values[0]))
                else:
                    self.__DEBUG_LOG__.warning("   Struct get failure, when FP Trace Id :%d"% j)
                    
        fileName = 'FP_TTI_Trace'
        self.__DEBUG_LOG__.info(" * %s parsed data saving..."% fileName)        
        fileName = os.path.join(self.ParsedDataDir, fileName)            
        CSaveDataToXls(fileName, sheetNameList, itemsList, parseData)                          
  

