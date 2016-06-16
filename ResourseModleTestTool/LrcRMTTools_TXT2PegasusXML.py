'''***************************************************************************
Created on 2012-1-29

FileName: csv2xml.py

@author: zecai

********************************************************************************
 Description:    

        Convert a csv file to some xml files like RMT_Parameters_Interface_**UE.xml.
        For example:
        4 users that includes all combinations generate a file called RMT_Parameters_Interface_4UE.xml.

********************************************************************************
 Steps:
        1. RMT_Parameters_Interface_Model.xml and csv2xml.py are in the same folder.
        2. Input LOWER_USER_NUM, UPPER_USER_NUM and MAX_USER_NUM that you need.
    
********************************************************************************
 Revision History:
        (Cai Zegao - 03/27/2012)  Optimize function setParameters()
        (Cai Zegao - 03/28/2012)  Update: create some xml files that you need every time 
        (Fan Shaungxi - 03/12/2015) Do some changes: make it adpate to LRC project
        (Fan Shaungxi - 04/22/2015) Add the 'Mark' parameter; 
                                   Keep the total user number always the given number.
        (Fan Shaungxi - 05/20/2015) add GetDataFromTxt
*****************************************************************************'''

import xml.dom.minidom
import codecs, sys, time, logging, os
from genericpath import exists
from xml.etree import ElementTree
# ################################################################################
CombinStartMark = "=>"

MODEL_FILE_NAME = 'RMT_Parameters_Interface_Model.xml'
#LOWER_USER_NUM <= UPPER_USER_NUM <= MAX_USER_NUM
LOWER_USER_NUM = 3
UPPER_USER_NUM = 80
#MAX_USER_NUM = 80

def debugLogSetup(log_name):
    global debug_log
    os.chdir(sys.path[0])
    logging.basicConfig(filename = os.path.join(os.getcwd(), log_name),
                         level = logging.WARN, 
                         filemode = 'a', 
                         format =  '%(asctime)s - %(levelname)s: %(message)s',
                         datefmt = '%Y-%m-%d %H:%M') 
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)  
    
    debug_log = logging.getLogger() 
    debug_log.setLevel(logging.DEBUG)
    debug_log.info('----------- TXT to pegasus XML, Debug Info start-------------\n')
    return debug_log

def debugLogPrint(stream):
    debug_log.info(str(stream) + '\n')
    #print str(stream) + '\n'
    
def getFilePath(csv_file_path, result_file_name):
    list_csv_path = csv_file_path.split('/')
    del list_csv_path[-1]
    list_csv_path.append(result_file_name)
    result_file_path = ('/').join(list_csv_path)
    
    return result_file_path


def GetDataFromTxt(FileName):    
    print ' * Get Data From Txt File.'
    
    dynamicFile = open(FileName,'r')
    file_original = dynamicFile.read()
    dynamicFile.close()
    str_unit = file_original.splitlines()  
        
    SF = []
    TbSize = []
    Harq = []
    TTi = []
      
    for i in range(0, len(str_unit)):  # i is line number
       
        if str_unit[i].find(CombinStartMark) >= 0:
            userIndx = str_unit[i].find(CombinStartMark)+ len(CombinStartMark)
            UserInfo = str_unit[i][userIndx:].split(';')
            
            SF_value = []
            TbSize_value = []
            HarqParam = []
            eTTi = []
            
            for j in range(0, len(UserInfo)-1, 3):  # j is the cloumn number 
                eTTi.append(UserInfo[j].strip())             
                SF_value.append(UserInfo[j+1].strip()) 
                TbSize_value.append(UserInfo[j+2].strip()) 
                HarqParam.append('1')
                
            SF.append(SF_value)
            TbSize.append(TbSize_value)
            TTi.append(eTTi)
            Harq.append(HarqParam)
            
    return (SF, TbSize, TTi, Harq)


def setParameters(root, node_name, node_value, combination_index, user_index, para_index, user_number):
    '''
    This function set RMT_Parameters_Interface_**UE.xml parameter.
        
    @param root: instance, element of document root 
    @param node_name: string, node name of document 
    @param node_value: int, node value of document
    @param combination_index: int, combination index of current users
           (3users: from 0 to max combination number - 1; 5users: form 0 to max combination number - 1 )
    @param user_index: int, user index of current users
           (3users index: 0, 1, 2; 5users index: 0, 1, 2, 3, 4)
    @param para_index: int, parameter index
           (such as: SetOfEdpdchs-0, TBSize-1, Tti-2, HarqParam-3)
    @param user_number: current user number(such as: 3, 4, 5...)
        
    @return: root 
    '''
    
    node_list_combination = root.findall('properties')
    node_list_user = node_list_combination[combination_index].findall('properties')
    node_list_para = node_list_user[user_index].findall('property')
    node_list_para[para_index].getchildren()[1].text = node_value

    #print user_number,
    return root
   
