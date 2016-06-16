# ################################################################################
# Author:   Fan Shaungxi(Fan, Shuangxi (NSN - CN/Hangzhou))
#*  description: split symbol data in according to slot format
#   InputFile :  get data from this file
#   DstFile:  save data after process data to this file 
# ################################################################################

import sys, os, xlwt, string, shutil, time

# ################################################################################
#*  description: get data from TTI trace
#   - Input :  
#         - InputFileName: TTI trace file 
#         - endian_flag:   indicate if need endian transfor
#         - Pars: (userId, SlotFormat, Time_indx, userId_indx,
#                  sfn_indx, Length_indx, data_indx)
# ################################################################################
def TTI_catch(InputFileName, endian_flag, Pars):    
    userId =      Pars[0]     
    SlotFormat =  Pars[1]
    
    Time_indx =   Pars[2]
    userId_indx = Pars[3]
    sfn_indx =    Pars[4]
    Length_indx = Pars[5]
    data_indx =   Pars[6]    
    
    SrcFile = open(InputFileName,'r')   
    data_raw = SrcFile.read().splitlines()
    LineNum = len(data_raw)
    
    Time =   []
    Sfn =    []
    Length = []
    Data =   []
    data_num = 0
    
    print " - User Id [%s]  Get data...\n"% (userId)
    for i in range(1,LineNum):
        thisline = data_raw[i].split(',')
        if len(thisline)>data_indx[-1]:            
            if userId == thisline[userId_indx]:
                line_data = []
                Time.append(thisline[Time_indx])
                Sfn.append(thisline[sfn_indx])
                Length.append(thisline[Length_indx])                                
                for element in data_indx:
                    line_data.append(int_to_hex(int(thisline[element],10)))
                data_num += 1
                Data.append(line_data)
    print " - Data extract complete...\n"  
    print "   number of data items: %d\n" % data_num  
    
    Symbol_data = [] 
    print " - Get symbol data... " 
    for i in range(0,data_num):            
        this_data = Data[i]
        if endian_flag == '1':
            this_data = endian_transform(Data[i])
        Symbol_data.append(this_data)

    Split_data =  []        
    print " - Split symbol data to solt... " 
    for i in range(0,data_num):            
        slot_data = SymbolData_split(Symbol_data[i], SlotFormat)
        Split_data.append(slot_data)   
            
    return  (Time, Sfn, Length, Symbol_data, Split_data)

# ################################################################################
#*  description: get userIds from TTI trace
#   - Input :  
#         - InputFileName: TTI trace file 
#         - userId_indx:   indicate the index of userId
# ################################################################################
def Get_userId(InputFileName, userId_indx):    
    UserIds =  []     
    SrcFile = open(InputFileName,'r')   
    data_raw = SrcFile.read().splitlines()
    LineNum = len(data_raw)
    print " - File line number: %d\n" % LineNum  
    print " - Get userIds... " 
    for i in range(1,LineNum):
        thisline = data_raw[i].split(',')
        if len(thisline)>userId_indx:
            if thisline[userId_indx] not in UserIds:
                UserIds.append(thisline[userId_indx])           
    return  UserIds
