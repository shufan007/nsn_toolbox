import os,sys,string
def hexstr_to_binstr(hexstr, N,outFileName):
       
    out1=''
    ftxt = open(outFileName,'w')
    for i in range(0,len(hexstr)):
        outstr += ('0'*(4-len(bin(int(hexstr[i],16))[2:]))+ bin(int(hexstr[i],16))[2:])

    for i in range(0,N):
        ftxt.write(outstr[i]+' ')

    ftxt.write('\n')
    ftxt.close()
    

def bin_to_hex(InputFile):
    
    SrcFile = open(InputFile,'r')
    DstFile = open(InputFile[0:-4]+'1.txt','w+')    
    data = SrcFile.read().splitlines()
    LineNum = len(data)
    print LineNum
    seekptr = 0
    
    hex_data = ''
    bin_data = ''
    hex_num = 0
    for i in range(0,LineNum):
        if (i+1)%4 == 0:
            hex_num += 1
            hex_data += hex(int(bin_data,2))[2:]
            
            bin_data =''
            bin_data += data[i]
            
        else:            
            bin_data += data[i]

        if hex_num>0 and hex_num%8 == 0:
            DstFile.write('0x'+hex_data+'\n')
            hex_data = ''
            hex_num = 0                    
    
    SrcFile.close()
    DstFile.close()

def endian_transform(InputFile):
    SrcFile = open(InputFile,'r')
    DstFile = open(InputFile[0:-4]+'_out.txt','w+')    
    data = SrcFile.read().splitlines()
    LineNum = len(data)
    print "line number: %d\n" % LineNum
    data_num = 0

    for i in range(0,LineNum):
        thisline = data[i].split()
        for j in range(0,len(thisline)):
            tran_data_i = thisline[j][6:8]+thisline[j][4:6]+thisline[j][2:4]+thisline[j][0:2]
            DstFile.write('0x'+tran_data_i+'\n')
            data_num += 1
    print "data number: %d\n" % data_num    
    SrcFile.close()
    DstFile.close()    
#********************  main  ****************

    
if __name__ == '__main__':
    #path= "D:\userdata\shufan\Desktop\2"
    
    hexstr = "0000099999992299887755443311"
    #hexstr1="E228DCA4C944C70E99D48000"

    N=81
    outFileName = 'result1.txt'
    
    #hexstr_to_binstr(hexstr, N,outFileName)
    
    #bin_to_hex(srcfile)
    ####################################
    
    srcfile = sys.argv[1]
    
    
    endian_transform(srcfile)
    
