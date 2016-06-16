

 RtlMemoryDump.py
 *************************** Usage: ***************************
   [Function:] Auto Memory dump for RunTimeLog
    -input: 
        [1] dump options: 
            0:  Codec & Rake memory
            1:  Codec memory only
            2:  Rake memory only
            dump_addr:  self defined dump address
        [2] dump length 
    Note:  defult option is Codec memory 
   @example:
        RtlMemoryDump.py
		RtlMemoryDump.py 0
		RtlMemoryDump.py 1
		RtlMemoryDump.py 2
        RtlMemoryDump.py 0x78000000 0x2000000       
   - output:
        - Out put Location: the dumped .bin files in "D:\memoryDump"
*****************************************************************

   [configurations:]
	(1) configuration in GlobDef.py:
		- Set k2_ip and Remote_ip( the ip of test PC) like:
			K2_ip          = '192.168.253.106' 
			Remote_ip      = '192.168.100.126'
		- k2IpMap
			K2IpMap = {
				'192.168.253.106' :   'K2_a',
				'192.168.253.107' :   'K2_b',
				'192.168.253.108' :   'K2_c'
				}
		- Set socketTcpPort [For codec memory dump only:]
			choose the valid socket port in your test PC
			@example:	socketTcpPort = 15004
	[For codec memory dump only:]
    (2) Set Parameters in 'RtlFreezeReqConfig.xls' to choose which kind of logs to be token
	---------------------------------------------------  