# ################################################################################
#*  description: split symbol data in the form of slot format
#   - Input :  get data from this file
#       - data:  hex data 
#       - SlotFormat: [Ndata1,Ntpc,Ntfci,Ndata2,Npilot]
#       @example: DPCH  slot format #8:
#           Ndata1 = 6, Ntpc = 2, Ntfci= 0, Ndata2 = 28, Npilot = 4
#           SlotFormat = [6,2,0,28,4]
#   - outpot: the string after split the symbol data,
#             can save the data to a file directly.
# ################################################################################                        
def SymbolData_split(data, SlotFormat):  
    header_str = ''
    print_str = ''
    
    Ndata1 = SlotFormat[0]
    Ntpc   = SlotFormat[1]
    Ntfci  = SlotFormat[2]
    Ndata2 = SlotFormat[3]
    Npilot = SlotFormat[4]
    NbitsPerSlot = Ndata1 + Ntpc + Ntfci + Ndata2 + Npilot        
    comp_num = 8; # number of compensate,
                        # @ example: total data 608 -> data 600, compensate_num = 8   
    data_num = len(data)
    #print " - hex_ata number: %d\n" % data_num       
    NBits = data_num/2*32; # length of binary
    #print " - bit number: %d" % NBits
    
    NBits = data_num/2*32; # length of binary    
    
    if data[0].find('0x')>=0:
        hex_startIdx = 2
    else:
        hex_startIdx = 0
        
    data_bin = ''
    dtx_bin =  ''
    #print hex_startIdx
    # arrange the data and the dtx part
    for i in range(0,data_num):
        if i%2==0:
            data_i = data[i][hex_startIdx:]
            #print data_i
            dtx_i = data[i+1][hex_startIdx:]
            data_bin += hex_to_bin(data_i)
            dtx_bin += hex_to_bin(dtx_i)
    
    # write the data in format:  data1 + tpc + tfci + data2 + pilot
    #NSlots = int((NBits/NbitsPerSlot)/15*15)
    NSlots = int(NBits/NbitsPerSlot)
    #print " - slot number: %d" % NSlots
    if Ntfci>0:
        header_str += ('            data1(%d) | tpc(%d) | tfci(%d) | data2(%d) | pilot(%d)\n'%\
                      (Ndata1,Ntpc,Ntfci,Ndata2, Npilot))
    else:
        header_str += ('            data1(%d) | tpc(%d) |      data2(%d)      | pilot(%d)\n'%\
                      (Ndata1,Ntpc,Ndata2, Npilot))  
        
    print_str += header_str        
    for i in range(0,NSlots):
        if (i%15) == 0:
            if NSlots>15:
                frame = int(i/15)
                print_str += '* frame: %d *\n'% frame
            else:
                frame = 0
        for j in range(0,2):
            if j == 0:
                print_str += '[slot %2d] data: '% (i%15)
                ThisLine = data_bin[frame*comp_num + i*NbitsPerSlot : frame*comp_num + (i+1)*NbitsPerSlot]
            elif j == 1:
                print_str += '          dtx : '
                ThisLine = dtx_bin[frame*comp_num + i*NbitsPerSlot : frame*comp_num + (i+1)*NbitsPerSlot]

            if Ndata1 != 0:
                print_str += '%s  ' % ThisLine[0 : Ndata1]         
            if Ntpc != 0:
                print_str += '%s  ' % ThisLine[Ndata1 : Ndata1+Ntpc]         
            if Ntfci != 0:
                print_str += '%s  '% \
                             ThisLine[Ndata1 + Ntpc : Ndata1 + Ntpc + Ntfci]         
            if Ndata2 != 0:
                print_str += '%s  '% \
                             ThisLine[Ndata1 + Ntpc + Ntfci : Ndata1 + Ntpc + Ntfci+ Ndata2]        
            if Npilot != 0:
                print_str += '%s  '% \
                             ThisLine[Ndata1+Ntpc+ Ntfci+ Ndata2 : Ndata1+ Ntpc+ Ntfci+ Ndata2 + Npilot]
                
            print_str +='\n'
            
    return print_str

# ################################################################################
#*  description: transfor hex data to binary string
#   - Input :  hex data str
#   - output:  binary string
# ################################################################################ 
def hex_to_bin(hex_str):
    bin_data = ''
    if len(hex_str)>8:
        hex_str = hex_str[0:8]
    tem = bin(int(hex_str,16))
    if len(tem)<34:
        tem = tem.replace('0b','0b'+'0'*(34-len(tem)))        
    tem = tem.replace('0b','')
    bin_data += tem
    
    return bin_data

# ################################################################################
#*  description: transfor int to binary string
#   - Input :  dec number
#   - output:  binary string
# ################################################################################ 
def dec_to_bin(int_data):
    bin_data = ''
    tem = bin(int_data)
    if len(tem)<34:
        tem = tem.replace('0b','0b'+'0'*(34-len(tem)))        
    tem = tem.replace('0b','')
    bin_data += tem
    
    return bin_data
