
#include <D:\userdata\shufan\Desktop\LogMap\EComponentId_DSPBase.h>


/* EComponentId_LtcomBase */

typedef enum {

    /* SS_LocalTelecom */
    ELtcomBaseFileId_LTCOM_MsgHandler                  = EComponentId_LtcomBase + 0x00,
    ELtcomBaseFileId_LTCOM_Msg_Sim                     = EComponentId_LtcomBase + 0x01,
    ELtcomBaseFileId_MeasurementSharedMemForProvider   = EComponentId_LtcomBase + 0x02,
    ELtcomBaseFileId_InterfaceLevelMeasProvider        = EComponentId_LtcomBase + 0x03,
    ELtcomBaseFileId_L1MeasurementCommon               = EComponentId_LtcomBase + 0x04,
    ELtcomBaseFileId_MeasurementBroSrv                 = EComponentId_LtcomBase + 0x05,
    ELtcomBaseFileId_MeasurementCac                    = EComponentId_LtcomBase + 0x06,
    ELtcomBaseFileId_MeasurementControl                = EComponentId_LtcomBase + 0x07,
    ELtcomBaseFileId_MeasurementDb                     = EComponentId_LtcomBase + 0x08,
    ELtcomBaseFileId_MeasurementFilter                 = EComponentId_LtcomBase + 0x09,
    ELtcomBaseFileId_MeasurementMain                   = EComponentId_LtcomBase + 0x0a

} EFileId_EComponentId_LtcomBase;

/* EComponentId_CommonDspBase */

typedef enum {

    /* CP_Startup */
    ECommonDspBaseFileId_CommonChannelDeviceCore1MemoryConfig = EComponentId_CommonDspBase + 0x00,
    ECommonDspBaseFileId_CommonChannelDeviceCore1MemoryDumpConfig = EComponentId_CommonDspBase + 0x01,
    ECommonDspBaseFileId_CommonChannelDeviceCore1Startup = EComponentId_CommonDspBase + 0x02,
    ECommonDspBaseFileId_CommonChannelDeviceCore1StartupParams = EComponentId_CommonDspBase + 0x03,
    ECommonDspBaseFileId_CommonChannelDeviceCore2Startup = EComponentId_CommonDspBase + 0x04,
    ECommonDspBaseFileId_CommonChannelDeviceCore2StartupParams = EComponentId_CommonDspBase + 0x05,
    ECommonDspBaseFileId_CommonChannelDeviceCore3Startup = EComponentId_CommonDspBase + 0x06,
    ECommonDspBaseFileId_CommonChannelDeviceCore3StartupParams = EComponentId_CommonDspBase + 0x07,
    ECommonDspBaseFileId_CommonChannelDeviceCore4Startup = EComponentId_CommonDspBase + 0x08,
    ECommonDspBaseFileId_CommonChannelDeviceCore4StartupParams = EComponentId_CommonDspBase + 0x09,
    ECommonDspBaseFileId_CommonChannelDeviceCore5MemoryConfig = EComponentId_CommonDspBase + 0x0a,
    ECommonDspBaseFileId_CommonChannelDeviceCore5MemoryDumpConfig = EComponentId_CommonDspBase + 0x0b,
    ECommonDspBaseFileId_CommonChannelDeviceCore5Startup = EComponentId_CommonDspBase + 0x0c,
    ECommonDspBaseFileId_CommonChannelDeviceCore5StartupParams = EComponentId_CommonDspBase + 0x0d,
    ECommonDspBaseFileId_CommonChannelDeviceCore6Startup = EComponentId_CommonDspBase + 0x0e,
    ECommonDspBaseFileId_CommonChannelDeviceCore6StartupParams = EComponentId_CommonDspBase + 0x0f,
    ECommonDspBaseFileId_CommonChannelDeviceCore7Startup = EComponentId_CommonDspBase + 0x10,
    ECommonDspBaseFileId_CommonChannelDeviceCore7StartupParams = EComponentId_CommonDspBase + 0x11,
    ECommonDspBaseFileId_CommonChannelDeviceCore8Startup = EComponentId_CommonDspBase + 0x12,
    ECommonDspBaseFileId_CommonChannelDeviceCore8StartupParams = EComponentId_CommonDspBase + 0x13,
    ECommonDspBaseFileId_DedicatedChannelDecviceCore1Startup = EComponentId_CommonDspBase + 0x14,
    ECommonDspBaseFileId_DedicatedChannelDecviceCore1StartupParams = EComponentId_CommonDspBase + 0x15,
    ECommonDspBaseFileId_DedicatedChannelDecviceCore5Startup = EComponentId_CommonDspBase + 0x16,
    ECommonDspBaseFileId_DedicatedChannelDecviceCore5StartupParams = EComponentId_CommonDspBase + 0x17,
    ECommonDspBaseFileId_MixedChannelDecviceCore1Startup = EComponentId_CommonDspBase + 0x18,
    ECommonDspBaseFileId_MixedChannelDecviceCore1StartupParams = EComponentId_CommonDspBase + 0x19,
    ECommonDspBaseFileId_MixedChannelDecviceCore5Startup = EComponentId_CommonDspBase + 0x1a,
    ECommonDspBaseFileId_MixedChannelDecviceCore5StartupParams
    /* CP_Common */
    ECommonDspBaseFileId_CommonStartup                 = EComponentId_CommonDspBase + 0x1c,
    ECommonDspBaseFileId_CopyNbrOfBits                 = EComponentId_CommonDspBase + 0x1d,
    ECommonDspBaseFileId_DspProfiling                  = EComponentId_CommonDspBase + 0x1e,
    ECommonDspBaseFileId_FixMath                       = EComponentId_CommonDspBase + 0x1f,
    ECommonDspBaseFileId_MemAutoDump                   = EComponentId_CommonDspBase + 0x20,
    ECommonDspBaseFileId_memctl                        = EComponentId_CommonDspBase + 0x21,
    ECommonDspBaseFileId_MsgParser                     = EComponentId_CommonDspBase + 0x22,
    ECommonDspBaseFileId_RunTimeCodeLoadSupport        = EComponentId_CommonDspBase + 0x23,
    ECommonDspBaseFileId_StartupMemoryConfiguration   
    /* CP_RunTimeLog */
    ECommonDspBaseFileId_CodecSysLog                   = EComponentId_CommonDspBase + 0x25,
    ECommonDspBaseFileId_Rtl_CopyMain                  = EComponentId_CommonDspBase + 0x26,
    ECommonDspBaseFileId_Rtl_DumpPool                  = EComponentId_CommonDspBase + 0x27,
    ECommonDspBaseFileId_Rtl_Lib                       = EComponentId_CommonDspBase + 0x28

} EFileId_EComponentId_CommonDspBase;

