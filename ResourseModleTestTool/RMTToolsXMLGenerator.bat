

rem ************************************************************
rem Test Set Generator: 
rem 	RMTTestSetGenerator.exe
rem ************************************************************
rem ------------------- Usage: --------------------------
rem  * Input:
rem     [1] R99 Service:
rem           0   AMR(12.2k)
rem           1   UL_UDI32k+DL32k
rem           2   UL_AMR12.2k+Packet(UL64k_DL64k)
rem     [2] Number of R99 Ues
rem     [3] HSUPA TTI:
rem           0   2msTti
rem           1   10msTti
rem 		  2	  2ms One Harq
rem     [4] Start Number of UPA Ues
rem     [5] Step of UPA Ues (defalut)
rem     [6] End Number of UPA Ues (defalut)

rem  * Note: The input parameters can be first 4, or all 6.
rem  * @Example: RMTTestSetGenerator 0 40 0 30
rem  * @Example: RMTTestSetGenerator 0 40 0 10 10 80
rem  * Output: 
rem         A file named Topxxx.txt, the top list of the test set combinations.
rem -------------------------------------------------------------------------


rem ************************************************************
rem TXT to Pegasus XML Tool: 
rem 	LrcRMTTools_CSV2PegasusXML.py
rem ************************************************************
rem ----------------------------------- Usage: ------------------------------
rem    [Function:] Convert CSV to Pegasus XML
rem     -Input:	
rem         -[1] FileName:  Name of csv file
rem         -[2] MARK: Additional Mark for property indication, 
rem                 (not set or use '-': to ignore this parameter)
rem         -[3] MAX_USER_NUM:  Max user number (User_num <= MAX_USER_NUM <= 80)
rem                 (defalut is: MAX_USER_NUM = User_num)     
rem     @Example: LrcRMTTools_CSV2PegasusXML.py Top60_10xHSUPA10msTti.txt
rem     @Example: LrcRMTTools_CSV2PegasusXML.py Top60_10xHSUPA10msTti.txt TC9015
rem     @Example: LrcRMTTools_CSV2PegasusXML.py Top60_10xHSUPA10msTti.txt TC9015 80
rem 	@Example: LrcRMTTools_CSV2PegasusXML.py Top60_10xHSUPA10msTti.txt - 80
rem     -Output: Pegasus XML file
rem -------------------------------------------------------------------------

@echo off
cd
set CurrentPath=%cd%
pushd %CurrentPath%
echo -----------------------------

rem DCMSCT_DSP_9007	48 x HSUPA  2ms TTI(one harq ) users + 48 x AMR users
 .\RMTTestSetGenerator.exe 0 48 2 48
  python LrcRMTTools_TXT2PegasusXML.py Top60_48xHSUPA2ms(OneHarq)+48x(AMR(12.2k)).txt TC9007
  
rem DCMSCT_DSP_9008	48 x HSUPA  10ms TTI (all harq )users + 48 x AMR users 
 .\RMTTestSetGenerator.exe 0 48 1 48
 python LrcRMTTools_TXT2PegasusXML.py Top60_48xHSUPA10msTti+48x(AMR(12.2k)).txt TC9008
 
rem DCMSCT_DSP_9013	10 x HSUPA  2ms TTI (one harq)users + 86 x AMR users
 .\RMTTestSetGenerator.exe 0 86 2 10
 python LrcRMTTools_TXT2PegasusXML.py Top60_10xHSUPA2ms(OneHarq)+86x(AMR(12.2k)).txt TC9013
 
rem DCMSCT_DSP_9014	40 x HSUPA 10ms TTI users + 24 x(UL AMR (12.2kbps)+Packet(UL64kbps/DL 64kbps))users all harq
 .\RMTTestSetGenerator.exe 2 24 1 40
 python LrcRMTTools_TXT2PegasusXML.py Top60_40xHSUPA10msTti+24x(UL_AMR12.2k+Packet(UL64k_DL64k)).txt TC9014
 
rem DCMSCT_DSP_9015	40 x HSUPA 2ms TTI(OneHarq) users + 48 x(UL UDI 32kbps +DL 32kbps )users
 .\RMTTestSetGenerator.exe 1 48 2 40
 python LrcRMTTools_TXT2PegasusXML.py Top60_40xHSUPA2ms(OneHarq)+48x(UL_UDI32k+DL32k).txt TC9015
 
