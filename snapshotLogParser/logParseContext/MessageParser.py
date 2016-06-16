# -*- coding: utf-8 -*-
# ##############################################################################
# Class: MassageDecode():
# [Function]:  class for Massage Decode
#       Author:         Fan, Shuangxi (NSN - CN/Hangzhou)
#       draft:          2014-10-14 
#       modify(split):  2015-11-20
#*      description:   
# ##############################################################################
#!/usr/bin/python

import os
import shutil
import datetime, time

from utils.common import debugLogSetup
from utils.CHexStrProcess import *
from utils.CBinDataConvert import *
    
'''
# ##############################################################################
TODO:
1. parse message directly, out put to txt file, 
   list the message Id and message header in front of the file

# ##############################################################################
'''

###################################################################   
#*  global variables defination
#  - Message Decoder paras 
###################################################################


HexDataWriteFlag = False
Msg_dumpId = 2

packet_header_len    = 16  # (16 Bytes)
protocol_header_len  = 42  # (42 Bytes)
Enthernet_header_len = 14  # (14 Bytes)
Ip_header_len        = 20  # (20 Bytes)
UDP_header_len       = 8   # (8 Bytes)

MsgHeader_len        = 6   # unit: word (24 Bytes)
MsgHeader_time_indx  = 3
MsgHeader_date_indx  = 4

MsgHeader_segment = {
    'time':     [10, 6, 6, 5, 5],
    'date':     [6, 2, 4, 4, 12, 3, 1]
    }


# pcap header (24 Bytes)
Pcap_header = (
    '0xD4C3B2A1',   # Magic
    '0x02000400',   # Version
    '0x00000000',   # Timezone
    '0x00000000',   # Sigflags
    '0xFFFF0000',   # Snaplen
    '0x01000000'    # Linktype
    )

# packet header (16 Bytes)
Packet_header = (
    '0x7F2B3B54',   # Timestamp (GMTime)
    '0x26EF0A00',   # Timestamp (microTime)
    '0x56000000',   # Caplen
    '0x56000000'    # Len
    )

# protocol_header (42 Bytes)
# include:
#  - Enthernet header   (14 Bytes),
#  - Ip header          (20 Bytes),
#  - UDP header         (8 Bytes)
Protocol_header = (
    '0xF07D68FA',   #(0) - Ethernet (14 Byte)
    '0x852560A8',   # 
    '0xFE3BBF07',
    '0x08004500',   #(3) - Internet Protocol (20 Byte, from third Byte) 
    '0x00487B58',   #(4)   Total Length (first 2 Byte) 
    '0x40003F11',
    '0xDD12C0A8',
    '0xFD6AC0A8',
    '0x647E3E88',   #(8) - UDP (8 Byte, from third Byte) 
    '0x2EE50034',   #(9)   Length (last 2 Bytes) 
    '0x0000'        #(10)   Checksum (2 Bytes)
    )

             
# ##############################################################################
# Class: MassageDecode():
# [Function]:  class for Massage Decode
# [Methods]:
# * unixTimeAdjust : Adjust timestr to hex unix timestamp
#    - input:
#      - timeList = [year,month,day,hours,minutes,seconds,microseconds]
#      - OrderFlag: '0' (defult) original order, '1' byte reversion order
#    - output:    
#      - GMTtime_str: hex str, UNIX-format
#      - microTime_str: hex str
# * msg_parse: parse message, packet the msg data to .pcap file
#   - main function for message parse
# ############################################################################## 