/* EComponentId_FpBase */

typedef enum {

    /* CP_TupFrameProtocol */
    EFpBaseFileId_Fp_Browser                           = EComponentId_FpBase + 0x00,
    EFpBaseFileId_Fp_Cber                              = EComponentId_FpBase + 0x01,
    EFpBaseFileId_Fp_CdmaTestAnalyzer                  = EComponentId_FpBase + 0x02,
    EFpBaseFileId_Fp_CdmaTestGenerator                 = EComponentId_FpBase + 0x03,
    EFpBaseFileId_Fp_CdmaTestHandler                   = EComponentId_FpBase + 0x04,
    EFpBaseFileId_Fp_Common                            = EComponentId_FpBase + 0x05,
    EFpBaseFileId_Fp_ConfigInd                         = EComponentId_FpBase + 0x06,
    EFpBaseFileId_Fp_Controlframe                      = EComponentId_FpBase + 0x07,
    EFpBaseFileId_Fp_CPn9PseudoNoiseGenerator          = EComponentId_FpBase + 0x08,
    EFpBaseFileId_Fp_CPseudoNoiseGenerator             = EComponentId_FpBase + 0x09,
    EFpBaseFileId_Fp_Crc                               = EComponentId_FpBase + 0x0a,
    EFpBaseFileId_Fp_database                          = EComponentId_FpBase + 0x0b,
    EFpBaseFileId_Fp_DchDl                             = EComponentId_FpBase + 0x0c,
    EFpBaseFileId_Fp_DchUl                             = EComponentId_FpBase + 0x0d,
    EFpBaseFileId_Fp_Edch                              = EComponentId_FpBase + 0x0e,
    EFpBaseFileId_Fp_EdchScheduledActivation           = EComponentId_FpBase + 0x0f,
    EFpBaseFileId_Fp_EdchScheduledDeletion             = EComponentId_FpBase + 0x10,
    EFpBaseFileId_Fp_edch_connection                   = EComponentId_FpBase + 0x11,
    EFpBaseFileId_Fp_edch_ctrlFrame                    = EComponentId_FpBase + 0x12,
    EFpBaseFileId_Fp_edch_database                     = EComponentId_FpBase + 0x13,
    EFpBaseFileId_Fp_edch_resource_manager             = EComponentId_FpBase + 0x14,
    EFpBaseFileId_Fp_FachPch                           = EComponentId_FpBase + 0x15,
    EFpBaseFileId_Fp_FpLoopTest                        = EComponentId_FpBase + 0x16,
    EFpBaseFileId_Fp_Msghandler                        = EComponentId_FpBase + 0x17,
    EFpBaseFileId_Fp_Rach                              = EComponentId_FpBase + 0x18,
    EFpBaseFileId_Fp_radparam                          = EComponentId_FpBase + 0x19,
    EFpBaseFileId_Fp_resource_manager                  = EComponentId_FpBase + 0x1a,
    EFpBaseFileId_Fp_RmCch                             = EComponentId_FpBase + 0x1b,
    EFpBaseFileId_Fp_RmDch                             = EComponentId_FpBase + 0x1c,
    EFpBaseFileId_Fp_RmTup                             = EComponentId_FpBase + 0x1d,
    EFpBaseFileId_Fp_RuntimeHookFunc                   = EComponentId_FpBase + 0x1e,
    EFpBaseFileId_Fp_TtiTrace                          = EComponentId_FpBase + 0x1f,
    EFpBaseFileId_Fp_UdpTestAnalyzer                   = EComponentId_FpBase + 0x20,
    EFpBaseFileId_Fp_UdpTestGenerator                  = EComponentId_FpBase + 0x21,
    EFpBaseFileId_Fp_UdpTestHandler                    = EComponentId_FpBase + 0x22

} EFileId_EComponentId_FpBase;

