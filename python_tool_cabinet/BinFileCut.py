import os,sys


def binFileCut(binfile_name, n):
     n = int(n)
     binfile = open(binfile_name, 'rb')   
     
     bytes = binfile.read()
     binfile.close()
     cnt = len(bytes)/4
     section_len = cnt/n
     start = 0
     for i in range(0, n-1):
          outfile = binfile_name[: -4] + '_' + str(i) + '.bin'
          datOut = open(outfile, 'w+')
          tmpString = bytes[start:(start + section_len *4)]   
          datOut.write(tmpString)
          datOut.close()
          start = start + section_len * 4
     
     outfile = binfile_name[: -4] + '_' + str(i+1) + '.bin'
     datOut = open(outfile, 'w+')
     tmpString = bytes[start: cnt*4]   
     datOut.write(tmpString)
     datOut.close()


if __name__ == '__main__':
  if len(sys.argv) != 3:
      print 'usage:'
      print 'split .bin file to n part: '
      print '@example BinFileCut.py 4'
      exit(0)     
  else: 
     binFileCut(sys.argv[1], sys.argv[2])
     
