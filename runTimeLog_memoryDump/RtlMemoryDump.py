# -*- coding: utf-8 -*-
# ##############################################################################
#       Function:       FreezeTrgger and Memory dump for codec RunTimeLog
#       Author:         Fan, Shuangxi (NSN - CN/Hangzhou)
#       Date:           2015-1-12
#         update:       2015-3-31
#*      description:    auto Memory dump for codec RunTimeLog
# ##############################################################################
#!/usr/bin/python

import os, sys, copy, logging
import time, datetime
import paramiko, telnetlib, socket
import subprocess, traceback, shutil
import xlrd
import binascii
from GlobDef import *

#-------------------------------------------

def debugLogSetup():
    global LogFileName
    global debug_log
    os.chdir(sys.path[0])
    logging.basicConfig(filename = os.path.join(os.getcwd(), LogFileName),
                        level = logging.WARN, 
                        filemode = 'w', 
                        #format =  '%(asctime)s - %(levelname)s: %(filename)s[line:%(lineno)d]: %(message)s',
                        format =  '%(asctime)s - %(levelname)s: [line:%(lineno)d]: %(message)s',
                        datefmt = '%Y-%m-%d %H:%M:%S'
                        )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)   
    debug_log = logging.getLogger()
    debug_log.setLevel(logging.DEBUG)
    debug_log.info('-----------Debug Info start-------------\n')

    
# #############################################################################
# function:  class for Ascii Hex Convert
# * 
#
# #############################################################################
class AsciiHexConvert:
    
    def __init__(self):
        pass
        
    # #####################################################
    # converts a HEX string message to ASCII(32-bit) string.
    # #####################################################
    def Hex2Ascii(self, HexMessage):
        
        HexMessage = ''.join(HexMessage)
        
        if len(HexMessage)%2 != 0:
            debug_log.error(">>> Hex2Ascii Error! can't convert a string with odd number of characters.\n")
            return -1
        
        AsciiMessage = binascii.unhexlify(HexMessage)
        
        return AsciiMessage
        
                
    # #####################################################
    # converts a ASCII(32-bit) string to HEX string message.
    # #####################################################
    def Ascii2Hex(self, AsciiMessage):
        
        HexMessageList = []
        
        HexMessage = binascii.hexlify(AsciiMessage)
        
        for i in range(0, len(HexMessage)/8):
            HexMessageList.append(HexMessage[i*8: (i+1)*8]) 
            
        HexMessageList.append(HexMessage[(i+1)*8: len(HexMessage)])
        
        return HexMessageList
                
    # #####################################################
    # StrAssignment: 
    #
    # #####################################################
    def StrAssignment(self, obj_str, start_indx, end_indx, sub_str):
        
        obj_strList = list(obj_str)
        obj_strList[start_indx:end_indx] = list(sub_str)[:]
        obj_str = ''.join(obj_strList)
        
        return obj_str
         
# #############################################################################
# function:  class for Ssh connection
# * command: for command execution
#
# #############################################################################
class Ssh:
    
    def __init__(self, ip, ssh_name, ssh_pass):
        
        global LSP_SSH_LOGIN_PORT
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, LSP_SSH_LOGIN_PORT, ssh_name, ssh_pass)
        self.ssh = ssh
        self.id = self.ssh.get_transport().getpeername()[0]
        
    def command(self, cmd):
        
        debug_log.info( "%s:~ > %s" % (self.id, cmd))
        (stdin, stdout, stderr) = self.ssh.exec_command(cmd)
        result = stdout.channel.recv_exit_status()
                   
        time.sleep(1)
        if result != 0:
            debug_log.error( "** Command execution error!")
            
        for line in stdout.readlines():
            debug_log.info("%s: %s \n" % (self.id, line.rstrip()))
                
        for line in stderr.readlines():
            debug_log.error("%s: (err) %s \n" % (self.id, line.rstrip()))
            
        return
        
    def ssh_close(self):
        debug_log.info(" * SSH Connect to " + self.id + " closed")
        self.ssh.close()

