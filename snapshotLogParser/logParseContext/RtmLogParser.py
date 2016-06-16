# -*- coding: utf-8 -*-
# ##############################################################################
# class LogProcess():
# [Function]:  Class for SysLog Parse
#       Author:         Fan, Shuangxi (NSN - CN/Hangzhou)
#       draft:          2014-10-14 
#       modify(split):  2015-11-20
#*      description:    
# ##############################################################################
#!/usr/bin/python

import os
import re

from utils.common import debugLogSetup, creat_dictionary
from utils.CHexStrProcess import *
from utils.CBinDataConvert import *
from utils.CDictionaryFormatAdjust import *
from utils.CSyntaxParse import *
    
'''
# ##############################################################################
TODO:

# ##############################################################################
'''
###################################################################   
#*  global variables defination
#  - Codec Log Trace Decoder paras 
###################################################################
DSP_Path = r"C_Application\SC_UP\DSP"
ERTLDumpId_File       = os.path.join(DSP_Path, r"ss_commondsp\cp_runtimelog\ERTLDumpId.h")
Time_field = ['year', 'month', 'day', 'hour', 'minute', 'second', 'millisec']

CodecLog_dumpId = 21

ComponentMapFile = "EComponentId_DSPBase.h"
FileIdFile       = "EFileId_DSPBase.h"

Log_Env_Path = os.path.join(DSP_Path, r"include\Codec_Env\Log_Env")
LomRTLLog_File = r"c_application\sc_up\arm\include\lom_env\definitions\LomRTLLog.h"
Rtl_Lib_File =  os.path.join(DSP_Path, r"ss_commondsp\cp_runtimelog\Rtl_Lib.h")

STRLLibMsgHeaderFile = [Rtl_Lib_File]
STRLLibMsgHeader = 'STRLLibMsgHeader'
# component Id, file id(file in component number), log id (in file)
# logId_segment  = [4, 12, 16]

# dumpblock length, dump Id
dumpHD_segment = [16, 16]  

fixPart_len = 5

# def fixed part struct 

logId = [

    ['u32',  'logNum',       16 ],  #    
    ['u32',  'fileId',       8  ],  # 8
    ['u32',  'componentId',  8  ]   # 8
]
        