/* EComponentId_TxBase */

typedef enum {

    /* SS_W1plTx */
    ETxBaseFileId_SPPE_Cc                              = EComponentId_TxBase + 0x00,
    ETxBaseFileId_SPPE_Cell                            = EComponentId_TxBase + 0x01,
    ETxBaseFileId_SPPE_Hs                              = EComponentId_TxBase + 0x02,
    ETxBaseFileId_SPPE_HsupaCell                       = EComponentId_TxBase + 0x03,
    ETxBaseFileId_SPPE_LoadTACDataOut                  = EComponentId_TxBase + 0x04,
    ETxBaseFileId_SPPE_LoadTACDataOutAif               = EComponentId_TxBase + 0x05,
    ETxBaseFileId_SPPE_Loopback                        = EComponentId_TxBase + 0x06,
    ETxBaseFileId_SPPE_Mem                             = EComponentId_TxBase + 0x07,
    ETxBaseFileId_SPPE_Monitor                         = EComponentId_TxBase + 0x08,
    ETxBaseFileId_SPPE_Rls                             = EComponentId_TxBase + 0x09,
    ETxBaseFileId_SPPE_TACCtrl                         = EComponentId_TxBase + 0x0a,
    ETxBaseFileId_SPPE_TACCtrlBroServFunc              = EComponentId_TxBase + 0x0b,
    ETxBaseFileId_SPPE_TACCtrlCc                       = EComponentId_TxBase + 0x0c,
    ETxBaseFileId_SPPE_TACCtrlCell                     = EComponentId_TxBase + 0x0d,
    ETxBaseFileId_SPPE_TACCtrlDspBrowser               = EComponentId_TxBase + 0x0e,
    ETxBaseFileId_SPPE_TACCtrlHs                       = EComponentId_TxBase + 0x0f,
    ETxBaseFileId_SPPE_TACCtrlHsupaCell                = EComponentId_TxBase + 0x10,
    ETxBaseFileId_SPPE_TACCtrlLoopback                 = EComponentId_TxBase + 0x11,
    ETxBaseFileId_SPPE_TACCtrlMonitor                  = EComponentId_TxBase + 0x12,
    ETxBaseFileId_SPPE_TACCtrlRecovery                 = EComponentId_TxBase + 0x13,
    ETxBaseFileId_SPPE_TACCtrlRls                      = EComponentId_TxBase + 0x14,
    ETxBaseFileId_SPPE_TACCtrlSpreader                 = EComponentId_TxBase + 0x15,
    ETxBaseFileId_SPPE_TACFlQueue                      = EComponentId_TxBase + 0x16,
    ETxBaseFileId_SPPE_TACFunctions                    = EComponentId_TxBase + 0x17,
    ETxBaseFileId_SPPE_TxBroSrv                        = EComponentId_TxBase + 0x18,
    ETxBaseFileId_TxStartUp                            = EComponentId_TxBase + 0x19,
    ETxBaseFileId_version                              = EComponentId_TxBase + 0x1a,
    ETxBaseFileId_SPPE_TACSupport                      = EComponentId_TxBase + 0x1b,
    ETxBaseFileId_tac_panic                            = EComponentId_TxBase + 0x1c,
    ETxBaseFileId_SPPE_ProprietaryTestModelsTx         = EComponentId_TxBase + 0x1d,
    ETxBaseFileId_SPPE_TM7_AntennaData_Frame_0         = EComponentId_TxBase + 0x1e,
    ETxBaseFileId_SPPE_TM7_AntennaData_Frame_1         = EComponentId_TxBase + 0x1f,
    ETxBaseFileId_SPPE_TM7_AntennaData_Frame_2         = EComponentId_TxBase + 0x20,
    ETxBaseFileId_SPPE_TM7_AntennaData_Frame_3         = EComponentId_TxBase + 0x21,
    ETxBaseFileId_SPPE_TM8_AntennaData_Frame_0         = EComponentId_TxBase + 0x22,
    ETxBaseFileId_SPPE_TM8_AntennaData_Frame_1         = EComponentId_TxBase + 0x23,
    ETxBaseFileId_SPPE_TM8_AntennaData_Frame_2         = EComponentId_TxBase + 0x24,
    ETxBaseFileId_SPPE_TM8_AntennaData_Frame_3         = EComponentId_TxBase + 0x25,
    ETxBaseFileId_SPPE_TM8_AntennaData_Frame_4         = EComponentId_TxBase + 0x26,
    ETxBaseFileId_SPPE_TM8_AntennaData_Frame_5         = EComponentId_TxBase + 0x27,
    ETxBaseFileId_SPPE_TM8_AntennaData_Frame_6         = EComponentId_TxBase + 0x28,
    ETxBaseFileId_SPPE_TM8_AntennaData_Frame_7         = EComponentId_TxBase + 0x29

} EFileId_EComponentId_TxBase;

