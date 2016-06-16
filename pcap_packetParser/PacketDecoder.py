#======================================================================================
#       Function:       main function for pcap file decode, and message decode
#       Author:         Fan, Shuangxi (NSN - CN/Hangzhou)
#       Date:           2014-09-15
#*  *   description:    This script can Extract message Data from pcap file
#                       save data to .xls file
#======================================================================================

#!/usr/bin/python

#coding=utf-8

import sys, os
import subprocess
import xlwt, xlrd
import time, datetime
import shutil
import re

from GlobDef import *
from ProtocolClasses import *
#------------------------------------------------------------------
'''
 TODO:
     1. add log process, output to log file
     2. extract messages struct from sack

'''    
# ##################################################################


# ##################################################################
# function: GetExtractedData
#*      This script can Extract message Data from pcap file,
#       save data to .xls file
# ##################################################################
def GetExtractedData(network_port, capture_time):
  
    # ------------- globol def --------------
    global printLevel_1
    printLevel_1 = 0
    
    global BasePath
    global API_Data_dir
    global raw_pcap_file
    global wireshark_paras_file
    global result_file   
            
    # full path
    
    API_Data_dir         = os.path.join(BasePath, API_Data_dir)    
    wireshark_paras_file = os.path.join(BasePath, wireshark_paras_file)    
    raw_pcap_file        = os.path.join(BasePath, raw_pcap_file)
    #raw_pcap_file        = os.path.join(API_Data_dir, raw_pcap_file)
    result_file          = os.path.join(API_Data_dir, result_file)    
    # ----------- globol def end ------------ 
    
    # move dir 'parsed_data'
    moveFile(API_Data_dir)   
    
    # read parameters from excel
    (filter_conditions) = read_wireshark_paras(wireshark_paras_file)
    
    # move old 'raw_data.pcap' and capture new one
    wait_time = 2
    if capture_time != None:
        if os.path.exists(raw_pcap_file):
            back_file = raw_pcap_file[0:-5]+'_old'+raw_pcap_file[-5:]
            if os.path.exists(back_file):
                try:
                    os.remove(back_file)                    
                except:
                    print "** '%s' may occupied by other progress,"% (back_file)
                    print "   please close the file."                   
            try:        
                shutil.move(raw_pcap_file, back_file)
            except:
                print "** '%s' or '%s' may occupied by other progress,"% (raw_pcap_file,back_file)
                print "   please close the file."  
            
        print " * packet capturing, please wait..."
        
        pcap_capture(network_port, capture_time, raw_pcap_file)
            
        print " * wait for raw_pcap_file file get"    
        capture_time_out = int(capture_time) + wait_time
        time.sleep(capture_time_out)

    time_count = 0

    while (os.path.exists(raw_pcap_file)==False):
        time.sleep(1)
        time_count += 1
        if time_count > wait_time:
            print "** time out for packet capture! the process will terminate."
            exit(1)

    # filter the raw pcap file
    print "\n * pcap file filting ..."
    print "   please wait for all filted pcap file get"    
    messageIds = pcap_filter(raw_pcap_file, filter_conditions)
    
    global pcap_filte_wait_time
    time.sleep(pcap_filte_wait_time)
    
    print ' * filtered pcap file location:\n   %s \n'% (API_Data_dir)
    
    SheetNameList = []
    ItemsList     = []
    DataList      = []
    
    print " * Pcap file decode..."
    
    sleep_time = 0.2
    time_out = 2
    for i in range(0, len(messageIds)):
        pcap_fileName = (messageIds[i]+'.pcap')
        pcap_fileName = os.path.join(API_Data_dir, pcap_fileName)
        
        time_conut = 0
        while os.path.exists(pcap_fileName) == False and time_conut < time_out:
            time.sleep(sleep_time)
            time_conut += sleep_time
                        
        Data_values = []    
        if os.path.exists(pcap_fileName):
            
            (Items, Data_values) = Pcap_decode(pcap_fileName)
            
            if Data_values:
                SheetNameList.append(messageIds[i])
                ItemsList.append(Items)
                DataList.append(Data_values)
                print " - Message Id: %s Decode Success!\n"% (messageIds[i])
        
        '''    
        #except:
            if printLevel_1:
                print " - Message Id: %s Decode Failure!\n"% (messageIds[i])
        '''
    # ----------------- save report values -----------------------
    if SheetNameList:
        print "\n------ save parsed data to xls ----------\n"

        try:            
            DataSave(result_file, SheetNameList, ItemsList, DataList)

        except:
            print " ** '%s' may occupied by other progress."% (result_file)
            exit(1)

        print '\n***************************************** '
    else:
        print "** No valid extracted data!"
        
    
    if os.path.isfile(result_file):
        print " * packet decoder success!"
        exit(0) 
    else:
        print " * packet decoder failure!"
        exit(1)    


