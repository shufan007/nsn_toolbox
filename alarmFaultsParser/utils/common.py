# -*- coding: utf-8 -*-
# ##############################################################################
#       Function:       Spalit and parse snapshot buffer
#       Author:         Fan, Shuangxi (NSN - CN/Hangzhou)
#       draft:          2014-10-14 
#       modify(split):  2015-11-20
#*      description:    split snapshot buffer by dump ID, parse each dump block
#           - InputFile:    get snapshot buffer (bin data or hex data)from this file
#           - DstFile:      save parsed info to some files 
# ##############################################################################
#!/usr/bin/python

import os, sys
import logging
import threading
import Tkinter, tkFileDialog

'''
# ##############################################################################
TODO:

# ##############################################################################
'''
 

class CThread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func =func
        self.args = args
        
    def run(self):
        apply(self.func, self.args)
        
        
#--------------------------------------------------------------
def debugLogSetup(LogFileName):
    logging.basicConfig(filename = LogFileName,
                        level = logging.WARN, 
                        filemode = 'w', 
                        format =  '%(asctime)s - %(levelname)s: [line:%(lineno)d]: %(message)s',
                        datefmt = '%Y-%m-%d %H:%M:%S')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)   
    __DEBUG__ = logging.getLogger()
    __DEBUG__.setLevel(logging.DEBUG)
    
    return __DEBUG__
#-------------------------------------------------------------------------
  
        
def getInputFileNamesGui():
    ftypes = [("All files", ".bin")]
    master = Tkinter.Tk()
    master.withdraw() # hiding tkinter window
    InputFile = tkFileDialog.askopenfilenames(title="Choose input .bin file", filetypes=ftypes)
    
    return InputFile    


# map: keys-> values
# creat a dictionary
def creat_dictionary(keys, values):
    Out_Dic = dict.fromkeys(keys, None)
    
    dic_size = min(len(keys), len(values))
    for i in range(0, dic_size):
        Out_Dic[keys[i]] = values[i]
    return Out_Dic

       