# #############################################################################
# class for AasyscomGwRegMsg process 
#  - no need to implementat at present
# #############################################################################
class GwRegMsg(AsciiHexConvert):
    
    def __init__(self):
        
        global AasyscomGwRegReqMsg
        global AasyscomGwRegReplyMsg
        
        self.AasyscomGwRegReqMsg = AasyscomGwRegReqMsg     
        self.AasyscomGwRegReplyMsg = AasyscomGwRegReplyMsg
        
        self.ReqMsgSet()
    # ###############################################
    # IpAdapt
    # 192.168.253.106 ->
    #    ['3139322e', '3136382e','3235332e','31303600']
    # EndianFlag: 
    #  0: (defult) original order
    #  1: invert
    # return: Ascii IpStr List
    # ###############################################  
    def AsciiIpAdapt(self, ip_str, EndianFlag = 0):
        
        ip_str += binascii.unhexlify('00')
            
        if EndianFlag == 1:
            ip_str = ip_str[::-1]
            
        AsciiIpStrList = self.Ascii2Hex(ip_str) 
        
        return AsciiIpStrList       
        
    # ###############################################
    # set the values of self.AasyscomGwRegReqMsg
    # ###############################################
    def ReqMsgSet(self):
        
        global K2_ip
        global Remote_ip
        global K2_addr
        global socketUdpClientSendPort
        
        # set rec_cpu
        K2_addr_numStr = chr(ord(K2_addr[-1]) - ord('a') + ord('3'))
        cpid_line = self.StrAssignment(self.AasyscomGwRegReqMsg[1], 2, 3, K2_addr_numStr)
        self.AasyscomGwRegReqMsg[1] = cpid_line
        
        # set localIP address 
        AsciiIpStrList = self.AsciiIpAdapt(K2_ip, 1) 
        self.AasyscomGwRegReqMsg[6:10] = AsciiIpStrList[:]
        
        # set remoteIP address 
        AsciiIpStrList = self.AsciiIpAdapt(Remote_ip, 1) 
        self.AasyscomGwRegReqMsg[11:15] = AsciiIpStrList[:]
        
        # UdpSendPort set
        self.AasyscomGwRegReqMsg[15] = "%08x"% int(socketUdpClientSendPort)
        
    # ###############################################
    # Reply Msg Decoder
    def ReplyMsgDecoder(self, ReplyMsgData):
        pass
           
    
