

rem ************************************************************
rem Test Set Generator: 
rem 	RMTTestSetGenerator.exe
rem ************************************************************
rem ------------------- Usage: --------------------------
rem * [Function:] RMT test set generator.
rem * Input:
rem    [1] R99 service:
rem          0   AMR(12.2k)
rem          1   UL_UDI32k+DL32k
rem          2   UL_AMR12.2k+Packet(UL64k_DL64k)
rem    [2] Number of R99 Ues
rem    [3] Number of UPA 2msTti Ues
rem    [4] Number of UPA 10msTti Ues
rem    [5] Number of UPA 2ms(OneHarq) Ues
rem * @Example: ./RMTTestSetGenerator_Mixed 0 0 10 20 0
rem * Output:
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

rem DCMSCT_DSP_9003: 10 x HSUPA 10ms TTI users + 70 x HSUPA 2ms TTI users +4 way SHO (10ms all harq + 2ms one harq) 
 .\RMTTestSetGenerator_mixed.exe 0 0 0 10 70
  python LrcRMTTools_TXT2PegasusXML.py Top60_70xHSUPA2ms(OneHarq)+10xHSUPA10msTti.txt TC9003

rem DCMSCT_DSP_9004: 40 x HSUPA 10ms TTI users + 40 x HSUPA 2ms TTI users +4 way SHO (10ms all harq + 2ms one harq)
 .\RMTTestSetGenerator_mixed.exe 0 0 0 40 40
  python LrcRMTTools_TXT2PegasusXML.py Top60_40xHSUPA2ms(OneHarq)+40xHSUPA10msTti.txt TC9004
  
rem DCMSCT_DSP_9005: 70 x HSUPA 10ms TTI users + 10 x HSUPA 2ms TTI users +4 way SHO (10ms all harq + 2ms all harq)
 .\RMTTestSetGenerator_mixed.exe 0 0 10 70 0
  python LrcRMTTools_TXT2PegasusXML.py Top60_10xHSUPA2msTti+70xHSUPA10msTti.txt TC9005
  
					
rem DCMSCT_DSP_9016: 24 x HSUPA  10ms+24 x HSUPA 2ms TTI users + 48 x AMR users		(10ms all harq + 2ms one harq)
 .\RMTTestSetGenerator_mixed.exe 0 48 0 24 24
  python LrcRMTTools_TXT2PegasusXML.py Top60_24xHSUPA2ms(OneHarq)+24xHSUPA10msTti+48x(AMR(12.2k)).txt TC9016
