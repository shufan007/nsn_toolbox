#================================================================================
#   # global variables defination:
#*  define global variabes, protocol name,
#   message struct and the mapped message id
#================================================================================
import os

###################################################################   
#*  global variables defination
###################################################################

raw_pcap_file        = 'raw_data.pcap'
wireshark_paras_file = "wireshark_paras.xls"
API_Data_dir         = "API_Data"
SavedData_dir        = "SavedData"
result_file          = "result.xls"
pcap_filte_wait_time = 3


###################################################################   
#*  global variables defination for pcap decode
###################################################################

pcap_header_len     = 24 # unit: byte
Ethernet_header_len = 14 
Vlan_header_len     = 4   
Ip_header_len       = 20
Udp_header_len      = 8
#-------------------------------------------
# dic Ethernet Type
EtherType = {'0x0600':'XEROX NS IDP',
    '0x0660':'DLOG',
    '0x0661':'DLOG',
    '0x0800':'IP',
    '0x0801':'X.75',
    '0x0802':'NBS',
    '0x0803':'ECMA',
    '0x0804':'Chaosnet',
    '0x0805':'X.25',
    '0x0806':'ARP',
    '0x0808':'Frame Relay ARP',
    '0x6559':'Raw Frame Relay',
    '0x8035':'RARP',
    '0x8037':'Novell Netware IPX',
    '0x809B':'Ether Talk',
    '0x80d5':'IBM SNA Service over Ethernet',
    '0x80f3':'AARP',
    '0x8100':'802.1Q',
    '0x8137':'IPX',
    '0x814c':'SNMP',
    '0x86dd':'IPv6',
    '0x880b':'PPP',
    '0x880c':'GSMP'
    }

# dic
ProtocolType = {'0x01':'ICMP',
    '0x02':'IGMP',
    '0x04':'IPv4',
    '0x06':'TCP',
    '0x11':'UDP'
    }


###################################################################
#   Message Struct Define:
#*  define the message struct and the mapped message id
###################################################################
# The first value of the tuple is the dynamic indiation info
# each stands for: (dynamic num index, dynamic part single length)
# if not dynamic, this triple set to (0,0)

# Messageheader stuple
TMessageheader = (
     ('id',             4),
     ('rec_board',      1),
     ('rec_cpu',        1),
     ('rec_task',       2),
     ('send_board',     1),
     ('send_cpu',       1),
     ('send_task',      2),
     ('length',         2),
     ('system',         1),
     ('user',           1)
         
    )

msg_header_len = 10

# ########################################################
# Message struct Tuble,
# and the dynamic indiation info add to the first line

# 5173: 'BTSMeasurementStartReq'
T5173_Items = ((0, 0), 
     TMessageheader,               
     (('transactionId', 4),
     ('status',         4),
     ('measurementId',  4),
     ('cellId',         4),
     ('measureType',    4),               
     ('sfn',            4))
    )


# 5174: 'MultipathCountReport'
T5174_Items = ((0, 0), 
     TMessageheader,               
     (('measureId',     4),
     ('sfn',            4),               
     ('num0Path',       4),
     ('num1Path',       4),
     ('num2Path',       4),
     ('num3Path',       4),
     ('num4Path',       4),
     ('num5Path',       4),
     ('num6Path',       4),
     ('num7Path',       4),
     ('num8Path',       4),
     ('num9Path',       4),
     ('num10Path',       4),
     ('num11Path',       4),
     ('num12Path',       4),
     ('num13Path',       4),
     ('num14Path',       4),
     ('num15Path',       4),      
     ('num16Path',       4))
    )

# 5175: 'PathDelayDifferenceReport'
T5175_Items = ((0, 0), 
     TMessageheader,               
     (('measureId',      4),
     ('sfn',             4),               
     ('pathDelayDiff',   4))
    )


# 5176: 'CellMeasurementStartReq'
T5176_Items = ((0, 0), 
     TMessageheader,               
     (('transactionId', 4),
     ('status',         4),
     ('measurementId',  4),
     ('cellId',         4), 
     ('measureType',    4))
    )


# 5177: 'InterferenceWaveLevelReport'
T5177_Items = ((0, 0), 
     TMessageheader,               
     (('measurementId',     4),
     ('sfn',                4), 
     ('rssiStatusBranch0',  4),
     ('waveLevelBranch0',   4),
     ('rssiStatusBranch01', 4),
     ('waveLevelBranch1',   4))
    )


# 5178: 'TotalPowerCountReport'
T5178_Items = ((0, 0), 
     TMessageheader,               
     (('measurementId',     4),
     ('sfn',                4),
     ('totalTpSeries0',     4),
     ('totalTpSeries1',     4), 
     ('hsdpaTpSeries0',     4),
     ('hsdpaTpSeries1',     4),
     ('nonHsdpaTpSeries0',  4),
     ('nonHsdpaTpSeries1',  4),      
     ('hspdschTp',          4))
    )

# 5179: 'CCHMeasurementStartReq'
T5179_Items = ((0, 0), 
     TMessageheader,               
     (('transactionId', 4),
     ('status',         4),
     ('measurementId',  4),
     ('cellId',         4),      
     ('pyChId',         4), 
     ('measureType',    4))
    )

# 517b: 'PrachUsageStatusReport'
T517b_Items = ((0, 0), 
     TMessageheader,               
     (('sfn',           4),
     ('numPrachMeasure',4),
     ('measureId0',      4),
     ('numCrcOk',       4),      
     ('numCrcNg',       4), 
     ('numDiscard',     4),
     ('measureId1',      4),
     ('numCrcOk',       4),      
     ('numCrcNg',       4), 
     ('numDiscard',     4))
    )

