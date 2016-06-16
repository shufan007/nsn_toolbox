#======================================================================================
#       Function:       Adjust new log mode in source files
#       Author:         Fan, Shuangxi (NSN - CN/Hangzhou)
#       Date:           2014-10-29
#*  *   description:    
# @input:

# @ return:

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
class ComponentLogAdapt:

    def __init__(self, ComponentMapFile, LogMapFilePath):
        
        global OutPutPath
        global SearchPath
        
        self.SearchPath = SearchPath
        
        ######################### control paramaters ########################
        # set print level to control the print
        self.printLevel_1 = 0
        self.printLevel_2 = 0    #run time log, debug log
        # some dir include keys like "UT","MT"..., should regect when searching files
        self.filterKeys = ['UT','UnitTest','ut_','MT','ModuleTest']
        self.dirFilterSwitch = 1     # control if open dir filter or not, "1" open, "0" close
        self.fileFilterSwitch = 1    # control if open file filter or not, "1" open, "0" close
        #####################################################################    
        
        self.ComponentMapFile   = ComponentMapFile
        self.LogMapFilePath     = LogMapFilePath

        self.ComponentBaseList = []
        self.ComponentDirList = []         
        self.DirRootList = []

        # ComponentFileList, ComponentRootList, save all the files and it's roots
        # it can initialized by the same length as ComponentDirList first
        self.ComponentFileList = []
        self.ComponentRootList = []
        self.FileNamekeyWord = ".c"  
             
        self.AdaptDirName = 'AdaptFile'
        if os.path.isdir(self.AdaptDirName) == False:
            #shutil.rmtree(self.AdaptDirName,True)
            os.makedirs(self.AdaptDirName)
            
        self.AdaptFilePath = os.path.join(OutPutPath, self.AdaptDirName)
        
        self.ExceptionLogFileName = 'LogAdaptExceptionLog.txt'
        
         
    ############################# Sub Model ##########################
    # read ComponentId map header file 
    # get ComponentBaseList and it's subComponentDirList
    ##################################################################        
    def GetComponentList(self):
        
        if self.printLevel_1:    
            print '\n- Log map file Path: ' + self.AdaptFilePath
            print '\n- Search Path: ' + self.SearchPath
      
        if os.path.isfile(self.ComponentMapFile):
            print " * Reading Component Map File..."
            H_ComponentId = open(self.ComponentMapFile,'r')
        else:
            print "** Component Map File \"%s\" not exit !!"% (self.ComponentMapFile)
            exit(1)
        Lines = H_ComponentId.read().splitlines()
        H_ComponentId.close()        
        LineNum = len(Lines)
   
        validNum = 0    
        for i in range(0, LineNum):
            ThisLine = Lines[i].strip()
            if ThisLine.find('=')>0 and ThisLine.find('*')>0:            
                self.ComponentBaseList.append(ThisLine[0: ThisLine.find('=')].strip())            
                if self.printLevel_2: # debug print
                    print ('ComponentBaseList[%d]: ' + self.ComponentBaseList[validNum])% (validNum)
                Thisdir = ThisLine[ThisLine.find('*')+1: ThisLine.rfind('*')-1].split(',')
                self.ComponentDirList.append([])            
                for j in range(0,len(Thisdir)):
                    self.ComponentDirList[validNum].append(Thisdir[j].strip())                
                    if self.printLevel_2: # debug print
                        print ('ComponentDirList[%d][%d]: '+self.ComponentDirList[validNum][j])% (validNum,j)
                validNum += 1            
                if self.printLevel_2: # debug print
                    print 'validNum: %d'% validNum            

        print ' * Component map file read complete ...'
        #sprint '## The Component ID and Component dir name have got ...'

        
    ############################# Sub Model ##########################
    # get sub directory(sub component) list   
    # get all child roots and dirs in current root
    # Get root for each subcomponent directory
    ##################################################################
    def GetSubDirList(self):

        self.GetComponentList()
        print ' * Get root for each subcomponent.... '
        
        # DirRoot use to store the root of each dir in ComponentDirList, 
        # so it can initialized by the same size as ComponentDirList

        for k in range(len(self.ComponentDirList)):
            self.DirRootList.append([[None]*len(self.ComponentDirList[k]) for i in range(len(self.ComponentDirList))])
        #DirRootList = copy.deepcopy(ComponentDirList) # another way to initalize dirRootList
            
        # get all child roots and dirs in current root,
        # filter those dirs content keys like 'UT','MT', ...
        rootList = []
        dirList = []
        for root,dirs,files in os.walk(self.SearchPath):   
            for dn in dirs:
                if self.dirFilterSwitch:     # dirFilterSwitch
                    dirFilterFlag = 0
                    for fdn in self.filterKeys:
                        if fdn in os.path.join(root,dn):
                            dirFilterFlag = 1
                            break                    
                    if dirFilterFlag == 0:                 
                        dirList.extend([dn])
                        rootList.extend([root])
                        #print 'os.path.join(root,dn):' + os.path.join(root,dn)
                else:
                    dirList.extend([dn])
                    rootList.extend([root])
        # Get root for each subcomponent directory                           
        for i in range(0, len(self.ComponentBaseList)):             
            for j in range(0,len(self.ComponentDirList[i])):                      
                for k in range(0, len(dirList)):
                    if cmp(dirList[k],self.ComponentDirList[i][j]) == 0:
                        self.DirRootList[i][j] = os.path.join(rootList[k], self.ComponentDirList[i][j])                  
                        if self.printLevel_2:    # debug print
                            print ('DirRootList[%d][%d]: '+ self.DirRootList[i][j]) % (i,j)
            #self.DirRootList[i].sort()
        #print '## All the subcomponent roots have got ...'
                            


    #*******************************************************************************************
    # function GetFilesFromDir:
    #
    # @ description:  This function can get all the file names with key word specified
    #                   from the given directory
    # @ input:
    #       Dir: directory root, may contion several dirs with .c files in it for process
    #           @example: "...\LRC_Trunk\C_Application\SC_UP\DSP\SS_Codec\CP_EncBcpDch"
    #       keyWord: specify the key word in file names, like ".c"
    #       filterKeys: specify the filter key words,like "UT","MT",..., should regect when searching files
    #       fileFilterSwitch: control if open file filter or not, "1" open, "0" close
    # @ return:
    #       fileNum: the number of the files
    #       fileList: the list of the file names
    #       rootList: the list of the files root
    #*******************************************************************************************
    def GetFilesFromDir(self, Dir):
        fileList = []
        rootList = []
        fileNum = 0
        for root,dirs,files in os.walk(Dir):                                                                  
            for fn in files:                    
                ###############################################################
                # The keyWord in file name must be shure only the keyWord,
                # and it must at the end of the file name,
                #   @example: if keyWord is '.c', we can't get '.cmd'
                ###############################################################
                if fn.rfind(self.FileNamekeyWord) == len(fn)-2:
                    if self.fileFilterSwitch: # fileFilterSwitch
                        fileFilterFlag = 0
                        for filterFileStr in self.filterKeys:
                            if filterFileStr in os.path.join(root,fn):
                                fileFilterFlag = 1
                                break                    
                        if fileFilterFlag == 0:                 
                            fileList.extend([fn])
                            rootList.extend([root])
                            fileNum += 1 
                    else:
                        fileList.extend([fn])
                        rootList.extend([root])
                        fileNum += 1   
        #fileList.sort()
        #rootList.sort()
        return (fileNum, fileList, rootList)

    ############################# Sub Model ##########################
    # GetComponentFiles
    # calling Function 'GetFilesFromDir' to get all the valid files
    ##################################################################     
    def GetComponentFiles(self):
        
        self.GetSubDirList()
        
        print ' * GetComponentFiles ....  '
        # ComponentFileList, ComponentRootList, save all the files and it's roots
        # it can initialized by the same length as ComponentDirList first
        self.ComponentFileList = [[]for i in range(len(self.ComponentDirList))]
        self.ComponentRootList = [[]for i in range(len(self.ComponentDirList))]          

        TotalFileNum = 0    
        for i in range(0, len(self.ComponentBaseList)):
            if self.printLevel_2:
                print 'Component number: %2d' % i
                print  self.ComponentBaseList[i]

            ComponentFileNum = 0
            for j in range(0,len(self.ComponentDirList[i])):            
                if self.printLevel_2:
                    print '  number = %d '% j
                    print '     dir: ' + self.ComponentDirList[i][j]
                                                          
                #************************** Function calling: GetFilesFromDir ********************
                (fileNum, fileList, rootList) = self.GetFilesFromDir(self.DirRootList[i][j])
                
                self.ComponentFileList[i].extend(fileList)
                self.ComponentRootList[i].extend(rootList)
                TotalFileNum += fileNum            
                #**********************************************************************************                            
    
        print ' * Get File List complete ...'
        print '## Total valid \'.c\' File Number:  %s' % TotalFileNum

    ############################# Sub Model ##########################
    # Adapt logs
    # calling Function 'LogAdapt' to adapt all the logs for each component
    ##################################################################
    def DirLogAdapt(self):
    
        self.GetComponentFiles()            
        print ' * LOG Adapt start ...  \n'
        totalLogNum = 0
        ExceptionLogFile = open(self.ExceptionLogFileName,'w')
        #print self.ComponentBaseList
        
        for i in range(0, len(self.ComponentBaseList)):
            ComponentName_i = self.ComponentBaseList[i].split('_')[1]
            MapFile = os.path.join(self.LogMapFilePath, 'ELogMapId_' + ComponentName_i + '.h')
            AdaptFileComponentPath = os.path.join(self.AdaptFilePath, ComponentName_i)
            #print MapFile
            if os.path.isdir(AdaptFileComponentPath):
                shutil.rmtree(AdaptFileComponentPath,True)
            os.makedirs(AdaptFileComponentPath)
            
            ExceptionLogFile.write("***Component: %s ***\n"% self.ComponentBaseList[i].split('_')[1])
            print " * Component: %s\n"% self.ComponentBaseList[i].split('_')[1]
            #*********************** Function calling: LogAdapt **********************
            for j in range(0,len(self.ComponentRootList[i])):
                SrcFile = os.path.join(self.ComponentRootList[i][j], self.ComponentFileList[i][j])
                AdaptFile = os.path.join(AdaptFileComponentPath, self.ComponentFileList[i][j])

                if self.printLevel_1:                
                    print "SrcFile: %s"% SrcFile
                    print "AdaptFile: %s"% AdaptFile

                #exit(1)    
                ad_log = LogAdapt(SrcFile, MapFile, AdaptFile)
                ad_log.AdaptSrcFile()                    

                if ad_log.ExceptionLog_str != '':
                    ExceptionLogFile.write(ad_log.ExceptionLog_str)

                totalLogNum += ad_log.logNum              
                if self.printLevel_1:
                    leftBlankLen = 20 - len(self.ComponentBaseList[i].split('_')[-1])
                    print self.ComponentBaseList[i].split('_')[-1] + ':' + ' '*leftBlankLen + ' %d'% (ad_log.logNum)            
            #************************************************************************

        ExceptionLogFile.close()            
        if self.printLevel_1:        
            print '--------------------------------------'        
        print '\n## total log number:  %d ' % (totalLogNum)
        print ' * LOG Adapt complete ...\n'    



