# -*- coding: utf-8 -*-
# ##############################################################################
#       Function:       Alarm Faults Parser from snapshot buffer
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

currentPath = os.getcwd()
utilsPath = os.path.join(currentPath, "utils")
logParseContextPath = os.path.join(currentPath, "ParseContext")
sys.path.append(currentPath)
sys.path.append(utilsPath)
sys.path.append(logParseContextPath)

from common import *

from SnapshotParser import Snapshot
from RtmLogParser import LogProcess
    
'''
# ##############################################################################
TODO:

# ##############################################################################
'''  
# ######################## global definations  ################################# 
global basePath

# #################################################################


def get_basePath(argv):
    global basePath
    if os.path.dirname(argv[0]) != '':      
        basePath = os.path.dirname(argv[0])
    else:
        basePath = os.getcwd()  
  

# #################################################################
# function: get_SnapShotFileList
# set global paras,such as: 
#  - RTLDumpId dic, RTLFreezeCause dic
#  - SnapShotFileList
# #################################################################
def get_SnapShotFileList(argv):    

    get_basePath(argv)   

    if len(argv)==1:
        SnapShotPath = getInputFileNamesGui()
    else:            
        SnapShotPath = argv[1]
        
    if os.path.split(SnapShotPath)[0] == '':
        SnapShotPath = os.path.join(basePath, SnapShotPath)
              
    SnapShotFileList = []
    if os.path.isdir(SnapShotPath):
        for root,dirs,files in os.walk(SnapShotPath):   
            for fn in files:
                if fn[-4:] == ".bin":
                    validFile = os.path.join(root, fn)
                    SnapShotFileList.append(validFile)        
    elif os.path.isfile(SnapShotPath):
        SnapShotFileList.append(SnapShotPath)        
    else:
        print"**Error: '%s' not exit! please check the path and the name of the file.\n"% SnapShotPath
        exit(-1) 
                              
    return SnapShotFileList


def get_ParsedDataDir(SnapShotFile):
    ParsedDataDir = SnapShotFile[0:SnapShotFile.rfind('.')] + "_ParsedData"    
    if os.path.isdir(os.path.split(SnapShotFile)[0]) == False:            
        current_path = os.getcwd()
        ParsedDataDir = os.path.join(current_path, ParsedDataDir)                
    if os.path.isdir(ParsedDataDir) == False:
        os.makedirs(ParsedDataDir)

    TempFileDir = os.path.join(ParsedDataDir, "temp")     
    if os.path.isdir(TempFileDir) == False:
        os.mkdir(TempFileDir) 
 
    return ParsedDataDir  


# ##########################################################    
# main function for log parse trigger
#
# ##########################################################
def log_parse_all(SnapShotFile, start_addr):  
    # ------------ snapshot dumpblock split ---------
    print" * Snapshot parser start..."
    snapshot_obj = Snapshot(SnapShotFile)  
    dumpblock_data = snapshot_obj.get_dumpblocks()
    # --------------------- Log decode ------------------  
    ParsedDataFile = SnapShotFile[0:SnapShotFile.rfind('.')] + "_ParsedLog.txt"     
    if dumpblock_data:
        print" * Log parse start..."             
        log_obj = LogProcess(dumpblock_data, ParsedDataFile)
        log_obj.log_parse()
        

# ########**** main ****#######***** main *****#######**** main ****#########
if __name__ == '__main__':
    
    if  len(sys.argv)==2 and sys.argv[1].upper().find('HELP')>=0:
        print'''
   *************************** Usage: ***************************
    -input:            
         -[1] alarmFaultsParser: input file, .bin file or directory with .bin files
               the .bin file in current path or full path            
   @example:
        alarmFaultsParser.py xxx.bin
        alarmFaultsParser.py RtlDumpBin
   - output:
        - Out put Location: the same path as input file
        - Parsed Log file is "xxx_ParsedLog.txt"            
   **************************************************************
        '''
        exit(0) 
        
    elif len(sys.argv)>=1 and len(sys.argv)<=2: 
        # --------- PreProcess----------------
        start_addr = '0'
        
        SnapShotFileList = get_SnapShotFileList(sys.argv)  
        # --------------------------------------------------------
        print" * data preprocess start...\n"       
        for i in range(0, len(SnapShotFileList)):            
            start = time.clock()
            print " * parse start --> %s \n"% os.path.split(SnapShotFileList[i])[1]                                            
            # ********************************************************
            # call funcion "log_parse_all"
            log_parse_all(SnapShotFileList[i], start_addr)
            
            # *********************************************************        
            print" * Duration: %.2f seconds.\n"% (float(time.clock()) - float(start))
          
        exit(0)

