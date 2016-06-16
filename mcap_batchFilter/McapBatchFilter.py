#======================================================================================
#       Function:       main function for mcap file filter
#       Author:         Fan, Shuangxi (NSN - CN/Hangzhou)
#       Date:           2016-04-05
#======================================================================================

#!/usr/bin/python

#coding=utf-8

import sys, os
import subprocess
import time
import re

from utils.common import *

# ##################################################################
infoFile          = "README"
fileType          = [".mcap"]
pcap_header_len   = 24 # unit: byte
outFile_suffixStr = 'filterData'
msgId_identify      = "messageId ==>"  # not used
filterRule_identify = "Filter_Rule ==>"

# ##################################################################
# function: GetExtractedData
#*      This script can Extract message Data from pcap file,
# ##################################################################
def GetExtractedData(fileList, filterRule, outDir): 

    validFileNum = 0     
    for i in range(0, len(fileList)):
        start = time.clock()
        print " *  [%d/%d] -->  %s  \n"% (i+1, len(fileList), os.path.split(fileList[i])[1])                                          
        # ********************************************************
        valid_flag = mcapFilterByFilterRule(fileList[i], filterRule, outDir)

        if valid_flag:
            validFileNum += 1  
            print "     FINISH, OK, take: %.2f seconds.\n"% (float(time.clock()) - float(start))
        else:  
            print "     FINISH, NO VALID DATA FOUND! take: %.2f seconds.\n"% (float(time.clock()) - float(start))
        
    return validFileNum


# ##################################################################
# function: pcap_filter
#*      filter pcap file with the filter condition
#       
# ##################################################################
def mcapFilterByFilterRule(capFile, filterRule, outDir):

    savefile = os.path.join(outDir, os.path.split(capFile)[1])
    fileType = capFile[capFile.rfind('.'):]
    valid_flag = 0

    filter_cmd = ['tshark', '-r', capFile, '-Y', filterRule, '-F', fileType[1:], '-w', savefile]        

    try:
        subprocess.Popen(filter_cmd).wait()

        if os.path.getsize(savefile) <= pcap_header_len:
            os.remove(savefile)
        else:
            valid_flag = 1
    except:
        print " ** Error: In calling tshark API, please turn 'README' for help.\n"        
        exit(1)

    return valid_flag


# ###############################################
# make filter str  
def get_filter_str(messageIds):
    filter_str = "" 
    for i in range(0, len(messageIds)):        
        filter_str += "(sicap[2:4] contains " + messageIds[i] + ")"
        filter_str += "||" 

    filter_str = filter_str[0: -2]

    return filter_str


# ###############################################
# read filter rule from infoFile file
def get_filterRule(infoFile):
    filterRule = []
    messageIdInfo = []

    if os.path.isfile(infoFile):
        print " * Reading infoFile File...\n"
        configureFile = open(infoFile, 'r')
    else:
        print" ** Error: infoFile File '%s' not exit !!\n"% infoFile
        return
    Lines = configureFile.read().splitlines()
    configureFile.close()
    
    LineNum = len(Lines)
    for i in range(0, LineNum):
        if Lines[i].find(filterRule_identify) != -1:                 
            filterRule = Lines[i][Lines[i].find(filterRule_identify)+len(filterRule_identify) : ].strip()
            break
        elif Lines[i].find(msgId_identify) != -1:
            #messageIdInfo = Lines[i][Lines[i].find(msgId_identify)+len(msgId_identify) : ].split(',')
            break

    return filterRule


# ###############################################
# split message Ids from messageIdInfo
def get_messageIdsFromMessageIdInfo(messageIdInfo):

    messageIds = []
    messageId_num = 0
    messageId_pattern = re.compile('[0-9a-fA-F]')
    for messageId in messageIdInfo:
        messageId = messageId.strip()
        print "  - message Id '%s' " % (messageId)
        if messageId_pattern.match(messageId) != None:
            if messageId.find('-')>0:
                msgId_start = int(messageId.split('-')[0].strip(),16)
                msgId_end = int(messageId.split('-')[1].strip(),16)
                for j in range(msgId_start, msgId_end+1):
                    messageId = '0'*(4-len(hex(j)[2:])) + hex(j)[2:]
                    #print " - message Id [%d]: %s" % (messageId_num, messageId)
                    messageIds.append(messageId)
                    messageId_num += 1
                            
            elif messageId.find('.')>=0:
                messageId = messageId[0:-2]        
                #print " - message Id [%d]: %s" % (messageId_num, messageId)
                messageIds.append(messageId)
                messageId_num += 1
            else:
                #print " - message Id [%d]: %s" % (messageId_num, messageId)
                messageIds.append(messageId)
                messageId_num += 1            
    if messageIds == []:
        print "** No valid messageId find in filter_condition file!"
        exit(1)
        
    return messageIds


# ########**** main ****#######***** main *****#######**** main ****#########
if __name__ == '__main__':
    
    if  len(sys.argv)==2 and sys.argv[1].upper().find('HELP')>=0:
        print'''
   *************************** Usage: ***************************
   # Set Filter_Rule in 'README -> [Initiation]' as the filter condition
        -input: 
             -[1] packet file or packet file dir:
       @example:
               python McapBatchFilter.py packetFile.mcap
               python McapBatchFilter.py packetFileDir
       - output:
         in dir " ***_filterData ":
             
   **************************************************************
        '''
        exit(0) 
        
    elif len(sys.argv) >= 1 and len(sys.argv) <= 2: 
        # --------- PreProcess----------------            
        basePath = get_basePathFromArgv(sys.argv)
        infoFile = os.path.join(basePath, infoFile)
        
        (fileList, dirDepth) = get_FileListFromArgv(sys.argv, fileType) 

        outDir = make_DirByDepth(fileList[0], outFile_suffixStr, dirDepth)
        
        print "\n * Total File(s): %d "% len(fileList)
        print "\n * Output Location: %s "% outDir

        filterRule = get_filterRule(infoFile)

        print "\n ==> Filter Process Start..."
        print "----------------------------------------------\n" 
        # --------------------------------------------------------     
        start = time.clock()

        validFileNum = GetExtractedData(fileList, filterRule, outDir)

        # ********************************************************* 
        print "\n----------------------------------------------\n" 
        print " * All files filter finished.  [ %d ] valid file(s) obtained.\n" % validFileNum 
                     
        print " * Duration: %.2f seconds.\n"% (float(time.clock()) - float(start))
      
        exit(0)

