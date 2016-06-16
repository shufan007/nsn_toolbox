#======================================================================================
#       Function:       pcap file capture and decode, API message parse, result check
#       Author:         Fan, Shuangxi (NSN - CN/Hangzhou)
#       Date:           2014-09-15
#*  *   description:    This script can capture and Decode Pcap file; 
#						Extract and parse message Data from pcap file, save parsed data to .xls file;
#                       Check the parsed data.
#======================================================================================

*************************** Notice ***************************
 Before using this tool, please make sure those software ready on your PC,
 and the version should not less than the version being given.
 
	1) python       2.7.2 
		If your python version less than 2.7.2, your should also install those 2 modules 'xlrd' and 'xlwt',
		you can download them from the net, or use the one being given(location: 'PcapPacketDecoder\python_modules\'),
		- @example: install 'xlrd', and its path is: "C:\Pegasus\workspaceWCDMA_SCT\SCTNyquist\Tools\API_CI\Common\PcapPacketDecoder\python_modules\xlrd-0.9.3"		
		  then cd to this path or use the full path, run: python setup.py install
	2) wireshark    1.10.3
	3) winPcap      4.1.3
**************************************************************

1. initiation:
	1) 	 Set environment variable of "tshark" when first use in one computer
		 @Example: if the path of 'tshark.exe' is "C:\apps\wireshark", 
		 we can set environment variable via
		 computer -> properties -> Advanced system settings -> Environment Variables
		 add  C:\apps\wireshark to 'Path'

	2)	set wireshark packet filter conditions in "wireshark_paras.xls",
		for it can filter the raw cap file to some specified files.

2. 	run "PacketDecoder.py" to decode the .pcap file.
	the usage of "PacketDecoder.py" as follows:
   ------------------------- Usage ----------------------------
        -input:		
             -[1] network_port:
				- if you don't know which port is the right one, 
				  use command "tshark -D" to view all the port,				 
             -[2] capture_time:
                  [defult:] not capture
       @example:
               python PacketDecoder.py 2       
               python PacketDecoder.py 2 100
       - output:
         in dir " API_Data ":
           -  " msgID.pcap "
           -  " msgID_decode.txt "           
           -  " result.xls "   
   -------------------------------------------------------------
   
3. 	run "ResultAnalysis.py" to check the parsed data.
	the usage of "ResultAnalysis.py" as follows:   
   ------------------------- Usage ----------------------------
        -input:
             -[1] msgID	
             -[2] checkOnPerReportSwitch
             -[3] FieldName1	
             -[4] valueMin1             
             -[5] valueMax1	
             -[6] FieldName2 (optional)	
             -[7] valueMin2  (optional)
             -[8] valueMax2	 (optional)			 
              ...                 
       @example:
               python ResultAnalysis.py 517b True numCrcOk 1 2
   ------------------------------------------------------------- 
   
   
[TODO]
1. 
	1) complete Msg Parse
	2) add one more access feature: 
	   double click to execute for identify .bin file in the same path;
	   save runtime info and exception log to file.
	3) close to save unpacked data
	4) add log level
	5) add enum to Tti Trace 
2. learn socket, complete mumdump, (for I&V not use pegasus send msg)
3. Innovation apply: packetDecoder tool, API measurement
4. sync python code to cloud server