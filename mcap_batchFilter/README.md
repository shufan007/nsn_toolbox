#======================================================================================
#       Function:       mcap file batch filter
#       Author:         Fan, Shuangxi (NSN - CN/Hangzhou)
#       Date:           2016-04-05
#*  *   description:    This script can filter mcap file in batch
#======================================================================================

 [Environment Set]
---------------------------------------------------------------------------------------
 Before using this tool, please make sure those software ready on your PC,
 and the version should not less than the version being given.
	1) python       2.7.2 
	2) wireshark    1.10.3
	3) winPcap      4.1.3
	3) MMT tool  17.60.04.02	
	4) Set environment variable of "MMT tool" when first use in one computer
		 @Example: if the path of "MMT tool" is "C:\BS3201_Tools\MMT", 
		 set it like this:
		 computer -> properties -> Advanced system settings -> Environment Variables
		 add  C:\BS3201_Tools\MMT to 'Path'	and remove other wareshark path
---------------------------------------------------------------------------------------

 [Initiation]
---------------------------------------------------------------------------------------
	Set the filter rules here (Note: keep the filter string in one line, no line break in it):
	####################################################################################################
	Filter_Rule ==>  (((sicap.header.Sender >= 0x14310000 && sicap.header.Sender <= 0x143dffff)) && (sicap.50aa || sicap.50ab))
	
	 ((sicap.header.Receiver == 0x12310250 && (sicap.1e0d.ReportName == 0x000007d9 || sicap.1e0e.ReportName == 0x000007d9)) || (sicap.header.Sender == 0x12310227 && (sicap.1e13.ReportName == 0x000007d9 || sicap.1e14.ReportName == 0x000007d9)))
	
	(((sicap.header.Sender >= 0x131d0000 && sicap.header.Sender <= 0x131dffff) || (sicap.header.Receiver >= 0x133d0000 && sicap.header.Receiver <= 0x133dffff)) && (sicap.5173 || sicap.5176 || sicap.5179 || sicap.518a || sicap.5190) || sicap.5192|| sicap.50f1)
	
	####################################################################################################
	
	Filter rule @Examples: 
	
	((sicap.header.Sender >= 0x12510000 && sicap.header.Sender <= 0x1251ffff) || (sicap.header.Receiver >= 0x12510000 && sicap.header.Receiver <= 0x1251ffff))

	(((sicap.header.Sender >= 0x12510000 && sicap.header.Sender <= 0x1251ffff) || (sicap.header.Receiver >= 0x12510000 && sicap.header.Receiver <= 0x1251ffff)) && (sicap.5173 || sicap.5176 || sicap.5179 || sicap.517e || sicap.5185 || sicap.5188 || sicap.518a || sicap.518c || sicap.518e || sicap.51a2 || sicap.5190 || sicap.5191 || sicap.5192))

	
 [Run]	
----------------------------------------------------------------------
        -input: 
             -[1] packet file or packet file dir:
       @example:
               python McapBatchFilter.py packetFile.mcap
               python McapBatchFilter.py packetFileDir
       - output:
         in dir " ***_extractedData "
   --------------------------------------------------------------------
   