# ############################################################################
# function:  class for RtlFreezeMessage process
# * readConfigureValues: read configure values from .xls file
#   
# * MessageSet: set the values of self.RtlFreezeReqMsg
#
# ############################################################################
class RtlFreezeMsg(AsciiHexConvert):
    
    def __init__(self):
        
        global RtlFreezeReqMsg
        global EPhysicalChannelType
        
        self.RtlFreezeReqMsg = RtlFreezeReqMsg     
        self.EPhysicalChannelType = EPhysicalChannelType
              
        (rec_cpu, messageInfo, ChannelType, cellId, userId) = self.readConfigureValues()
        self.rec_cpu     = rec_cpu 
        self.messageInfo = messageInfo
        self.ChannelType = ChannelType
        self.cellId      = cellId
        self.userId      = userId
        
        self.RtlFreezeReqMsgList = []
        self.get_RtlFreezeReqMsgList()
        
        
    # #####################################################
    # read configure values from .xls file
    # #####################################################
    def readConfigureValues(self):
        #-------- global def ---------
        global RtlFreezeReqConfigFile
        
        value_col = 2        
        rec_cpu_row = 6        
        messageInfo_from_row  = 15
        messageInfo_end_row   = 21        
        EPhysicalChannelType_row = 23
        cellId_row = 24
        userId_row = 25
        
        #------- global def end ------       
        messageInfo = []
        
        data = xlrd.open_workbook(RtlFreezeReqConfigFile)
        table = data.sheets()[0]
        
        rec_cpu = str(int(table.row(rec_cpu_row)[value_col].value))
        
        for i in range(messageInfo_from_row, messageInfo_end_row+1):
            messageInfo.append(str(int(table.row(i)[value_col].value)))
            
        ChannelType = str(table.row(EPhysicalChannelType_row)[value_col].value) 

        cellId  = str(int(table.row(cellId_row)[value_col].value))
        userId  = str(int(table.row(userId_row)[value_col].value))
                
        return (rec_cpu, messageInfo, ChannelType, cellId, userId) 
    
    # #####################################################
    # set the values of RtlFreezeReqMsg
    # #####################################################
    def MessageSet(self, cpu):

        thisRtlFreezeReqMsg = copy.deepcopy(self.RtlFreezeReqMsg)
        
        cpid_line = self.StrAssignment(thisRtlFreezeReqMsg[1], 2, 4, cpu)               
        thisRtlFreezeReqMsg[1] = cpid_line           
            
        for i in range(0, len(self.messageInfo)):            
            thisRtlFreezeReqMsg[i+4] = "%08x"% int(self.messageInfo[i])
                
        ChannelType = self.EPhysicalChannelType[self.ChannelType]
        
        ChannelType_hexStr = "%08x"% ChannelType
        thisRtlFreezeReqMsg[11] = ChannelType_hexStr
        
        thisRtlFreezeReqMsg[12] = "%08x"% int(self.cellId)
        thisRtlFreezeReqMsg[13] = "%08x"% int(self.userId)
        
        return thisRtlFreezeReqMsg
        
        
    # #####################################################
    # get_RtlFreezeReq MsgList
    # such as, get core1 and core5 msg
    # #####################################################        
    def get_RtlFreezeReqMsgList(self):
        
        global K2_addr 
        global CoreId
        
        # set rec_cpu
        K2_addr_numStr = chr(ord(K2_addr[-1]) - ord('a') + ord('3'))
        
        for core_id in CoreId:
            cpu = K2_addr_numStr + core_id           
            thisRtlFreezeReqMsg = self.MessageSet(cpu)
            self.RtlFreezeReqMsgList.append(thisRtlFreezeReqMsg)

    # #####################################################
    # Send RtlFreezeReqMsg to K2 by UDP
    #  - before that, should send AasyscomGwRegReqMsg by TCP,
    #    and make shure the reply is ok.
    # #####################################################
    def MessageSend(self):
        
        global statusIndx
            
        ms_obj = SocketMessageSend()        
        GwRegMsg_obj = GwRegMsg()
        
        debug_log.info(" * Sending AasyscomGwRegReqMsg to BTS... \n")
        recvMsgInfo = " * [ AasyscomGwRegReplyMsg:] \n"
                       
        try:
            sendMsgInfo = " * [ AasyscomGwRegReqMsg:] \n"
            for i in range(0, len(GwRegMsg_obj.AasyscomGwRegReqMsg)):
                sendMsgInfo += "%s %s \n" % (LeftSpace, GwRegMsg_obj.AasyscomGwRegReqMsg[i])               
            debug_log.debug(sendMsgInfo)
            
            RecvHexMessageList = ms_obj.TCPSendAndRecvMsg(GwRegMsg_obj.AasyscomGwRegReqMsg)            
            try:
                for i in range(0, len(RecvHexMessageList)):
                    repcvMsgInfo += "%s %s \n" % (LeftSpace, RecvHexMessageList[i])
                status = int(RecvHexMessageList[statusIndx][0:2], 16)    
                recvMsgInfo += "%s * AasyscomGwRegReplyMsg.status = %s (%s)"% (LeftSpace, status, RecvHexMessageList[statusIndx])
                                
                debug_log.debug(recvMsgInfo)
                
            except Exception, recvMsge:
                debug_log.warning("** AasyscomGwRegReplyMsg recv failed!")
                debug_log.warning(recvMsge)
            
        except Exception, sendMsge:
            debug_log.warning( "** AasyscomGwRegReqMsg send failed!")
            debug_log.warning(sendMsge)
            #sys.exit(-1)
        
        status = 0
        debug_log.info(" * Sending 'RtlFreezeReqMsg' to BTS... \n")
        if status in statusOK_value:           
            for k in range(0, len(self.RtlFreezeReqMsgList)):
                RtlFreezeReqMsg = self.RtlFreezeReqMsgList[k]
                FreezeReqMsgInfo = " * [RtlFreezeReqMsg(cpid: %s):] \n"% RtlFreezeReqMsg[1][0:4]
                for i in range(0, len(RtlFreezeReqMsg)):
                    FreezeReqMsgInfo += "%s %s \n"% (LeftSpace, RtlFreezeReqMsg[i])
                debug_log.debug(FreezeReqMsgInfo)                    
                recvMessage = ms_obj.UDPSendAndRecvMsg(RtlFreezeReqMsg)                
                try:
                    debug_log.warning( " * [recvMessage (UDP)]:\n %s"% recvMessage)                    
                except Exception, RtlFreezeRecvMsge:
                    debug_log.warning("** [RtlFreezeReplyMsg (UDP)] get failed!\n")
                    debug_log.warning(RtlFreezeRecvMsge)
                    
                #debug_log.info(" * --------------------------------------\n")
            
