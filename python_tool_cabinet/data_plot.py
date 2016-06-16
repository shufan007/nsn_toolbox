# -*- coding: utf-8 -*-

import xlrd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from math import *


class CDraw(object):
    
    def __init__(self, filename, casename): 
        
        self.colorsList = 'rgbyckm'
        self.linesList = ['--','-o','-*', '-+', '-^']  
          
        file = xlrd.open_workbook(filename)
        self.data=file.sheet_by_name(casename)  
        
        self.x = None
        self.yData = []
        self.version = []
        
        self.get_data_from_file()
        self.draw_x_y()
        
    def get_data_from_file(self):
        dataStart_index = 1    
        nrows = data.nrows-dataStart_index
        ncols = data.ncols
        
        if nrows > 30:
            nrows = 30
            
        self.x = range(0, nrows)
            
        for j in range(0, ncols):
            y_j = []           
            for i in range(0, nrows):
                cell_data = self.data.cell_value(i+dataStart_index,j)
                y_j.append(cell_data) 
            self.yData.append(y_j) 
              
               
        for k in range(dataStart_index, nrows+dataStart_index):
            ver = self.data.cell_value(k, 24)
            self.version.append(ver)
            
    
    def draw_x_y(self):           
        
        plt.figure(figsize=(15,10))
        ax = plt.subplot(1,1,1)
        lines = []
            
        for j in range(0, len(yData)):           
            for i in range(0, len(x)):                
                ax.text(x[i]+0.1, yData[j][i]+0.1, str(yData[j][i]))
                
            line_style = self.colorsList[j%len(self.colorsList)] + self.linesList[j%len(self.linesList)]
            lines.append(line_style)
            ax_j = plt.plot(x, yData[j], line_style,label = "core "+str(j))
    
    
            handles, labels = ax.get_legend_handles_labels()          
    
        ax.legend(handles, labels)
        plt.axis([0, len(x), 0, 100])
        plt.xticks(x, self.version)
    
        for label in ax.xaxis.get_ticklabels():
            label.set_rotation(60)
            
        plt.grid(True)    
    
        plt.xlabel("Version")
        plt.ylabel("cpuload_avg")
        plt.title("cpuload_result")
        plt.show()
        plt.savefig("D:\cpuload_result.png")

    

if __name__== "__main__":

    filename = sys.argv[1]
    casename = sys.argv[2]
    
    CDraw(filename,casename)
    

    

    
    