# ################################################################################
#*  description: endian transform for hex data
#   - Input :  hex data list
#   - output:  hex data after endian transform
# ################################################################################ 
def endian_transform(data):    
    data_num = len(data)
    #print " - endian transform ...\n"
    #print "   - data number: %d\n" % data_num
    post_data = []
    header = ''
    start = 0
    if data[0].find('0x')>=0:
        header = '0x'
        start = 2            
    for i in range(0,data_num):
        data_i = data[i][start:]
        tran_data_i = ''
        byte_len = len(data_i)/2
        for j in range(0,byte_len):
            tran_data_i += data_i[(byte_len-1-j)*2:(byte_len-j)*2]
        post_data.append(header+tran_data_i)
        
    return post_data

# #####################################################
def int_to_hex(int_data):
    hex_data = ''
    tem = hex(int_data)
    if len(tem)<10:
        tem = tem.replace('0x','0x'+'0'*(10-len(tem)))                
    tem = tem.replace('0x','')
    if len(tem)>8:
        tem = tem[0:8]
    hex_data = tem            
    return hex_data

# ################################################################################
#*  description: read hex data from InputFile
#   - Input :  hex data file name
#   - output:  hex data list
# ################################################################################
def get_file_data(InputFileName):
    SrcFile = open(InputFileName,'r')   
    data_raw = SrcFile.read().splitlines()
    LineNum = len(data_raw)
    print " - data line number: %d\n" % LineNum
    data = []
    data_num = 0    
    for i in range(0,LineNum):
        thisline = data_raw[i].split()
        for j in range(0,len(thisline)):
            data.append(thisline[j])
            data_num += 1
    print " - data number: %d\n" % data_num    
    return data
# ################################################################################
#*  description: split time from dec time data
#   - Input :
#          - time_dec:     dec time data
#          - time_bit_len: bit length of hour, minute, second, millisec
#          - Order_flag:   indicate the order to get time part
#                0 (default), positive order
#                1,           reverse order         
#   - output:  time str like 00:00:00.000
# ################################################################################
def time_parse(time_dec,time_bit_len, Order_flag = 0):
    time_bin = dec_to_bin(time_dec)
    time_str = ''
    
    if Order_flag == 0:
        hour =   str(int(time_bin[0:time_bit_len[0]],2))
        minute = str(int(time_bin[time_bit_len[0]:time_bit_len[0]+time_bit_len[1]],2))
        second = str(int(time_bin[time_bit_len[0]+time_bit_len[1]:time_bit_len[0]+time_bit_len[1]+time_bit_len[2]],2))
        millisec = str(int(time_bin[time_bit_len[0]+time_bit_len[1]+time_bit_len[2]:],2))
    else:
        millisec =  str(int(time_bin[0:time_bit_len[3]],2))
        second = str(int(time_bin[time_bit_len[3]:time_bit_len[3]+time_bit_len[2]],2))
        minute = str(int(time_bin[time_bit_len[3]+time_bit_len[2]:time_bit_len[3]+time_bit_len[2]+time_bit_len[1]],2))
        hour =   str(int(time_bin[time_bit_len[3]+time_bit_len[2]+time_bit_len[1]:],2))
        
    hour = '0'*(2-len(hour))+hour
    minute = '0'*(2-len(minute))+minute
    second = '0'*(2-len(second))+second
    millisec = '0'*(3-len(millisec))+millisec
    
    time_str += "%s:%s:%s.%s "% (hour,minute,second,millisec)
    return time_str

