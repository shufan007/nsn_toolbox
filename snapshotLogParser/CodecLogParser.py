# -*- coding: utf-8 -*-
# ##############################################################################
#       Function:       Spalit and parse Codec Log from snapshot buffer
#       Author:         Fan, Shuangxi (NSN - CN/Hangzhou)
#       draft:          2014-10-14 
#       modify(split):  2015-11-20
#*      description:    split snapshot buffer by dump ID, parse each dump block
#           - InputFile:    get snapshot buffer (bin data or hex data)from this file
#           - DstFile:      save parsed info to some files 
# ##############################################################################
#!/usr/bin/python

import sys, os
import time

from utils.common import *
from utils.CSyntaxParse import CEnumExtract

from logParseContext.SnapshotParser import Snapshot
from logParseContext.RtmLogParser import LogProcess
from logParseContext.MessageParser import MassageDecode
from logParseContext.TtiTraceParser import TtiTrace
    
'''
# ##############################################################################
TODO:

* use thread for unpack .bin and parse 
* use thread for parallel parse log

1. add enum info to Tti Trace parsed data
2. 
	1) complete Msg Parse
	2) add one more access feature: 
	   -> double click to execute for identify .bin file in the same path;
           -> read .bin files from a dir or current path 
	   -> save runtime info and exception log to file.
	3) close to save unpacked data
        
3. Read source code from svn
4. parse message directly, out put to txt file, 
   list the message Id and message header in front of the file
5. performance optimization:
   - speed the way of unpack .bin file
   - use mmap, use slicing to read from the file
   - set struct and save the structs ectected from source file
   - record the modify time of the source file 
   - flush file
   - use array to instand some list

# ##############################################################################
'''  
# ######################## global definations  ################################# 

CodecLog_dumpId = 21    
Msg_dumpId = 2 

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

DSP_Path = r"C_Application\SC_UP\DSP"
ERTLDumpId_File       = os.path.join(DSP_Path, r"ss_commondsp\cp_runtimelog\ERTLDumpId.h")
ERTLFreezeCause_File  = os.path.join(DSP_Path, r"ss_commondsp\cp_runtimelog\ERTLFreezeCause.h")
# #################################################################


# #################################################################
# get Source Path from SourcePath file
# #################################################################
def get_SourcePath(basePath):    
    SourcePathFile = "README.md"  
    SourcePathFile = os.path.join(basePath, SourcePathFile)
    if os.path.isfile(SourcePathFile):
        print " - Reading SourcePath File...\n"
        configureFile = open(SourcePathFile, 'r')
    else:
        print"**Error: SourcePath File '%s' not exit !!\n"% SourcePathFile
        return
    Lines = configureFile.read().splitlines()
    configureFile.close()
    
    LineNum = len(Lines)
    for i in range(0, LineNum):
        ThisLine = Lines[i].strip()
        if ThisLine.find('=')>0:                 
            SourcePath = ThisLine.split('=')[1].strip()  
            break
    return SourcePath


