/**
*******************************************************************************
* @file                  $HeadURL$
* @version               $LastChangedRevision$
* @date                  $LastChangedDate$
* @author                $Author$
*
* @brief                 FaultHandling header file
* @module                SS_LocalOam\CP_FaultManager
* @owner                 Liu Junjie
*
*                        Detailed description
*
* Copyright 2010 Nokia Siemens Networks. All rights reserved.
*******************************************************************************/
#ifndef _FAULTHANDLING_H
#define _FAULTHANDLING_H

#ifdef __cplusplus
extern "C"{
#endif /* __cplusplus */

#include <glo_def.h>
#include <EFaultId.h>
#include <FaultInd.h>
#include <TCounter.h>
#include <TAaSysComSicad.h>

#define     FM_NUM_OF_FAULTS_IN_TABLE            ((u32) 80)
#define     FM_CANCEL_FAULT_INFO                 ((TFaultInfo) 0xFFFFFFFF)
#define     FM_NOT_REPEATING                     ((u8) 0xFF)
#define     FM_NO_DETECTION_WINDOW               ((u16) 0xFFFF)
#define     FM_CANCEL_REPEATING                  ((u16) 0xFFFD)
#define     FM_CANCELLING                        ((u16) 0xFFFC)
#define     FM_STARTING_REPEATING                ((u8) 0xFE)
#define     FM_RECOVERY_TIMER_INTERVAL           ((u32) 2*5+1)
#define     FM_MAX_NUMBER_OF_SAVED_FAULTS        ((u32) 10000)

typedef u32 TFaultTypeIndex;

typedef struct SRepeatBuffer
{
    FaultInd  repeatFault;
    TCounter  numberOfRepeatTimes;
} SRepeatBuffer;

typedef struct SFaultTimeStamp
{
    u32 year        :12;  /* word 1 */
    u32 month       :4;
    u32 day         :5;
    u32 hour        :5;
    u32 minute      :6;
    
    u32 second      :6;   /* word 2 */
    u32 millisec    :10;
    u32 reserved    :16;
} SFaultTimeStamp;

typedef struct SFaultState
{
    EFaultId            faultId;
    TAaSysComSicad      faultSource;
    SFaultTimeStamp     faultTime;
    TFaultInfo          faultInfo[5];
} SFaultState;

/**
*******************************************************************************
*
*   @brief    SenderBlocked checks blocked status of faults of given task.
*
*             Returns value from faultSourceDataBlocked bitfield
*             telling if given task is blocked.
*
*   @param    task: Input; Typically OSE process id of a certain process.
*   @return   GLO_FALSE if faults of the task are not blocked,
*             GLO_TRUE if faults of the task are blocked.
*
*******************************************************************************/
TBoolean SenderBlocked(const TTask task);

/**
*******************************************************************************
*
*   @brief    SetSenderBlocked sets blocking status of faults of given task.
*
*   @param    task: Input; Typically OSE process id of a certain process.
*   @param    blockState: Input; boolean value, true means that faults will
*                                be blocked for this process
*   @return   -
*
*******************************************************************************/
void SetSenderBlocked(const TTask task, const TBoolean blockState );

/**
*******************************************************************************
*
*   @brief    ReceiveFaultInd handles FaultInd messages (FAULT_IND_MSG).
*
*             Function will put received fault indication to faultHistoryBuffer.
*             If needed:
*                 Update active fault buffer,
*                     if faultDetectionWindow defined
*                        Timer is set to call ActiveFaultTimerInd.
*                 Send message to WAM and add fault to repeat buffer.
*                 Send message to Browser.
*                 Call recovery function.
*
*   @param    inMsgPtr: Input; Pointer to received FaultInd message.
*   @return   -
*
*******************************************************************************/
void * ReceiveFaultInd(void ** inMsgPtr);

/**
*******************************************************************************
*
*   @brief    RepeatTimerInd resends fault to OAM if acknowledgement message
*             has not been received and repeat times are left.
*             Activated by timer set with ActivateTimer.
*
*             Searches fault from repeat buffer and when found:
*             IF repeat times left
*                Decrements number of repeat times.
*                Resends fault to WAM calling SendRepeatFault.
*                Sets new timer request.
*             ELSE
*                Remove the fault from repeatBuffer.
*
*   @param    -
*   @return   -
*
*******************************************************************************/
void * RepeatTimerInd(void ** inMsgPtr);

/**
*******************************************************************************
*
*   @brief    ReceiveFaultAckMsg handles FaultAckMsg messages, removes fault
*             from repeat fault buffer.
*
*             Searches fault from repeat buffer and when found,
*             the fault is removed from repeat buffer if faultState is the same
*             as in the received message.
*
*   @param    inMsgPtr: Input; Pointer to payload of FaultAckMsg message.
*   @return   -
*
*******************************************************************************/
void * ReceiveFaultAckMsg(void ** inMsgPtr);

/**
*******************************************************************************
*
*   @brief    GetFaultTypeIndex searches and returns index of given faultId from
*             fault type table. If not found, index of EFaultId_UnknownFaultId
*             is returned.
*
*             If faultId EFaultId_UnknownFaultId is not defined then returns
*             number of fault types.
*
*   @param    faultId: Input; Fault id number.
*   @return   Index of the fault id in CPU specific fault type table.
*
*******************************************************************************/
TFaultTypeIndex GetFaultTypeIndex(const EFaultId faultId);

/**
*******************************************************************************
*
*   @brief    SendFaultReportCancel sends a fault indication message to fault
*             manager process to cancel active fault.
*
*             Allocates FaultInd message, fills given faultId and faultInfo
*             parameters to the message, faultState is set to EFaultState_Cancel.
*             All faultInfo fields are filled with same given items value.
*             Items value can be used e.g. to tell which items of multiactive
*             fault are cancelled.
*             Sends the message to FM.
*
*             If allocation fails, SendFaultReport is called to send
*             EFaultId_BufferAllocation fault.
*
*             SendFaultReportCancel is called from ActiveFaultTimerInd after
*             detection window time if fault indication frequency has not been
*             overrun or from recovery function when recovery has been
*             successful. Corresponding message can be sent also outside e.g.
*             from Massi.
*
*   @param    faultId: Input; Fault id number, see SFaultTypeDataTable.h.
*   @param    items: Input; Value set to faultInfo fields. Used e.g. to tell
*                           which items of multiactive fault are cancelled.
*   @param    faultIndex: Input; index of faultId in fault type data table.
*   @return   -
*
*******************************************************************************/
void SendFaultReportCancel(const EFaultId faultId, const TFaultInfo items,
                           const TFaultTypeIndex faultIndex);

void SendFaultCancel(const EFaultId   faultId,    const TFaultInfo faultInfo1,
                     const TFaultInfo faultInfo2, const TFaultInfo faultInfo3,
                     const TFaultInfo faultInfo4, const TFaultInfo faultInfo5);

/**
*******************************************************************************
*
*   @brief    FatalErrorRising rises Fatal OSE Error, used in Testing purpose.
*
*   @param    inMsgPtr: Input; Pointer to received message.
*   @return   -
*
*******************************************************************************/
void * FatalErrorRising(void ** inMsgPtr);

/**
*******************************************************************************
*
*   @brief    TestFaultReq sends fault to Fault Manager, used in Testing purpose.
*
*   @param    inMsgPtr: Input; Pointer to received message.
*   @return   -
*
*******************************************************************************/
void * TestFaultReq (void ** inMsgPtr);


#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif

