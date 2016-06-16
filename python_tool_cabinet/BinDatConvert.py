#======================================================================================
#       Function:       binary file and hex file convert
#       Author:         Fan, Shuangxi (NSN - CN/Hangzhou)
#       Date:           2014-09-25
#       @example:  python  BinDatConvert.py  hexfile|binfile 
#======================================================================================
#!/usr/bin/python
#coding=utf-8

import os, sys, time
import struct,re

# #####################################################
def Byte_to_hex(Byte_data):
    hex_data = ''
    for i in range(0,len(Byte_data)):
        temp = ''
        temp = ord(Byte_data[i])
        temp = hex(temp)
        if len(temp)==3:
            temp = temp.replace('0x','0x0')
        temp = temp.replace('0x','')
        hex_data += temp      
    return hex_data

# #####################################################
def u32_unpack(u32_byte):    
    temp = struct.unpack('I', u32_byte)[0]
    temp = hex(temp)
    if len(temp)<10:
        temp = temp.replace('0x','0x'+'0'*(10-len(temp))) 
    elif len(temp) == 11:
        temp = temp[0:-1]
    temp = temp.replace('0x','')    
    return temp

# #####################################################
# function: Invert the Byte order of the hex str.
# ##################################################### 
def AdjustEndian(hexStr):
    result =  ''
    str_len = len(hexStr)
    #print str_len
    for i in range(0, str_len/2):
        result += hexStr[str_len-(i+1)*2:str_len-i*2]
        #print result
    return result

# #####################################################
# function: Convert hex file to bin file.
# #####################################################
def Hex_to_Bin(hex_file, out_file, endian_flag):   
    print ('Convert hex file:%s to binary file' %(hex_file))  
    fin = open(hex_file,'r')
    #DataLines = fin.readlines()
    DataLines = fin.read().splitlines()
    print len(DataLines)
    fin.close()    
    fout = open(out_file,'wb')

    str_cut_index = 0
    if DataLines[0].upper().find('0X')>=0:
        str_cut_index = 2
    result =''
    for eachLine in DataLines:
        #m = re.findall('0x(\w{8})', eachLine)
        
        hexString = eachLine[str_cut_index:].strip()
        #print hexString
        if endian_flag == '1': 
            hexString = AdjustEndian(hexString)
            #print hexString
            #exit(1)
        for i in range(0,len(hexString)/2):
            b = int(hexString[i*2:i*2+2],16)
            result += struct.pack('B',b)               
    fout.write(result)        
    
    fout.close()
# #####################################################
# convert bin file to hex file.
# #####################################################
def Bin_to_Hex(bin_file, out_file, endian_flag, start_addr, length):
    # adjust inputs: start
    start_addr = (start_addr/4)*4    
    print ('Convert binary file: %s to hex file' %(bin_file))
    bin_file = open(bin_file, 'rb')   
        
    bin_file.seek(start_addr)
    byte_data = bin_file.read()
    bin_file.close()
    # adjust inputs: length
    if length == 'To_End':
        length = (len(byte_data)/4)*4
    else:
        length = (length/4)*4
        
    dat_Out = open(out_file, 'w+')       
    index = 0
    out_data = []
    while index < length:
        try:
            u32_byte = byte_data[index:(index+4)]
        except:
            print "Input length out of range!"
            break
        
        out_str = u32_unpack(u32_byte).upper()
        if endian_flag == '1':
            out_str = AdjustEndian(out_str)            
        dat_Out.write('0x%s\n'% out_str)
        #out_data.append(out_str)
        index = index + 4

    #dat_Out.writelines(out_data)
    dat_Out.close()
  

# *********************** main ***************************
if __name__ == '__main__': 
    time_start = time.clock()
    if len(sys.argv)>1 and len(sys.argv)<=5 and sys.argv[1]!='-help':
        Infile = sys.argv[1]
        # ------------- for hex_to_bin ------------- 
        if Infile[-4:] == '.dat' or Infile[-4:] == '.txt':
            hex_file = Infile
            endian_flag = '0'
            out_file = Infile[0:-4]+'.bin'          
            if len(sys.argv)==3:
                out_file = sys.argv[2]
                
            Hex_to_Bin(hex_file, endian_flag, out_file)
            
        else:
            # ------------- for bin_to_hex ------------- 
            bin_file = Infile            
            out_file = Infile[0:-4]+'.dat'
            endian_flag = '0'
            start_addr = 0
            length = 'To_End'
                                      
            if len(sys.argv)>=3:
                endian_flag = sys.argv[2]           
            if len(sys.argv)>=4:
                start_addr = int(sys.argv[3],16)          
            if len(sys.argv)==5:
                length = int(sys.argv[4],16)
                
            Bin_to_Hex(bin_file, out_file, endian_flag, start_addr, length)       
 
            
        print 'Duration: %.2f  seconds'% (time.clock() - time_start)        
    else:
        print '''    
         ******************** usage: ******************
        [1] convert binary format to hexadecimal format:
         - input: 
             [1] bin_file: input bin file name
             [2] endian_flag: '0'(defult) not invert, '1' invert            
             [3] start_addr(hex): extract data from here, defult is 0                 
             [4] length(hex): extract data end to here
                 defult is 'To_End' (to the end of the file)
         @example python BinDatConvert.py xxx.bin
         @example python BinDatConvert.py xxx.bin 1
         @example python BinDatConvert.py xxx.bin 0 17f00
         @example python BinDatConvert.py xxx.bin 1 17f00 12000
        ------------------------------------------------
        [2] convert hexadecimal format to binary format:
         - input: 
             [1] hex_file: input bin file name
             [2] endian_flag: '0'(defult) not invert, '1' invert
         @example python BinDatConvert.py xxx.dat
         @example python BinDatConvert.py xxx.dat 1
         **********************************************        
        '''
        exit(0)
