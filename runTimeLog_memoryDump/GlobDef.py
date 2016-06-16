
import os, sys
#----------------------------------------------

# ------------- global defination -------------
K2_ip          = '192.168.253.106' 
Remote_ip      = '192.168.100.126'

# dumpInfo: dump addr and length

CodecDumpInfo = [
    ['Core1', '0x78000000', '0x2000000'],
    ['Core5', '0x7c000000', '0x2000000']
]

RakeDumpInfo = [
    ['Core2', '0x70000000', '0x1400000'],
    ['Core3', '0x71400000', '0x1400000'],
    ['Core4', '0x72800000', '0x1400000'],
    ['Core6', '0x73c00000', '0x1400000'],
    ['Core7', '0x75000000', '0x1400000'],
    ['Core8', '0x76400000', '0x1400000']    
]

#----------------------------------------
#
# CoreId: core1, core5
CoreId = ['1', '5']

# K2IpMap
K2IpMap = {
    '192.168.253.106' :   'K2_a',
    '192.168.253.107' :   'K2_b',
    '192.168.253.108' :   'K2_c'
}

# K2IpMap
K2PortMap = {
    'K2_a' :   12005,
    'K2_b' :   12006,
    'K2_c' :   12007
}

K2_addr = K2IpMap[K2_ip]
UdpSendPort = K2PortMap[K2_addr]

#--------------------------------------
# LSP
memdumpDir       = r"/tmp/memdumpDir"
memdumpToolPath  = r"/opt/memdump/k2_memdump"
uploadRemote_dir = r"/tmp"
#----------------------------------------
# remote
dumpBinDir  = r"MemoryDump"
CodecMemDir = r"CodecMemory"
RakeMemDir  = r"RakeMemory"

LogFileName = "DebugLog.txt"
LeftSpace = ' '*8
#--------------------------------------

LSP_SSH_LOGIN_NAME = "root"
LSP_SSH_LOGIN_PWD  = ""
LSP_SSH_LOGIN_PORT = 22
LSP_Addr           = K2_ip

#socketHost     = '192.168.255.1'
socketHost        = K2_ip
socketClient      = Remote_ip

socketTcpPort               = 15004

socketUdpServerPort         = 16008
socketUdpClientSendPort     = UdpSendPort
socketUdpClientRecvPort     = 51000

socketTimeout    = 3
#memCopyTime = 10

#---------------- AasyscomGwRegMsg Def ------------------------
# NOTE: should consider the endian

AasyscomGwRegReqMsg = [
    '00002bd3', # 1st word, # header: msgId
    '123d031e',   # 2nd word,  # sic: rec_board(1), rec_cpu(1), rec_task(2)
    '10110940',   # 3th word,  # ownSic: send_board(1), send_cpu(1), send_task(2)
    '00500004',   # 4th word, length(2), flags(2)    
    '1011ffff',   # 5th word,  localSicAddr
    '10110940',   # 6th word,  remoteSicAddr
                # 7~11th word, SAaSysComGwIpAddress localIP  
    '00363031',   # 7~10th word,  address = 601.352.861.291
    '2e333532',
    '2e383631',
    '2e323931',
    '00003e88',   # 11th word,  port = 16008
                # 12~16th word, SAaSysComGwIpAddress remoteIP
    '00363231',   # 12~15th word, address = 621.001.861.291
    '2e303031',
    '2e383631',
    '2e323931',
    '00002ee5',   # 16th word,  port = 12005
    
    '00000001',   # 17th word,  protocol = 1
    '00000001',   # 18th word,  retainMsgHeader = 1
    '00000001',   # 19th word,  msgID = 1
    '00000000'    # 20th word,  reliability = 0
]


statusIndx = 20
statusOK_value = [0, 7, 8]

AasyscomGwRegReplyMsg = [
    '00002bd4', # 1st word, # header: msgId
    '123d031d',   # 2nd word,  # sic: rec_board(1), rec_cpu(1), rec_task(2)
    '123d031e',   # 3th word,  # ownSic: send_board(1), send_cpu(1), send_task(2)
    '005c0004',   # 4th word, length(2), flags(2)    
    '1011ffff',   # 5th word,  localSicAddr
    '10110940',   # 6th word,  remoteSicAddr
                # 7~11th word, SAaSysComGwIpAddress localIP   
    '3139322e',   # 7~10th word,  address = 192.168.253.106
    '3136382e',
    '3235332e',
    '31303600',
    '00003e88',   # 11th word,  port = 16008
                # 12~16th word, SAaSysComGwIpAddress remoteIP
    '3139322e',   # 12~15th word, address = 192.168.100.126
    '3136382e',
    '3130302e',
    '31323600',
    '00002ee5',   # 16th word,  port = 12005
    
    '00000001',   # 17th word,  protocol = 1
    '00000001',   # 18th word,  retainMsgHeader = 1
    '00000001',   # 19th word,  msgID = 1
    '00000000',   # 20th word,  reliability = 0
    '00000000',   # 21th word,  status = 0 , 7, 8 are ok
    '000002a6',   # 22th word,  routeId = 678
    '00002ee5'    # 23th word,  port = 12005   
]

#---------------- RtlFreezeMessage Def ------------------------

RtlFreezeReqConfigFile = "CodecRtlFreezeReqConfig.xls"

RtlFreezeReqMsg = [
    '0000fd50', # 1st word, # header: msgId
                # API_header_byte:
    '12350250',   # 2nd word,  # rec_board(1), rec_cpu(1), rec_task(2)
    '10110940',   # 3th word, send_board(1), send_cpu(1), send_task(2)
    '00380000',   # 4th word, length(2), system(1), user(1)    
                # messageInformationElements:
    '00000001',   # 5th word,  msgSet
    '00000001',   # 6th word,  logSet
    '00000001',   # 7th word,  fpttiSet
    '00000001',   # 8th word,  nonHsl1traSet 
    '00000001',   # 9th word,  hsL1traSet
    '00000001',   # 10th word,  encSet
    '00000001',   # 11th word,  decSet
    '00000000', # 12th word, # EPhysicalChannelType
                # messageInformationElements:
    '00000001',   # 13th word,  cellId
    '00000001'    # 14th word,  userId    
]


EPhysicalChannelType = {
    'EPhysicalChannelType_None'     : 0,
    'EPhysicalChannelType_Pcpich'   : 1,
    'EPhysicalChannelType_Scpich'   : 2,
    'EPhysicalChannelType_Pccpch'   : 3,
    'EPhysicalChannelType_Sccpch'   : 4,
    'EPhysicalChannelType_Pich'     : 5,
    'EPhysicalChannelType_Aich'     : 6,
    'EPhysicalChannelType_Dpch'     : 7,
    'EPhysicalChannelType_Psch'     : 8,
    'EPhysicalChannelType_Ssch'     : 9,
    'EPhysicalChannelType_HsPdsch'  : 10,
    'EPhysicalChannelType_HsScch'   : 11,
    'EPhysicalChannelType_EAgch'    : 12,
    'EPhysicalChannelType_EHichRgch' : 13,
    'EPhysicalChannelType_Mich'     : 14,
    'EPhysicalChannelType_FDpch'    : 15,
    'EPhysicalChannelType_NumOfItems' : 16
}        
              
 