# ##################################################################
# function: SaveData_to_xls
#*      this function for save extract data to .xls file
#   -return:
#       no return value, but the saved .xls file
#             
# ##################################################################
def SaveData_to_xls(saveFileName, items, data):
    
    #   Initialize a workbook object, add a sheet,
    #   and the sheet can be overwritten
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('sheet 1',cell_overwrite_ok = True)

    #   ----- Seting style for excel table --------    
    #   Item style
    item_style = xlwt.XFStyle()
    #   Create a font to use with the style
    font0 = xlwt.Font()  
    font0.name = 'Times New Roman'
    font0.height = 0x00F8 # height.
    font0.colour_index = xlwt.Style.colour_map['blue']
    font0.bold = True
    item_style.font = font0 

    #   Setting the background color of a cell
    pattern = xlwt.Pattern()    # Creat the pattern
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = xlwt.Style.colour_map['light_yellow']
    item_style.pattern = pattern   

    #   Data style
    data_style = xlwt.XFStyle()
    #   Create a font to use with the style
    font1 = xlwt.Font()  
    font1.name = 'Times New Roman'
    font1.height = 0x00D8 
    font1.colour_index = xlwt.Style.colour_map['black']
    #    font1.bold = True
    data_style.font = font1         

    # ------- write items of the sheet   --------
    for i in range(0, len(items)):   
        sheet.write(0, i, items[i],item_style)
        
    # ------- write data for each item   --------
    for i in range(0, len(data)):
        for j in range(0 ,len(items)):            
            sheet.write(i+1,j,data[i][j],data_style)
    
    wbk.save(saveFileName)  # save data to file

# ################################################################################
#*  description: post process after get data from TTI trace
#   - Input :  
#         - symbol_file, split_file, excel_file --- file names
#         - Datas: (Time, Sfn, Length, Symbol_data, Split_data)
#         - cfn_flag: indicate if cfn need consider
#                0 (default), compute cfn
#                1,           not compute cfn             
#   - Output :
#         saved  data files
# ################################################################################
    
def TTI_trace_post(symbol_file, split_file, excel_file, Datas, cfn_flag = 0):
    Time        = Datas[0]
    Sfn         = Datas[1]
    Length      = Datas[2]
    Symbol_data = Datas[3]
    Split_data  = Datas[4]
    
    SymbolFile = open(symbol_file,'w+')     
    SplitFile = open(split_file,'w+') 
    
    print " - write hex symbol and slot split data to file..."
    Save_Data = []
    for i in range(0,len(Sfn)):
        time_str = "Timestamp:"
        time_data = time_parse(int(Time[i],10),time_bit_len, 1)
        time_str += time_data
        sfn_str = 'sfn:[%s] '% Sfn[i]
        cfn_str = ''
        if cfn_flag == 0:
            cfn = (int(Sfn[i],10)-frame_offset)%256
            cfn_str = 'cfn:[%d] '% cfn
        length_str = 'length:[%s] '% Length[i]
        header = (time_str + sfn_str + cfn_str + length_str)
        symbol_str = header
        symbol_str += "data: "
        
        for j in range(0,len(Symbol_data[i])):
            symbol_str += Symbol_data[i][j]
            symbol_str += ' '
            
        SymbolFile.write(symbol_str +'\n') 
        
        split_str = (header+'\n')
        split_str += Split_data[i]
        SplitFile.write(split_str)
        
        # data collect for save to excel
        save_data_i = []
        save_data_i.append(time_data)
        save_data_i.append(Sfn[i])
        if cfn_flag == 0:
            save_data_i.append(cfn)
        save_data_i.append(Length[i])
        save_data_i.extend(Symbol_data[i])
        
        Save_Data.append(save_data_i) 
        
    SymbolFile.close()
    SplitFile.close()
    # ------------------------ save data to excel -------------------------------
    print " - write symbol data to .xls file..."
    Items = []
    Items.append('Timestamp')
    Items.append('sfn')
    if cfn_flag == 0:
        Items.append('cfn')
    Items.append('length')
    data_len = len(Symbol_data[i])
    for i in range(0, data_len/2):
        Items.append('data_%d'%i)
        Items.append('dtx')
        
    SaveData_to_xls(excel_file, Items, Save_Data)    
    
