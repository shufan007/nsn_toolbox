# -*- coding: utf-8 -*-
# ##############################################################################
# class Snapshot():
# [Function]:  class for snapshot bin preprocess
#       Author:         Fan, Shuangxi (NSN - CN/Hangzhou)
#       draft:          2014-10-14 
#       modify(split):  2015-11-20
#*      description:    
# ##############################################################################
#!/usr/bin/python

import os

from utils.common import debugLogSetup
from utils.CHexStrProcess import *
from utils.CBinDataConvert import *

'''
# ##############################################################################
TODO:
1. 
	2) add one more access feature: 
	   -> double click to execute for identify .bin file in the same path;
           -> read .bin files from a dir or current path 
	   -> save runtime info and exception log to file.
	3) close to save unpacked data

2. performance optimization:
   - speed the way of unpack .bin file
   - use mmap, use slicing to read from the file
   - set struct and save the structs ectected from source file
   - record the modify time of the source file 
   - flush file
   - use array to instand some list
6. judge and note 'header mask' at the beginning. [Done]

# ##############################################################################
'''

# ######################## global definations  ################################# 

###################################################################   
#*  global variables defination
#  - for source code path defination 
###################################################################

DSP_Path = r"C_Application\SC_UP\DSP"

HexDataWriteFlag = False
###################################################################   
#*  global variables defination: dir and file name defination 
#  - for snapshot header parse and block split
###################################################################

KByte = 1024
MByte = 1024 * KByte

# Byte Block length for single unpack bin process
ByteBlock_Len = 1 * MByte

###################################################################   
#*  global variables defination
#  - SnapshotHeader paras 
###################################################################

# SnapshotHeader paras 
SnapshotHeader_mask = "ABCDABCD"
SnapshotHeader_len  = 6     # Unit: word 
SnapshotHeader_segment = {
    'date':     [22, 4, 6],    # year, month, day
    'time':     [6, 6, 8, 12]  # hour, minute, second, millisec
    }
    
# DumpSubHeader paras
DumpSubHeader_len = 6       # Unit: word
                
DumpSubHeader_segment = {
    'dumpId_and_cause': [16, 16],            # dumpId, dumpCause
    'date':             [22, 4, 6],          # year, month, day
    
    # hour, minute, second, millisec, extendInfoFlag, extraHeaderFlag
    'time_and_flag':    [6, 6, 6, 12, 1, 1]  
    }

# dumpblock length, dump Id
dumpHD_segment = [16, 16]  

# the order can be use
Time_field = ['year', 'month', 'day', 'hour', 'minute', 'second', 'millisec']
#-------------------------------------------


# ##############################################################################   
            