def setParameterValue(root, node_name, node_value):
    node_list = root.getElementsByTagName('property')
    for node in node_list:
        if node.getElementsByTagName('name')[0].childNodes[0].nodeValue == node_name:
            node.getElementsByTagName('value')[0].childNodes[0].nodeValue = node_value
            return root

def setParameterName(root, fault_node_name, new_node_name):
    node_list = root.getElementsByTagName('property')
    for node in node_list:
        if node.getElementsByTagName('name')[0].childNodes[0].nodeValue == fault_node_name:
            node.getElementsByTagName('name')[0].childNodes[0].nodeValue = new_node_name
            return root

def getParameter(root, node_name):
    node_list = root.getElementsByTagName('property')
    for node in node_list:
        if node.getElementsByTagName('name')[0].childNodes[0].nodeValue == node_name:
            node_value = node.getElementsByTagName('value')[0].childNodes[0].nodeValue
            
    try:
        return node_value
    except UnboundLocalError, e:
        debugLogPrint('*** Can not get node value: %s' %e)
        sys.exit(0)

def copyXMLFile(out_file_name, in_file_name):
    
    if not exists(in_file_name):
        debugLogPrint(' %s is not exist' %in_file_name)
        sys.exit(0)
        
    in_file = open(in_file_name, 'r')
    in_file_original = in_file.read()
    in_file.close()
        
    out_file = open(out_file_name, 'w')
    out_file.write(in_file_original)
    out_file.close()
    
def writeToXMLFile(dom, file_name):
    xml_file = open(file_name, 'w')
    writer = codecs.lookup('utf-8')[3](xml_file)
    dom.writexml(writer, encoding = 'utf-8')
    xml_file.close()
    
def generateReslutFile(root, file_name):
    result_file_test = open(file_name, 'w')
    result_file_test.write('<?xml version="1.0" encoding="utf-8"?>\n')
    ElementTree.ElementTree(root).write(result_file_test)
    result_file_test.close()
    
def addCombinationNode(dom, root, combination_number, user_number):
    global MARK
    
    node_list = root.getElementsByTagName('properties')
    
    #rename first combination name
    node_list[0].setAttribute('name', MARK +'Combination1_'+str(user_number)+'UE')
    
    
    for i in range(0, combination_number-1):
        #add a blank line
        node_enter = dom.createTextNode('\n')
        root.appendChild(node_enter)
        
        #add a tab
        node_one_tab = dom.createTextNode('    ')
        root.appendChild(node_one_tab)
        
        #add a combination node
        node_new = node_list[0].cloneNode(True)
        node_new.setAttribute('name', node_new.getAttribute('name')[0: 11+len(MARK)]+str(i+2)+'_'+str(user_number)+'UE')
        root.appendChild(node_new)
        
        #add a blank line
        node_enter = dom.createTextNode('\n')
        root.appendChild(node_enter)
        
        #add a tab
        node_one_tab = dom.createTextNode('    ')
        root.appendChild(node_one_tab)
        
    return root

def addUserNode(dom, root, user_number):
    global MAX_USER_NUM
    # shufan: initialized with the MAX_USER_NUM
    if MAX_USER_NUM != None:        
        user_number = MAX_USER_NUM
    
    node_list = root.getElementsByTagName('properties')[0].getElementsByTagName('properties')
    
    #add user node
    for i in range(0, user_number-1):
        #add a blank line
        node_enter = dom.createTextNode('\n')
        root.getElementsByTagName('properties')[0].appendChild(node_enter)
        
        #add two tab
        node_two_tab = dom.createTextNode('        ')
        root.getElementsByTagName('properties')[0].appendChild(node_two_tab)
        
        #add a user node
        node_new = node_list[0].cloneNode(True)
        node_new.setAttribute('name', node_new.getAttribute('name')[0:4]+str(i+2)) 
        root.getElementsByTagName('properties')[0].appendChild(node_new)
        
        #add a blank line
        node_enter = dom.createTextNode('\n')
        root.getElementsByTagName('properties')[0].appendChild(node_enter)
        
        #add a tab
        node_four_space = dom.createTextNode('    ')
        root.getElementsByTagName('properties')[0].appendChild(node_four_space)
            
    return root

def getLogFileNamesGui():
    import Tkinter, tkFileDialog
    ftypes = [("Log files", ".csv"), ("All files", ".*")]
    master = Tkinter.Tk()
    master.withdraw() #hiding tkinter window
    return tkFileDialog.askopenfilenames(title="Choose Test Set file", filetypes=ftypes)