/* EComponentId_CodecL1traBase */

typedef enum {

    /* CP_L1Transmission_Nyquist */
    ECodecL1traBaseFileId_BrowserReconfInitPwrReport   = EComponentId_CodecL1traBase + 0x00,
    ECodecL1traBaseFileId_HwDbApi                      = EComponentId_CodecL1traBase + 0x01,
    ECodecL1traBaseFileId_hw_api_faraday               = EComponentId_CodecL1traBase + 0x02,
    ECodecL1traBaseFileId_L1Tra_BrowserTtiTrace        = EComponentId_CodecL1traBase + 0x03,
    ECodecL1traBaseFileId_L1Tra_ControlMsgTerminationPoint = EComponentId_CodecL1traBase + 0x04,
    ECodecL1traBaseFileId_L1Tra_Database               = EComponentId_CodecL1traBase + 0x05,
    ECodecL1traBaseFileId_L1Tra_DelayBudget            = EComponentId_CodecL1traBase + 0x06,
    ECodecL1traBaseFileId_L1Tra_EventHandler           = EComponentId_CodecL1traBase + 0x07,
    ECodecL1traBaseFileId_L1Tra_IfW1PlCc               = EComponentId_CodecL1traBase + 0x08,
    ECodecL1traBaseFileId_L1Tra_IfW1PlCommon           = EComponentId_CodecL1traBase + 0x09,
    ECodecL1traBaseFileId_L1Tra_IfW1PlHsdpa            = EComponentId_CodecL1traBase + 0x0a,
    ECodecL1traBaseFileId_L1Tra_IfW1PlHsupa            = EComponentId_CodecL1traBase + 0x0b,
    ECodecL1traBaseFileId_L1Tra_IfW1PlInit             = EComponentId_CodecL1traBase + 0x0c,
    ECodecL1traBaseFileId_L1Tra_IfW1PlLoopback         = EComponentId_CodecL1traBase + 0x0d,
    ECodecL1traBaseFileId_L1Tra_IfW1PlRls              = EComponentId_CodecL1traBase + 0x0e,
    ECodecL1traBaseFileId_L1Tra_Process                = EComponentId_CodecL1traBase + 0x0f,
    ECodecL1traBaseFileId_L1Tra_ProprietaryTestModels  = EComponentId_CodecL1traBase + 0x10,
    ECodecL1traBaseFileId_L1Tra_RfpMeasurementProvider = EComponentId_CodecL1traBase + 0x11,
    ECodecL1traBaseFileId_L1Tra_SRIO                   = EComponentId_CodecL1traBase + 0x12,
    ECodecL1traBaseFileId_L1Tra_TransactionDb          = EComponentId_CodecL1traBase + 0x13,
    ECodecL1traBaseFileId_L1Tra_TxCell                 = EComponentId_CodecL1traBase + 0x14,
    ECodecL1traBaseFileId_L1Tra_TxChannel              = EComponentId_CodecL1traBase + 0x15,
    ECodecL1traBaseFileId_L1Tra_TxChannelAgch          = EComponentId_CodecL1traBase + 0x16,
    ECodecL1traBaseFileId_L1Tra_TxChannelAich          = EComponentId_CodecL1traBase + 0x17,
    ECodecL1traBaseFileId_L1Tra_TxChannelCc            = EComponentId_CodecL1traBase + 0x18,
    ECodecL1traBaseFileId_L1Tra_TxChannelDpch          = EComponentId_CodecL1traBase + 0x19,
    ECodecL1traBaseFileId_L1Tra_TxChannelFdpch         = EComponentId_CodecL1traBase + 0x1a,
    ECodecL1traBaseFileId_L1Tra_TxChannelHichAndRgch   = EComponentId_CodecL1traBase + 0x1b,
    ECodecL1traBaseFileId_L1Tra_TxChannelHsCommon      = EComponentId_CodecL1traBase + 0x1c,
    ECodecL1traBaseFileId_L1Tra_TxChannelHsPdsch       = EComponentId_CodecL1traBase + 0x1d,
    ECodecL1traBaseFileId_L1Tra_TxChannelHsScch        = EComponentId_CodecL1traBase + 0x1e,
    ECodecL1traBaseFileId_L1Tra_TxChannelPccpchAndPcpich = EComponentId_CodecL1traBase + 0x1f,
    ECodecL1traBaseFileId_L1Tra_TxChannelPich          = EComponentId_CodecL1traBase + 0x20,
    ECodecL1traBaseFileId_L1Tra_TxChannelRel99         = EComponentId_CodecL1traBase + 0x21,
    ECodecL1traBaseFileId_L1Tra_TxChannelSccpch        = EComponentId_CodecL1traBase + 0x22,
    ECodecL1traBaseFileId_L1Tra_TxChannelScpich        = EComponentId_CodecL1traBase + 0x23,
    ECodecL1traBaseFileId_L1Tra_TxSpreaderConfig       = EComponentId_CodecL1traBase + 0x24,
    ECodecL1traBaseFileId_L1Tra_Utilities              = EComponentId_CodecL1traBase + 0x25,
    ECodecL1traBaseFileId_ul_map                       = EComponentId_CodecL1traBase + 0x26,
    ECodecL1traBaseFileId_AaMem_Ref_wa                 = EComponentId_CodecL1traBase + 0x27,
    ECodecL1traBaseFileId_FixWcdmaTimer                = EComponentId_CodecL1traBase + 0x28

} EFileId_EComponentId_CodecL1traBase;

