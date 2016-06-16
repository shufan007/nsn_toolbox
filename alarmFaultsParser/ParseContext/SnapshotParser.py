# -*- coding: utf-8 -*-
# ##############################################################################
# class Snapshot():
# [Function]:  class for snapshot bin preprocess
#       Author:         Fan, Shuangxi (NSN - CN/Hangzhou)
#       date:  2015-11-20
#*      description:    
# ##############################################################################
#!/usr/bin/python

import os

from CBinDataConvert import *
         
# ##############################################################################
# [Function]:  class for snapshot bin preprocess
# - get_dumpblocks 
# [Methods]:
#      get_dumpblocks      
# ##############################################################################                
class Snapshot():
    
    def __init__(self, SnapShotFile):  
        self.SnapShotFile = SnapShotFile  

    def get_dumpblocks(self):   
        binData_obj = CBinDataConvert()    
        start_addr  = 0
        length      = 'To_End'
        endian_flag = '0'

        (hex_data, actual_length) = binData_obj.Bin_to_Hex(self.SnapShotFile,\
                                    start_addr,\
                                    length,\
                                    endian_flag)             
        
        return hex_data   



  
        