# get the created time of a file or dir
# return: 
#   -  time str as: year-month-day_hour-min-sec
def get_create_time(fileName):
    stat_info = os.stat(fileName)
    creatTimeTuple = time.localtime(stat_info.st_ctime)
    
    time_format_str = '%Y_%m_%d_%H_%M_%S'
    time_str = time.strftime(time_format_str, creatTimeTuple)
    
    return time_str
    

# get current time str
# return: 
#   -  time str as: year-month-day_hour-min-sec
def get_CurrentTime_str():
    
    time_format_str = '%Y_%m_%d_%H_%M_%S'
    timeArray = time.localtime(time.time())
    time_str = time.strftime(time_format_str, timeArray)
    
    return time_str
    
    
    
# ##################################################################
# move files
# ##################################################################
def moveFile(FilePath):    

    if os.path.isdir(FilePath):
        #time_str = get_create_time(FilePath)
        
        FilePath_old = FilePath + '_LastSave'
        if os.path.isdir(FilePath_old):
            try:
                shutil.rmtree(FilePath_old, True)
            except:
                print "Some files in '%s' may occupied by other progress,"% (FilePath_old)
                print "please close all of files in %s."% (FilePath_old)
        try:        
            shutil.move(FilePath, FilePath_old)
        except:
            print "Some files in '%s' or '%s' may occupied by other progress,"% (FilePath, FilePath_old)
            print "please close all of files in '%s' and '%s'."% (FilePath, FilePath_old)
    try:        
        os.makedirs(FilePath)
    except:
        print "Some files in '%s' may occupied by other progress,"% (FilePath)
    

# ##################################################################
# function: pcap_capture
#*      use tshark to capture pcap file
#       
# ##################################################################
def pcap_capture(network_port, capture_time, raw_pcap_file):
    
    print "\n * capture conditions:"
    print "  - network_port: %s"% network_port
    print "  - capture_time: %s seconds"% capture_time

    capture_cmd = ['tshark','-i',network_port,'-a','duration:'+capture_time, '-F','pcap','-w', raw_pcap_file]
    subprocess.Popen(capture_cmd)

    #capture_cmd_str = 'tshark'+'-i'+network_port+'-a'+'duration:'+capture_time+ '-F'+'pcap'+'-w'+raw_pcap_file
    #os.system(capture_cmd_str)

# ##################################################################
# function: pcap_filter
#*      filter pcap file with the filter condition
#       
# ##################################################################
def pcap_filter(pcap_org_file, filter_conditions):
    
    totalNum = 0    
        
    ip_dst = filter_conditions[0]
    ip_src = filter_conditions[1]
    messageIds = filter_conditions[2]
    filter_strs = get_filter_str(ip_dst, ip_src, messageIds) 
    
    for i in range(0,len(filter_strs)):
        pcap_filter_i = filter_strs[i] 
        savefile = messageIds[i] + ".pcap"
        savefile = os.path.join(API_Data_dir, savefile)
        #print " - filter %s ..."% (messageIds[i])
        filter_cmd_i = ['tshark', '-r', pcap_org_file, '-Y', pcap_filter_i, '-F', 'pcap', '-w', savefile]        
        subprocess.Popen(filter_cmd_i)
        '''
        filter_cmd_i = 'tshark '+ ' -r '+ pcap_org_file+' -Y '+pcap_filter_i+' -F '+' pcap '+' -w '+savefile
        os.system(filter_cmd_i) 
        print filter_cmd_i
        exit(1)
        '''       
        totalNum += 1

    #print " %d file(s) filtered success..." % totalNum
    return messageIds
    