/* EComponentId_CodecCommonBase */

typedef enum {

    /* CP_CodecCommon */
    ECodecCommonBaseFileId_CodecBcpInit                = EComponentId_CodecCommonBase + 0x00,
    ECodecCommonBaseFileId_CodecMsgParamCheck          = EComponentId_CodecCommonBase + 0x01,
    ECodecCommonBaseFileId_CodecMsgTrace               = EComponentId_CodecCommonBase + 0x02,
    ECodecCommonBaseFileId_CodecPmCounters             = EComponentId_CodecCommonBase + 0x03,
    ECodecCommonBaseFileId_CodecRadParam               = EComponentId_CodecCommonBase + 0x04,
    ECodecCommonBaseFileId_CodecStartup                = EComponentId_CodecCommonBase + 0x05,
    ECodecCommonBaseFileId_Dec_PNGenerator             = EComponentId_CodecCommonBase + 0x06,
    ECodecCommonBaseFileId_TestModelProcess            = EComponentId_CodecCommonBase + 0x07

} EFileId_EComponentId_CodecCommonBase;

/* EComponentId_CodecEncBase */

typedef enum {

    /* CP_EncBcpDch */
    ECodecEncBaseFileId_Enc_BcpDchPost                 = EComponentId_CodecEncBase + 0x00,
    ECodecEncBaseFileId_Enc_BcpDchPre                  = EComponentId_CodecEncBase + 0x01,
    ECodecEncBaseFileId_Enc_BcpHandle                  = EComponentId_CodecEncBase + 0x02,
    ECodecEncBaseFileId_Enc_BcpLibrary                 = EComponentId_CodecEncBase + 0x03,
    ECodecEncBaseFileId_Enc_BcpTest                    = EComponentId_CodecEncBase + 0x04,
    ECodecEncBaseFileId_R99LIB_bitreverse              = EComponentId_CodecEncBase + 0x05,
    ECodecEncBaseFileId_R99LIB_crc                     = EComponentId_CodecEncBase + 0x06,
    ECodecEncBaseFileId_Rel99_crc_bitreverse           = EComponentId_CodecEncBase + 0x07,
    ECodecEncBaseFileId_tbmerge                       
    /* CP_Encoder */
    ECodecEncBaseFileId_encoder                        = EComponentId_CodecEncBase + 0x09,
    ECodecEncBaseFileId_Enc_Agch                       = EComponentId_CodecEncBase + 0x0a,
    ECodecEncBaseFileId_Enc_Bch                        = EComponentId_CodecEncBase + 0x0b,
    ECodecEncBaseFileId_enc_cctrch_processing          = EComponentId_CodecEncBase + 0x0c,
    ECodecEncBaseFileId_enc_database                   = EComponentId_CodecEncBase + 0x0d,
    ECodecEncBaseFileId_Enc_Dch                        = EComponentId_CodecEncBase + 0x0e,
    ECodecEncBaseFileId_Enc_EmReceiver                 = EComponentId_CodecEncBase + 0x0f,
    ECodecEncBaseFileId_Enc_FachPch                    = EComponentId_CodecEncBase + 0x10,
    ECodecEncBaseFileId_Enc_Hich                       = EComponentId_CodecEncBase + 0x11,
    ECodecEncBaseFileId_Enc_Rgch                       = EComponentId_CodecEncBase + 0x12,
    ECodecEncBaseFileId_enc_test_model_map             = EComponentId_CodecEncBase + 0x13,
    ECodecEncBaseFileId_enc_trch_processing           
    /* CP_EncoderLibrary */
    ECodecEncBaseFileId_conv_coder                     = EComponentId_CodecEncBase + 0x15,
    ECodecEncBaseFileId_crc                            = EComponentId_CodecEncBase + 0x16,
    ECodecEncBaseFileId_dtx_insertion                  = EComponentId_CodecEncBase + 0x17,
    ECodecEncBaseFileId_interleaving1                  = EComponentId_CodecEncBase + 0x18,
    ECodecEncBaseFileId_interleaving2                  = EComponentId_CodecEncBase + 0x19,
    ECodecEncBaseFileId_physical_channel_mapping       = EComponentId_CodecEncBase + 0x1a,
    ECodecEncBaseFileId_pilot_map                      = EComponentId_CodecEncBase + 0x1b,
    ECodecEncBaseFileId_rate_matching                  = EComponentId_CodecEncBase + 0x1c,
    ECodecEncBaseFileId_secondinterleaving             = EComponentId_CodecEncBase + 0x1d,
    ECodecEncBaseFileId_tb_concat_and_segment          = EComponentId_CodecEncBase + 0x1e,
    ECodecEncBaseFileId_tfci_enc                       = EComponentId_CodecEncBase + 0x1f,
    ECodecEncBaseFileId_tfci_map                       = EComponentId_CodecEncBase + 0x20,
    ECodecEncBaseFileId_tpc_map                        = EComponentId_CodecEncBase + 0x21,
    ECodecEncBaseFileId_trchmux                        = EComponentId_CodecEncBase + 0x22,
    ECodecEncBaseFileId_turboInterleaver               = EComponentId_CodecEncBase + 0x23,
    ECodecEncBaseFileId_turbo_enc                      = EComponentId_CodecEncBase + 0x24,
    ECodecEncBaseFileId_turbo_intrl                    = EComponentId_CodecEncBase + 0x25

} EFileId_EComponentId_CodecEncBase;