def mainFlow(file_path):
    global MARK
        
    #internal_start_time is every user_number's start time
    internal_start_time = time.time()
    
    (SF, TbSize, TTi, Harq) = GetDataFromTxt(file_path)
    
    combination_number = len(SF)
    user_number = len(SF[0])  
        
    debugLogPrint(' - Starting... user_number: %s' %user_number)

    #copy and create a xml file
    result_file_name = MARK + MODEL_FILE_NAME[0:25] + str(user_number) + 'UE' +  MODEL_FILE_NAME[-4:]
    #result_file_name = result_file_name +'_' + csv_file_name[:-4] +  MODEL_FILE_NAME[-4:]
    result_file = getFilePath(file_path, result_file_name)
    result_file_temp = getFilePath(file_path, MODEL_FILE_NAME[0:25] + 'temp' +  MODEL_FILE_NAME[-4:])
    copyXMLFile(result_file_temp, MODEL_FILE_NAME)
    
    #parse new xml file
    if not exists(result_file_temp):
        debugLogPrint('%s is not exist' %result_file_temp)
        sys.exit(0)

    dom = xml.dom.minidom.parse(result_file_temp)
    root = dom.documentElement
    
    #set combination number name
    setParameterName(root, 'CombinationNum_1UE', MARK +'CombinationNum_' + str(user_number) + 'UE')
    
    # '>>>add user node.'
    root = addUserNode(dom, root, user_number)

    # add combination node
    root = addCombinationNode(dom, root, combination_number, user_number)
    
    #set combination number
    root = setParameterValue(root, MARK + 'CombinationNum_' + str(user_number) + 'UE', str(combination_number))   
    
    #write to temp xml file
    writeToXMLFile(dom, result_file_temp)
    
    '''****************************ElementTree*************************************'''
    element_root = ElementTree.parse(result_file_temp).getroot()
    
    #set xml file parameters      
    for combination_index in range(0, combination_number):
        for index in range(0, user_number):
            setParameters(element_root, 'SetOfEdpdchs', table_SetOfEdpdchs_Enum_Pegasus[int(SF[combination_index][index])], combination_index, index, 0, user_number)
                    
            setParameters(element_root, 'TBSize', TbSize[combination_index][index], combination_index, index, 1, user_number)

            setParameters(element_root, 'Tti', TTi[combination_index][index], combination_index, index, 2, user_number)

            #full Harq is 0xFF(255), one Harq is 1
            if Harq[combination_index][index] == '0':
                setParameters(element_root, 'HarqParam', '255', combination_index, index, 3, user_number)
            elif Harq[combination_index][index] == '1':
                setParameters(element_root, 'HarqParam', '1', combination_index, index, 3, user_number)  
        
    #generate  result file
    generateReslutFile(element_root, result_file)
    
    debugLogPrint(' - End user_number: %2d,  combination_number: %3d,  time: %.2f' %(user_number, combination_number, time.time() - internal_start_time))

if __name__ == '__main__':
    
    table_SetOfEdpdchs_Enum_Pegasus = [
        'ESetOfEDpdchs_Ver2_None',      #0  None <---> ccrs in LRC 
        'ESetOfEDpdchs_Ver2_SF32',      #1
        'ESetOfEDpdchs_Ver2_SF16',      #2
        'ESetOfEDpdchs_Ver2_SF8',       #3
        'ESetOfEDpdchs_Ver2_SF4',       #4
        'ESetOfEDpdchs_Ver2_2SF4',      #5
        'ESetOfEDpdchs_Ver2_2SF2',      #6
        'ESetOfEDpdchs_Ver2_2SF4_2SF2'  #7
        ]   
    
    if len(sys.argv) >= 2 and len(sys.argv) <= 4:
        
        global file_name
        global MARK 
        global MAX_USER_NUM
        #get txt file
        #txt_file_path = getLogFileNamesGui()       
        file_path = sys.argv[1] 
        file_name = os.path.basename(file_path)  
                  
        if len(sys.argv) == 2 or (len(sys.argv) == 3 and sys.argv[2] == '-'):
            MARK = ''            
        else:
            MARK = sys.argv[2] + '_' 
                           
        MAX_USER_NUM = None
        if len(sys.argv) == 4:
            MAX_USER_NUM = int(sys.argv[3])
                       
        #start debug function
        debug_file_path = getFilePath(file_path, 'debug.txt')
        debugLogSetup(debug_file_path)
        
        debugLogPrint('* TXT to pegasus XML start')
        start_time = time.time()       
    
        flag = mainFlow(file_path)
    
        debugLogPrint('* Done! Take time: %.2f' %(time.time() - start_time))
    else:
        print '''       
    *************************** Usage: ***************************
    [Function:] Convert CSV to Pegasus XML
    -Input:	
        -[1] FileName:  Name of txt file
        -[2] MARK: Additional Mark for property indentification, 
                (not set or use '-': to ignore this parameter) 
        -[3] MAX_USER_NUM:  Max user number (User_num <= MAX_USER_NUM <= 80)
                (defalut is: MAX_USER_NUM = User_num)
        
    @Example: LrcRMTTools_CSV2PegasusXML.py Top60_10xHSUPA10msTti.txt
    @Example: LrcRMTTools_CSV2PegasusXML.py Top60_10xHSUPA10msTti.txt TC9015
    @Example: LrcRMTTools_CSV2PegasusXML.py Top60_10xHSUPA10msTti.txt TC9015 80
    @Example: LrcRMTTools_CSV2PegasusXML.py Top60_10xHSUPA10msTti.txt - 80
    
    -Output: Pegasus XML file
              
    ************************************************************** 
        '''
        
