#======================================================================================
#       Function:       Maped Log Adjust
#       Author:         Fan, Shuangxi (NSN - CN/Hangzhou)
#       Date:           2014-11-20
#*  *   description:    add reserve id for new log
#======================================================================================
#!/usr/bin/python

#coding=utf-8
import os, sys
import shutil, string, copy
import re, time


#****************************************************************************************
# class ComponentLogAdapt:
#
# @ description:  
#****************************************************************************************
class MapedLogAdjust:

    def __init__(self,  LogMapFilePath):
        
        global OutPutPath

        ######################### control paramaters ########################
        # set print level to control the print
        self.printLevel_1 = 0
        
        self.MinExtendNum = 5
        self.MaxExtendNum = 50
        self.ExtendRate   = 0.2
        
        self.LogFill_str =  r'    "\0",'

        #####################################################################    
        
        self.LogMapFilePath     = LogMapFilePath
              
        # ComponentFileList, ComponentRootList, save all the files and it's roots
        # it can initialized by the same length as ComponentDirList first
        self.ComponentFileList = []
             
        self.AdjustDirName = 'AdjustFile'
        
        if os.path.isdir(self.AdjustDirName) == False:
            os.makedirs(self.AdjustDirName)
            
        self.AdjustFilePath = os.path.join(OutPutPath, self.AdjustDirName)

        # ----------------------- class field def start --------------------------
        self.LogMapFileName_pattern    = re.compile('ELogMapId_\w+\.h$')
        
        self.FileIndicate_pattern      = re.compile('/\*\s+\-+\s+\w+\s+\-+\s+\*/')        
        
        self.enumDefStart_pattern      = re.compile('^typedef\s+enum\s+\{$')
        self.enumDefEnd_pattern        = re.compile('^\}\w+;$')
        self.LogId_pattern             = re.compile('E\w+_\d{3,4}')
        self.LogIdInFileNum_pattern    = re.compile('_\d{3,4}')
        self.LogIdNum_pattern          = re.compile(',\s{1}\d{1,4}\)')
        
        self.CharArrayDefStart_pattern = re.compile('char\s+\*\s+\w+')        
        self.CharArrayDefEnd_pattern   = re.compile('^\};$') 
        self.LogNum_pattern            = re.compile('\[\d+\]') 
        self.LogStr_pattern            = re.compile('".+",?$')   
        self.LogInsert_pattern         = re.compile('\s+Log Number') 
        
        self.LogReserve_str = ' ** Reserve ** Log Number'        
        # ----------------------- class field def end --------------------------        
          
                
    #*******************************************************************************************
    # function GetFilesFromDir:
    # @ description:  This function can get all the file names with key word specified
    #                   from the given directory
    #*******************************************************************************************
    def GetFilesFromDir(self, Dir):
        fileList = []
        for root,dirs,files in os.walk(Dir):                                                                  
            for fn in files:                    
                if self.LogMapFileName_pattern.match(fn):
                    fileList.extend([fn])  
        return fileList


    ############################# Sub Model ##########################
    # Adjust logs for all files of a File List
    # calling Function 'LogIdExtend' to process all the log Ids for each file
    ##################################################################
    def LogIdAdjust(self):
    
        fileList = self.GetFilesFromDir(self.LogMapFilePath) 

        if os.path.isdir(self.AdjustFilePath):
            shutil.rmtree(self.AdjustFilePath,True)
        os.makedirs(self.AdjustFilePath)        
        
        print ' * LOG Adjust start ...  \n'
        
        print " * Component file:\n"      
        
        for i in range(0, len(fileList)):
            
            print "  - %s\n"% fileList[i]
            #*********************** Function calling: LogIdExtend **********************

            MapFile    = os.path.join(self.LogMapFilePath, fileList[i])
            AdjustFile = os.path.join(self.AdjustFilePath, fileList[i])
   
            self.LogIdExtend(MapFile, AdjustFile)          
          
            #************************************************************************
        
        print ' * LOG Adjust complete ...\n'       
    
    
    def getLogNumInFile(self, fileLine):
        m = self.LogIdInFileNum_pattern.search(fileLine)
        num = None
        if m:
            num = int(m.group()[1:])
        return num
              
        
    def getLogNumInComponent(self, fileLine):
        m = self.LogIdNum_pattern.search(fileLine)
        num = None
        if m:
            num = int(m.group()[2:-2])
        return num
    
    
    # replace LogIdNumInComponent and LogIdNumInFile(defult)    
    def replace_LogId(self, fileLine, LogIdNumInComponent, LogIdNumInFile = None):
        
        if LogIdNumInFile != None:
            LogIdNumInFile_str = "_%03d"%  LogIdNumInFile 
            fileLine = self.LogIdInFileNum_pattern.sub(LogIdNumInFile_str, fileLine)
            
        LogIdNumInComponent_str = ", %d)"% LogIdNumInComponent    
        fileLine = self.LogIdNum_pattern.sub(LogIdNumInComponent_str, fileLine)
        
        return fileLine
    
    
    def get_extendLogNum(self, originalLogNum):
        
        extendLogNum = int(originalLogNum * self.ExtendRate)
        if extendLogNum < self.MinExtendNum:
            extendLogNum = self.MinExtendNum
        elif extendLogNum > self.MaxExtendNum:
            extendLogNum = self.MaxExtendNum
        return extendLogNum   
    
    
    def add_LogIdToFile(self, File_fp, fileLine, LogIdNumInComponent, LogIdNumInFile):
        addNum = self.get_extendLogNum(LogIdNumInFile)
        
        for i in range(0, addNum):
            LogIdNumInFile_str = "_%03d"%  (LogIdNumInFile + i)
            
            fileLine = self.LogIdInFileNum_pattern.sub(LogIdNumInFile_str, fileLine)
            
            LogIdNumInComponent_str = ", %d)"% (LogIdNumInComponent + i)   
            fileLine = self.LogIdNum_pattern.sub(LogIdNumInComponent_str, fileLine)
            
            File_fp.write(fileLine)
        #File_fp.write("\n")
        
        return addNum


    # replace LogIdNumInComponent and LogIdNumInFile(defult)    
    def replace_LogNote(self, fileLine, LogIdNumInComponent, LogIdNumInFile = None):      
        
        if LogIdNumInFile != None:
            LogIdNumInFile_str = "_%03d"%  (LogIdNumInFile) 
            fileLine = self.LogIdInFileNum_pattern.sub(LogIdNumInFile_str, fileLine)
            
        LogIdNumInComponent_str = "[%d]"% (LogIdNumInComponent)    
        fileLine = self.LogNum_pattern.sub(LogIdNumInComponent_str, fileLine)
        
        return fileLine
    
    
    
    def add_LogNoteToFile(self, File_fp, fileLine, LogIdNumInComponent, LogIdNumInFile):
        addNum = self.get_extendLogNum(LogIdNumInFile)
        
        fileLine = self.LogInsert_pattern.sub(self.LogReserve_str, fileLine)        
        for i in range(0, addNum):                        
            
            LogIdNumInFile_str = "_%03d"%  (LogIdNumInFile + i)
            fileLine = self.LogIdInFileNum_pattern.sub(LogIdNumInFile_str, fileLine)
            
            LogIdNumInComponent_str = "[%d]"% (LogIdNumInComponent + i)   
            fileLine = self.LogNum_pattern.sub(LogIdNumInComponent_str, fileLine)
            

            
            File_fp.write(fileLine)
            File_fp.write(self.LogFill_str + '\n')
            
        #File_fp.write("\n")
        
        return addNum   
        
    #*******************************************************************************************    
    # LogExtend: extend log Id to the log map file
    #     
    #*******************************************************************************************
    def LogIdExtend(self, MapFile, AdjustFile):
        #LogNumList       = []
        #ExtendLogNumList = []
        LogNum = 0
        
        enumDefStartFlag      = 0
        enumDefEndFlag        = 0
        CharArrayDefStartFlag = 0
        CharArrayDefEndFlag   = 0
        
        FileNum             = 0
        LogIdNumInComponent = 0
        LastLogIdLine       = None 
        
        #---------------- get input file data -----------------
        
        MapFile_fp = open(MapFile,'r')
        MapDataLines = MapFile_fp.readlines()
        MapLineNum = len(MapDataLines)
        MapFile_fp.close()
        
        AdjustFile_fp  = open(AdjustFile, 'w')
                    

        for i in range(0, MapLineNum):    
                
            SrcLine = MapDataLines[i]       
                        
            if enumDefStartFlag == 0:
                
                AdjustFile_fp.write(SrcLine)
                if self.enumDefStart_pattern.search(SrcLine):
                    enumDefStartFlag = 1

            elif enumDefStartFlag == 1 and enumDefEndFlag == 0:
                
                if FileNum == 0 and self.FileIndicate_pattern.search(SrcLine):
                    
                    AdjustFile_fp.write(SrcLine)
                    
                    FileNum += 1                    
                    LogIdNumInFile = 0
                    
                elif FileNum == 1:
                    
                    if self.LogId_pattern.search(SrcLine):
                        
                        LastLogIdLine = SrcLine
                        
                        fileLine = self.replace_LogId(SrcLine, LogIdNumInComponent, LogIdNumInFile)
                        
                        AdjustFile_fp.write(fileLine)
                        
                        LogIdNumInFile += 1
                        LogIdNumInComponent += 1
                        
                    elif self.FileIndicate_pattern.search(SrcLine):

                        addNum = self.add_LogIdToFile(AdjustFile_fp, LastLogIdLine, LogIdNumInComponent, LogIdNumInFile)
                        AdjustFile_fp.write("\n")
                        
                        AdjustFile_fp.write(SrcLine)
                        
                        FileNum += 1
                        LogIdNumInFile = 0
                        LogIdNumInComponent += addNum

                        
                elif FileNum >1:
                    
                    if self.LogId_pattern.search(SrcLine):                      
                        
                        LastLogIdLine = SrcLine
                        
                        fileLine = self.replace_LogId(SrcLine, LogIdNumInComponent, LogIdNumInFile)
                        AdjustFile_fp.write(fileLine)                     
                        
                        LogIdNumInFile += 1
                        LogIdNumInComponent += 1                        
                        
                    elif self.FileIndicate_pattern.search(SrcLine) or self.enumDefEnd_pattern.search(SrcLine):
                                                    
                        if self.enumDefEnd_pattern.search(SrcLine):
                            enumDefEndFlag = 1
                            if LastLogIdLine.rfind('),') < 0:
                                LastLogIdLine = LastLogIdLine[0:-1] + ',\n' 
                            
                        addNum = self.add_LogIdToFile(AdjustFile_fp, LastLogIdLine, LogIdNumInComponent, LogIdNumInFile)
                                                                        
                        LogIdNumInComponent += addNum
                        LogIdNumInFile += addNum
                                                                    
                        if self.enumDefEnd_pattern.search(SrcLine):
                            LastLogIdLine = LastLogIdLine[0:-2] + '\n' 
                            
                            LogIdNumInFile_str = "_%03d"%  (LogIdNumInFile)                           
                            
                            fileLine = self.LogIdInFileNum_pattern.sub(LogIdNumInFile_str, LastLogIdLine)
                            
                            LogIdNumInComponent_str = ", %d)"% (LogIdNumInComponent)   
                            fileLine = self.LogIdNum_pattern.sub(LogIdNumInComponent_str, fileLine)
                            
                            AdjustFile_fp.write(fileLine)
                            
                        FileNum += 1
                        LogIdNumInFile = 0 
                        
                        AdjustFile_fp.write("\n")
                        AdjustFile_fp.write(SrcLine)                                                            
                    
            elif enumDefEndFlag == 1 and CharArrayDefStartFlag == 0:
                
                AdjustFile_fp.write(SrcLine)
                
                if self.CharArrayDefStart_pattern.search(SrcLine):
                    CharArrayDefStartFlag = 1
                    FileNum = 0
                    LogIdNumInComponent = 0
                
            elif CharArrayDefStartFlag == 1 and CharArrayDefEndFlag == 0:                
                
                if  FileNum == 0:
                    if self.FileIndicate_pattern.search(SrcLine):
                        AdjustFile_fp.write(SrcLine)
                        
                        FileNum += 1                    
                        LogIdNumInFile = 0 
                    else:
                        AdjustFile_fp.write(SrcLine)
                    
                elif FileNum == 1:
                    
                    if self.LogId_pattern.search(SrcLine):
                        
                        LastLogIdLine = SrcLine
                        
                        fileLine = self.replace_LogNote(SrcLine, LogIdNumInComponent, LogIdNumInFile)
                        
                        AdjustFile_fp.write(fileLine)
                        
                        LogIdNumInFile += 1
                        LogIdNumInComponent += 1
                        
                    elif self.FileIndicate_pattern.search(SrcLine):

                        addNum = self.add_LogNoteToFile(AdjustFile_fp, LastLogIdLine, LogIdNumInComponent, LogIdNumInFile)
                        AdjustFile_fp.write("\n")
                        
                        AdjustFile_fp.write(SrcLine)
                        
                        FileNum += 1
                        LogIdNumInFile = 0
                        LogIdNumInComponent += addNum
                        
                    elif self.LogStr_pattern.search(SrcLine):
                        AdjustFile_fp.write(SrcLine) 
                        
                        
                elif FileNum >1:
                    
                    if self.LogId_pattern.search(SrcLine):                      
                        
                        LastLogIdLine = SrcLine
                        
                        fileLine = self.replace_LogNote(SrcLine, LogIdNumInComponent, LogIdNumInFile)
                        
                        AdjustFile_fp.write(fileLine)                     
                        
                        LogIdNumInFile += 1
                        LogIdNumInComponent += 1                        
                        
                    elif self.FileIndicate_pattern.search(SrcLine) or self.CharArrayDefEnd_pattern.search(SrcLine):
                                                
                        addNum = self.add_LogNoteToFile(AdjustFile_fp, LastLogIdLine, LogIdNumInComponent, LogIdNumInFile)
                                                                           
                        LogIdNumInComponent += addNum
                        LogIdNumInFile +=addNum
                                                                    
                        if self.CharArrayDefEnd_pattern.search(SrcLine):                        
                            
                            LogIdNumInFile_str = "_%03d"%  (LogIdNumInFile)
                            fileLine = self.LogIdInFileNum_pattern.sub(LogIdNumInFile_str, LastLogIdLine)
                            
                            LogIdNumInComponent_str = "[%d]"% (LogIdNumInComponent)   
                            fileLine = self.LogNum_pattern.sub(LogIdNumInComponent_str, fileLine)
                            fileLine = self.LogInsert_pattern.sub(self.LogReserve_str, fileLine)

                            AdjustFile_fp.write(fileLine)
                            AdjustFile_fp.write(self.LogFill_str[0:-1] + '\n')
                            AdjustFile_fp.write("\n")
                            
                            AdjustFile_fp.write(SrcLine) 
                            
                            CharArrayDefEndFlag = 1
                            FileNum -= 1
                            
                        elif self.FileIndicate_pattern.search(SrcLine):
                            AdjustFile_fp.write("\n")                            
                            AdjustFile_fp.write(SrcLine)                            
                            
                            FileNum += 1
                            LogIdNumInFile = 0                        
                        
                    elif self.LogStr_pattern.search(SrcLine):
                        AdjustFile_fp.write(SrcLine)
                        
            elif CharArrayDefEndFlag == 1:
                AdjustFile_fp.write(SrcLine)
                
                                    
        AdjustFile_fp.close()  
       
#*************************########---  main  ---#######************************
if __name__ == '__main__':
    
    global SearchPath    
    global OutPutPath
    
    if len(sys.argv)==2 and sys.argv[1]!= '-help':
        
        if os.path.dirname(sys.argv[0]) != '':
        
            OutPutPath = os.path.dirname(sys.argv[0])
        else:
            OutPutPath = os.getcwd()            
                
        SearchPath = sys.argv[1]       
                        
        # file path: option 2
        Log_Env_path = ['include','Codec_Env','Log_Env']
        
        LogMapFilePath = SearchPath
        for i in range(0,len(Log_Env_path)):
            LogMapFilePath   = os.path.join(LogMapFilePath, Log_Env_path[i])
           
    
        start = time.clock()

        log_ad = MapedLogAdjust(LogMapFilePath)
        log_ad.LogIdAdjust()

        duration = time.clock() - start  # Run time duration
        print "## Run time duration: %.2f  seconds"% (duration)
        exit(0)

    else:
        print '''
   *************************** Usage: ***************************
   FUNCTION:
       -input:            
         -[1] source code search path
         
       @example: python MapedLogAdjust.py D:\userdata\shufan\LRC_Trunk\C_Application\SC_UP\DSP
   **************************************************************
        '''
        exit(0)