/* EComponentId_CodecHsEncBase */

typedef enum {

    /* CP_EncBcpHsdpa */
    ECodecHsEncBaseFileId_Enc_BcpHsdpaHandle           = EComponentId_CodecHsEncBase + 0x00,
    ECodecHsEncBaseFileId_Enc_BcpHsdpaLibrary          = EComponentId_CodecHsEncBase + 0x01,
    ECodecHsEncBaseFileId_Enc_BCPHsdpaPost             = EComponentId_CodecHsEncBase + 0x02,
    ECodecHsEncBaseFileId_Enc_BcpHsdpaPre              = EComponentId_CodecHsEncBase + 0x03,
    ECodecHsEncBaseFileId_HSDPA_crcTables              = EComponentId_CodecHsEncBase + 0x04,
    ECodecHsEncBaseFileId_HSDPA_crc_bitreverse        
    /* CP_EncHsdpaL1Lib */
    ECodecHsEncBaseFileId_BitScrambling                = EComponentId_CodecHsEncBase + 0x06,
    ECodecHsEncBaseFileId_Enc_HrntiCalc                = EComponentId_CodecHsEncBase + 0x07,
    ECodecHsEncBaseFileId_Enc_HsEncoderRM              = EComponentId_CodecHsEncBase + 0x08,
    ECodecHsEncBaseFileId_Enc_HsScch                   = EComponentId_CodecHsEncBase + 0x09,
    ECodecHsEncBaseFileId_Enc_HsScchCntrl              = EComponentId_CodecHsEncBase + 0x0a,
    ECodecHsEncBaseFileId_Enc_HsScchOrder              = EComponentId_CodecHsEncBase + 0x0b

} EFileId_EComponentId_CodecHsEncBase;