# ###################################################################
# class LogProcess():
# [Function]:  Class for SysLog Parse
# * Parse the header of Log Trace from dump bin
# * Read log str from header Log map files in "Log_Env_Path",
#     @example  fiels in "......\include\Codec_Env\Log_Env\"
#   then parse log by logId 
# [Methods]:
# * __get_Component_Dic: read ComponentId map header file
# * __get_ComponentFile_Dic: map: component -> file 
# * __get_LogStrList: get log str list 
#   - By read one given ELogMapId_xxx.h file 
# * __get_ComponentLog_Dic: map: component -> Log
#   - read each ELogMapId_xxx.h file,
#     get the maped Dictionary: self.ComponentLog_Dic
# * __find_allMatchedIndex: find all matched str index
#   - here we mainly use it for search strs like: "%", "%s",...
# * __string_parse:  parse ASCII string
#** __parse_logStr: parse one Log string
#   - primary function of class
#** log_parse:  parse all sysLog, output the parsed log file
#   - main function of class
# ################################################################### 
class LogProcess():
            
    def __init__(self, Log_DumpData, RTLDumpId, SourcePath, ParsedDataDir, __DEBUG_LOG__):

        self.hexStr_obj = CHexStrProcess()
        self.binData_obj = CBinDataConvert()
        self.cenum_obj = CEnumExtract()
        self.cstructPro_obj = CStructProcess()
        
        global Log_Env_Path                     
        global LomRTLLog_File
        #global Rtl_Lib_File
        global TempFileDir 
        TempFileDir = os.path.join(ParsedDataDir, 'temp')     
        if os.path.isdir(TempFileDir) == False:
            os.mkdir(TempFileDir)          
        self.__DEBUG_LOG__ = __DEBUG_LOG__

        global CodecLog_dumpId
        global logId
        #global logId_segment
        global STRLLibMsgHeader
        global STRLLibMsgHeaderFile

        global fixPart_len
        
        self.Log_Env_Path = os.path.join(SourcePath, Log_Env_Path)       
        self.log_dumpId = CodecLog_dumpId
        self.log_dump_data = Log_DumpData
        
        LomRTLLog_File_eunm_dic = self.cenum_obj.get_enum_dic(os.path.join(SourcePath, LomRTLLog_File))
        self.ERuntimeLogLevel_dic = LomRTLLog_File_eunm_dic['ERuntimeLogLevel']
        
        #self.logId_segment = logId_segment
        for i in range(0, len(STRLLibMsgHeaderFile)):
            STRLLibMsgHeaderFile[i] = os.path.join(SourcePath, STRLLibMsgHeaderFile[i])
               
        cs = CStructExtract(STRLLibMsgHeaderFile, TempFileDir)        
        cs.get_Struct_Map()      
    
        STRLLibMsgHeaderStruct = cs.struct_Dic[STRLLibMsgHeader]
        del STRLLibMsgHeaderStruct[0]
        
        self.HeaderStruct = []
        self.HeaderStruct.extend(logId)
        self.HeaderStruct.extend(STRLLibMsgHeaderStruct)
        
        self.HeaderStruct_SegmentList = self.cstructPro_obj.get_u32SegmentFromStruct(self.HeaderStruct)
        self.HeaderStruct_Items = self.cstructPro_obj.get_Items_from_Struct(self.HeaderStruct)
        
        self.ComponentId_Dic = {}
        self.__get_Component_Dic()
        
        self.ComponentFile_Dic = {}
        self.__get_ComponentFile_Dic()
        
        self.ComponentLog_Dic = {}
        self.__get_ComponentLog_Dic()
   
        dumpName = RTLDumpId[CodecLog_dumpId]
        file_name = dumpName[dumpName.find('_')+1:] + '.txt'         
        outFileName = os.path.join(ParsedDataDir, file_name)
        
        self.ParsedLogData = []
        self.OutFile = open(outFileName, 'w')    
        
    # #################################################################
    # read ComponentId map header file:  EComponentId_DSPBase.h
    # get the maped Dictionary: self.ComponentId_Dic
    # ################################################################# 
    def __get_Component_Dic(self):        
        global ComponentMapFile
        global logId
        
        ComponentId_len = logId[2][2]/4   # unit: 4 bit
        ComponentMapFile = os.path.join(self.Log_Env_Path, ComponentMapFile)
        
        if os.path.isfile(ComponentMapFile):
            self.__DEBUG_LOG__.info(" * Reading Component Map File...")
            H_ComponentId = open(ComponentMapFile,'r')
        else:
            self.__DEBUG_LOG__.warning("** Component Map File \"%s\" not exit !!"% ComponentMapFile)
            return
        
        Lines = H_ComponentId.read().splitlines()
        H_ComponentId.close()
        
        LineNum = len(Lines)   
        for i in range(0, LineNum):
            ThisLine = Lines[i].strip()

            if ThisLine.find('=')>0: 
                if ThisLine.find(',')>0:
                    ComponentId   = ThisLine.split('=')[1].split(',')[0].strip()
                else:
                    ComponentId   = ThisLine.split('=')[1].strip()
                    
                if ComponentId == '0':
                    ComponentId = 0
                else:
                    ComponentId = int(ComponentId[2: 2+ComponentId_len], 16)
                    
                ComponentName = ThisLine.split('=')[0].split('_')[1].strip()
                self.ComponentId_Dic[ComponentId] = ComponentName         
        
        self.__DEBUG_LOG__.info(" * Component dic creat complete ...")
        
    # #################################################################
    # map: component -> file 
    # read EFileId_DSPBase.h file 
    # get the maped Dictionary: self.ComponentFile_Dic
    # #################################################################        
    def __get_ComponentFile_Dic(self):        
        global FileIdFile        
        FileIdFile = os.path.join(self.Log_Env_Path, FileIdFile)        
        if os.path.isfile(FileIdFile):
            self.__DEBUG_LOG__.info(" * Reading FileId map File...")
            H_FileId = open(FileIdFile,'r')
        else:
            self.__DEBUG_LOG__.warning("** FileId Map File \"%s\" not exit !!"% FileIdFile)
            return
        Lines = H_FileId.read().splitlines()
        H_FileId.close()
        
        # self.ComponentFile_Dic initialization 
        for key in self.ComponentId_Dic:
            self.ComponentFile_Dic[self.ComponentId_Dic[key]] = []
                    
        LineNum = len(Lines)
        for i in range(0, LineNum):
            ThisLine = Lines[i].strip()
            if ThisLine.find('=')>0: 
                ComponentName   = ThisLine.split('=')[1].split('+')[0].split('_')[1].strip()
                fileName = ThisLine.split('=')[0][ThisLine.split('=')[0].find('_')+1:].strip()               
                self.ComponentFile_Dic[ComponentName].append(fileName)
                
            #print "ComponentName: %s fileName: %s"% (ComponentName, fileName)            
        self.__DEBUG_LOG__.info(" * Component -> File dic creat complete ...")
        
    # #################################################################
    # get log str list 
    # read one given ELogMapId_xxx.h file 
    # #################################################################  
    def __get_LogStrList(self, LogMapFile):        
        # pattern in log map file 
        FileIndicate_pattern      = re.compile('/\*\s+\-+\s+\w+\s+\-+\s+\*/')
        LogId_pattern             = re.compile('E\w+_\d{3,4}')
        LogStr_pattern            = re.compile('".+",?$')
        CharArrayDefEnd_pattern   = re.compile('^\};$')                
        #---------------- get input file data -----------------        
        MapFile_fp = open(LogMapFile,'r')
        MapDataLines = MapFile_fp.readlines()
        MapLineNum = len(MapDataLines)
        MapFile_fp.close()
        
        LogStrList = []
        MapFileLine_indx = 0
        
        for i in range(0, MapLineNum):
            if MapDataLines[i].find('char *')==0:
                MapFileLine_indx = i+1
                break
                              
        while MapFileLine_indx < MapLineNum:
        #while search_num <=1:
            MapFileLine_indx += 1
            ThisLine = MapDataLines[MapFileLine_indx]           
            if LogStr_pattern.search(ThisLine):
                #MapIdLine = MapDataLines[MapFileLine_indx -1]
                #MapId = LogId_pattern.search(MapIdLine).group()
                ThisLine = ThisLine.strip()
                if ThisLine[-1] == ',':                    
                    logStr = ThisLine[0:-1]
                else:
                    logStr = ThisLine
                    
                LogStrList.append(logStr)
                        
            if CharArrayDefEnd_pattern.search(ThisLine):
                break
               
        return LogStrList
        
    ##################################################################
    # map: component -> Log 
    # read each ELogMapId_xxx.h file 
    # get the maped Dictionary: self.ComponentLog_Dic
    ##################################################################  
    def __get_ComponentLog_Dic(self):        
        for i in range(0, len(self.ComponentId_Dic)):
            LogMapFile = "ELogMapId_%s.h"% self.ComponentId_Dic[i]
            LogMapFile = os.path.join(self.Log_Env_Path, LogMapFile)
            if os.path.isfile(LogMapFile):
                LogStrList = self.__get_LogStrList(LogMapFile)        
                self.ComponentLog_Dic[i] = LogStrList
                
    # #################################################################
    # find all matched str index
    # here we mainly use it for search strs like: "%", "%s",...
    # #################################################################
    def __find_allMatchedIndex(self, srcStr, searchStr):
        indexList = []
        idx = 0
        while idx < len(srcStr):
            temp_str = srcStr[idx:]
            temp_idx = temp_str.find(searchStr)
            if temp_idx>=0:
                idx += temp_idx
                indexList.append(idx)
                idx += 1
            else:
                break 
             
        return indexList
    
    # #################################################################
    # parse ASCII string
    # #################################################################
    def __string_parse(self, values):
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
            
    # #################################################################
    # primary function of class
    # parse one Log string
    # #################################################################  
    def __parse_logStr(self, logStr, values):
        p_pattern = re.compile('%#p')
        
        while p_pattern.search(logStr):
            logStr = p_pattern.sub('0x%08x', logStr)
          
        Exception0_str = "[**Exception_0] Log parse failure! please check log type."
        
        if logStr.find(r'%s') >= 0:
            
            s_index = logStr.index(r'%s')
            out_values = [] 
            
            indexList = self.__find_allMatchedIndex(logStr, r'%')            
            s_index_num = 0
            
            for i in range(0, len(indexList)):
                if indexList[i] == s_index:
                    s_index_num = i
                    break
                
            for i in range(0, s_index_num):        
                out_values.append(int(values[i], 16))
            
            out_values.append(self.__string_parse(values[s_index_num: len(values)-(len(indexList) - s_index_num)+1]))
            
            for i in range(len(values)-(len(indexList) - s_index_num)+1, len(values)):        
                out_values.append(int(values[i], 16))                
                        
            if len(values)>0:
                try:
                    out_str = logStr % tuple(out_values)  
                except:
                    out_str = Exception0_str
            else:
                out_str = logStr            
        else:                       
            for i in range(0, len(values)):
                values[i] = int(values[i], 16)
                      
            if len(values)>0:
                try:
                    out_str = logStr % tuple(values)  
                except:
                    out_str = Exception0_str
            else:
                out_str = logStr
        
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
        dic_format_obj.RemoveItemByKeyPattern("reserve")
        dic_format_obj.AdjustFormatByKeyPattern("Ptr", "0x%08x")
        global Time_field
        dic_format_obj.TimeFormatAdjust(Time_field)
        (adjusttKeys, adjusttValues) = dic_format_obj.get_AdjustedItems()
        return (adjusttKeys, adjusttValues)

        
    # #################################################################
    # print log to file
    # #################################################################            
    def __log_print(self):
        # print header line
        print_str = ('--'*60 + " \n")
        print_str += " logLevel,      TimeStamp,     nid, [frame: slot], userId, "
        print_str += "[fileName:line], SYSLOG_PRINT ......\n"
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
        Exception1_str = "[**Exception_1] Log parse failure! log may not exit in log map file, please check."         
        indx = 0        
        while indx <len(self.log_dump_data):                      
            # get this dump block data len(Byte len), then Byte -> word
            thisDumpLen = self.hexStr_obj.word_split(self.log_dump_data[indx], dumpHD_segment, 'Big')[0]/4 
            
            thisBlockFixPart = self.log_dump_data[indx+1: indx +1+ fixPart_len]
            HeaderVlues = self.cstructPro_obj.get_StructValues(thisBlockFixPart, self.HeaderStruct, self.HeaderStruct_SegmentList)       
            
            (itemList, valueList) = self.ItemsValuesCommonAdpat(self.HeaderStruct_Items, HeaderVlues)
          
            Out_Dic = creat_dictionary(itemList, valueList)

            componentName = self.ComponentId_Dic[Out_Dic['componentId']]
            fileName = self.ComponentFile_Dic[componentName][Out_Dic['fileId']]
            
            LogLevel = self.ERuntimeLogLevel_dic[Out_Dic['logLevel']].split('_')[1]
            LogLevel_strLen = 6
            LogLevel = LogLevel+' '*(LogLevel_strLen - len(LogLevel))
            
            thisLog = ''            
            thisLog += ("[%s], "% LogLevel)
            thisLog += ("%s, "% Out_Dic['TimeStamp'])
            thisLog += ("%s, "% hex(Out_Dic['nid'])[2:].upper())
            thisLog += ("[%04d: %02d], "% (Out_Dic['frameNr'], Out_Dic['slotNr']))
            thisLog += ("%d, "% (Out_Dic['userId']))
            thisLog += ("[%s: %d], "% (fileName, Out_Dic['line']))

            try:
                thisLogStr = self.ComponentLog_Dic[Out_Dic['componentId']][Out_Dic['logNum']][1:-1]  
                thisData = self.log_dump_data[indx +1+ fixPart_len: indx +1 + thisDumpLen]
                thisLogStr_out = self.__parse_logStr(thisLogStr, thisData)                 
            except:
                thisLogStr_out = Exception1_str
                
            thisLog += thisLogStr_out
            
            if thisLogStr_out.find("Exception_0")>=0:                
                thisLog += " * LogStr: %s, "% thisLogStr
                thisLog += " * Data: %s"% thisData
            
            self.ParsedLogData.append(thisLog)            
            indx += (thisDumpLen + 1)            
        #-----------------------------------------
        # sort by time and write to file   
        self.ParsedLogSortByTime()    
        self.__log_print()
        self.__DEBUG_LOG__.info(" - Codec Log Trace parse complete...")