rem DCMSCT_DSP_9017	80 x HSUPA 10ms TTI users (DL:A-DPCH+HSDPA)(60DCD +20 MCD)+4 way SHO  all harq (UPA User Num 10:10:80)
 .\RMTTestSetGenerator.exe 0 0 1 10 10 80

 echo txt to xml...
 python LrcRMTTools_TXT2PegasusXML.py Top60_10xHSUPA10msTti.txt TC9017 80
 python LrcRMTTools_TXT2PegasusXML.py Top60_20xHSUPA10msTti.txt TC9017 80 
 python LrcRMTTools_TXT2PegasusXML.py Top60_30xHSUPA10msTti.txt TC9017 80
 python LrcRMTTools_TXT2PegasusXML.py Top60_40xHSUPA10msTti.txt TC9017 80  
 python LrcRMTTools_TXT2PegasusXML.py Top60_50xHSUPA10msTti.txt TC9017 80
 python LrcRMTTools_TXT2PegasusXML.py Top60_60xHSUPA10msTti.txt TC9017 80 
 python LrcRMTTools_TXT2PegasusXML.py Top60_70xHSUPA10msTti.txt TC9017 80
 python LrcRMTTools_TXT2PegasusXML.py Top60_80xHSUPA10msTti.txt TC9017 80  
 
rem DCMSCT_DSP_9018	80 x HSUPA 10ms TTI users (DL:A-DPCH+HSDPA)(44DCD +36 MCD)+4 way SHO all harq, (UPA User Num 10:10:80)
 .\RMTTestSetGenerator.exe 0 0 1 10 10 80

 echo txt to xml...
 python LrcRMTTools_TXT2PegasusXML.py Top60_10xHSUPA10msTti.txt TC9018 80
 python LrcRMTTools_TXT2PegasusXML.py Top60_20xHSUPA10msTti.txt TC9018 80 
 python LrcRMTTools_TXT2PegasusXML.py Top60_30xHSUPA10msTti.txt TC9018 80
 python LrcRMTTools_TXT2PegasusXML.py Top60_40xHSUPA10msTti.txt TC9018 80  
 python LrcRMTTools_TXT2PegasusXML.py Top60_50xHSUPA10msTti.txt TC9018 80
 python LrcRMTTools_TXT2PegasusXML.py Top60_60xHSUPA10msTti.txt TC9018 80 
 python LrcRMTTools_TXT2PegasusXML.py Top60_70xHSUPA10msTti.txt TC9018 80
 python LrcRMTTools_TXT2PegasusXML.py Top60_80xHSUPA10msTti.txt TC9018 80  

rem TC9019: 80x2ms HSUPA one harq service. Generate data for 10UE/20UE/30UE/40UE/50UE/60UE/70UE/80UE.
 .\RMTTestSetGenerator.exe 0 0 2 10 10 80
 echo txt to xml...
 python LrcRMTTools_TXT2PegasusXML.py Top60_10xHSUPA2ms(OneHarq).txt TC9019 80
 python LrcRMTTools_TXT2PegasusXML.py Top60_20xHSUPA2ms(OneHarq).txt TC9019 80  
 python LrcRMTTools_TXT2PegasusXML.py Top60_30xHSUPA2ms(OneHarq).txt TC9019 80
 python LrcRMTTools_TXT2PegasusXML.py Top60_40xHSUPA2ms(OneHarq).txt TC9019 80 
 python LrcRMTTools_TXT2PegasusXML.py Top60_50xHSUPA2ms(OneHarq).txt TC9019 80
 python LrcRMTTools_TXT2PegasusXML.py Top60_60xHSUPA2ms(OneHarq).txt TC9019 80  
 python LrcRMTTools_TXT2PegasusXML.py Top60_70xHSUPA2ms(OneHarq).txt TC9019 80
 python LrcRMTTools_TXT2PegasusXML.py Top60_80xHSUPA2ms(OneHarq).txt TC9019 80 

 rem TC9020: 19x2ms HSUPA service. Generate data for 10UE/19UE
  .\RMTTestSetGenerator.exe 0 0 0 10
  .\RMTTestSetGenerator.exe 0 0 0 19
 echo txt to xml...
 python LrcRMTTools_TXT2PegasusXML.py Top60_10xHSUPA2msTti.txt TC9020
 python LrcRMTTools_TXT2PegasusXML.py Top60_19xHSUPA2msTti.txt TC9020