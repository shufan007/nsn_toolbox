#======================================================================================
#       Function:       Extract Log and Map log id
#       Author:         Fan Shaungxi(Fan, Shuangxi (NSN - CN/Hangzhou))
#       Date:           2014-08-01
#*  *   description:    This Script can extract the Log from the .c files,
#                       and map the log with log Id, map file with file Id,
#                       put the map to .h files
# @input:
#       ComponentMapFile: is a '.h' file, should put at the same path with the component
#           @example: " ...\DSP\EComponentId_DSPBase.h "
# @ return:
#   The function No return value, it creat some .h files and saved them in LogFilePath
#   The files like "EFileId_DSPBase.h" located at the root path,
#   and files like "ELogMapId_CodecDecBase.h" located at the dir like "LogMapHeaderFile"
#======================================================================================
#!/usr/bin/python

#coding=utf-8
import os, sys, shutil,string, copy, time

#****************************************************************************************
# function ComponentMap:
#
# @ description:  this function read component name and the corresponding dirs,
#                 from input file ComponentMapFile ,
#                 map all the .c files and logs in the dirs, save the map to .h files
# @ input:
#       ComponentMapFile: is a '.h' file, should put at the same path with the component
#           @example:  " ...\DSP\EComponentId_DSPBase.h "
# @ return:
#   The function No return value, it creat some .h files and saved them in LogFilePath
#   The files like "EFileId_DSPBase.h" located at the root path,
#   and files like "ELogMapId_CodecDecBase.h" located at the dir like "LogMapHeaderFile"
#****************************************************************************************
def ComponentMap(ComponentMapFile):
    
    ######################### control paramaters ########################
    # set print level to control the print
    printLevel_1 = 1
    printLevel_2 = 0    #run time log, debug log
    # some dir include keys like "UT","MT"..., should regect when searching files
    filterKeys = ['UT','UnitTest','ut_','MT','ModuleTest']
    dirFilterSwitch = 1     # control if open dir filter or not, "1" open, "0" close
    fileFilterSwitch = 1    # control if open file filter or not, "1" open, "0" close
    ##################################################################### 
    global OutPutPath
    global SearchPath    
  
    if printLevel_1:    
        print '\n- Log map file Path: ' + OutPutPath
        print '\n- Search Path: ' + SearchPath

    ############################# Sub Model ##########################
    # read ComponentId map header file 
    # get ComponentBaseList and it's subComponentDirList
    ##################################################################       
    if os.path.isfile(ComponentMapFile):
        print " * Reading Component Map File..."
        H_ComponentId = open(ComponentMapFile,'r')
    else:
        print "** Component Map File \"%s\" not exit !!"% (ComponentMapFile)
        return
    Lines = H_ComponentId.read().splitlines()
    LineNum = len(Lines)
    ComponentBaseList = []
    ComponentDirList = []    
    validNum = 0    
    for i in range(0, LineNum):
        ThisLine = Lines[i].strip()
        if ThisLine.find('=')>0 and ThisLine.find('*')>0:            
            ComponentBaseList.append(ThisLine[0: ThisLine.find('=')].strip())            
            if printLevel_2: # debug print
                print ('ComponentBaseList[%d]: ' + ComponentBaseList[validNum])% (validNum)
            Thisdir = ThisLine[ThisLine.find('*')+1: ThisLine.rfind('*')-1].split(',')
            ComponentDirList.append([])            
            for j in range(0,len(Thisdir)):
                ComponentDirList[validNum].append(Thisdir[j].strip())                
                if printLevel_2: # debug print
                    print ('ComponentDirList[%d][%d]: '+ComponentDirList[validNum][j])% (validNum,j)
            validNum += 1            
            if printLevel_2: # debug print
                print 'validNum: %d'% validNum            
    H_ComponentId.close()
    print ' * Component map file read complete ...'
    #sprint '## The Component ID and Component dir name have got ...'

    ############################# Sub Model ##########################
    # get sub directory(sub component) list   
    # get all child roots and dirs in current root
    # Get root for each subcomponent directory
    ##################################################################    
    print ' * Get root for each subcomponent.... '
    ComponentPathFile = os.path.join(OutPutPath,'ComponentPath.txt')
    if os.path.isfile(ComponentPathFile):
        os.remove(ComponentPathFile)        
    ComponentPath = open(ComponentPathFile ,'w+')
    
    # DirRoot use to store the root of each dir in ComponentDirList, 
    # so it can initialized by the same size as ComponentDirList
    DirRootList = []
    for k in range(len(ComponentDirList)):
        DirRootList.append([None for i in range(len(ComponentDirList[k]))])
    #DirRootList = copy.deepcopy(ComponentDirList) # another way to initalize dirRootList
        
    # get all child roots and dirs in current root,
    # filter those dirs content keys like 'UT','MT', ...
    rootList = []
    dirList = []
    for root,dirs,files in os.walk(SearchPath):   
        for dn in dirs:
            if dirFilterSwitch:     # dirFilterSwitch
                dirFilterFlag = 0
                for fdn in filterKeys:
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
    for i in range(0, len(ComponentBaseList)):        
        ComponentPath.write('\nComponent number: [* %d *]\n' % i)
        ComponentPath.write(' ' + ComponentBaseList[i] + '\n')        
        for j in range(0,len(ComponentDirList[i])):           
            ComponentPath.write('   sub component %d : '% j)
            ComponentPath.write( ComponentDirList[i][j] + '\n')                        
            for k in range(0, len(dirList)):
                if cmp(dirList[k],ComponentDirList[i][j]) == 0:
                    DirRootList[i][j] = os.path.join(rootList[k],ComponentDirList[i][j])
                    ComponentPath.write('        path:  ' + os.path.join(DirRootList[i][j], ComponentDirList[i][j]) + '\n')                    
                    if printLevel_2:    # debug print
                        print ('DirRootList[%d][%d]: '+DirRootList[i][j]) % (i,j)
    ComponentPath.close()
    #print '## All the subcomponent roots have got ...'

    ############################# Sub Model ##########################
    # fileId MAP
    # calling Function 'GetFilesFromDir' to get all the valid files
    # map files with file Id, and saved to '.h' file
    ################################################################## 
    print ' * fileId MAP start ....  '
    # ComponentFileList, ComponentRootList, save all the files and it's roots
    # it can initialized by the same length as ComponentDirList first
    ComponentFileList = [[]for i in range(len(ComponentDirList))]
    ComponentRootList = [[]for i in range(len(ComponentDirList))]
    FileNamekeyWord = ".c"           
    # ----------------- FileId map header file -------------------
    FileIdHeaderFile = os.path.join(OutPutPath, 'EFileId_' + ComponentMapFile.split('_')[-1])
    if os.path.isfile(FileIdHeaderFile):
        os.remove(FileIdHeaderFile)        
    H_FileId = open(FileIdHeaderFile,'w+')    
    H_FileId.write('\n#include <' + ComponentMapFile + '>\n\n')
    TotalFileNum = 0    
    for i in range(0, len(ComponentBaseList)):
        if printLevel_2:
            print 'Component number: %2d' % i
            print  ComponentBaseList[i]
        H_FileId.write('\n/* ' + ComponentBaseList[i] + ' */\n\n')
        H_FileId.write('typedef enum {\n')

        ComponentFileNum = 0
        for j in range(0,len(ComponentDirList[i])):            
            if printLevel_2:
                print '  number = %d '% j
                print '     dir: ' + ComponentDirList[i][j]
                
            H_FileId.write('\n    /* ' + ComponentDirList[i][j] + ' */\n')                        
            if ComponentDirList[i][j].find('_')>0:
                Component = ComponentDirList[i][j].split('_')[-1]                
            #************************** Function calling: GetFilesFromDir ********************
            if DirRootList[i][j] != None:
                (fileNum, fileList, rootList) = \
                          GetFilesFromDir(DirRootList[i][j], FileNamekeyWord, filterKeys, fileFilterSwitch)
                
                ComponentFileList[i].extend(fileList)
                ComponentRootList[i].extend(rootList)
                TotalFileNum += fileNum            
                #**********************************************************************************                            
                for k in range(0, len(fileList)):
                    fileId = 'E'+ ComponentBaseList[i].split('_')[-1] + 'FileId' + '_' + fileList[k][0:-2]
                    leftBlankLen = 50 - len(fileId)  
                    H_FileId.write('%s'% '    '+ fileId + ' '*leftBlankLen)                
                    if j<len(ComponentDirList[i]) and k < len(fileList)-1:
                        H_FileId.write((' = ' + ComponentBaseList[i] + ' + ' + '0x%02x' + ',\n')% ComponentFileNum)
                    elif j==len(ComponentDirList[i])-1 and k == len(fileList)-1:
                        H_FileId.write((' = ' + ComponentBaseList[i] + ' + ' + '0x%02x' + '\n')% ComponentFileNum)                    
                    ComponentFileNum += 1    
        H_FileId.write('\n} ' + 'EFileId_' + ComponentBaseList[i] + ';\n')                
    H_FileId.close()    
    print ' * fileId_MAP complete ...'
    print '## Total valid \'.c\' File Number:  %s' % TotalFileNum

    ############################# Sub Model ##########################
    # LOGID MAP
    # calling Function 'LogMap' to map all the logs for each component,
    # and saved to '.h' files
    ##################################################################         
    print ' * LOGID MAP start ...  \n'
    totalLogNum = 0    
    LogDirName = 'LogMapHeaderFile'
    LogFilePath = os.path.join(OutPutPath, LogDirName)
    print '* Log file location:\n    %s'% (LogFilePath)
    if os.path.isdir(LogFilePath):
        shutil.rmtree(LogFilePath,True)        
    os.makedirs(LogFilePath)
    if printLevel_1:        
        print '----- Component Log number: -------- \n'              
    for i in range(0, len(ComponentBaseList)):        
        #*********************** Function calling: LogMap **********************       
        logNum = LogMap(ComponentRootList[i],\
                        ComponentFileList[i],\
                        ComponentBaseList[i].split('_')[-1],\
                        LogFilePath)
        
        totalLogNum += logNum                
        if printLevel_1:
            leftBlankLen = 20 - len(ComponentBaseList[i].split('_')[-1])
            print ComponentBaseList[i].split('_')[-1] + ':' + ' '*leftBlankLen + ' %d'% (logNum)            
        #************************************************************************
    if printLevel_1:        
        print '--------------------------------------'        
    print '\n## total log number:  %d ' % (totalLogNum)
    print ' * LOGID_MAP complete ...\n'    

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