# ##############################################################################
# function:  class for Socket Message Send
# * Hex2Ascii: convert hex to Ascii
# * Ascii2Hex: convert Ascii to hex
# * UDPSendAndRecvMsg: send a given string message(coded in HEX) to BTS by UDP.
#                      Receve UDP message replied by Server
# * TCPSendAndRecvMsg: send and receive message by TCP
# ##############################################################################
class SocketMessageSend(AsciiHexConvert):
    
    def __init__(self): 
        
        global socketHost
        global socketClient
        
        global socketTcpPort
        
        global socketUdpServerPort
        global socketUdpClientSendPort
        global socketUdpClientRecvPort
        
        global socketTimeout
        
        self.socketHost   = socketHost
        self.socketClient = socketClient
        
        self.socketTcpPort = socketTcpPort
        
        self.socketUdpServerPort = socketUdpServerPort
        self.socketUdpClientSendPort = socketUdpClientSendPort
        self.socketUdpClientRecvPort = socketUdpClientRecvPort
        
        self.BUFFER = 1024
        
        self.socketTimeout = socketTimeout           
    
          
    # ###############################################
    # send given string message(coded in HEX) to BTS  
    # receive the reply message
    # ###############################################
    def TCPSendAndRecvMsg(self, HexMessage):
        
        AsciiMessage = self.Hex2Ascii(HexMessage)
        sock  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            debug_log.info('>>> [%s :%s]Trying to connect (TCP) with BTS...\n'% (self.socketHost, self.socketTcpPort))
            sock.settimeout(self.socketTimeout)
            sock.connect((self.socketHost, self.socketTcpPort))
            debug_log.info(">>> (TCP) Connection has been established with BTS successfully!\n")        
        except Exception, SockConnect_e:
            sock.close()
            debug_log.error(">>> [%s :%s]Failed to connect with BTS!\n"% (self.socketHost, self.socketTcpPort))
            debug_log.error(SockConnect_e)
            return -1
                             
        try:
            debug_log.info('>>> [%s :%s]send message to BTS...\n'% (self.socketHost, self.socketTcpPort))
            sock.send(AsciiMessage)
            debug_log.info(">>> Message has been sent!\n")
            
        except Exception, SockSend_e:
            sock.close()
            debug_log.error('>>> [%s :%s]Failed to send message to BTS!\n'% (self.socketHost, self.socketTcpPort))
            debug_log.error(SockSend_e)
            return -1
        
        recv = sock.recv(self.BUFFER)
        
        sock.close()
        
        RecvHexMessageList = self.Ascii2Hex(recv)             
        
        return RecvHexMessageList
           
                                
    # ###################################################
    # send a given string message(coded in HEX) to BTS 
    # ###################################################
    def UDPSendAndRecvMsg(self, HexMessage): 
                
        AsciiMessage = self.Hex2Ascii(HexMessage)  
        
        UdpSend_sock  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UdpSend_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1) 
        UdpSend_sock.bind(("", self.socketUdpClientSendPort))
        
        UdpRecv_sock  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UdpRecv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1) 
        try:
            UdpRecv_sock.bind(("", self.socketUdpClientRecvPort))
        except Exception, UdpRecv_e:
            debug_log.warning( "** UdpRecv_sock bind error!" )
            debug_log.error(UdpRecv_e)
        
        try:
            debug_log.info('>>> [%s :%s]Trying to connect (UDP) with BTS...\n'% (self.socketHost, self.socketUdpServerPort))
            UdpSend_sock.settimeout(self.socketTimeout)
            UdpSend_sock.connect((self.socketHost, self.socketUdpServerPort))
            debug_log.info(">>> (UDP) Connection has been established with BTS successfully!\n")        
        except Exception, UdpSend_e:
            UdpSend_sock.close()
            debug_log.warning(">>> [%s :%s]Failed to connect with BTS!\n"% (self.socketHost, self.socketUdpServerPort))
            debug_log.error(UdpSend_e)
            return -1
        
        try:
            debug_log.info('>>> [%s :%s]send message to BTS...\n'% (self.socketHost, self.socketUdpServerPort))
            UdpSend_sock.send(AsciiMessage)
            debug_log.info(">>> Message has been sent!\n")
        except Exception, UdpSend_e:
            UdpSend_sock.close()
            debug_log.warning('>>> [%s :%s]Failed to send message to BTS!\n'% (self.socketHost, self.socketUdpServerPort))
            debug_log.error(UdpSend_e)
            return -1

        try:
            UdpRecv_sock.settimeout(1)
            recvMessage = UdpRecv_sock.recvfrom(self.BUFFER)[0]
        except Exception, UdpRecv_e:
            recvMessage = "** Get recvMessage failed!"
            debug_log.error(UdpRecv_e)
       
        UdpSend_sock.close()
        UdpRecv_sock.close()
        
        return recvMessage
 
            