# ###############################################
# read wireshark paramaters from .xls file
def read_wireshark_paras(file_name):
    #-------- global def ---------
    filter_from_row = 2
    #------- global def end ------
    
    data = xlrd.open_workbook(file_name)
    table = data.sheets()[0]
    nrows = table.nrows
    #ncols = table.ncols
    
    ip_dst = str(table.row(filter_from_row)[0].value)
    ip_src = []
    for i in range(filter_from_row, filter_from_row+3):
        if str(table.row(i)[1].value).find('192')>=0:
            ip_src.append(str(table.row(i)[1].value))
 
    print "\n * filter conditions:"
    print "  - ip.dst = %s"% (ip_dst)
    print "  - ip.src = %s"% (ip_src)
    messageIds = []
    messageId_num = 0
    messageId_pattern = re.compile('[0-9a-fA-F]')
    for i in range(filter_from_row, nrows):
        messageId = str(table.row(i)[2].value)
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
        
    filter_conditions = [ip_dst, ip_src, messageIds]
    return (filter_conditions)

# ###############################################
# make filter str  
def get_filter_str(ip_dst, ip_src, messageIds):
    filter_strs = []
    ip_dst_str = "(ip.dst == " + ip_dst + ")"
    ip_src_str = ''
    for i in range(0, len(ip_src)): 
        ip_src_str += "(ip.src == "
        ip_src_str += ip_src[i] + ")||"
        
    ip_src_str = "(" + ip_src_str[0:-2]+")"
    
    for i in range(0,len(messageIds)):        
        messageId_str = "(data.data[0:4] contains " + messageIds[i] + ")"
        filter_str = ip_dst_str + "&&" + ip_src_str + "&&" + messageId_str
        filter_strs.append(filter_str)

    return filter_strs

# ##################################################################
# function: Pcap_decode
#*      main function for pcap decode
#   -return:
#       Items, message items
#       Data_values, message data values
#             
# ##################################################################
def Pcap_decode(pcap_fileName):
    
    global printLevel_1
    # path = os.getcwd() #get current root
    outFileName = pcap_fileName[0:-5]+'_decode.txt'       
    # pcap file header parse
    #print " Pcap file parse start......\n"
    Items = []
    Data_values = []    
    
    pcap = Pcap(pcap_fileName)
    pcap.pcap_decode()
    
    if pcap.packet_num == 0:
        
        removed_flag = 0
        while removed_flag == 0:
            try:
                os.remove(pcap_fileName)
                removed_flag = 1
            except:
                pass
                #print "** '%s' may occupied by other progress this time."% (pcap_fileName)

        if printLevel_1:
            pcap_fileName = os.path.split()[-1]
            print " * %s is empty! No packet in it!"% pcap_fileName
            print "  Please check the raw_data.pcap file and filter conditions! "
            print " * The Pcap_decode procedure stop!" 
            
        return (Items, Data_values)
    
    
    Decode_txt = open(outFileName,'w')     
    # print file header info
    Decode_txt.write(pcap.pcap_headerstr)        

    # write pacp packet data to out file    
    
    for i in range(0, pcap.packet_num):
        Decode_txt.write(pcap.packet_headerstrs[i])
        # Ethernet decode
        eth = Ethernet(pcap.packet_data[i])
        try:
            eth.frame_decode()
        except:
            continue
        
        Decode_txt.write(eth.printstr)
        data_start = Ethernet_header_len
        if eth.type == '802.1Q':
            vl = Vlan(pcap.packet_data[i],data_start)
            vl.frame_decode()
            Decode_txt.write(vl.printstr)
            data_start += Vlan_header_len            
            if vl.type == 'IP':            
                ip = Internet(pcap.packet_data[i],data_start)
                ip.frame_decode()
                Decode_txt.write(ip.printstr)
                data_start += Ip_header_len
        # Ip decode
        elif eth.type == 'IP':
            ip = Internet(pcap.packet_data[i],data_start)
            ip.frame_decode()
            Decode_txt.write(ip.printstr)
            data_start += Ip_header_len
        else:
            Decode_txt.write('  ******* This is not Vlan or Internet Protocol......\n')
            continue
            #return

        # UDP decode
        if ip.protocol == 'UDP':
            udp = Udp(pcap.packet_data[i],data_start)
            udp.frame_decode()
            Decode_txt.write(udp.printstr)

            #------ udp data part ...... message decode -------
            msg = Message(udp.data)
            msg.frame_decode()
            Decode_txt.write(msg.printstr)
            Data_values.append(msg.dec_value) 
            if len(msg.items)> len(Items):
                Items = msg.items
        else:
            Decode_txt.write('  ******* This is not User Datagram Protocol......\n')
            continue
            #return
        Decode_txt.write('----------------------------------------------------\n')        
    Decode_txt.close()
    
    '''
    for k in range(0,len(msg.msg_struct)):
        Items.append(msg.msg_struct[k][0])
    '''    
    return (Items, Data_values)
         