#****************************************************************************************
# class LogAdapt:
#
# @ description:  

#****************************************************************************************
class LogAdapt:

    def __init__(self, SrcFile, MapFile, AdaptFile):
        self.SrcFile = SrcFile
        self.MapFile = MapFile
        self.SrcFileNameStr = os.path.basename(SrcFile)[0:-2]
        # ----------------------- control paramaters -----------------------
        self.printLevel_1 = 0
        self.printLevel_2 = 0
        # ----------------------- class field def start --------------------------
        self.keyWord      = 'AaSysLogPrint'
        self.printD      = 'AaSysLogPrintD'
        self.newPrint     = 'SYSLOG_PRINT'
        self.debugTnfoStr = '_DEBUG_INFO_'
        
        self.LINE_str = '__LINE__'
        self.FILE_str = '__FILE__'

         # pattern in source file file
        self.keyWord_pattern        = re.compile(self.keyWord+'[D]?\s?')
        self.keyWordLine_pattern    = re.compile(self.keyWord+'[D]?\s{0,}\(.*EAaSysLogSeverityLevel.*,')
        self.SeverityLevel_pattern  = re.compile('EAaSysLogSeverityLevel.*,')
        self.mapLog_pattern         = re.compile('".*"?\b')
        self.Log_Unnormal_pattern   = re.compile('(".*){3,}')        
        self.srcLog_pattern         = re.compile('".*"|".*\\|.*"')
        
        self.NonSpace_pattern       = re.compile('\S')
        self.doubleSlash_pattern    = re.compile('//')
        
        self.printD_pattern         = re.compile(self.printD)
        self.LINE_pattern           = re.compile(self.LINE_str + '\s*\,')
        self.FILE_pattern           = re.compile(self.FILE_str + '\s*\,')
        
        # pattern in log map file 
        self.FileIndicate_pattern      = re.compile('/\*\s+\-+\s+\w+\s+\-+\s+\*/')
        self.LogId_pattern             = re.compile('E\w+_\d{3,4}')
        self.LogStr_pattern            = re.compile('".+",?$')
        self.CharArrayDefEnd_pattern   = re.compile('^\};$')

        self.NotFindLog_num     = 0
        self.NotFindLogLine     = []
        self.UnnormalLog_num    = 0
        self.UnnormalLogLine    = []

        self.logNum = 0              # the number of logs extract from one file        
        # ----------------------- class field def end --------------------------        
          
        #---------------- get input file data -----------------
        SrcFile_fp = open(SrcFile,'r')
        self.SrcDataLines = SrcFile_fp.readlines()
        self.SrcLineNum = len(self.SrcDataLines)
        SrcFile_fp.close()
        
        MapFile_fp = open(MapFile,'r')
        self.MapDataLines = MapFile_fp.readlines()
        self.MapLineNum = len(self.MapDataLines)
        MapFile_fp.close()
        
        self.MapFileLine_indx = 0
        self.MapFileLine_indx0 = None
        self.MapFileLine_indx_last = None
        
        self.get_MapFileLine_startIndx()

                
        self.AdaptFile   = open(AdaptFile,'w')
        self.ExceptionLog_str = ''
        
        

    def get_MapFileLine_startIndx(self):
        
        for i in range(0, self.MapLineNum):
            if self.MapDataLines[i].find('char *')==0:
                self.MapFileLine_indx = i+1
                break
            
        # find the file name first indx
        while self.MapFileLine_indx < self.MapLineNum:
            ThisLine = self.MapDataLines[self.MapFileLine_indx]
            self.MapFileLine_indx += 1            
            if self.FileIndicate_pattern.search(ThisLine) and \
               ThisLine.find(self.SrcFileNameStr+' ')>=0 :
                
                self.MapFileLine_indx0     = self.MapFileLine_indx
                self.MapFileLine_indx_last = self.MapFileLine_indx

                break         

        
    # get log Id from MapFile
    def GetLogId(self, LogStr):
        
        MapId = None
        find_flag = 0
        search_num = 0
        #print "self.MapFileLine_indx : %d"%  self.MapFileLine_indx                
        while search_num <=1 and self.MapFileLine_indx <self.MapLineNum:
        #while search_num <=1:
            self.MapFileLine_indx += 1

            ThisLine = self.MapDataLines[self.MapFileLine_indx]
           
            if self.LogStr_pattern.search(ThisLine) and ThisLine.find(LogStr) >= 0:
                MapIdLine = self.MapDataLines[self.MapFileLine_indx -1]
                MapId = self.LogId_pattern.search(MapIdLine).group()
                self.MapFileLine_indx_last = self.MapFileLine_indx
                find_flag = 1
                break
                        
            elif self.FileIndicate_pattern.search(ThisLine) or \
              self.CharArrayDefEnd_pattern.search(ThisLine):
                
                if search_num == 0:
                    self.MapFileLine_indx = self.MapFileLine_indx0
                else:
                    self.MapFileLine_indx = self.MapFileLine_indx_last
                    #self.MapFileLine_indx = self.MapFileLine_indx0
                    
                search_num += 1
               
        return MapId

    #*******************************************************************************************    
    # function LogAdapt: can called by function LogMap(): or run alone
    #       extract log print from one .c file, and return the log list
    #*******************************************************************************************
    def AdaptSrcFile(self):        
        keyWordLen = len(self.keyWord)
        #--------- AaSysLogPrint and " flag to locate the log -----------           
        LogPrintFlag = 0        # if 'AaSysLogPrint' exist
        printStrSplitFlag = 0   # sign if one log split into two or more parts
                                # with "\" or "...", "..."       
        #-------------------------------------------------------------------------    

        for i in range(0, self.SrcLineNum):
            
            if self.printLevel_1:
                print "Line num: %d"% i
                
            SrcLine = self.SrcDataLines[i]        
            ThisLine = SrcLine.strip()
            Log_str = None                        
            #-------------------------- start find the valid log -----------------------------
            # check if the log exit ...
            # check if the log just at the behind of key word 'AaSysLogPrint',
            # or at the next line        
            if LogPrintFlag == 0 and self.keyWordLine_pattern.search(ThisLine):
                keyWordLocation = ThisLine.find(self.keyWord)
            else:
                keyWordLocation = -1
                        
            if keyWordLocation < 0 and LogPrintFlag != 1:
                self.AdaptFile.write(SrcLine)
               
            else:
                
                # UnnormalLog check
                if self.Log_Unnormal_pattern.search(SrcLine):
                    self.UnnormalLog_num += 1
                    self.UnnormalLogLine.append(i)               
                
                if keyWordLocation >= 0:
                    LogPrintFlag = 1

                    if keyWordLocation > 0:
                        if ThisLine.find('//')==0:
                            SrcLine = self.doubleSlash_pattern.sub('/* ', SrcLine)+ ' '*SrcLine.find('//')+'*/\n' 
                    
                    Indent_str = ''
                    SpaceStart = self.NonSpace_pattern.search(self.SrcDataLines[i+1])                        
                    if SpaceStart != None:
                        Indent_str += ' '*(SpaceStart.start())
                        
                    if ThisLine.find(');')>0 or ThisLine.find('"')>0:
                        Indent_str = ' '*(SrcLine.find('(')-9)                                    
                       
                    ThisLine = ThisLine[keyWordLen + keyWordLocation: ]
                    
                    if self.printD_pattern.search(SrcLine):
                        if self.LINE_pattern.search(SrcLine):
                            SrcLine = self.LINE_pattern.sub("", SrcLine)
                            
                        if self.FILE_pattern.search(SrcLine):
                            SrcLine = self.FILE_pattern.sub("", SrcLine)                           
                    
                    SrcLine = self.keyWord_pattern.sub(self.newPrint, SrcLine)

                    if self.SeverityLevel_pattern.search(SrcLine) and self.srcLog_pattern.search(SrcLine) == None:
                        self.AdaptFile.write(SrcLine)
                        continue
                    elif self.SeverityLevel_pattern.search(self.SrcDataLines[i+1]):
                        self.AdaptFile.write(self.SrcDataLines[i+1])
                        continue                      
                    elif self.SeverityLevel_pattern.search(SrcLine) and self.srcLog_pattern.search(SrcLine):
                        printLine = SrcLine[0:SrcLine.find(',')]
                        if printLine.find(',')<0:
                            printLine += ','
                            
                        self.AdaptFile.write(printLine+'\n')
                        
                        Log_str = Indent_str + SrcLine[SrcLine.find(',')+1:]
                        
                
                #-------------- start find '"' ----------------
                quotLocation1 = ThisLine.find('"')            
                if quotLocation1 >=0:                
                    LogPrintFlag = 0                
                    quotLocation2 = ThisLine[quotLocation1+1:].rfind('"')
                    Log_section_num = 1
                    
                    if quotLocation2>=0:                                        
                        Log = ThisLine[quotLocation1 : quotLocation1 + quotLocation2+2]
                        #----- check the situation if one log split into two or more parts with '"..."' 
                        ThisLine = self.SrcDataLines[i+1].strip()

                        while ThisLine.find('"')==0:
                            printStrSplitFlag = 1
                            #Log = Log[0:-1] + ThisLine[1: ThisLine[1:].find('"')+2]
                            Log = Log[0:-1] + ThisLine[1: ThisLine[1:].rfind('"')+2]                        
                            Log_section_num += 1
                            ThisLine = self.SrcDataLines[i+Log_section_num].strip()        
                        if printStrSplitFlag == 1:
                            if self.printLevel_1:
                                print 'Here find: Print string split by two or several pair of "" ,'
                                #print ' in file: ' + SrcFileName +  '\n line number: %d'% i    
                            printStrSplitFlag = 0                            
                        
                        # get log
                        self.logNum += 1
                       
                        MapId = self.GetLogId(Log)
                        
                        if MapId != None:
                            self.AdaptFile.write(Indent_str + MapId + ',\n')
                            self.AdaptFile.write(Indent_str + self.debugTnfoStr + ',\n')
                            '''
                            try:
                                self.AdaptFile.write(Indent_str + MapId + ',\n')
                                self.AdaptFile.write(Indent_str + self.debugTnfoStr + ',\n')
                            except:
                                print "Line: %d"% i
                            '''

                            if Log_str != None:
                                self.AdaptFile.write(Log_str)
                            else:
                                self.AdaptFile.write(self.SrcDataLines[i]) 
                        else:
                            self.NotFindLog_num +=1
                            self.NotFindLogLine.append(i)                           
                        
                    else:
                        # ##############################################################
                        # ***** only find one '"',
                        # so the print str must split into two or more parts with "\"
                        # ##############################################################
                        
                        # backSlashLocation = ThisLine[quotLocation1+1:].find('\\')
                        backSlashLocation = ThisLine[quotLocation1+1:].rfind('\\')
                        if backSlashLocation >= 0:
                            Log = ThisLine[quotLocation1: -1]
                            ThisLine = self.SrcDataLines[i+1].strip()
                            backSlashLocation = ThisLine.find('\\')
                            if self.printLevel_1:
                                print 'Here find: Print string split by one or several "\\",'
                                #print 'in file: '+ InputFile + '\n line number: %d'% i                        

                            while backSlashLocation >=0:                            
                                Log = Log + ThisLine[0:backSlashLocation-1]
                                Log_section_num += 1
                                ThisLine = self.SrcDataLines[i+Log_section_num].strip()
                                backSlashLocation = ThisLine.find('\\')                            
                            if ThisLine.find('"')>=0:
                                Log = Log + ThisLine[0:ThisLine.find('"')] 
                #else:  #############################################################
                        # if not find '"' in this line, mabe it in the next line,
                        # so the process go to next loop to find '"' directly,
                        # for LogPrintFlag have valued 1 already
                        #############################################################                                    
                                        
        if self.printLevel_1:
            print '************************************** '
            print 'processed lines: ', self.SrcLineNum
            print 'extract log num: ', self.logNum
            print 'NotFindLog_num:  ', self.NotFindLog_num                    
            print '************************************** '    

        self.AdaptFile.close()
        
        
        if self.NotFindLog_num>0 or self.UnnormalLog_num>0:
            self.ExceptionLog_str += " # File: ...%s\n"% self.SrcFile.split('SC_UP')[1]
            self.ExceptionLog_str += "  - Total log num:  [%d]\n"% self.logNum
            
        if self.NotFindLog_num>0:
            
            self.ExceptionLog_str += "  - NotFindLog_num: [%d]\n"% self.NotFindLog_num
            self.ExceptionLog_str += "  - NotFindLog_Line: "
            for i in range(0,self.NotFindLog_num):
                if i<self.NotFindLog_num-1:
                    self.ExceptionLog_str += "%d, "% self.NotFindLogLine[i]
                else:
                    self.ExceptionLog_str += "%d\n"% self.NotFindLogLine[i]
                    
                if (i+1)%10 == 0 and i<self.NotFindLog_num-1:
                    self.ExceptionLog_str += "\n"
                    self.ExceptionLog_str += "%s"% ' '*len("  - NotFindLog_Line: ")
                elif i==self.NotFindLog_num-1:
                    self.ExceptionLog_str += "\n"

        if self.UnnormalLog_num>0:
                
            self.ExceptionLog_str += "  - UnnormalLog_num: [%d]\n"% self.UnnormalLog_num
            self.ExceptionLog_str += "  - UnnormalLogLine: "
            for i in range(0,self.UnnormalLog_num):
                if i<self.UnnormalLog_num-1:
                    self.ExceptionLog_str += "%d, "% self.UnnormalLogLine[i]
                else:
                    self.ExceptionLog_str += "%d\n"% self.UnnormalLogLine[i]
                    
                if (i+1)%10 == 0 and i < self.UnnormalLog_num-1:
                    self.ExceptionLog_str += "\n"
                    self.ExceptionLog_str += "%s"% ' '*len('  - UnnormalLogLine: ')
                elif i == self.UnnormalLog_num-1:
                    self.ExceptionLog_str += "\n"
       
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
           
        ComponentMapFile = os.path.join(LogMapFilePath,"EComponentId_DSPBase.h")
    
        start = time.clock()

        log_adapt = ComponentLogAdapt(ComponentMapFile, LogMapFilePath)
        log_adapt.DirLogAdapt()

        duration = time.clock() - start  # Run time duration
        print "## Run time duration: %.2f  seconds"% (duration)
        exit(0)

    else:
        print '''
   *************************** Usage: ***************************
   FUNCTION:
    - Read component name and corresponding dirs from input file,
    - map all the .c files, extract and Map Log from all .c files,
    - Out put file 'EFileId_DSPBase.h' located at the root path,
    - 'ELogMapId_***Base.h' files in dir "LogMapHeaderFile",
    -input:            
         -[1] source code search path
         
       @example: python LogAdapt.py D:\userdata\shufan\LRC_Trunk\C_Application\SC_UP\DSP
   **************************************************************
        '''
        exit(0)