#*****************########---  main  ---#######****************
if __name__ == '__main__':
    
    start = time.clock()   
    #---------------- defult parameters -------------------
    endian_flag = 0   # defult
    frame_offset = 0  # defult
    SlotFormat =  [6,2,0,28,4]  # defult 
    #---------------- init start -------------------
    Time_indx =   18
    time_bit_len = [5,6,6,15] # hour, minute, second, millisec
    userId_indx = 20
    sfn_indx =    23
    Length_indx = 32
    data_indx =   [24,25,26,27,28,29,30,31,33,36,37,38] 
    #---------------- init end -------------------     

    if len(sys.argv)>=2 and len(sys.argv)<=5:
        InputFileName = sys.argv[1]
        if len(sys.argv)>=3:   #  User Id was gaven
            userId = sys.argv[2]
            if len(sys.argv)>=4:
                frame_offset = int(sys.argv[3],10)
            if  len(sys.argv)>=5:
                endian_flag = sys.argv[4]
            if  len(sys.argv)==6:   
                SlotFormat = sys.argv[5]

            # ------------ save data ------------------
            print " - write hex symbol and slot split data to file..."
            symbol_file = str(userId) +'_symbol.txt'
            excel_file = str(userId) +'_symbol.xls' 
            split_file = str(userId) +'_slot_split.txt' 
            
            Pars = (userId, SlotFormat, Time_indx, userId_indx, sfn_indx, Length_indx, data_indx) 
            
            Datas = TTI_catch(InputFileName, endian_flag, Pars)
                                       
            TTI_trace_post(symbol_file, split_file, excel_file, Datas)
                                        
        else:  # User Id not gaven, should find all user Id
            
            # ------------ save data to files ------------------
            current_path = os.getcwd()
        
            Split_File_Dir = "Split_files"
            Symbol_File_Dir = "Symbol_files"
            Split_File_Dir = os.path.join(current_path, Split_File_Dir)
            Symbol_File_Dir = os.path.join(current_path, Symbol_File_Dir)
            if os.path.isdir(Split_File_Dir):
                shutil.rmtree(Split_File_Dir,True)        
            os.makedirs(Split_File_Dir)                                    
        
            if os.path.isdir(Symbol_File_Dir):
                shutil.rmtree(Symbol_File_Dir,True)        
            os.makedirs(Symbol_File_Dir)
            
            # get user Ids
            UserIds = Get_userId(InputFileName, userId_indx)
            
            print " - writing data..."
            for i in range(0,len(UserIds)):
                split_file = os.path.join(Split_File_Dir, str(UserIds[i]) +'_slot_split.txt')
                symbol_file = os.path.join(Symbol_File_Dir, str(UserIds[i]) +'_symbol.txt') 
                excel_file = os.path.join(Symbol_File_Dir, str(UserIds[i]) +'_symbol.xls')
                
                Pars = (UserIds[i], SlotFormat, Time_indx, userId_indx, sfn_indx, Length_indx, data_indx) 
                
                Datas = TTI_catch(InputFileName, endian_flag, Pars)
                                           
                TTI_trace_post(symbol_file, split_file, excel_file, Datas, 1)          

    else:
        print '''
   *************************** Usage: ***************************
        -input:            
             -[1] input file name:
             -[2] user Id
             -[3] frame offset
             -[4] endian_transform_flag:
                 0, not transfor (defult)
                 1, transfor
             -[5] SlotFormat:
                 can input your own slot format,
                 defult is [6,2,0,28,4]
                 
        If only parameter [1] gaven, the tool will find all user Ids,
        then process them one by one
       @example:
                python TTI_Parse.py ***.txt       
                python TTI_Parse.py ***.txt 163 2
                python TTI_Parse.py ***.txt 163 2 0
                python TTI_Parse.py ***.txt 163 2 1
                python TTI_Parse.py ***.txt 163 2 0 [6,2,0,28,4]
                python TTI_Parse.py ***.txt 163 2 1 [6,2,0,28,4]       
       - output:
           - file named "***_slot_split.txt" are slotsplit file
           - file named "***_symbol.txt" are hex symbol data file
   
   **************************************************************
        '''       
            
    print 'Duration: %.2f  seconds'% (time.clock() - start) 
    
    exit(0) 