# ##############################################################################
# function:  class for memory dump
# * assemble_dumpCommond: assemble the dump Commond
# * SendMessage: send message to k2
# * downLoadDumpBinFile: down Load Dump Bin File
# * connect_K2: connect_K2
# * atuoMemoryDump: atuoMemoryDump 
# ##############################################################################
class MemDump(Ssh):
    
    def __init__(self, lsp_addr, dumpInfo, dumpBinDir):
               
        global memdumpDir
        global memdumpToolPath
        global uploadRemote_dir
        global memdumpToolPath
        
        self.lsp_addr = lsp_addr
        self.dumpInfo = dumpInfo
        self.dumpBinDir = dumpBinDir
        self.memdumpDir = memdumpDir
        self.memdumpToolPath = memdumpToolPath

        self.memdumpToolPath = memdumpToolPath
        self.uploadRemote_dir = uploadRemote_dir
        
        self.dumpFile = []
        self.dumpCommond = []
        self.assemble_dumpCommond()

    # ###############################################
    # connect_K2 
    # ###############################################    
    def connect_K2(self):
        global LSP_SSH_LOGIN_NAME
        global LSP_SSH_LOGIN_PWD
        global LSP_SSH_LOGIN_PORT
        
        result = True
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.lsp_addr, LSP_SSH_LOGIN_PORT, LSP_SSH_LOGIN_NAME, LSP_SSH_LOGIN_PWD)
        except Exception, ssh_connect_e:
            debug_log.warning("** SSH trying Connect to " + self.lsp_addr + " failed!\n")
            debug_log.warning(ssh_connect_e)
            result=False
            return result
         
        ssh.close()
        
        try:
            debug_log.info(" * SSH Connect to " + self.lsp_addr + " start\n")
            SeverConsole = Ssh(self.lsp_addr, LSP_SSH_LOGIN_NAME, LSP_SSH_LOGIN_PWD)
        except Exception, ssh_e:
            debug_log.warning("** SSH Connect to " + self.lsp_addr + " failed!\n")
            debug_log.warning(ssh_e)
            result=False
            return result
              
        SeverConsole.command('pwd')
        SeverConsole.command('chmod 777 /tmp/*')

        if os.path.isdir(self.memdumpDir):
            SeverConsole.command('rm -rf '+ self.memdumpDir)
            
        SeverConsole.command('mkdir '+ self.memdumpDir)
        
        debug_log.info(" * memory dumping, please wait ...\n")
        
        for commond_str in self.dumpCommond:
            try:
                SeverConsole.command(commond_str)
          
            except Exception, command_e:
                debug_log.warning("** connect K2 exception!\n")
                debug_log.warning(command_e)
                result=False
                return result
    
        # Disconnect
        SeverConsole.ssh_close()
        return result

    
    def assemble_dumpCommond(self):
        # ****************************************
        # TODO:
        #  1. add timestamp to dump file name
        # ****************************************
        for i in range(0, len(self.dumpInfo)):
            dumpFileName = self.dumpInfo[i][0] + "_dump_addr"+ '_' + self.dumpInfo[i][1][2:] + '__len_' + self.dumpInfo[i][2][2:] + '.bin'
            this_commond = self.memdumpToolPath + ' ' + self.dumpInfo[i][1] + ' ' + self.dumpInfo[i][2]+ ' '    
                    
            this_commond += (self.memdumpDir + r'/'+ dumpFileName)
            self.dumpFile.append(dumpFileName)
            self.dumpCommond.append(this_commond)
        
    # ###############################################
    # upLoad File to k2
    # ###############################################    
    def uploadFile(self, MainPath):
        global LSP_SSH_LOGIN_NAME
        global LSP_SSH_LOGIN_PWD
        global LSP_SSH_LOGIN_PORT
        
        result = True
        MemoryDumpFilePath = MainPath+("\\External")
        MemoryDumpFileName = "memdump.tar"
        debug_log.info(" * memory dump file in path:" + MemoryDumpFilePath + ", memory dump script is:"+ MemoryDumpFileName)
        #uplaod start
        try:
            t_connetion=paramiko.Transport((self.lsp_addr,LSP_SSH_LOGIN_PORT))
            t_connetion.connect(username = LSP_SSH_LOGIN_NAME, password = LSP_SSH_LOGIN_PWD)
            sftp=paramiko.SFTPClient.from_transport(t_connetion)
            debug_log.info(' * Uploading file:'+os.path.join(MemoryDumpFilePath, MemoryDumpFileName)+" to remote path:/tmp/memdump.tar")
            #sftp.put(os.path.join(MemoryDumpFilePath,MemoryDumpFileName),os.path.join(uploadRemote_dir,MemoryDumpFileName))
            sftp.put(os.path.join(MemoryDumpFilePath, MemoryDumpFileName),"/tmp/memdump.tar")
            debug_log.info(' * Uploading file:' + os.path.join(MemoryDumpFilePath, MemoryDumpFileName)+"successfully!")
            t_connetion.close() 
        except Exception:
            debug_log.warning("** connect K2 error!")
            result = False
            return result
        return result  
    
    
    # ###############################################
    # downLoad File from k2
    # ###############################################
    def downLoadFile(self):
        global LSP_SSH_LOGIN_NAME
        global LSP_SSH_LOGIN_PWD
        global LSP_SSH_LOGIN_PORT
        
        result = True        
        debug_log.info(" * dumped .bin file will be saved in path:"+ self.dumpBinDir)
        try:
            t_connetion = paramiko.Transport((self.lsp_addr, LSP_SSH_LOGIN_PORT))
            t_connetion.connect(username=LSP_SSH_LOGIN_NAME, password=LSP_SSH_LOGIN_PWD)
            sftp = paramiko.SFTPClient.from_transport(t_connetion)
            #files = sftp.listdir(self.memdumpDir)
            
            for f in self.dumpFile:
                debug_log.info(' - Downloading file:'+self.memdumpDir+'/'+f )
                sftp.get(self.memdumpDir+'/'+f, os.path.join(self.dumpBinDir,f))
                debug_log.info(' - Downlaoding file:'+self.memdumpDir+'/'+ f +" successfully!")
            t_connetion.close() 
        except Exception, downLoadFile_e:
            debug_log.warning("** File Downlod Failed!")
            debug_log.warning(downLoadFile_e)
            result = False
            return result

        return result
           
    
    # ###############################################
    # main function for atuo Memory Dump 
    # ###############################################        
    def atuoMemoryDump(self):
        
        result = True
        debug_log.info(" * K2 IP address is:" + self.lsp_addr)

        if not result:
            return result
        #generate memory dump file
        result = self.connect_K2()
        if not result:
            return result
            
        #doloadMemory dump bin file
        result = self.downLoadFile()
        
        return result
    