/* EComponentId_CodecDecBase */

typedef enum {

    /* CP_Decoder */
    ECodecDecBaseFileId_DecTraceCommon                 = EComponentId_CodecDecBase + 0x00,
    ECodecDecBaseFileId_Dec_ApiMeasProvider            = EComponentId_CodecDecBase + 0x01,
    ECodecDecBaseFileId_Dec_BcpDriver                  = EComponentId_CodecDecBase + 0x02,
    ECodecDecBaseFileId_Dec_BcpQm                      = EComponentId_CodecDecBase + 0x03,
    ECodecDecBaseFileId_Dec_Control                    = EComponentId_CodecDecBase + 0x04,
    ECodecDecBaseFileId_Dec_DataBase                   = EComponentId_CodecDecBase + 0x05,
    ECodecDecBaseFileId_Dec_DataBaseDch                = EComponentId_CodecDecBase + 0x06,
    ECodecDecBaseFileId_Dec_DataBaseDpcch              = EComponentId_CodecDecBase + 0x07,
    ECodecDecBaseFileId_Dec_DataBaseEDch_Single        = EComponentId_CodecDecBase + 0x08,
    ECodecDecBaseFileId_Dec_DataBaseEDch_Slave         = EComponentId_CodecDecBase + 0x09,
    ECodecDecBaseFileId_Dec_DataBaseEDch_UserPlane     = EComponentId_CodecDecBase + 0x0a,
    ECodecDecBaseFileId_Dec_DataBaseRach               = EComponentId_CodecDecBase + 0x0b,
    ECodecDecBaseFileId_Dec_DchTcp3dSwDriver           = EComponentId_CodecDecBase + 0x0c,
    ECodecDecBaseFileId_Dec_Debugging                  = EComponentId_CodecDecBase + 0x0d,
    ECodecDecBaseFileId_Dec_EdchCdmaDriver             = EComponentId_CodecDecBase + 0x0e,
    ECodecDecBaseFileId_Dec_EdchChDataPool             = EComponentId_CodecDecBase + 0x0f,
    ECodecDecBaseFileId_Dec_HarqControl                = EComponentId_CodecDecBase + 0x10,
    ECodecDecBaseFileId_Dec_Measurements               = EComponentId_CodecDecBase + 0x11,
    ECodecDecBaseFileId_Dec_MeasurementsDch            = EComponentId_CodecDecBase + 0x12,
    ECodecDecBaseFileId_Dec_MeasurementsDpcch          = EComponentId_CodecDecBase + 0x13,
    ECodecDecBaseFileId_Dec_MeasurementsEDch           = EComponentId_CodecDecBase + 0x14,
    ECodecDecBaseFileId_Dec_MeasurementsRach           = EComponentId_CodecDecBase + 0x15,
    ECodecDecBaseFileId_Dec_MemPool                    = EComponentId_CodecDecBase + 0x16,
    ECodecDecBaseFileId_Dec_PicHandler                 = EComponentId_CodecDecBase + 0x17,
    ECodecDecBaseFileId_Dec_PostBcp                    = EComponentId_CodecDecBase + 0x18,
    ECodecDecBaseFileId_Dec_PostProcess                = EComponentId_CodecDecBase + 0x19,
    ECodecDecBaseFileId_Dec_PostProcessCodeBlockMessage = EComponentId_CodecDecBase + 0x1a,
    ECodecDecBaseFileId_Dec_PostProcessDatabase        = EComponentId_CodecDecBase + 0x1b,
    ECodecDecBaseFileId_Dec_PostProcessFPFunctions     = EComponentId_CodecDecBase + 0x1c,
    ECodecDecBaseFileId_Dec_PostProcessPn9Measurement  = EComponentId_CodecDecBase + 0x1d,
    ECodecDecBaseFileId_Dec_PreBcp                     = EComponentId_CodecDecBase + 0x1e,
    ECodecDecBaseFileId_Dec_PreProcess                 = EComponentId_CodecDecBase + 0x1f,
    ECodecDecBaseFileId_Dec_PreProcessCompressedMode   = EComponentId_CodecDecBase + 0x20,
    ECodecDecBaseFileId_Dec_PreProcessRach             = EComponentId_CodecDecBase + 0x21,
    ECodecDecBaseFileId_Dec_PreProcessTrChDeMux        = EComponentId_CodecDecBase + 0x22,
    ECodecDecBaseFileId_Dec_Srio                       = EComponentId_CodecDecBase + 0x23,
    ECodecDecBaseFileId_Dec_Tcp3dEdmaDriver            = EComponentId_CodecDecBase + 0x24,
    ECodecDecBaseFileId_Dec_TtiTrace                   = EComponentId_CodecDecBase + 0x25,
    ECodecDecBaseFileId_Dec_Vcp2dDriver               
    /* CP_DecoderLibrary */
    ECodecDecBaseFileId_Dec_BitReversal                = EComponentId_CodecDecBase + 0x27,
    ECodecDecBaseFileId_Dec_CalculatePhyChSet          = EComponentId_CodecDecBase + 0x28,
    ECodecDecBaseFileId_Dec_CopyNoOfBits               = EComponentId_CodecDecBase + 0x29,
    ECodecDecBaseFileId_Dec_CRC                        = EComponentId_CodecDecBase + 0x2a,
    ECodecDecBaseFileId_Dec_EDchQuantizeAndDemapping   = EComponentId_CodecDecBase + 0x2b,
    ECodecDecBaseFileId_Dec_FirstDeInterleaving        = EComponentId_CodecDecBase + 0x2c,
    ECodecDecBaseFileId_Dec_R99LIB_crc                 = EComponentId_CodecDecBase + 0x2d,
    ECodecDecBaseFileId_Dec_RateDecrementation         = EComponentId_CodecDecBase + 0x2e,
    ECodecDecBaseFileId_Dec_RateDematching             = EComponentId_CodecDecBase + 0x2f,
    ECodecDecBaseFileId_Dec_RateMatchingParametersDPCH = EComponentId_CodecDecBase + 0x30,
    ECodecDecBaseFileId_Dec_SecondDeinterleaving       = EComponentId_CodecDecBase + 0x31,
    ECodecDecBaseFileId_Dec_SlotBasedRateDecrementation = EComponentId_CodecDecBase + 0x32,
    ECodecDecBaseFileId_Dec_SlotBasedSecondDeinterleaving = EComponentId_CodecDecBase + 0x33,
    ECodecDecBaseFileId_Dec_SoftSlicing                = EComponentId_CodecDecBase + 0x34,
    ECodecDecBaseFileId_Dec_SoftSymbolQuantization     = EComponentId_CodecDecBase + 0x35

} EFileId_EComponentId_CodecDecBase;