# ##########################################################    
# main function for log parse trigger
#  - Codec Log Trace
#  - Message Trace
#  - TTi Trace
#    such as: L1TraNonHs Trace;
#             L1TraHs Trace;
#             Encoder Trace;
#             Decoder Trace;
#             FP Trace
# ##########################################################
def log_parse_all(SnapShotFile, basePath, start_addr): 
    # set SourcePath (global para)
   
    SourcePath = get_SourcePath(basePath)
    ParsedDataDir = make_DirByFilePath(SnapShotFile, "ParsedData")
    TempFileDir = os.path.join(ParsedDataDir, 'temp')     
    if os.path.isdir(TempFileDir) == False:
        os.mkdir(TempFileDir) 

    __DEBUG_LOG__ = debugLogSetup(os.path.join(TempFileDir, 'DEBUG_LOG.log'))   

    cf_obj = CEnumExtract()
    # RTLDumpId dic
    RTLDumpId = cf_obj.get_enum_dic(os.path.join(SourcePath, ERTLDumpId_File))['ERTLDumpId']   
    # RTLFreezeCause dic
    RTLFreezeCause = cf_obj.get_enum_dic(os.path.join(SourcePath, ERTLFreezeCause_File))['ERTLFreezeCause']   
    # ------------ snapshot dumpblock split ---------
    print" * Snapshot parser start..."
    snapshot_obj = Snapshot(SnapShotFile, start_addr , RTLDumpId, RTLFreezeCause, ParsedDataDir, __DEBUG_LOG__)  
    (dumpblock_data, dumpblock_Data_len) = snapshot_obj.get_dumpblocks()
    
    threads = []
    # ##########################################################
    # --------------------- Log Trace decode ------------------
    global CodecLog_dumpId        
    if dumpblock_data[CodecLog_dumpId]:
        print" * Codec Log RtmLog parse start..."             
        log_obj = LogProcess(dumpblock_data[CodecLog_dumpId], RTLDumpId, SourcePath, ParsedDataDir, __DEBUG_LOG__)
        #log_obj.log_parse()

        t = CThread(log_obj.log_parse, (), '')
        t.setDaemon(True)
        threads.append(t)

        
    # ##########################################################            
    # --------------------- message decode --------------------
    global Msg_dumpId
    if dumpblock_data[Msg_dumpId]: 
        print" * Message data parse start..."            
        msg_obj = MassageDecode(dumpblock_data[Msg_dumpId], RTLDumpId, ParsedDataDir, __DEBUG_LOG__)
        #msg_obj.msg_parse()   

        t = CThread(msg_obj.msg_parse, (), '')
        t.setDaemon(True)
        threads.append(t)  
          
    # ##########################################################
    # -------------------- Tti trace decode ---------------------
    global Tti_Trace_DumpId
    # Tti_Trace_DumpId    = [4, 5, 6, 19, 20]
    # get all Tti Trace Data
    All_Tti_Trace_Data  = []
    #dumpblock_Data_len = []
    for dumpId in Tti_Trace_DumpId:
        if dumpblock_data[dumpId]:
            All_Tti_Trace_Data.append(dumpblock_data[dumpId])
            #dumpblock_Data_len.append(self.dumpblock_Data_len[dumpId])
     
    if All_Tti_Trace_Data:
        print" * Tti Trace parser start..."         
        Tti_obj = TtiTrace(All_Tti_Trace_Data, dumpblock_Data_len, RTLDumpId, SourcePath, ParsedDataDir, __DEBUG_LOG__)
        #Tti_obj.Tti_Trace_Parse_All()

        t = CThread(Tti_obj.Tti_Trace_Parse_All, (), '')
        t.setDaemon(True)
        threads.append(t)


    for i in range(0, len(threads)):
        threads[i].start()
        threads[i].join()

    print" ----------------------------------------\n"
        

# ########**** main ****#######***** main *****#######**** main ****#########
if __name__ == '__main__':
    
    if  len(sys.argv)==2 and sys.argv[1].upper().find('HELP')>=0:
        print'''
   *************************** Usage: ***************************
   # Add SourcePath in 'README'
    -input:            
         -[1] SnapShotFile: input file, .bin file or directory with .bin files
               the .bin file in current path or full path
         -[2] start_addr(offset): unpack .bin file from here
             (defult: '0')             
   @example:
        CodecLogParser.py xxx.bin
        CodecLogParser.py RtlDumpBinDir
        CodecLogParser.py xxx.bin 17f00               
   - output:
        - Out put Location: the same path as input file
        - "xxx_ParseInfo.txt", information parsed from snapshot buffer
        - Parsed Log in directory "xxx_ParsedData"            
   **************************************************************
        '''
        exit(0) 
        
    elif len(sys.argv)>=1 and len(sys.argv)<=3: 
        # --------- PreProcess----------------
        start_addr = '0'           
        if len(sys.argv)==3:        
            start_addr = sys.argv[2]        
        
        basePath = get_basePathFromArgv(sys.argv)

        fileType = [".bin"]
        (fileList, dirDepth) = get_FileListFromArgv(sys.argv, fileType)  
        # --------------------------------------------------------
        print" * data preprocess start...\n"       
        for i in range(0, len(fileList)):            
            start = time.clock()
            print " * parse start --> %s \n"% os.path.split(fileList[i])[1]                                            
            # ********************************************************
            # call funcion "log_parse_all"
            log_parse_all(fileList[i], basePath, start_addr)
            
            # *********************************************************        
            print" * Duration: %.2f seconds.\n"% (float(time.clock()) - float(start))
          
        exit(0)

