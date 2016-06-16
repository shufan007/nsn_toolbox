#======================================================================================
#       Function:       API report data result analysis
#       Author:         Fan, Shuangxi (NSN - CN/Hangzhou)
#       Date:           2014-12-29
#*  *   description:    read API report data, check the data accronding to the rules being given
#                      
#======================================================================================
import sys, os
import xlrd, time
import re
from GlobDef import *

# ###############################################

# class: ResultAnalysis

# ###############################################
class ResultAnalysis(object):
    
    def __init__(self, Paras):
        
        global BasePath
        global result_file
        global API_Data_dir
        
        result_file = os.path.join(API_Data_dir, result_file)    
        self.result_file = os.path.join(BasePath, result_file) 
        
        self.Paras = Paras
        
        self.msgId = None
        self.FieldNameList = []
        self.valueMinList  = []
        self.valueMaxList  = [] 
        self.checkNum = None
        
        self.split_paras()
        
        self.checkData = []
        self.field_num = len(self.FieldNameList)
        self.data_len = None
        
        
    def split_paras(self):
        
        if (len(self.Paras) -2)%3 == 0:
            
            self.msgId = self.Paras[0]
            
            try:
                self.checkNum = int(self.Paras[1])
            except:
                print "** checkNum should be a number."
                exit(2)
                   
            for i in range(0, (len(self.Paras) -2)/3):
                self.FieldNameList.append(self.Paras[i*3+2])
                self.valueMinList.append(int(self.Paras[i*3+3]))
                self.valueMaxList.append(int(self.Paras[i*3+4]))
            
        else:
            print "** Invalid parameter list!"
            exit(2)
            
            
        
    def check_resultFile(self):
        
        # check if result_file exist
        print " * check if result_file exist ......\n"    
        check_period = 1
        wait_time = 120
        time_count = 0
        while (os.path.exists(self.result_file)==False):
            time.sleep(check_period)
            time_count += check_period
            if time_count > wait_time:
                print "** result_file: %s not find!"% (self.result_file)
                print "** time out for result_file check!"            
                exit(2)        


                
    # get field data accronding to field name
    # one field may have several data
    def get_field_data(self, fieldName, items, data):
        fieldData = []
        for i in range(0, len(items)):
            if items[i].upper().find(fieldName.upper())>=0:
                fieldData.append(data[i])
        return  fieldData
    
    

    # get the checkData
    def get_checkData(self):
        
        # get data and items of all the sheets
        (SheetNameList, ItemList, DataList) = read_data_from_xls(self.result_file)
        
        # get data and items of the sheet named with msgId   
        for i in range(0, len(SheetNameList)):
            if SheetNameList[i] == self.msgId:
                items = ItemList[i]
                data  = DataList[i]
                break
        
        # get the col data that will be checked
        DataCol = []        
        for i in range(0, self.field_num):            
            fieldData = self.get_field_data(self.FieldNameList[i], items, data)            
            DataCol.append(fieldData)
            

        # transfor the col data to row data
        
        self.data_len = len(DataCol[0][0])
            
        self.checkData = [None for i in range(0, self.data_len)] 
        
        for i in range(0, self.data_len):
            thisDataLine = [[] for jj in range(0, self.field_num)]
            for j in range(0, self.field_num):
                for k in range(0, len(DataCol[j])):
                    thisDataLine[j].append(DataCol[j][k][i])

            self.checkData[i] = thisDataLine
                                              
                                
        
    # ###############################################        
    # check one Group Data
    # return: matched_flag
    #   1   match
    #   0   not match
    # ###############################################
    def check_oneGroupData(self, DataList):
        
        matched_flag = 0
        match_flagList = [0 for i in range(0, self.field_num)]
        
        for i in range(0, self.field_num):
            for j in range(0, len(DataList[i])):                    
                if int(DataList[i][j]) >= self.valueMinList[i] and int(DataList[i][j]) <= self.valueMaxList[i]:
                    match_flagList[i] = 1                        
        
        if sum(match_flagList) == self.field_num:
            matched_flag = 1
            
        return matched_flag 
        
    
    # final check 
    def check_data(self):
        
        self.check_resultFile()
        self.get_checkData()
        
        matched_num = 0
        if self.checkData:           
            for i in range(0, self.data_len):
                matched_flag = self.check_oneGroupData(self.checkData[i])
                matched_num += matched_flag           
            
        else:
            print " check data get failed! "
            exit(2)
            
        # result report            
        print "\n ************* check result report: ************** "
        print " * Report number: %d, Matched number: %d"% (self.data_len, matched_num)
            
        if self.checkNum == matched_num:
            
            print " * check * PASS!"
            print " ********************************************** "
            exit(0)
        else:
            print " * check * Failure!"
            print " ********************************************** "
            exit(1) 
                                  

   
# ###############################################
# read item and data from .xls file
# ###############################################
def read_data_from_xls(file_name):
    #-------- global def ---------
    item_line       = 1
    data_line_start = 2
    
    SheetNameList = []
    ItemList      = []
    DataList      = []
    #------- global def end ------
    
    data = xlrd.open_workbook(file_name)
    
    SheetNameList = data.sheet_names()
    
    for k in range(0, len(data.sheets())):
        table = data.sheets()[k]
        data_col = []
        
        ItemList.append(table.row_values(item_line))            
            
        for j in range(0, table.ncols):
            data_col.append(table.col_values(j)[data_line_start:])
            
        DataList.append(data_col)
        
    return (SheetNameList, ItemList, DataList)

        

#********************************  main  **********************************
if __name__ == '__main__':

    BasePath = ''
   
    if len(sys.argv)>=1:
        BasePath = os.path.dirname(sys.argv[0])
        
    if len(sys.argv) >= 6:
        Paras = sys.argv[1:]                       
        #start = time.clock()
        ra = ResultAnalysis(Paras)
        ra.check_data()
        
        #print 'Duration: %.2f  seconds'% (time.clock() - start)            
        exit(0)                     
        
    else:
        print'''

   *************************** Usage: ***************************
        -input:
             -[1] msgID	
             -[2] checkNum
             -[3] FieldName1	
             -[4] valueMin1             
             -[5] valueMax1
             -[6] FieldName2 (optional)	
             -[7] valueMin2  (optional)
             -[8] valueMax2  (optional)	             
              ...   
              
       @example:
               python ResultAnalysis_numCheck.py 5184 10 FieldName1 valueMin1 valueMax1
   
   **************************************************************
        '''
        exit(1)   
