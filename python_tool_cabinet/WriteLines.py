####################################################################
# Get a part of lines from a file, write them to another file
# @example cutLinesFromFile.py SrcFile BeginLine Length DstFile
####################################################################
import os
import sys
import string
import time

def GetLines(SrcFile,BeginLine,Length,DstFile):
    SrcFile = open(SrcFile,'rb')
    DstFile = open(DstFile,'w+')

    BeginLine = string.atoi(BeginLine)
    Length = string.atoi(Length)
    lineLen = len(SrcFile.readline()) # get length of each line
    #lineLen = 12  
    SrcFile.seek((BeginLine-1)*lineLen)   # step to the position
    cnt=0
    while cnt < Length: # write each line from BeginLine 
        DstFile.write(SrcFile.read(lineLen).strip('\n'))
        cnt = cnt+1
        
    SrcFile.close()
    DstFile.close()

if __name__ == '__main__':
    if len(sys.argv)==1 or len(sys.argv)!=5 :
        print 'usage:'
        print 'Get a part of lines from a file, write them to another file '
        print '@example cutLinesFromFile.py SrcFile BeginLine Length DstFile'
        exit(0)
    start = time.clock()       
    GetLines(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
    end = time.clock()

    print 'time: ',
    print end-start