def GetFilesFromDir(Dir, keyWord, filterKeys, fileFilterSwitch):
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
            if fn.rfind(keyWord) == len(fn)-2:
                if fileFilterSwitch: # fileFilterSwitch
                    fileFilterFlag = 0
                    for filterFileStr in filterKeys:
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
    return (fileNum, fileList, rootList)

#*******************************************************************************************
# function LogMap:
#
# @ description:  This function can extract the Logs from the all .c files of given dirs
#               with calling function ExtractLog():, and map the log with log Id, map file with file Id
# @ input:
#       DirRootList: dir root list, may contion several dirs with .c files in it for process
#           @example: [ "...\LRC_Trunk\C_Application\SC_UP\DSP\SS_Codec\CP_EncBcpDch",
#                       "...\LRC_Trunk\C_Application\SC_UP\DSP\SS_Codec\CP_Encoder" ]
#       ComponentBase: Component Base dir, like "CodecBase", it pass the base name to LogMap
#       LogFilePath: A dir name joined with path and the log file can saved in it
# @ return:
#       TotalLogNum: the number of the logs 
#   The function creat '.h' file and saved it in LogFilePath
#*******************************************************************************************

def LogMap(rootList,fileList, ComponentBase, LogFilePath):

    ################# control paramaters ###################
    printLevel_1 = 0
    printLevel_2 = 0
    ########################################################    
    H_LogIdMap = open(os.path.join(LogFilePath, 'ELogMapId_' + ComponentBase + '.h'),'w+')
    H_LogIdMap.write('\n#define LOGID_MAP(_FILE_ID_,_LOGID_)    (((u32)_FILE_ID_ << 16) | _LOGID_)'+ '\n\n')
    H_LogIdMap.write('%s'% '/* E' + ComponentBase + 'MapID */' + '\n')
    H_LogIdMap.write('\nTypedef enum {'+ '\n\n')    

    ############################# Sub Model ##########################
    # LOGID MAP 
    # Call function "ExtractLog" to extract logs from each file
    # Map each log with one log Id
    ##################################################################  
    FileLogCollect = []
    FileLogNumCollect = []
    LogFileNum = 0
    allFileNum = len(fileList)
    for i in range(0, allFileNum):        
        if printLevel_1:    
            print 'extract log from ' + fileList[i]
        #**************** Function Calling: ExtractLog *****************        
        # calling function ExtractLog to get LogList of each file
        LogList = ExtractLog(os.path.join(rootList[i], fileList[i]))        
        #***************************************************************        
        filelogNum = len(LogList)
        if filelogNum>0:
            FileLogCollect.append(LogList)
            FileLogNumCollect.append(filelogNum)
            LogFileNum += 1
        else:
            fileList[i] = None

    for i in range(0,allFileNum - LogFileNum):
        fileList.remove(None)

    LogNum = 0        
    for i in range(0, LogFileNum):
        filelogNum = FileLogNumCollect[i]
        if filelogNum > 0:            
            fileId = 'E'+ ComponentBase + 'FileId' + '_' + fileList[i][0:-2]
            fileMapId = 'E'+ ComponentBase + 'MapId' + '_' + fileList[i][0:-2]
            if printLevel_2:
                print fileMapId                                       
            H_LogIdMap.write('%s'% '\n    '+ '/* ------ ' + fileMapId + ' --------- */' + '\n')            
            leftBlankLen = 40 - len(fileMapId)-3            
            for j in range(0, filelogNum):                        
                H_LogIdMap.write(('    ' + fileMapId + '_%03d' + ' '*leftBlankLen)% (j))                
                if (i < LogFileNum-1) or (j< filelogNum-1):
                    H_LogIdMap.write((' = LOGID_MAP(' + fileId + ', %d)' +  ',\n')% (LogNum))
                elif (i == LogFileNum-1) and (j == filelogNum-1):
                    H_LogIdMap.write((' = LOGID_MAP(' + fileId + ', %d)' +  '\n')% (LogNum))                    
                LogNum += 1                    
    H_LogIdMap.write('  \n\n/* *******  New log map Id please add from here !!!!******** */\n')
    H_LogIdMap.write('  /* *******  and add the Id number   ******** */\n\n\n')    
    H_LogIdMap.write('}E' + ComponentBase + 'MapID' + ';\n')

    ############################# Sub Model ##########################
    # MAPID PRINT 
    # List Logs in char *MapId...[]
    ##################################################################
    if printLevel_1:    
        print '------- MAPID PRINT .... -------'    
    H_LogIdMap.write('\n\n\n#ifdef _MAPID_PRINT_'+ '\n\n')
    H_LogIdMap.write('char * EMapId_' + ComponentBase + '_PRINT[] = ' + '\n')
    H_LogIdMap.write('{\n')

    LogFileNum = len(fileList)
    LogNum = 0
    for i in range(0, LogFileNum):
        filelogNum = FileLogNumCollect[i]
        if filelogNum > 0:            
            fileMapId = 'E' + ComponentBase + 'MapId' + '_' + fileList[i][0:-2]                                     
            H_LogIdMap.write('\n    /* ----------- '+ fileMapId + ' ------------ */\n\n')            
            for j in range(0, filelogNum):                                
                H_LogIdMap.write(('    /* Log Number:[%d], ' + fileMapId + '_%03d' + ' */\n')% (LogNum, j))                
                if (i < LogFileNum-1) or (j< filelogNum-1):
                    H_LogIdMap.write('    ' + FileLogCollect[i][j] +  ',\n')
                elif (i == LogFileNum-1) and (j == filelogNum-1):
                    H_LogIdMap.write('    ' + FileLogCollect[i][j] +  '\n')
                LogNum += 1
            if printLevel_2:                
                print 'MAPID_PRINT ' + fileMapId 
    H_LogIdMap.write('  \n\n/* *******  New log  please add from here !!!!******** */\n\n\n')    
    H_LogIdMap.write('}\n\n')
    H_LogIdMap.write('#endif\n\n')       
    H_LogIdMap.close()
    return LogNum

