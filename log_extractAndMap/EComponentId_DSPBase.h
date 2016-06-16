/**
*******************************************************************************
* @file                  $HeadURL$
* @version               $LastChangedRevision$
* @date                  $LastChangedDate$
* @author                $Author$
*
* Original author        <tsheng>
* @module                Codec
* @owner                 Codec
*
* Copyright 2014 Nokia Networks. All rights reserved.
*******************************************************************************/

#ifndef _E_COMPONENTID_DSPBASE_H
#define _E_COMPONENTID_DSPBASE_H

#ifdef __cplusplus
extern "C"{
#endif

/*EComponentId_DSPBase.h*/
typedef enum EComponentId_DSPBase
{
    EComponentId_CodecBase        = 0,
    EComponentId_LtcomBase        = 0x1000,   /* SS_LocalTelecom */
    EComponentId_CommonDspBase    = 0x2000,   /* CP_Startup, CP_Common, CP_RunTimeLog */
    EComponentId_FpBase           = 0x3000,   /* CP_TupFrameProtocol */
    EComponentId_TxBase           = 0x4000,   /* SS_W1plTx */
    EComponentId_CodecL1traBase   = 0x5000,   /* CP_L1Transmission_Nyquist */
    EComponentId_CodecCommonBase  = 0x6000,   /* CP_CodecCommon */
    EComponentId_CodecEncBase     = 0x7000,   /* CP_EncBcpDch, CP_Encoder, CP_EncoderLibrary */
    EComponentId_CodecHsEncBase   = 0x8000,   /* CP_EncBcpHsdpa, CP_EncHsdpaL1Lib */
    EComponentId_CodecDecBase     = 0x9000,   /* CP_Decoder, CP_DecoderLibrary */
    EComponentId_CodecRmBase      = 0xa000,   /* CP_CodecResourceManager */
    EComponentId_CodecBrowser     = 0xb000,   /* CP_CodecBrowser */
    EComponentId_Others           = 0xc000
} EComponentId_DSPBase;

#ifdef __cplusplus
}
#endif

#endif /* _E_COMPONENTID_DSPBASE_H */

/**
*******************************************************************************
*
* Description         : component id define used in codec sub-system.
*
* Reference           :
*
* Additional Information :
*
* Definition Provided by : Codec
*
********************************************************************************/