# ##############################################################################
# function:  class for File(s) Manage
# * get_FileTimeStemp: 
# * SendMessage: 
# * get_CurrentTime_str: 
# * moveFile: connect_K2
# ##############################################################################    
class FileManage():
    
    def __int__(self):        
        pass
    
    # ##################################################################
    # get the created time of a file or dir
    # return: 
    #   -  time str as: year-month-day_hour-min-sec
    # ##################################################################
    def get_FileTimeStemp(self,fileName):
        stat_info = os.stat(fileName)
        creatTimeTuple = time.localtime(stat_info.st_ctime)
        
        time_format_str = '%Y_%m_%d_%H_%M_%S'
        time_str = time.strftime(time_format_str, creatTimeTuple)
        return time_str 
    
    # ##################################################################
    # get current time str
    # return: 
    #   -  time str as: year-month-day_hour-min-sec
    # ##################################################################
    def get_CurrentTime_str(self):
        time_format_str = '%Y_%m_%d_%H_%M_%S'
        timeArray = time.localtime(time.time())
        time_str = time.strftime(time_format_str, timeArray)        
        return time_str                
        
    # ##################################################################
    # move files
    # ##################################################################
    def moveFile(self, FilePath):    
    
        if os.path.isdir(FilePath):
            #time_str = get_FileTimeStemp(FilePath)
            FilePath_old = FilePath + '_LastSave'
            if os.path.isdir(FilePath_old):
                try:
                    shutil.rmtree(FilePath_old, True)
                except Exception:
                    debug_log.warning( "** Some files in '%s' may occupied by other progress, please close all of files in %s."% (FilePath_old))
            try:        
                shutil.move(FilePath, FilePath_old)
            except Exception:
                debug_log.warning( "** Some files in '%s' or '%s' may occupied by other progress,"% (FilePath, FilePath_old))
                debug_log.warning( "   please close all of files in '%s' and '%s'."% (FilePath, FilePath_old))
        try:        
            os.makedirs(FilePath)
        except Exception:
            debug_log.warning( "** Some files in '%s' may occupied by other progress,"% (FilePath))
        

            