# 517c: 'PreambleMeasurementReport'
T517c_Items = ((0, 0), 
     TMessageheader,
     (('sfn',            4),
     ('numPreambleMeasure', 4),
     ('measureId',      4),
     ('numRxPreamble',  4),
     ('numTxAck',       4),
     ('numTxNack',      4),
     ('measureId',      4),
     ('numRxPreamble',  4),
     ('numTxAck',       4),
     ('numTxNack',      4))
    )


# 517d: 'RachBLERMeasurementReport'
T517d_Items = ((0, 0), 
     TMessageheader,
     (('sfn',               4),
     ('numRachBlerMeasure', 4),
     ('measureId',          4),
     ('numMeasuredTb',      4),
     ('numCrcNgTb',         4),
     ('measureId',          4),
     ('numMeasuredTb',      4),
     ('numCrcNgTb',         4))
    )


# 517e: 'DCHMeasurementStartReq'
T517e_Items = ((0, 0), 
     TMessageheader,
     (('transactionId', 4),
     ('status',         4),
     ('measurementId',  4),
     ('cellId',         4),      
     ('userId',         4),
     ('measureType',    4),
     ('chId',           4),      
     ('pnTiers',        4))
    )


# 517f: 'BLERMeasurementReport'
T517f_Items = ((msg_header_len + 2, 4),
     TMessageheader,
     (('sfn',            4),
     ('numDchBlerMeasure', 4),
     ('measureId',      4),
     ('uuSyncStatus',   4),
     ('numMeasuredTb',  4),
     ('numCrcNgTb',     4))
    )


# 5180: 'BERMeasurementReport'
T5180_Items = ((msg_header_len + 2, 5),
     TMessageheader,               
     (('sfn',            4),
     ('numDchBerMeasure', 4),
     ('measureId',      4),
     ('uuSyncStatus',   4),
     ('pnSyncStatus',   4),
     ('measuredBits',   4),
     ('ngBits',         4))
    )


# 5181: 'EstimatedBERMeasurementReport'
T5181_Items = ((msg_header_len + 2, 4),
     TMessageheader,               
     (('sfn',            4),
     ('numEstBerMeasure', 4),
     ('measureId',      4),
     ('uuSyncStatus',   4),
     ('measuredBits',   4),
     ('ngBits',         4))
    )

# 5182: 'ReceptionLevelMeasurementReport'
T5182_Items = ((msg_header_len + 2, 5),
     TMessageheader,               
     (('sfn',            4),
     ('numReceptionlevelMeasure', 4),
     ('measureId',      4),
     ('SyncStatus',     4),
     ('rscp',           4),
     ('iscp',           4),
     ('rxSir',          4))               
    )

# 5183: 'RTTMeasurementReport'
T5183_Items = ((msg_header_len + 2, 2),
     TMessageheader,               
     (('sfn',            4),
     ('numRttMeasure',     4),
     ('cellId',         4),
     ('rtt',            4))              
    )

# 5184: 'TxPowerMeasurementReport'
T5184_Items = ((msg_header_len + 2, 6),
     TMessageheader,               
     (('sfn',           4),
     ('numTxPowerMeasure',  4),
     ('measureId',      4),
     ('status',         4),
     ('pilotAvgTxPower',4),
     ('dpdchAvgTxPower',4),
     ('pilotMaxTxPower',4),
     ('pilotMinTxPower',4))              
    )


# 51a1: 'ReceivedTotalWideBandPowerReport'
T51a1_Items = ((0, 0), 
     TMessageheader,               
     (('measurementId',     4),
     ('sfnReport',          4), 
     ('rssiStatusBranch0',  4),
     ('rtwpBranch0',        4),
     ('rssiStatusBranch1',  4),
     ('rtwpBranch1',        4),
     ('nonServingEdchPower', 4),
     ('totalEdchPower',     4))
    )

# ########################################################
# dic: messageId message struct
# ########################################################
MessageId = {'5173':(T5173_Items,'BTSMeasurementStartReq'),
             '5174':(T5174_Items,'MultipathCountReport'),                          
             '5175':(T5175_Items,'PathDelayDifferenceReport'),             
             '5176':(T5176_Items,'CellMeasurementStartReq'),             
             '5177':(T5177_Items,'InterferenceWaveLevelReport'),             
             '5178':(T5178_Items,'TotalPowerCountReport'),
             '5179':(T5179_Items,'CCHMeasurementStartReq'),
             '517b':(T517b_Items,'PrachUsageStatusReport'),
             '517c':(T517c_Items,'PreambleMeasurementReport'),
             '517d':(T517d_Items,'RachBLERMeasurementReport'),
             '517e':(T517e_Items,'DCHMeasurementStartReq'),
             '517f':(T517f_Items,'BLERMeasurementReport'),
             '5180':(T5180_Items,'BERMeasurementReport'),
             '5181':(T5181_Items,'EstimatedBERMeasurementReport'),
             '5182':(T5182_Items,'ReceptionLevelMeasurementReport'),             
             '5183':(T5183_Items,'RTTMeasurementReport'),   
             '5184':(T5184_Items,'TxPowerMeasurementReport'),
             '51a1':(T51a1_Items,'ReceivedTotalWideBandPowerReport')
    }