/* EComponentId_CodecRmBase */

typedef enum {

    /* CP_CodecResourceManager */
    ECodecRmBaseFileId_CodecRM_Msg_Sim                 = EComponentId_CodecRmBase + 0x00,
    ECodecRmBaseFileId_CodecRM_Msg_Sim_LB              = EComponentId_CodecRmBase + 0x01,
    ECodecRmBaseFileId_Dec_RmDch                       = EComponentId_CodecRmBase + 0x02,
    ECodecRmBaseFileId_Dec_RmEDch                      = EComponentId_CodecRmBase + 0x03,
    ECodecRmBaseFileId_Dec_RmRach                      = EComponentId_CodecRmBase + 0x04,
    ECodecRmBaseFileId_enc_resource_manager            = EComponentId_CodecRmBase + 0x05,
    ECodecRmBaseFileId_Rm_MsgHandlersFspb              = EComponentId_CodecRmBase + 0x06

} EFileId_EComponentId_CodecRmBase;

/* EComponentId_CodecBrowser */

typedef enum {

    /* CP_CodecBrowser */
    ECodecBrowserFileId_BrowserDlTfMeasurement         = EComponentId_CodecBrowser + 0x00,
    ECodecBrowserFileId_BrowserEncTtiTrace             = EComponentId_CodecBrowser + 0x01,
    ECodecBrowserFileId_BrowserL1TraTtiTrace           = EComponentId_CodecBrowser + 0x02,
    ECodecBrowserFileId_BrowserPrefMeasurement         = EComponentId_CodecBrowser + 0x03,
    ECodecBrowserFileId_CodecBroCommon                 = EComponentId_CodecBrowser + 0x04,
    ECodecBrowserFileId_CodecBroSrv                    = EComponentId_CodecBrowser + 0x05,
    ECodecBrowserFileId_CodecBrowserDecoder            = EComponentId_CodecBrowser + 0x06,
    ECodecBrowserFileId_CodecBrowserEncoder            = EComponentId_CodecBrowser + 0x07,
    ECodecBrowserFileId_csl_hlt                        = EComponentId_CodecBrowser + 0x08,
    ECodecBrowserFileId_EncBrowser                     = EComponentId_CodecBrowser + 0x09,
    ECodecBrowserFileId_HsdpaEncBroSrv                 = EComponentId_CodecBrowser + 0x0a

} EFileId_EComponentId_CodecBrowser;
