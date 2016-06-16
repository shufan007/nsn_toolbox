# ################################################################################
# Author:   Fan Shaungxi(Fan, Shuangxi (NSN - CN/Hangzhou))
#*  description: split symbol data in according to slot format
#   InputFile :  get hex data from this file
#   DstFile:  save data after process data to this file 
# ################################################################################

import sys
                   
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
    print_str = ''     
    Ndata1 = SlotFormat[0]
    Ntpc   = SlotFormat[1]
    Ntfci  = SlotFormat[2]
    Ndata2 = SlotFormat[3]
    Npilot = SlotFormat[4]
    NbitsPerSlot = Ndata1 + Ntpc + Ntfci + Ndata2 + Npilot        
    compensate_num = 8; # number of compensate,
                        # @ example: total data 608 -> data 600, compensate_num = 8   
    data_num = len(data)
    print " - hex_ata number: %d\n" % data_num       
    NBits = data_num/2*32; # length of binary
    print " - bit number: %d" % NBits
    
    if data[0].find('0x')>=0:
        hex_startIdx = 2
    else:
        hex_startIdx = 0
        
    data_bin = ''
    dtx_bin =  ''
    # arrange the data and the dtx part
    for i in range(0,data_num):
        if i%2==0:
            data_i = data[i][hex_startIdx:]
            dtx_i = data[i+1][hex_startIdx:]
            data_bin += hex_to_bin(data_i)
            dtx_bin += hex_to_bin(dtx_i)
    
    # write the data in format:  data1 + tpc + tfci + data2 + pilot
    NSlots = int((NBits/NbitsPerSlot)/15*15)
    print " - slot number: %d" % NSlots
    
    print_str += ('          data1(%d) | tpc(%d) | tfci(%d) | data2(%d) | pilot(%d)'%\
                  (Ndata1,Ntpc,Ntfci,Ndata2, Npilot))
    
    for i in range(0,NSlots):
        if (i%15) == 0:
            frame = int(i/15)
            print_str += '\n* frame: %d *\n'% frame
        for j in range(0,2):
            if j == 0:
                print_str += '[slot %2d] data: '% (i%15)
                ThisLine = data_bin[frame*compensate_num + i*NbitsPerSlot : frame*compensate_num + (i+1)*NbitsPerSlot]
            elif j==1:
                print_str += '          dtx : '
                ThisLine = dtx_bin[frame*compensate_num + i*NbitsPerSlot : compensate_num + (i+1)*NbitsPerSlot]

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
    tem = bin(int(hex_str,16))
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
    print " - endian transform ...\n"
    print "   - data number: %d\n" % data_num
    post_data = []
    header = ''
    start = 0
    if data[0].find('0x')>=0:
        header = '0x'
        start = 2            
    for i in range(0,data_num):
        data_i = data[i][start:]
        tran_data_i = data_i[6:8] + data_i[4:6] + data_i[2:4] + data_i[0:2]
        post_data.append(header+tran_data_i)
        
    return post_data

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
        
#*****************########---  main  ---#######****************
if __name__ == '__main__':

    if len(sys.argv)>=2 and len(sys.argv)<=4:
        inFileName = sys.argv[1]
        hex_data = get_file_data(sys.argv[1])    
        SlotFormat = [6,2,0,28,4]  # defult
        SymbolSplitFile = open(inFileName[0:-4]+'_slot_split.txt','w+')    
        if len(sys.argv)==4:
            SlotFormat_char = sys.argv[3][1:-1].split(',')
            SlotFormat = []
            for i in range(0,len(SlotFormat_char)):
                SlotFormat.append(int(SlotFormat_char[i]))
        else:
            print " Defult Slot Format: %s" % (SlotFormat)            
            
        if len(sys.argv)>=3 and sys.argv[2]=='1':        
            EndianTransforFile = open(inFileName[0:-4]+'_endian_transfored.txt','w+')
            out_data = endian_transform(hex_data)
            for i in range(0, len(out_data)):
                EndianTransforFile.write("%s\n"% out_data[i])
            EndianTransforFile.close()                                    
            printstr = SymbolData_split(out_data, SlotFormat)
            SymbolSplitFile.write(printstr)
            SymbolSplitFile.close()
            exit(0)                     
        else:
            print " no endian transform..."
            printstr = SymbolData_split(hex_data, SlotFormat)
            SymbolSplitFile.write(printstr)
            SymbolSplitFile.close()
            exit(0)
    else:
        print'''

   *************************** Usage: ***************************
        -input:            
             -[1] input hex file name:
               the hex data file name in current path
               the data format in the input data file can be:
                 000F003C FF0FFF3C 0F007800 0FFE7C00
                 00780080 FE7C00FF 7C00000F 7C00FF0F
                 00000F00 00FF0FFE
                 ... ...                
             -[2] endian_transform_flag:
                 0, not transfor (defult)
                 1, transfor
             -[3] SlotFormat:
                 can input your own slot format,
                 defult is [6,2,0,28,4]
       @example:
                python SymbolSplit.py symbol_data.txt
                python SymbolSplit.py symbol_data.txt 0
                python SymbolSplit.py symbol_data.txt 1
                python SymbolSplit.py symbol_data.txt 0 [6,2,0,28,4]
                python SymbolSplit.py symbol_data.txt 1 [6,2,0,28,4]       
       - output:
           - file named "***_endian_transfored.txt"
             for the endian transformed data, if set endian transform
           - file named "***_slot_split.txt.txt"
             for the slot split data
   
   **************************************************************
        '''
        exit(0)            

