# -*- coding: utf-8 -*-
# ##############################################################################
# class LogProcess():
# [Function]:  Class for SysLog Parse
#       Author:         Fan, Shuangxi (NSN - CN/Hangzhou)
#       date:  2015-11-25
#*      description:    
# ##############################################################################
#!/usr/bin/python

import os
import re

from common import creat_dictionary
from CHexStrProcess import *
from CDictionaryFormatAdjust import *
from CSyntaxParse import *
    
'''
# ##############################################################################
TODO:

# ##############################################################################
'''
###################################################################   
#*  global variables defination
#  - Codec Log Trace Decoder paras 
###################################################################


SourcePath = "refs"

EFaultId_file       = os.path.join(SourcePath, r"EFaultId.h")
FaultHandling_file  = os.path.join(SourcePath, r"FaultHandling.h")

SFaultState_str = "SFaultState"
EFaultId_str    = "EFaultId"

fieldDic = {
    'EFaultId':         'u32',
    'TAaSysComSicad':   'u32',
    'TFaultInfo':       'u32'
    }

Time_field = ['year', 'month', 'day', 'hour', 'minute', 'second', 'millisec']

singleDataLen = 9  # 9 x u32      

# ###################################################################
# class LogProcess():
# [Function]:  Class for SysLog Parse
# * Parse the header of Log Trace from dump bin
# * Read log str from header Log map files in "Log_Env_Path",
#     @example  fiels in "......\include\Codec_Env\Log_Env\"
#   then parse log by logId 
# [Methods]:
# * get_validData: 
# * ParsedLogSortByTime
# * ItemsValuesCommonAdpat
# * string_parse:  parse ASCII string
#** parse_logStr: parse one Log string
#   - primary function of class
#** log_parse:  parse all sysLog, output the parsed log file
#   - main function of class
# ################################################################### 
class LogProcess():
            
    def __init__(self, Log_DumpData, ParsedDataFile):

        self.hexStr_obj = CHexStrProcess()
        self.cenum_obj = CEnumExtract()
        self.cstructPro_obj = CStructProcess()
        self.log_dump_data = None
        self.get_validData(Log_DumpData) 

        EFaultId_dic = self.cenum_obj.get_enum_dic(EFaultId_file)
        self.EFaultId_dic = EFaultId_dic[EFaultId_str]
              
        cs = CStructExtract(FaultHandling_file) 
        cs.unifyFieldByDic(fieldDic)       
        cs.get_Struct_Map()      

        SFaultState_map = {'SFaultState': "SFaultState"}
        SFaultStateStruct_Dic = cs.get_UnfoldStructMapbyDic(SFaultState_map)
        #print SFaultStateStruct_Dic

        self.SFaultStateStruct = SFaultStateStruct_Dic[SFaultState_str]

        self.SFaultStateStruct_SegmentList = self.cstructPro_obj.get_u32SegmentFromStruct(self.SFaultStateStruct)
        self.SFaultStateStruct_Items = self.cstructPro_obj.get_Items_from_Struct(self.SFaultStateStruct)
        
        self.ParsedLogData = []
        self.OutFile = open(ParsedDataFile, 'w')

        
    def get_validData(self, log_dump_data):
        indx = 0
        while indx <len(log_dump_data):
            checksum = 0
            for i in range(0, singleDataLen):
                checksum |= int(log_dump_data[indx+i][2:], 16)
            if 0 == checksum:                
                break
            indx += singleDataLen

        if indx > 0:
            self.log_dump_data = log_dump_data[0: indx]
        else:
            print "** No valid data found from input file! please check it."
            exit(0)

    # #################################################################
    # parse ASCII string
    # #################################################################
    def string_parse(self, values):
        out_str = ''
        print_format = "%c%c%c%c"
        for i in range(0, len(values)):
            value_i = self.hexStr_obj.word_split(values[i], [8,8,8,8])
            if i == len(values)-1:
                for j in range(0, len(value_i)):
                    if value_i[j] == 0:
                        value_i = value_i[0:j]
                        print_format = print_format[0: 2*j]
                        break                                
            out_str += print_format % tuple(value_i)
            
        return out_str
            

    # #############################################################       
    # ParsedLogSortByTime: 
    # #############################################################
    def ParsedLogSortByTime(self): 
        time_pattern = re.compile(',\d{2}:\d{2}:\d{2}\.\d{3,},')
        m = time_pattern.search(self.ParsedLogData[0])     
        (start, end) = m.span()

        self.ParsedLogData = sorted(self.ParsedLogData, key=lambda x:x[start+1: end])


    def ItemsValuesCommonAdpat(self, keys, values):
        key_pattern = 'Ptr'
        dic_format_obj = CDictionaryFormatAdjust(keys, values)
        dic_format_obj.RemoveItemByKeyPattern("reserved")
        #dic_format_obj.AdjustFormatByKeyPattern("Ptr", "0x%08x")
        global Time_field
        dic_format_obj.TimeFormatAdjust(Time_field)
        (adjusttKeys, adjusttValues) = dic_format_obj.get_AdjustedItems()
        return (adjusttKeys, adjusttValues)

        
    # #################################################################
    # print log to file
    # #################################################################            
    def log_print(self):
        # print header line
        #print_str = ('--'*60 + " \n")
        print_str = "\n TimeStamp,  "
        print_str += ' '*12 + " faultId:fault_type, "
        print_str += ' '*25 + "faultSource, "
        print_str += ' '*2 + "faultInfo [hex(dec)...]\n"
        print_str += ('--'*60 + " \n")        
        self.OutFile.write(print_str)
             
        for i in range(0, len(self.ParsedLogData)):            
            self.OutFile.write(self.ParsedLogData[i] + '\n')
            
        self.OutFile.close()


    # #################################################################
    # main function of class: LogProcess
    # parse all sysLog, output the parsed log file
    # #################################################################            
    def log_parse(self):        
        
        indx = 0        
        while indx <len(self.log_dump_data): 
            thisBlock = self.log_dump_data[indx: indx + singleDataLen]
            HeaderVlues = self.cstructPro_obj.get_StructValues(thisBlock, self.SFaultStateStruct, self.SFaultStateStruct_SegmentList)            
            (itemList, valueList) = self.ItemsValuesCommonAdpat(self.SFaultStateStruct_Items, HeaderVlues)         
            Out_Dic = creat_dictionary(itemList, valueList)

            fault_type = self.EFaultId_dic[Out_Dic['faultId']]            
            thisLog = ''  
            thisLog += ("%s, "% Out_Dic['TimeStamp'])
            thisLog += ("%04d:%s, "% (Out_Dic['faultId'],fault_type))
            thisLog += ("0x%08x, "% (Out_Dic['faultSource']))
            faultInfo_str = ''
            for i in range(0,5):
                faultInfo_field = "faultInfo[%d]"% i
                faultInfo_str += "0x%08x(%d),"% (Out_Dic[faultInfo_field], Out_Dic[faultInfo_field])
            faultInfo_str = "[%s]"% faultInfo_str[0:-1]
            thisLog += faultInfo_str
            
            self.ParsedLogData.append(thisLog)            
            indx += singleDataLen          
        #-----------------------------------------
        # sort by time and write to file   
        self.ParsedLogSortByTime()    
        self.log_print()
        print" - Fault Log parse complete..."

        