# ########**** main ****#######***** main *****#######
if __name__ == '__main__':
    
    # ****************************************
    # TODO:
    #  1. set interaction
    # ****************************************    
    global dumpBinDir
    global CodecMemDir
    global RakeMemDir 
    
    global LSP_Addr    
    global RtlFreezeReqConfigFile
    global memCopyTime
    
    global CodecDumpInfo
    global RakeDumpInfo

    global LeftSpace
    
    BasePath = ''

    # set defult option, 1  -- Codec memory
    if len(sys.argv) == 1:
        sys.argv.append('1')
    
    if ( len(sys.argv) == 2 and sys.argv[1].upper().find('HELP')<0) or len(sys.argv) == 3:       
        debugLogSetup()       
        BasePath = os.path.dirname(sys.argv[0])         
        dumpBinDir = os.path.join(BasePath, dumpBinDir)
        CodecDumpBinDir = os.path.join(dumpBinDir, CodecMemDir)
        RakeDumpBinDir = os.path.join(dumpBinDir, RakeMemDir)
        
        if os.path.isdir(dumpBinDir):            
            FM_obj = FileManage()
            FM_obj.moveFile(dumpBinDir)               
            #shutil.rmtree(dumpBinDir, True)
            
        os.system("mkdir " + dumpBinDir) 
        debug_log.info(" * The dumped bin file will be saved in '%s'."% dumpBinDir)
        
    if len(sys.argv) == 2 and sys.argv[1].upper().find('HELP')<0: 
        # codec and rake memory dump        
        if sys.argv[1] == '0':

            os.system("mkdir " + CodecDumpBinDir)
            os.system("mkdir " + RakeDumpBinDir)
            
            RtlFreezeReqConfigFile = os.path.join(BasePath, RtlFreezeReqConfigFile)               
            debug_log.info("\n  ------------ Send Message: RtlFreezeMsg -----------------")
            Rtl_msg_obj = RtlFreezeMsg()
            Rtl_msg_obj.MessageSend()
        
            debug_log.info("* Please waiting for SnapShot memory Copy..." ) 
            debug_log.info( "  -------------------- Memory Dumping ------------------------")
            debug_log.info( " * Codec Memory Dumping...")
            md_obj = MemDump(LSP_Addr, CodecDumpInfo, CodecDumpBinDir)   
            #result1 = False
            result1 = md_obj.atuoMemoryDump()
                       
            if not result1:
                debug_log.warning("** Codec Log memory dump failed!" )          
            
            debug_log.info(" * Rake Log Memory Dumping...")
            md_obj = MemDump(LSP_Addr, RakeDumpInfo, RakeDumpBinDir)        
            result2 = md_obj.atuoMemoryDump()            
        
            if not result2:
                debug_log.warning("** Rake Log memory dump failed!")
         # codec memory dump    
        elif sys.argv[1] == '1':
            os.system("mkdir " + CodecDumpBinDir)
                               
            RtlFreezeReqConfigFile = os.path.join(BasePath, RtlFreezeReqConfigFile)                
            debug_log.info("  ------------ Send Message: RtlFreezeMsg -----------------")
            Rtl_msg_obj = RtlFreezeMsg()
            Rtl_msg_obj.MessageSend()
        
            debug_log.info("* Please waiting for SnapShot memory Copy...")
            debug_log.info( "  -------------------- Memory Dumping ------------------------")
            debug_log.info( " * Codec Memory Dumping...")
                       
            md_obj = MemDump(LSP_Addr, CodecDumpInfo, CodecDumpBinDir)        
            result1 = md_obj.atuoMemoryDump()
            
            if not result1:
                debug_log.warning("** Codec Log memory dump failed!")
            
        # rake memory dump            
        elif sys.argv[1] == '2':
            os.system("mkdir " + RakeDumpBinDir)          
            debug_log.info("* Please waiting for SnapShot memory Copy..." )      
            debug_log.info("  -------------------- Memory Dumping ------------------------" )                 
            debug_log.info(" * Rake Log Memory Dumping...")
            md_obj = MemDump(LSP_Addr, RakeDumpInfo, RakeDumpBinDir)        
            result2 = md_obj.atuoMemoryDump()            
        
            if not result2:
                debug_log.warning("** Rake Log memory dump failed!" )
                
    # self defined memory dump            
    elif len(sys.argv) == 3:
        dumpInfo = [['', sys.argv[1], sys.argv[2]]]
        
        debug_log.info( "* Please waiting for SnapShot memory Copy...")              
        debug_log.info( "  -------------------- Memory Dumping ------------------------")            
        md_obj = MemDump(LSP_Addr, dumpInfo, dumpBinDir)        
        result = md_obj.atuoMemoryDump()            
    
        if not result:
            debug_log.warning( "** memory dump failed!")    
    else:
        print'''

   *************************** Usage: ***************************
    -input: 
        [1] dump options: 
            0:  Codec & Rake memory 
            1:  Codec memory only
            2:  Rake memory only
            dump_addr:  self defined dump address
        [2] dump length
    Note:  defult option is Codec memory 
   @example:
        %s
        %s 0
        %s 1
        %s 2
        %s 0x78000000 0x2000000
        
   - output:
        - Out put Location: the dumped .bin files in " %s\"
            
   **************************************************************
        '''% (sys.argv[0], sys.argv[0], sys.argv[0], sys.argv[0],sys.argv[0], dumpBinDir)

        exit(0)  
    
