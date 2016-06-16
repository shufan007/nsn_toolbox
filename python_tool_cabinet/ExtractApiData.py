#==============================================================
#       Function:       Extract data from Api log
#       Author:         Fan Shaungxi
#*  *   description:    This Script can extract the data part from the Api log report file,
#                       and save the data to .xls file
#==============================================================
import os, sys, string, time, xlwt


def GetApiData(LogFile):
    
    SrcFile = open(LogFile,'r')
    DataLine = SrcFile.read().splitlines()   
    LineNum = len(DataLine)
    
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

# ------- Get items of the sheet   --------
    StartFlag = 0
    ItemNum = 0
    i = 0
    while StartFlag < 2:       
        if DataLine[i].find('MESSAGE')>0:
            StartFlag = StartFlag + 1
             
        if DataLine[i].find('=')>0:
            ThisLine = DataLine[i].split()
            sheet.write(0, ItemNum, ThisLine[0],item_style)    # write the item
            ItemNum = ItemNum + 1 
            
        i = i+1
        
# ------- Get data for each item   --------
    
    row = 0             #   row of the data
    itemIdx = 0         #   item index of eatch data (range from 0 to ItemNum)
    for i in range(0, LineNum):
        
#   Note:   becase the number of '=' is much more than 'MESSAGE', so, 
#           here we first judge '=' other than 'MESSAGE' in consideration of the efficiency.
        if DataLine[i].find('=')>0:
            ThisLine = DataLine[i].split()
            sheet.write(row,itemIdx,ThisLine[2],data_style)    # write the data
            itemIdx = itemIdx + 1
        elif DataLine[i].find('MESSAGE')>0:
            row = row + 1
            itemIdx = 0           

    print '************************************** '
    print 'processed lines:    ', LineNum
    print 'extract data lines: ', row   
    print '************************************** '
    
    SrcFile.close()
    wbk.save(LogFile[0:-4]+'.xls')  # save data to .xls file    


#********************  main  ****************
if __name__ == '__main__':
    if len(sys.argv)==1 or len(sys.argv)!=2 :
        print 'usage:'
        print 'Extract data from api log report file, save it to .xls file'
        print '@example ExtractApiData.py test.txt'
        exit(0)
    start = time.clock()
    
    GetApiData(sys.argv[1])
    
    end = time.clock()

    duration = end - start
    
    print 'duration: %.2f  seconds'% duration