#*******************************************************************************************    
# function ExtractLog: can called by function LogMap(): or run alone
#       extract log print from one .c file, and return the log list
# @ input:
#       InputFile: the .c file will be process
#           @example: "...\DSP\SS_Codec\CP_Decoder\Enc_Dch.c"
# @ return:
#       LogList: a list with all logs extracted from the InputFile
#*******************************************************************************************
def ExtractLog(InputFile):

    ######################### control paramaters ########################
    printLevel_1 = 0
    printLevel_2 = 0
    #----------- switchs -------------
    saveDataSwitch = 0            # control if save data to file, "1" save, "0" not save
    annotationFilterSwitch = 0    # control if open annotation filters or not, "1" open, "0" close
                                  # filters are: "#if 0 ... #endif", "/*...*/" and "//"
    ######################################################################                                  
    #---------------------------------    
    SrcFile = open(InputFile,'r')
    
    saveDataFile = InputFile[0:-2]+'.txt'
    if saveDataSwitch:
        DstFile = open(saveDataFile, 'w+')
    if os.path.isfile(saveDataFile):
        os.remove(saveDataFile)
        
    LogList = []
    DataLine = SrcFile.read().splitlines()
    LineNum = len(DataLine)
    keyWord = 'AaSysLogPrint'
    keyWordLen = len(keyWord)
    #--------- AaSysLogPrint and " flag to locate the log -----------   
    if annotationFilterSwitch:       
        #--------- filter flag: #if 0, //,/*...*/ -----------
        if0Flag = 0             #   #if 0 flag
        endifFlag = 0           #   #endif
        slashStarFlag = 0       #   /*  flag
        starSlashFlag = 0       #   */ flag
        doubleSlashFlag = 0     #   //  flag
        
        if0FilteNum = 0
        starFilteNum = 0
        doubleSlashFilteNum = 0
    
    LogPrintFlag = 0        # if 'AaSysLogPrint' exist
    printStrSplitFlag = 0   # sign if one log split into two or more parts
                            # with "\" or "...", "..."       
    logNum = 0              # the number of logs extract from one file
    
    for i in range(0, LineNum):
        ThisLine = DataLine[i].strip()
        # #############################################################
        # This part is in consider of those annotation included by
        # "#if 0 ... #endif", "/*...*/" and "//",
        # those code are invalid, we can set filters to avoid those log.
        # but those annotation may open when needed,
        # so, it's better to keep the logs they covered.
        # we can close those filters by "if 0"
        # #############################################################        
        if annotationFilterSwitch:
            # ------------ set filters of "#if 0 ... #endif", "/*...*/" and "//" ------------                       
            #--------------------------- #if 0  #endif filter -------------------------
            # Note: if there is not only 1 blank between #if and 0,like '#if  0',
            # then we can't use 'if ThisLine.find('#if 0')>=0:' to judge
            # so, we shuld consider the situation of more blanks between '#if' and '0'            
            if ThisLine.find('#if')==0:
                if ThisLine.split()[0].find('#if')== 0 and ThisLine.split()[1].find('0') == 0:
                    if0Flag = if0Flag + 1
                    continue                
            if if0Flag>0:
                #-------------------------------------
                # just to get if0FilteNum, can remove
                if ThisLine.find(keyWord)>=0:
                    if0FilteNum = if0FilteNum +1                    
                    if printLevel_2:
                        print 'filte by #if0 #endif line:',i+1
                #-------------------------------------                    
                if ThisLine.find('#endif')>=0:
                    endifFlag = endifFlag + 1
                if if0Flag == endifFlag:
                    if0Flag = 0
                    endifFlag = 0                    
                continue
            #------------------- /*...*/ filter -------------------
            slashStarLocation = ThisLine.find('/*')            
            if slashStarLocation >= 0:
                if slashStarLocation > 0:
                    ThisLine = ThisLine[0:slashStarLocation]
                    #-------------------------------------
                    # just to get slashFilteNum, can remove
                    if ThisLine.find(keyWord)>=0:
                        starFilteNum = starFilteNum +1
                        if printLevel_2:
                            print 'filte by /* ... */ 1 line ,line:',i+1
                     #-------------------------------------                        
                elif slashStarLocation == 0:
                    slashStarFlag = slashStarFlag + 1
                    ThisLine = ThisLine[2:]                        
            if slashStarFlag>0:
                #-------------------------------------
                # just to get slashFilteNum, can remove
                if ThisLine.find(keyWord)>=0:
                    starFilteNum = starFilteNum +1
                    if printLevel_2:
                        print 'filte by /* .... */ line:',i+1
                #-------------------------------------                        
                if ThisLine.find('*/')>=0:
                    starSlashFlag = starSlashFlag + 1            
                if slashStarFlag == starSlashFlag:
                    slashStarFlag = 0
                    starSlashFlag = 0                    
                continue
            #------------------- // filter -------------------
            doubleSlashLocation = ThisLine.find('//')       
            if doubleSlashLocation >= 0:
                if doubleSlashLocation > 0:
                    ThisLine = ThisLine[0:doubleSlashLocation]
                elif doubleSlashLocation == 0:
                    #-------------------------------------
                    # just to get starFilteNum, can remove
                    if ThisLine.find(keyWord)>=0:
                        doubleSlashFilteNum = doubleSlashFilteNum +1
                        if printLevel_2:
                            print 'filte by // line:',i+1
                    #-------------------------------------   
                    continue                
        # end if annotationFilterSwitch
        # ...close annotation filters of "#if 0 ... #endif","/*...*/" and "//"
                    
        #-------------------------- start find the valid log -----------------------------
        # check if the log exit ...
        # check if the log just at the behind of key word 'AaSysLogPrint',
        # or at the next line        
        if LogPrintFlag == 0:
            keyWordLocation = ThisLine.find(keyWord)
        else:
            keyWordLocation = -1
                    
        if keyWordLocation >= 0 or LogPrintFlag == 1:
            if keyWordLocation == 0:
                LogPrintFlag = 1
                ThisLine = ThisLine[keyWordLen:]
            #-------------- start find '"' ----------------
            quotLocation1 = ThisLine.find('"')            
            if quotLocation1 >=0:                
                logNum = logNum+1
                LogPrintFlag = 0                
                #quotLocation2 = ThisLine[quotLocation1+1:].find('"')
                quotLocation2 = ThisLine[quotLocation1+1:].rfind('"')
                if quotLocation2>=0:                                        
                    Log = ThisLine[quotLocation1 : quotLocation1 + quotLocation2+2]
                    #----- check the situation if one log split into two or more parts with '"..."' 
                    ThisLine = DataLine[i+1].strip()
                    j=1
                    while ThisLine.find('"')==0:
                        printStrSplitFlag = 1
                        #Log = Log[0:-1] + ThisLine[1: ThisLine[1:].find('"')+2]
                        Log = Log[0:-1] + ThisLine[1: ThisLine[1:].rfind('"')+2]                        
                        j=j+1
                        ThisLine = DataLine[i+j].strip()        
                    if printStrSplitFlag == 1:
                        if printLevel_1:
                            print 'Here find: Print string split by two or several pair of "" ,'
                            print ' in file: ' + InputFile +  '\n line number: %d'% i                            
                        printStrSplitFlag = 0                       
                    LogList.append(Log)
                    #LogList.extend([Log])
                else:
                    # ##############################################################
                    # ***** only find one '"',
                    # so the print str must split into two or more parts with "\"
                    # ##############################################################
                    
                    # backSlashLocation = ThisLine[quotLocation1+1:].find('\\')
                    backSlashLocation = ThisLine[quotLocation1+1:].rfind('\\')
                    if backSlashLocation >= 0:
                        Log = ThisLine[quotLocation1: -1]
                        ThisLine = DataLine[i+1].strip()
                        backSlashLocation = ThisLine.find('\\')
                        if printLevel_1:
                            print 'Here find: Print string split by one or several "\\",'
                            print 'in file: '+ InputFile + '\n line number: %d'% i                        
                        j=1
                        while backSlashLocation >=0:                            
                            Log = Log + ThisLine[0:backSlashLocation-1]
                            j=j+1
                            ThisLine = DataLine[i+j].strip()
                            backSlashLocation = ThisLine.find('\\')                            
                        if ThisLine.find('"')>=0:
                            Log = Log + ThisLine[0:ThisLine.find('"')] 
            #else:  #############################################################
                    # if not find '"' in this line, mabe it in the next line,
                    # so the process go to next loop to find '"' directly,
                    # for LogPrintFlag have valued 1 already
                    #############################################################                                    
                if saveDataSwitch:      
                    DstFile.write(str(logNum)+'  '+str(i)+'  ' + Log + '\n')      
    if printLevel_1:
        #print '************************************** '
        print 'processed lines:    ', LineNum
        print 'extract log lines: ', logNum    
    #----------------------------------------------------------  
    if annotationFilterSwitch:        
        if printLevel_2:        
            print 'The log filte by #if 0 number:    ', if0FilteNum
            print 'The log filte by /*...*/ number:    ', starFilteNum
            print 'The log filte by // number:    ', doubleSlashFilteNum
    #-----------------------------------------------------------
    if printLevel_1:            
        print '************************************** '    
    SrcFile.close()
    if saveDataSwitch:
        DstFile.close()
        
    return LogList