# ##################################################################
# class: DataSave
# 
# [Function]: save data to xls file
#
# [Methods]:
# * set_styles : creat and set some styles for sheet table to choose
#      set colour, pattern, ......
#      set border for num and Item line, as well as each col
# * get_col_width: compute col width
#      adaptive col with:
#          - adjust col width accronding to item and value width
# * sort_by_itemKey: sort list values by one given item key 
# * SaveData_to_xls:  write data to .xls file
#    - fix header line
#    - return:
#       no return value, but the saved .xls file
# 
# ##################################################################
class DataSave():
    
    def __init__(self, FileName, SheetNameList, ItemsList, DataList):
        
        # judge data num
        self.data_num = len(ItemsList)
        
        if isinstance(ItemsList[0], list) == False:
            self.data_num = 1
           
        # ------- glob def -------------
        self.LineLetter_num = 10
        
        self.LetterWidth = 350
        self.maxWidth    = 4000
        self.minWidth    = 2000   
        self.compensationWidth = 50 
        
        #----------------------------
        self.FileName      = FileName
        self.SheetNameList = SheetNameList
        self.ItemsList     = ItemsList
        self.DataList      = DataList       
                
        #   Initialize a workbook object, add a sheet,
        #   and the sheet can be overwritten
        self.wbk = xlwt.Workbook()
    
        self.eader_style = None
        self.item_style  = None
        self.data_style  = None
        
        self.set_styles()
        self.SaveData_to_xls()
               

    def set_styles(self):
        
        # colour style def
        colour_style0 = 'light_orange' 
        colour_style1 = 'light_blue' 
        colour_style2 = 'lime'
        colour_style3 = 'yellow'        
        
        #   ----- Seting style for excel table --------
        # set alignment        
        alignment0 = xlwt.Alignment()
        alignment0.horz = xlwt.Alignment.HORZ_CENTER  
    
        alignment1 = xlwt.Alignment()
        alignment1.horz = xlwt.Alignment.HORZ_CENTER
        alignment1.vert = xlwt.Alignment.VERT_TOP    
        alignment1.wrap = True
        
        # set borders   
        borders0 = xlwt.Borders() 
        borders0.left = 1
        #borders0.left = xlwt.Borders.DASHED 
        borders0.right = 1 
        #borders0.top = 1 
        #borders0.bottom = 1 
        borders0.left_colour =0x3A  
        borders0.right_colour=0x3A   
        
        #   Create a font to use with the style
        font0 = xlwt.Font()  
        font0.name = 'Times New Roman'
        font0.height = 0x00F0 # height.
        font0.colour_index = xlwt.Style.colour_map['blue']
        font0.bold = True
        #font0.escapement = xlwt.Font.ESCAPEMENT_SUPERSCRIPT
        font0.family = xlwt.Font.FAMILY_ROMAN
        #   Setting the background color of a cell
        
        #   Create a font to use with the style
        font1 = xlwt.Font()  
        font1.name = 'Times New Roman'
        font1.height = 0x00F0 
        font1.colour_index = xlwt.Style.colour_map['black']
        #    font1.bold = True        
        
        # set pattern
        pattern0 = xlwt.Pattern()    # Creat the pattern
        pattern0.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern0.pattern_fore_colour = xlwt.Style.colour_map[colour_style2]
        
        # set pattern
        pattern1 = xlwt.Pattern()    # Creat the pattern
        pattern1.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern1.pattern_fore_colour = xlwt.Style.colour_map[colour_style3]
           
        #   header style
        header_style = xlwt.XFStyle()
        header_style.font = font0
        header_style.alignment = alignment1
        header_style.borders = borders0 
        header_style.pattern = pattern1
        
        #   Item style
        item_style = xlwt.XFStyle()    
        item_style.font = font0
        item_style.alignment = alignment1
        item_style.borders = borders0
        item_style.pattern = pattern0   
    
        #   Data style
        data_style = xlwt.XFStyle()
        data_style.font = font1
        data_style.alignment = alignment0
        data_style.borders = borders0
        
        self.header_style = header_style
        self.item_style = item_style
        self.data_style = data_style        
        
    # get col width accronding to item_str_len and data_str_len
    def get_col_width(self, item_str_len, data_str_len):
            
        item_width = self.LetterWidth * item_str_len
        value_width = self.LetterWidth * data_str_len

        if value_width > item_width:
            col_width = value_width
            
        else:
            if item_str_len <= self.LineLetter_num:
                col_width = item_width

            elif item_width/2 > value_width:
                col_width = item_width/2
                
            else: 
                col_width = value_width
        
        col_width += self.compensationWidth
        
        #col_width = item_width
        '''    
        if col_width > maxWidth:
            col_width = maxWidth
        '''
        if col_width < self.minWidth:
            col_width = self.minWidth
            
        return col_width
            
    #from operator import itemgetter, attrgetter
    def sort_by_itemKey(self, itemKey):
       
        for i in range(0, self.data_num):
            match_indx = -1
            for j in range(0, len(self.ItemsList[i])):
                if self.ItemsList[i][j].find(itemKey)>=0:
                    match_indx = j
                    break
            if match_indx >=0 :      
                self.DataList[i] = sorted(self.DataList[i], key=lambda x:x[match_indx])
                #self.DataList[i] = sorted(self.DataList[i], key=itemgetter(match_indx))

        
    def SaveData_to_xls(self):
       
        sheet_num = 0
        for k in range(0, self.data_num):
            
             # get items and data
            
            items = self.ItemsList[k]
            data = self.DataList[k]
            
            sheetName = self.SheetNameList[k]
            
            # creat a sheet
            sheet_k = self.wbk.add_sheet(sheetName, cell_overwrite_ok = False)
            
            # frozen headings  
            # position: first 2 rows
            #           first 1 col
            sheet_k.panes_frozen   =  True
            sheet_k.horz_split_pos = 2
            sheet_k.vert_split_pos = 1
            
            # ------- write items of the sheet   --------
            valid_col_indx = 0
            for i in range(0, len(items)):
                                              
                if items[i] != None:
                    
                    try:
                        col_width = self.get_col_width(len(items[i].strip()), len(str(data[0][i]).strip()))
                    except:
                        col_width = self.get_col_width(len(items[i].strip()), len(items[i].strip()))
                    
                    sheet_k.col(valid_col_indx).width =  col_width
                    
                    '''
                    print "items[i]: %s, len(items[i]): %d, col_width: %d"% \
                          (items[i].strip(), len(items[i].strip()), col_width)
                    '''
                    try:
                        sheet_k.write(0, valid_col_indx, valid_col_indx+1, self.header_style)
                        sheet_k.write(1, valid_col_indx, items[i], self.item_style)
                    except:
                        print " ** items[%d]: %s"% (i, items[i])
                        sheet_k.write(1, valid_col_indx, items[i][1], self.item_style)
                        
                    valid_col_indx += 1  
                
            # ------- write data for each item   --------
            
            for i in range(1, len(data)+1):
                valid_col_indx = 0
                for j in range(0 ,len(items)):
                    if items[j] != None:
                        try:
                            sheet_k.write(i+1, valid_col_indx, data[i-1][j], self.data_style)
                        except:
                            sheet_k.write(i+1, valid_col_indx, '-', self.data_style)
                            
                        valid_col_indx += 1
            print " * sheet: '%s' write success!"% self.SheetNameList[k]
            sheet_num += 1                 
        try:
            self.wbk.save(self.FileName)  # save data to .xls file 
            
        except:
            print " ** The .xls file: %s may opending now! "% self.FileName
        


#********************************  main  **********************************
if __name__ == '__main__':
    
    BasePath = ''
    capture_time = None
   
    if len(sys.argv)>=1:
        BasePath = os.path.dirname(sys.argv[0])
        
    usage_flag = 0
    if (len(sys.argv)==2 and sys.argv[1].find('help')>=0) or len(sys.argv)==1 or len(sys.argv)>3:
        usage_flag = 1

    elif len(sys.argv)<=3:
        
        if len(sys.argv) >= 2:
            network_port = sys.argv[1]
            
        if len(sys.argv) == 3:
            capture_time = sys.argv[2]
            
        start = time.clock() 
        
        GetExtractedData(network_port, capture_time)
        
        print ' - Duration: %.2f  seconds'% (time.clock() - start) 
                          
        
    if usage_flag == 1:
        print'''

   *************************** Usage: ***************************
        -input:	
             -[1] network_port:
             -[2] capture_time: (unit: second)
                  [defult:] not capture
       @example:
               python PacketDecoder.py 2       
               python PacketDecoder.py 2 100
       - output:
         in dir " parsed_data ":
           -  " msgID.pcap "
           -  " msgID_decode.txt "           
           -  " result.xls "
   
   **************************************************************
        '''
        exit(0)   