# ##############################################################################
# class Snapshot():
# [Function]:  class for snapshot bin preprocess
# - part_unpack_parse used, which can speed the unpack process
# [Methods]:
# * __header_parse:    parse snapshot header
# * __subheader_parse: parse subheader
# * __snapshot_split:  exteact and split data of each dump block
# * __write_data:      write header data and dump block data to files
# * get_dumpblocks:
#  - main function for parse all trace data
#  - Codec Log Trace
#  - Message Trace
#  - TTi Trace
#    such as: L1TraNonHs Trace; L1TraHs Trace; Encoder Trace; FP Trace
#             
# ##############################################################################                
class Snapshot():
    
    def __init__(self, SnapShotFile, start_addr, RTLDumpId, RTLFreezeCause, ParsedDataDir, __DEBUG_LOG__):
        global ERTLDumpId_File
        global ERTLFreezeCause_File
        global TempFileDir
        TempFileDir = os.path.join(ParsedDataDir, 'temp')     
        if os.path.isdir(TempFileDir) == False:
            os.mkdir(TempFileDir)         
        self.__DEBUG_LOG__ = __DEBUG_LOG__

        self.hexStr_obj = CHexStrProcess()
        self.binData_obj = CBinDataConvert()
      
        self.debug_level = 0
        self.SnapShotFile = SnapShotFile
        
        global ByteBlock_Len
        self.ByteBlockLen = ByteBlock_Len
        self.ByteBlock_num = 0
    
        self.RTLDumpId = RTLDumpId
        self.RTLFreezeCause = RTLFreezeCause
        
        self.dumpId_num          = len(self.RTLDumpId)
        self.freezeCause_num     = len(self.RTLFreezeCause) 
        
        self.start_addr = int(start_addr, 16)
        
        self.endian_flag = '0'
        
        self.header_unpack_len = 6*4
        self.ByteIndx = self.start_addr
        self.actual_length = self.ByteBlockLen
                                       
        self.hex_data = []
        self.data_len = 0
        self.snapshotSize = 0

        self.subheader_indx = None 
        
        self.dumpblock_data     = [[] for i in range(0, self.dumpId_num)]
        self.dumpblock_eachNr   = [0 for i in range(0, self.dumpId_num)]
        self.dumpblock_Data_len = [[] for i in range(0, self.dumpId_num)]        
        
        self.header_str = ''
        self.subheader_info = ''

        self.ParseInfoFile = os.path.join(ParsedDataDir, "ParseInfo.log")
        
        
    # #############################################################
    # parse snapshot header 
    # #############################################################
    def __header_parse(self):        
        header_flag = 0
        header_start = self.ByteBlockLen        
        while header_flag == 0:            
            '''
            (hex_data, actual_length) = self.binData_obj.Bin_to_Hex(self.SnapShotFile,\
                                        self.ByteIndx,\
                                        self.ByteBlockLen,\
                                        self.endian_flag)
            #self.ByteIndx += actual_length
            self.ByteIndx += self.ByteBlockLen
            self.ByteBlock_num += 1                                        
            '''
            (hex_data, actual_length) = self.binData_obj.Bin_to_Hex(self.SnapShotFile,\
                                        self.ByteIndx,\
                                        self.header_unpack_len,\
                                        self.endian_flag) 

            self.actual_length = actual_length 
            
            for i in range(0, len(hex_data)):
                if hex_data[i].upper().find(SnapshotHeader_mask) >= 0:
                    header_flag = 1
                    header_start = i
                    self.snapshotSize = int(hex_data[i+5], 16)
                    break
                #elif self.ByteBlock_num == 1 and i == 0:
                elif i == 0:
                    self.__DEBUG_LOG__.warning("** Snapshot Header mask not find in the header of the .bin file.")
                    exit(-1)
        
        if header_flag == 1:            
            (hex_data, actual_length) = self.binData_obj.Bin_to_Hex(self.SnapShotFile,\
                                        self.ByteIndx,\
                                        self.snapshotSize,\
                                        self.endian_flag)             
            
            self.hex_data = hex_data[header_start:]
            self.data_len = int(self.snapshotSize/4) + 1 - header_start
            '''
            if header_start + SnapshotHeader_len > self.ByteBlockLen:
                (hex_data, actual_length) = self.binData_obj.Bin_to_Hex(self.SnapShotFile,\
                                            self.ByteIndx,\
                                            self.ByteBlockLen,\
                                            self.endian_flag)
                self.ByteIndx += self.ByteBlockLen
                self.hex_data.extend(hex_data)
                self.data_len += int(actual_length/4)
                self.actual_length = actual_length
                self.ByteBlock_num += 1
            '''
            date_str    = self.hex_data[1]
            time_str    = self.hex_data[2]
            frameNr_str = self.hex_data[3]
            slotNr_str  = self.hex_data[4]

            date_len = SnapshotHeader_segment['date']
            time_len = SnapshotHeader_segment['time']
            
            date = self.hexStr_obj.word_split(date_str, date_len)
            time = self.hexStr_obj.word_split(time_str, time_len)              
            frameNr = int(frameNr_str, 16)
            slotNr = int(slotNr_str, 16)            
            
            # package header string              
            self.header_str = ''
            self.header_str += "Snapshot Header:\n"
            self.header_str += "  Mask:     %s \n"% (self.hex_data[header_start].split())
            self.header_str += "  Date:     %04d-%02d-%02d \n"% tuple(date)
            self.header_str += "  Time:     %02d:%02d:%02d.%03d \n"% tuple(time)
            self.header_str += "  FrameNr:  %d \n  SlotNr:   %d\n"% (frameNr, slotNr)
            self.header_str += "  snapshotSize:  %d (Bytes)\n"% (self.snapshotSize)
            self.header_str += "%s\n"% ('**'*30)
        else:
            self.__DEBUG_LOG__.warning( "** No dump block data in this file.")
            exit(1) 
            
        # set the offset to subheader   
        self.subheader_indx = header_start + SnapshotHeader_len
        
    # #############################################################    
    # parse snapshot subheader  
    # #############################################################
    def __subheader_parse(self,Indata):
        OutData = []
        
        dumpId_and_cause_len = DumpSubHeader_segment['dumpId_and_cause']
        date_len = DumpSubHeader_segment['date']
        time_len = DumpSubHeader_segment['time_and_flag']      
        
        dumpId_and_cause = self.hexStr_obj.word_split(Indata[0], dumpId_and_cause_len)
        Byte_len = int(Indata[1], 16)
        date = self.hexStr_obj.word_split(Indata[2], date_len)
        time_and_flag = self.hexStr_obj.word_split(Indata[3], time_len)

        OutData.append(dumpId_and_cause)
        OutData.append(Byte_len)
        OutData.append(date)
        OutData.append(time_and_flag)

        return OutData  
            
    # #############################################################    
    # split all dumpblocks
    # #############################################################
    def __snapshot_split(self):        
        # for print string align
        dumpBlockNr_len = 2
        dumpName_strlen = 15
        cause_strlen    = 8
        addr_strlen     = 5
        data_len_strlen = 4
        dumpId_strlen   = 2
        
        self.__DEBUG_LOG__.info(" * [Get Dump Blocks:]")
        self.subheader_info = '[Dump Blocks:]\n'
        
        dumpBlockNr = 0       
        #while self.subheader_indx + DumpSubHeader_len < self.data_len:
        while self.subheader_indx + DumpSubHeader_len < self.data_len:            
            if self.debug_level == 1:
                self.__DEBUG_LOG__.info(" subheader_indx: %d, value: %s"% self.subheader_indx, self.hex_data[self.subheader_indx])
  
            SubheaderData = self.hex_data[self.subheader_indx: self.subheader_indx+DumpSubHeader_len]
            OutData = self.__subheader_parse(SubheaderData)
            
            dumpId = OutData[0][0]
            freezeCauseId = OutData[0][1] 
            
            if (dumpId>=0 and dumpId< self.dumpId_num) \
               and (freezeCauseId>=0 and freezeCauseId< self.freezeCause_num):
                
                self.dumpblock_eachNr[dumpId] += 1
                dumpName = self.RTLDumpId[dumpId]
                dumpName = dumpName[dumpName.find('_')+1:]

                freezeCause = self.RTLFreezeCause[freezeCauseId]
                freezeCause = freezeCause[freezeCause.find('_')+1:]
                
                Byte_len = OutData[1]
                this_data_len = Byte_len/4
                self.dumpblock_Data_len[dumpId].append(this_data_len)

                date = OutData[2]
                time = OutData[3][0:4]
                extendInfoFlag  = OutData[3][4]
                extraHeaderFlag = OutData[3][5]
                           
                self.subheader_info += " [%0*d] "%(dumpBlockNr_len,dumpBlockNr)
                self.subheader_info += "%04d-%02d-%02d "% tuple(date)
                self.subheader_info += "%02d:%02d:%02d.%03d "% tuple(time)
                dumpName_str = dumpName + ',' + ' '*(dumpName_strlen-len(dumpName))
                self.subheader_info += "dumpId(%0*d): %s "%(dumpId_strlen,dumpId, dumpName_str)
                cause_str = freezeCause + ',' + ' '*(cause_strlen-len(freezeCause))
                self.subheader_info += "freeze_cause(%-2d): %s "%(freezeCauseId, cause_str)
                self.subheader_info += "subheader_addr: %0*d, "% (addr_strlen, self.subheader_indx)
                self.subheader_info += "data_length:%*d (%4d Bytes)\n"% (data_len_strlen, this_data_len, Byte_len)
                #self.subheader_info += "extendInfoFlag: %s, "% (extendInfoFlag)
                #self.subheader_info += "extraHeaderFlag: %s\n"% (extraHeaderFlag)

                # print to screen
                self.__DEBUG_LOG__.info("[dumpId: %02d], Cause:%2d, block_addr: %0*d, data_len:%4d"%\
                      (dumpId, freezeCauseId, addr_strlen, self.subheader_indx, this_data_len))
                    
                # get DumpSubHeader data part
                data_part_start_indx = self.subheader_indx + DumpSubHeader_len
                if data_part_start_indx + this_data_len < self.data_len:
                    for i in range(data_part_start_indx, data_part_start_indx + this_data_len):
                        self.dumpblock_data[dumpId].append(self.hex_data[i])
                    '''        
                    elif self.actual_length == self.ByteBlockLen:
                        (hex_data, actual_length) = self.binData_obj.Bin_to_Hex(self.SnapShotFile,\
                                                    self.ByteIndx,\
                                                    self.ByteBlockLen,\
                                                    self.endian_flag)
                        self.ByteIndx += self.ByteBlockLen
                        self.hex_data.extend(hex_data)
                        self.data_len += int(actual_length/4)
                        self.actual_length = actual_length
                        self.ByteBlock_num += 1
                    '''    
                else:
                    for i in range(self.subheader_indx, self.data_len):
                        self.dumpblock_data[dumpId].append(self.hex_data[i])
                    break
                
                self.subheader_indx += (DumpSubHeader_len + this_data_len)
                dumpBlockNr += 1
            else:
                break        
        # ------------------- sum up -------------------    
        global KByte    
        self.__DEBUG_LOG__.info(" * Total block number: %d, Total data length: %d KByte(s)"% (dumpBlockNr, self.data_len/KByte))
        
        '''        
        unpackedData_len = (self.ByteBlockLen * self.ByteBlock_num)/ KByte
        print "\n * unpacked binary data length: %d KByte(s)"% unpackedData_len
        '''
        self.__DEBUG_LOG__.info(" --------------------------------------------")
        
    # #############################################################    
    # write splited datas to separated files
    # #############################################################
    def __write_data(self):                
        # write extract dump block data
        global HexDataWriteFlag
        
        if True == HexDataWriteFlag:
            OutData = open(os.path.join(TempFileDir, 'ValidData.dat'),'w')
            for i in range(0, len(self.hex_data)):
                OutData.write(self.hex_data[i]+'\n')
            OutData.close()
               
        subHD_str = '[Dump Block Info:]\n'
        BlockId_str = ' BlockId: '
        BlockNr_str = ' BlockNr: '
        dumpBlock_totalNr = 0
        for dumpId in range(0,  self.dumpId_num):
            if self.dumpblock_eachNr[dumpId]>0:
                dumpBlock_totalNr += self.dumpblock_eachNr[dumpId]
                BlockId_str += " %02d "% (dumpId)
                BlockNr_str += " %-2d "% (self.dumpblock_eachNr[dumpId])
                
        BlockId_str += "\n"
        BlockNr_str += "\n"
        subHD_str += (BlockId_str + BlockNr_str)
        subHD_str += " Total block number: [%d]\n"% (dumpBlock_totalNr)
        
        global KByte
        subHD_str += " Total data length: %d KByte(s)\n"% (self.data_len/KByte)
        
        subHD_str += "%s\n"% ('--'*30)
        self.subheader_info =  subHD_str + self.subheader_info

        parseInfo_file = open(self.ParseInfoFile,'w')                                
        parseInfo_file.write(self.header_str)
        parseInfo_file.write(self.subheader_info)        
        parseInfo_file.close()

        # write dumpblock       
        self.__DEBUG_LOG__.info(" * [Dump Blocks:]")
        for i in range(0,  self.dumpId_num):           
            if self.dumpblock_data[i]!= []:
                dumpName = self.RTLDumpId[i]
                self.__DEBUG_LOG__.info("  dumpblock_data[%02d]: %s, total length: %d"% \
                      (i, dumpName, len(self.dumpblock_data[i])))
                
                if True == HexDataWriteFlag:
                    file_name = dumpName[dumpName.find('_')+1:] + '.dat'
                    dumpblock_filename = os.path.join(TempFileDir, file_name)
                    dumpblock_file = open(dumpblock_filename,'w')                    
                    for j in range(0,len(self.dumpblock_data[i])):
                        #dumpblock_file.write(self.dumpblock_data[i][j].split('\n')[0]+'\n')
                        dumpblock_file.write(self.dumpblock_data[i][j]+'\n')
                    dumpblock_file.close()

        self.__DEBUG_LOG__.info(" ----------------------------------------")        
        
    # ##########################################################    
    # get_dumpblocks
    # function: split all dump blocks
    # return dumpblock_data, dumpblock_Data_len
    # ##########################################################
    def  get_dumpblocks(self):                
        # ------------ snapshot dumpblock split ---------
        self.__header_parse()
        self.__snapshot_split()        
        self.__write_data()
        
        return (self.dumpblock_data, self.dumpblock_Data_len)
        