class MassageDecode():
    '''
    ##################################################################
    TODO: 
    1. parse message data directly
    2. get message struct from source files
    3. output -> .xls file
    4. save history record
    
    ##################################################################
    '''    
    def __init__(self, msg_dump_data, RTLDumpId, ParsedDataDir, __DEBUG_LOG__):         
        self.hexStr_obj = CHexStrProcess()
        self.RTLDumpId = RTLDumpId

        self.ParsedDataDir = ParsedDataDir
        TempFileDir = os.path.join(ParsedDataDir, 'temp')     
        if os.path.isdir(TempFileDir) == False:
            os.mkdir(TempFileDir) 
        self.TempFileDir = TempFileDir
        self.__DEBUG_LOG__ = __DEBUG_LOG__    

        global Msg_dumpId
        self.msg_dumpId = Msg_dumpId
        self.msg_dump_data = msg_dump_data
        
    # ######################################################
    # unixTimeAdjust:
    # ######################################################
    def unixTimeAdjust(self, timeList, OrderFlag = '0'):
        format = '%Y-%m-%d %H:%M:%S'
        year        = timeList[0]
        month       = timeList[1]
        day         = timeList[2]
        hours       = timeList[3]
        minutes     = timeList[4]
        seconds     = timeList[5]
        microseconds = timeList[6]
        
        date_time = datetime.datetime(year, month, day, hours, minutes, seconds)
        mk_time = time.mktime(date_time.timetuple())
        '''
        time_struct = time.localtime(mk_time)
        dt = time.strftime(format, value)
        '''
        GMTtime_str   = "%08x"% int(mk_time)
        microTime_str = "%08x"% int(microseconds)

        if OrderFlag == '1':
            GMTtime_str = self.hexStr_obj.AdjustEndian(GMTtime_str)
            #microTime_str = self.hexStr_obj.AdjustEndian(microTime_str)

        return (GMTtime_str, microTime_str)  

    # ######################################################
    # msg_parse: packet the message trace data to .pcap file
    #  - main function for message trace parse
    # ######################################################
    def msg_parse(self):       
        if self.msg_dump_data != []:
            pcap_data = []
            # add pcap header
            for i in range(0,len(Pcap_header)):         
                pcap_data.append(Pcap_header[i]+'\n')
                
            # get packet header
            packet_header_data = []
            for i in range(0,len(Packet_header)):         
                packet_header_data.append(Packet_header[i]+'\n')
    
            # get protocol header
            protocol_header_data = []
            for i in range(0,len(Protocol_header)):         
                protocol_header_data.append(Protocol_header[i]+'\n')
      
            msg_indx = 0
            while msg_indx < len(self.msg_dump_data):
                # message header process
                # MsgHeader_len = 6  unit: word (24 Bytes)
                msg_header = self.msg_dump_data[msg_indx : msg_indx + MsgHeader_len]
                
                time_str = msg_header[MsgHeader_time_indx] # MsgHeader_time_indx = 3                
                date_str = msg_header[MsgHeader_date_indx] # MsgHeader_date_indx = 4

                time_len = MsgHeader_segment['time']
                date_len = MsgHeader_segment['date']

                time = self.hexStr_obj.word_split(time_str, time_len)                
                date = self.hexStr_obj.word_split(date_str, date_len)

                year        = 2015
                month       = date[2]+1
                day         = date[0]
                hours       = time[3]
                minutes     = time[2]
                seconds     = time[1]
                microseconds = time[0]
                  
                timeList = [year,month,day,hours,minutes,seconds,microseconds]
                
                (GMTtime_str,microTime_str) = self.unixTimeAdjust(timeList, '1')
                GMTtime_str   = '0x'+ GMTtime_str +'\n'
                microTime_str = '0x'+ microTime_str +'\n'

                packet_header_data[0] = GMTtime_str
                packet_header_data[1] = microTime_str

                msg_indx += MsgHeader_len
                
                # get info from message data part                
                MsgData_len = int(self.msg_dump_data[msg_indx+3][2:6],16)
                UDP_len = MsgData_len + UDP_header_len
                Ip_Total_len = UDP_len + Ip_header_len
                packet_len = Ip_Total_len + Enthernet_header_len

                packet_len_str = "%08x"% (packet_len)
                packet_len_str = '0x' + self.hexStr_obj.AdjustEndian(packet_len_str)
                
                Ip_Total_len_str = "%04x"% (Ip_Total_len)
                UDP_len_str = "%04x"% (UDP_len)
                                
                # add packet header
                packet_header_data[2] = packet_len_str +'\n'
                packet_header_data[3] = packet_len_str +'\n'

                pcap_data.extend(packet_header_data)
                    
                # add protocol header
                protocol_header_data[4] = '0x'+Ip_Total_len_str + protocol_header_data[4][6:]
                protocol_header_data[9] = protocol_header_data[9][0:6] + UDP_len_str +'\n'
                pcap_data.extend(protocol_header_data)              

                # add message data part
                this_msg_data = self.msg_dump_data[msg_indx : msg_indx+MsgData_len/4]
                #pcap_data.extend(this_msg_data)
                for i in range(0,len(this_msg_data)):
                    #pcap_data.append(this_msg_data[i].split('\n')[0]+'\n')
                    pcap_data.append(this_msg_data[i]+'\n')
                    
                msg_indx += MsgData_len/4
               
            # write data file                      
            dumpName = self.RTLDumpId[self.msg_dumpId]
            dumpName = dumpName[dumpName.find('_')+1:]               
            #file_name = ("dumpId(%d)_%s_pcap.dat"%(self.msg_dumpId,dumpName)) 
            file_name = ("%s_Pcap.dat"%(dumpName))
            pcap_filename = os.path.join(self.ParsedDataDir, file_name)   
            pcap_file = open(pcap_filename,'w')
            for i in range(0,len(pcap_data)):
                pcap_file.write(pcap_data[i])
            pcap_file.close()
            
            # generate binary pcap file
            out_file = pcap_filename[0:-9]+'.pcap'
            binData_obj = CBinDataConvert()
            binData_obj.Hex_to_Bin(pcap_filename, out_file, '0')
            
            self.__DEBUG_LOG__.info(" * Out file: %s"% os.path.basename(out_file)) 
            
            global HexDataWriteFlag
            if True == HexDataWriteFlag:                
                try:
                    shutil.move(pcap_filename, self.TempFileDir)
                except:
                    os.remove(pcap_filename)
            else:
                os.remove(pcap_filename)
                
        self.__DEBUG_LOG__.info(" * Message data parse finish!")
                                  