#*************************########---  main  ---#######************************
if __name__ == '__main__':
    
    global SearchPath    
    global OutPutPath
   
    if len(sys.argv)>=2 and len(sys.argv)<=3 and sys.argv[1]!= '-help':
        
        if os.path.dirname(sys.argv[0]) != '':
        
            OutPutPath = os.path.dirname(sys.argv[0])
        else:
            OutPutPath = os.getcwd()            
                
        SearchPath = sys.argv[1]       

        # set defult input: 'EComponentId_DSPBase.h'
        ComponentFile = "EComponentId_DSPBase.h" 
        
        if len(sys.argv)==3:        
            ComponentFile = sys.argv[2]        
        
        ComponentFile = os.path.join(OutPutPath, ComponentFile) 
                   
        start = time.clock() 
        
        ComponentMap(ComponentFile)  
        
        duration = time.clock() - start
        print "## Run time duration: %.2f  seconds"% (duration)
        
        exit(0)

    else:
        print '''
   *************************** Usage: ***************************
   FUNCTION:
    - Read component name and corresponding dirs from input file,
    - map all the .c files, extract and Map Log from all .c files,
      save them to .h file located at the root path.
      
    - Out put file 'EFileId_DSPBase.h' located at the root path,
    - 'ELogMapId_***Base.h' files in dir "LogMapHeaderFile"
    
    -input:            
         -[1] source code search path
         -[2] ComponentId define file
             (defult: EComponentId_DSPBase.h)     
       @example: python LogMap.py D:\userdata\shufan\LRC_Trunk\C_Application\SC_UP\DSP
       @example: python LogMap.py D:\userdata\shufan\LRC_Trunk\C_Application\SC_UP\DSP EComponentId_DSPBase.h       
   **************************************************************
        '''
        exit(1)

