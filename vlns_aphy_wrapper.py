#!/usr/bin/python3
import sys
import os
import platform
import datetime
import time
import traceback
from ctypes import *

class APhySdkVersion(Structure):
    _fields_ = [("major", c_ushort),
                ("minor", c_ushort),
                ("patch", c_ushort),
                ("label1", c_char_p),
                ("label2", c_char_p),
                ("stamp", c_char_p),
                ("versionString", c_char_p)]

# APhyPortEnum
APHY_PORT_0_E = c_int(0)
APHY_PORT_1_E = c_int(1)
APHY_PORT_2_E = c_int(2)
APHY_PORT_3_E = c_int(3)

# EnDisStateEnum
STATE_DISABLE_E = c_int(0)
STATE_ENABLE_E = c_int(1)

# FifoIfEnum
FIFO_IF_SPI_E = c_int(0)
FIFO_IF_I2C_E = c_int(1)

EventHandlerFunc = CFUNCTYPE(c_void_p, c_void_p, c_void_p)

class EventsClient(Structure):
    _fields_ = [("pClientContext", c_void_p),
                ("handlers", EventHandlerFunc * 6)]

# Va70xxDeviceIdEnum
VA7044_0 = c_int(0)
VA7044_1 = c_int(1)
VA7031_0 = c_int(2)
VA7031_1 = c_int(3)
VA7031_2 = c_int(4)
VA7031_3 = c_int(5)
VALENS_MAX_DEVICES = c_int(6)

# VlnsProcIdEnum
PROC_DEV_7044_0_E = c_int(0)
PROC_DEV_7044_1_E = c_int(1)
PROC_DEV_7031_0_E = c_int(2)
PROC_DEV_7031_1_E = c_int(3)
PROC_DEV_7031_2_E = c_int(4)
PROC_DEV_7031_3_E = c_int(5)
PROC_FUSA_SERVICE_E = c_int(6)
PROC_MAX_E = c_int(7)
PROC_DEVICES_COUNT_E = c_int(6)
PROC_VA7044_COUNT = c_int(2)
PROC_VA7031_COUNT = c_int(4)

# Va70xxEventEnum
VA70XX_EVENT_APP_ERROR = c_int(1)
VA70XX_EVENT_NOTIFICATION_RECV = c_int(2)
VA70XX_EVENT_FUSA_HW_EVT = c_int(3)
VA70XX_EVENT_FUSA_SW_EVT = c_int(4)
VA70XX_EVENT_TX_FIFO_DATA = c_int(5)
VA70XX_EVENT_MAX = c_int(6)

# Va70xxEventBitmaskEnum
VA70XX_EVENT_BITMASK_NONE_E = c_int(0)
VA70XX_EVENT_BITMASK_APP_ERROR_E = c_int(2)
VA70XX_EVENT_BITMASK_NOTIFICATION_RECV_E = c_int(4)
VA70XX_EVENT_BITMASK_FUSA_HW_EVT_E = c_int(8)
VA70XX_EVENT_BITMASK_FUSA_SW_EVT_E = c_int(16)
VA70XX_EVENT_BITMASK_TX_FIFO_DATA_E = c_int(32)

# VlnsAppErrorSeverityEnum
APP_ERROR_MINOR_E = c_int(0)
APP_ERROR_MAJOR_E = c_int(1)
APP_ERROR_FATAL_E = c_int(2)
MAX_APP_ERROR = c_int(3)

# AppMsgTypeEnum
APP_MSG_COMMAND_E = c_int(0)
APP_MSG_EVENT_E = c_int(1)

# HostStatusEnum
HOST_STATUS_SUCCESS_E = c_int(0)
HOST_STATUS_FAIL_E = c_int(1)
HOST_STATUS_FAIL_INVALID_INPUT_E = c_int(2)
HOST_STATUS_FAIL_UNKN_CMD_E = c_int(3)
HOST_STATUS_FAIL_NOT_READY_E = c_int(4)

# AppTransportStatusEnum
APP_TRANSPORT_SUCCESS_E = c_int(0)
APP_TRANSPORT_INVALID_ARGS_E = c_int(1)
APP_TRANSPORT_SEND_FAILED_E = c_int(2)
APP_TRANSPORT_POLL_SOCKET_FAILED_E = c_int(4)
APP_TRANSPORT_NO_DATA_TO_READ_E = c_int(8)
APP_TRANSPORT_RECEIVE_FAILED_E = c_int(16)
APP_TRANSPORT_WAIT_FOR_RESPONSE_FAILED_E = c_int(32)
APP_TRANSPORT_INIT_MUTEX_FAILED_E = c_int(64)
APP_TRANSPORT_LOCK_MUTEX_FAILED_E = c_int(128)
APP_TRANSPORT_UNLOCK_MUTEX_FAILED_E = c_int(256)
APP_TRANSPORT_DESTROY_MUTEX_FAILED_E = c_int(512)
APP_TRANSPORT_SHUTDOWN_SOCK_FAILED_E = c_int(1024)
APP_TRANSPORT_CLOSE_SOCK_FAILED_E = c_int(2048)
APP_TRANSPORT_FULL_POLL_OF_TRANSACTIONS_E = c_int(4096)
APP_TRANSPORT_RESPONSE_PARSE_ERROR_E = c_int(8192)
APP_TRANSPORT_UNDEFINED_BEHAVIOUR_E = c_int(16384)

class TransactionStatus(Structure):
    _fields_ = [("transportStatus", c_int),
                ("hostStatus", c_int)]

# BLOCK_ID_Enum
BLOCK_ID_ACMP_E = c_int(1)
BLOCK_ID_MNG_E = c_int(2)
BLOCK_ID_APHY_E = c_int(3)
BLOCK_ID_MSIO_AL_E = c_int(4)
BLOCK_ID_I2C_AL_E = c_int(5)
BLOCK_ID_BIST_AL_E = c_int(6)
BLOCK_ID_RCLK_AL_E = c_int(7)
BLOCK_ID_CSI_SNK_E = c_int(8)
BLOCK_ID_CSI_SRC_E = c_int(9)
BLOCK_ID_CSI_SNK_PHY_E = c_int(10)
BLOCK_ID_CSI_SRC_PHY_E = c_int(11)
MAX_BLOCK_ID_E = c_int(12)

# MNG_NOTIFICATION_ID_Enum
WAIT_FOR_HOST_ID_E = c_int(0)
FW_INIT_DONE_ID_E = c_int(1)
FW_ERROR_ID_E = c_int(2)
FW_RX_FIFO_OVRFLW_E = c_int(3)

# A_PHY_NOTIFICATION_ID_Enum
A_PHY_READY_IND_E = c_int(1)
A_PHY_LINK_UP_E = c_int(2)
A_PHY_LINK_DOWN_E = c_int(3)
A_PHY_POOR_LINK_QUALITY_E = c_int(4)
A_PHY_ENTER_SLEEP_ON_START_UP_E = c_int(5)
A_PHY_ENTER_TEST_MODE_E = c_int(6)
A_PHY_BIST_PER_THRESH_CROSSED_E = c_int(7)
A_PHY_BIST_BER_THRESH_CROSSED_E = c_int(8)
A_PHY_NORMAL_PER_THRESH_CROSSED_E = c_int(9)
A_PHY_CABLE_DIAG_DONE_E = c_int(10)
A_PHY_PACKET_FAILURE_DETECTED_E = c_int(11)
A_PHY_BIST_END_TRAFFIC_E = c_int(12)
A_PHY_NO_KEEP_ALIVE_ERR_E = c_int(13)
A_PHY_ACMD_PATCH_REG_FREE_E = c_int(14)
A_PHY_ACMD_RETURN_TO_DEFAULT_E = c_int(15)
A_PHY_RETRAIN_COND_FAILED_E = c_int(16)
A_PHY_RTS_ALARM_E = c_int(17)
A_PHY_ENTER_COORDINATED_SLEEP_E = c_int(18)
A_PHY_RTS_ALARM_HEAL_E = c_int(19)
A_PHY_BIST_RCV_WRONG_E = c_int(20)
A_PHY_MISSING_PKT_ERROR_E = c_int(21)

# APhyNofiticationBitmaskEnum
A_PHY_BITMASK_READY_IND_E = c_int(2)
A_PHY_BITMASK_LINK_UP_E = c_int(4)
A_PHY_BITMASK_LINK_DOWN_E = c_int(8)
A_PHY_BITMASK_POOR_LINK_QUALITY_E = c_int(16)
A_PHY_BITMASK_ENTER_SLEEP_ON_START_UP_E = c_int(32)
A_PHY_BITMASK_ENTER_TEST_MODE_E = c_int(64)
A_PHY_BITMASK_BIST_PER_THRESH_CROSSED_E = c_int(128)
A_PHY_BITMASK_BIST_BER_THRESH_CROSSED_E = c_int(256)
A_PHY_BITMASK_NORMAL_PER_THRESH_CROSSED_E = c_int(512)
A_PHY_BITMASK_CABLE_DIAG_DONE_E = c_int(1024)
A_PHY_BITMASK_PACKET_FAILURE_DETECTED_E = c_int(2048)
A_PHY_BITMASK_BIST_END_TRAFFIC_E = c_int(4096)
A_PHY_BITMASK_NO_KEEP_ALIVE_ERR_E = c_int(8192)
A_PHY_BITMASK_ACMD_PATCH_REG_FREE_E = c_int(16384)
A_PHY_BITMASK_ACMD_RETURN_TO_DEFAULT_E = c_int(32768)
A_PHY_BITMASK_RETRAIN_COND_FAILED_E = c_int(65536)
A_PHY_BITMASK_RTS_ALARM_E = c_int(131072)
A_PHY_BITMASK_ENTER_COORDINATED_SLEEP_E = c_int(262144)
A_PHY_BITMASK_RTS_ALARM_HEAL_E = c_int(524288)
A_PHY_BITMASK_BIST_RCV_WRONG_E = c_int(1048576)
A_PHY_BITMASK_MISSING_PKT_ERROR_E = c_int(2097152)

# Rclk7031NotificationIdEnum
RCLK_MN_ZERO_E = c_int(0)
RCLK_MN_CHANGE_E = c_int(1)
RCLK_MN_STEADY_E = c_int(2)
RCLK_READ_FIFO_E = c_int(3)
RCLK_CLOCK_TYPE_VALID_E = c_int(4)
RCLK_MIS_CLK_PKT_EVT_E = c_int(5)
RCLK_PKT_PARSE_ERROR_E = c_int(6)

# Rclk7031NotificationBitmaskEnum
RCLK_BITMASK_MN_ZERO_E = c_int(1)
RCLK_BITMASK_MN_CHANGE_E = c_int(2)
RCLK_BITMASK_MN_STEADY_E = c_int(4)
RCLK_BITMASK_READ_FIFO_E = c_int(8)
RCLK_BITMASK_CLOCK_TYPE_VALID_E = c_int(16)
RCLK_BITMASK_MIS_CLK_PKT_EVT_E = c_int(32)
RCLK_BITMASK_PKT_PARSE_ERROR_E = c_int(64)

# Rclk7044NotificationIdEnum
RCLK_VALIDOWN_INTR_E = c_int(0)
RCLK_PKT_OF_INTR = c_int(1)

# Rclk7044NotificationBitmaskEnum
RCLK_BITMASK_VALIDOWN_INTR_E = c_int(1)
RCLK_BITMASK_PKT_OF_INTR_E = c_int(2)

# MsioNotifyBitmaskEnum
MSIO_BITMASK_TX_FIFO_UNDERFLOW_E = c_int(1)
MSIO_BITMASK_TX_FIFO_OVERFLOW_E = c_int(2)
MSIO_BITMASK_RX_FIFO_UNDERFLOW_E = c_int(4)
MSIO_BITMASK_RX_FIFO_OVERFLOW_E = c_int(8)
MSIO_BITMASK_VALIDOWN_INT_E = c_int(16)
MSIO_BITMASK_APKT_PARSE_ERROR_E = c_int(32)
MSIO_BITMASK_MSIO_DATA_UPDATE_E = c_int(64)
MSIO_BITMASK_TS_ERR_E = c_int(128)
MSIO_BITMASK_MSIO_DATA_0_E = c_int(256)
MSIO_BITMASK_MSIO_DATA_1_E = c_int(512)
MSIO_BITMASK_MSIO_DATA_2_E = c_int(1024)
MSIO_BITMASK_MSIO_DATA_3_E = c_int(2048)
MSIO_BITMASK_MSIO_DATA_4_E = c_int(4096)
MSIO_BITMASK_MSIO_DATA_5_E = c_int(8192)
MSIO_BITMASK_MSIO_DATA_6_E = c_int(16384)
MSIO_BITMASK_MSIO_DATA_7_E = c_int(32768)
MSIO_BITMASK_MSIO_DATA_8_E = c_int(65536)
MSIO_BITMASK_MSIO_DATA_9_E = c_int(131072)
MSIO_BITMASK_MSIO_DATA_10_E = c_int(262144)
MSIO_BITMASK_MSIO_DATA_11_E = c_int(524288)
MSIO_BITMASK_MSIO_DATA_12_E = c_int(1048576)
MSIO_BITMASK_MSIO_DATA_13_E = c_int(2097152)
MSIO_BITMASK_MSIO_DATA_14_E = c_int(4194304)
MSIO_BITMASK_MSIO_DATA_15_E = c_int(8388608)

# BistNotifyBitmaskEnum
BIST_RX_NOTIFY_BITMASK_APKT_PARSE_ERROR_E = c_int(1)
BIST_TX_NOTIFY_BITMASK_VALIDOWN_E = c_int(2)
BIST_NOTIFY_BITMASK_BER_VAL_E = c_int(4)
BIST_NOTIFY_BITMASK_PER_VAL_E = c_int(8)
BIST_RX_NOTIFY_BITMASK_REMOTE_SLEEP_TO_E = c_int(16)
BIST_RX_NOTIFY_BITMASK_REMOTE_SLEEP_PKT_RCV_E = c_int(32)

class NotificationIdUnion(Structure):
    _fields_ = [("rawU32", c_uint),
                ("aphy", c_int),
                ("mng", c_int),
                ("msio", c_int),
                ("bist", c_int),
                ("rclk", c_int),
                ("rclk7044", c_int)]

class NotificationInfo(Structure):
    _fields_ = [("blockId", c_int),
                ("blockIfNum", c_uint),
                ("notifications", c_uint)]

SyncCallback = CFUNCTYPE(c_void_p, c_void_p)

SyncCallbackLinkError = CFUNCTYPE(c_void_p, c_void_p, c_int, c_uint)

SyncCallbackLinkDown = CFUNCTYPE(c_void_p, c_void_p, c_int)

class SyncCallbacks(Structure):
    _fields_ = [("pArg", c_void_p),
                ("idle", SyncCallback),
                ("error", SyncCallback),
                ("linkError", SyncCallbackLinkError),
                ("linkDown", SyncCallbackLinkDown),
                ("fwInitDone", SyncCallback)]

# SyncFsmSignalEnum
SYNC_SIGNAL_NONE = c_int(0)
SYNC_SIGNAL_BOOT = c_int(1)
SYNC_SIGNAL_RESET = c_int(2)
SYNC_SIGNAL_WAIT_FOR_HOST = c_int(3)
SYNC_SIGNAL_FW_INIT_DONE = c_int(4)
SYNC_SIGNAL_LINK_UP = c_int(5)
SYNC_SIGNAL_MN_STEADY = c_int(6)
SYNC_SIGNAL_GOTO_IDLE = c_int(7)
SYNC_SIGNAL_GOTO_ERROR = c_int(8)

# SyncFsmStateEnum
SYNC_STATE_BOOT = c_int(0)
SYNC_STATE_RESET = c_int(1)
SYNC_STATE_WAIT4HOST = c_int(2)
SYNC_STATE_INIT_7044 = c_int(3)
SYNC_STATE_ACTIVATE_STEADY_CONDITION = c_int(4)
SYNC_STATE_MN_STEADY_HANDLING = c_int(5)
SYNC_STATE_IDLE = c_int(6)
SYNC_STATE_ERROR = c_int(7)

class FsmInput(Structure):
    _fields_ = [("signal", c_int),
                ("service", c_int)]

class FsmInputsQueue(Structure):
    _fields_ = [("mutex", c_void_p),
                ("cond", c_void_p),
                ("data", FsmInput * 16),
                ("head", c_ulonglong),
                ("tail", c_ulonglong),
                ("count", c_ulonglong)]

class DevHostSync(Structure):
    _fields_ = [("isRunning", c_bool),
                ("thread", c_void_p),
                ("callbacks", SyncCallbacks),
                ("local", c_int),
                ("remote", c_int * 4),
                ("prevState", c_int),
                ("currentState", c_int),
                ("fsmQueue", FsmInputsQueue)]

# VlnsVersionTypeEnum
ALL_VERSIONS_E = c_int(0)
APP_VERSION_E = c_int(1)
LIB_VERSION_E = c_int(2)
DRV_VERSION_E = c_int(3)
FW_VERSION_E = c_int(4)
MAX_VERSION_E = c_int(5)

class VlnsVersion(Structure):
    _fields_ = [("appVer", c_char * 32),
                ("libVer", c_char * 32),
                ("drvVer", c_char * 32),
                ("fwVer", c_char * 32)]

# RegisterOpEnum
REGISTER_OP_UNREGISTER_E = c_int(0)
REGISTER_OP_REGISTER_E = c_int(1)

# HostStateEnum
HOST_BOOT_STATE_E = c_int(0)
HOST_FW_LOAD_STATE_E = c_int(1)
HOST_INIT_STATE_E = c_int(2)
HOST_OPERATIONAL_STATE_E = c_int(3)
HOST_RESET_STATE_E = c_int(4)

# DeviceStateEnum
DEV_BOOT_STATE_E = c_int(0)
DEV_SW_PROTOCOL_STATE_E = c_int(1)
DEV_INIT_STATE_E = c_int(2)
DEV_OPERATIONAL_STATE_E = c_int(3)
DEV_SLEEP_STATE_E = c_int(4)
DEV_ERROR_STATE_E = c_int(5)

# LinkStateEnum
LINK_STATE_UNKNOWN_ERROR_E = c_int(0)
LINK_STATE_POWER_UP_E = c_int(1)
LINK_STATE_START_UP_E = c_int(2)
LINK_STATE_SLEEP_E = c_int(3)
LINK_STATE_NORMAL_E = c_int(4)
LINK_STATE_RESERVED_E = c_int(5)
LINK_STATE_RESERVED2_E = c_int(6)
LINK_STATE_TEST_E = c_int(7)
LINK_STATE_MAX_E = c_int(8)

# LinkQualityLevelEnum
LINK_QUALITY_NO_E = c_int(0)
LINK_QUALITY_BAD_E = c_int(1)
LINK_QUALITY_MARGINAL_BAD_E = c_int(2)
LINK_QUALITY_MARGINAL_GOOD_E = c_int(3)
LINK_QUALITY_GOOD_E = c_int(4)
LINK_QUALITY_EXCELLENT_E = c_int(5)
LINK_QUALITY_MAX_E = c_int(6)

# LinkPortGearEnum
LINK_PORT_GEAR_1_E = c_int(1)
LINK_PORT_GEAR_2_E = c_int(2)
LINK_PORT_GEAR_3_E = c_int(3)
LINK_PORT_GEAR_MAX_E = c_int(4)

# LinkPortCodingEnum
LINK_PORT_CODING_NRZ_E = c_int(0)
LINK_PORT_CODING_PAM4_E = c_int(1)
LINK_PORT_CODING_MAX_E = c_int(2)

class APhyPortLinkInfo(Structure):
    _fields_ = [("state", c_int),
                ("quality", c_int)]

class APhyPortConfig(Structure):
    _fields_ = [("gear", c_int),
                ("coding", c_int),
                ("downLinkRetransEnabled", c_bool)]

class LinkRxCounters(Structure):
    _fields_ = [("nrmlGood", c_ulonglong),
                ("origGood", c_ulonglong),
                ("total", c_ulonglong)]

class RegInfo(Structure):
    _fields_ = [("address", c_uint),
                ("mask", c_uint),
                ("value", c_uint)]

class VlnsAPhySdk(object):
    def __init__(self, libpath=None):
        
        if libpath is None:
            is_linux = lambda: True if platform.system() == "Linux" else False            
            libpath = "{0}libvalens_aphy.{1}".format("./" if is_linux() else "", "so" if is_linux() else "dll")
            abs_path = os.path.dirname(os.path.abspath(__file__))+'/'
            libpath = "{0}libvalens_aphy.{1}".format(abs_path if is_linux() else "", "so" if is_linux() else "dll")
            print('------------------',libpath)
        lib = cdll.LoadLibrary(libpath)

        #**************************************
        # valens_aphy.h
        #**************************************

        self.valens_aphy_init = lib.valens_aphy_init
        self.valens_aphy_init.argtypes = [c_bool]
        self.valens_aphy_init.restype = c_bool

        self.valens_aphy_destroy = lib.valens_aphy_destroy
        self.valens_aphy_destroy.restype = c_bool

        self.aphy_sdk_version = lib.aphy_sdk_version
        self.aphy_sdk_version.restype = APhySdkVersion

        #**************************************
        # app/core/app_transport.h
        #**************************************

        self.app_transport_init_subsystem = lib.app_transport_init_subsystem
        self.app_transport_init_subsystem.argtypes = [c_bool]
        self.app_transport_init_subsystem.restype = c_int

        self.app_transport_destroy_subsystem = lib.app_transport_destroy_subsystem
        self.app_transport_destroy_subsystem.restype = c_int

        self.app_transport_get_or_create = lib.app_transport_get_or_create
        self.app_transport_get_or_create.argtypes = [c_char_p,c_int,POINTER(c_int)]
        self.app_transport_get_or_create.restype = c_void_p

        self.app_transport_destroy = lib.app_transport_destroy
        self.app_transport_destroy.argtypes = [c_void_p]
        self.app_transport_destroy.restype = c_int

        self.app_transport_transaction_timeout = lib.app_transport_transaction_timeout
        self.app_transport_transaction_timeout.argtypes = [c_void_p,c_uint]
        self.app_transport_transaction_timeout.restype = c_int

        self.app_transport_send = lib.app_transport_send
        self.app_transport_send.argtypes = [c_void_p,POINTER(c_byte),c_ulonglong]
        self.app_transport_send.restype = c_int

        self.app_transport_receive = lib.app_transport_receive
        self.app_transport_receive.argtypes = [c_void_p,POINTER(c_byte),c_ulonglong,POINTER(c_ulonglong),c_int]
        self.app_transport_receive.restype = c_int

        self.app_transport_run_transaction = lib.app_transport_run_transaction
        self.app_transport_run_transaction.argtypes = [c_void_p,c_ushort,POINTER(c_byte),c_ulonglong,POINTER(c_byte),c_ulonglong,POINTER(c_ulonglong),POINTER(TransactionStatus)]
        self.app_transport_run_transaction.restype = c_bool

        self.app_transport_fusa_run_transaction = lib.app_transport_fusa_run_transaction
        self.app_transport_fusa_run_transaction.argtypes = [c_void_p,c_int,c_ushort,POINTER(c_byte),c_ulonglong,POINTER(c_byte),c_ulonglong,POINTER(c_ulonglong),POINTER(TransactionStatus)]
        self.app_transport_fusa_run_transaction.restype = c_bool

        self.app_transport_get_events = lib.app_transport_get_events
        self.app_transport_get_events.argtypes = [c_void_p,c_void_p,c_ulonglong,POINTER(c_ulonglong)]
        self.app_transport_get_events.restype = c_int

        self.event_manager_subscribe = lib.event_manager_subscribe
        self.event_manager_subscribe.argtypes = [c_void_p,c_void_p]
        self.event_manager_subscribe.restype = c_int

        self.event_manager_unsubscribe = lib.event_manager_unsubscribe
        self.event_manager_unsubscribe.argtypes = [c_void_p,c_void_p]
        self.event_manager_unsubscribe.restype = c_int

        self.app_transport_get_service = lib.app_transport_get_service
        self.app_transport_get_service.argtypes = [c_void_p]
        self.app_transport_get_service.restype = c_int

        self.get_transport_status_info = lib.get_transport_status_info
        self.get_transport_status_info.argtypes = [c_int]
        self.get_transport_status_info.restype = c_char_p

        self.get_host_status_info = lib.get_host_status_info
        self.get_host_status_info.argtypes = [c_int]
        self.get_host_status_info.restype = c_char_p

        self.event_get_name = lib.event_get_name
        self.event_get_name.argtypes = [c_int]
        self.event_get_name.restype = c_char_p

        self.device_to_service = lib.device_to_service
        self.device_to_service.argtypes = [c_int]
        self.device_to_service.restype = c_int

        self.get_service_name = lib.get_service_name
        self.get_service_name.argtypes = [c_int]
        self.get_service_name.restype = c_char_p

        self.vlns_proc_id_is_7044 = lib.vlns_proc_id_is_7044
        self.vlns_proc_id_is_7044.argtypes = [c_int]
        self.vlns_proc_id_is_7044.restype = c_bool

        self.vlns_proc_id_is_7031 = lib.vlns_proc_id_is_7031
        self.vlns_proc_id_is_7031.argtypes = [c_int]
        self.vlns_proc_id_is_7031.restype = c_bool

        self.vlns_proc_id_has_sink = lib.vlns_proc_id_has_sink
        self.vlns_proc_id_has_sink.argtypes = [c_int]
        self.vlns_proc_id_has_sink.restype = c_bool

        self.vlns_proc_id_has_source = lib.vlns_proc_id_has_source
        self.vlns_proc_id_has_source.argtypes = [c_int]
        self.vlns_proc_id_has_source.restype = c_bool

        #**************************************
        # app/core/notifications.h
        #**************************************

        self.notifications_format_aphy_bitmask = lib.notifications_format_aphy_bitmask
        self.notifications_format_aphy_bitmask.argtypes = [c_char_p,c_ulonglong,c_int,c_char_p,c_bool]
        self.notifications_format_aphy_bitmask.restype = c_bool

        self.notifications_format_rclk7031_bitmask = lib.notifications_format_rclk7031_bitmask
        self.notifications_format_rclk7031_bitmask.argtypes = [c_char_p,c_ulonglong,c_int,c_char_p,c_bool]
        self.notifications_format_rclk7031_bitmask.restype = c_bool

        self.notifications_format_rclk7044_bitmask = lib.notifications_format_rclk7044_bitmask
        self.notifications_format_rclk7044_bitmask.argtypes = [c_char_p,c_ulonglong,c_int,c_char_p,c_bool]
        self.notifications_format_rclk7044_bitmask.restype = c_bool

        self.notifications_get_block_if_num_count = lib.notifications_get_block_if_num_count
        self.notifications_get_block_if_num_count.argtypes = [c_int,c_int]
        self.notifications_get_block_if_num_count.restype = c_uint

        self.notifications_format_notification_id_union = lib.notifications_format_notification_id_union
        self.notifications_format_notification_id_union.argtypes = [c_char_p,c_ulonglong,c_int,c_uint,c_int,c_char_p,c_bool]
        self.notifications_format_notification_id_union.restype = c_bool

        self.parse_notification = lib.parse_notification
        self.parse_notification.argtypes = [POINTER(c_byte),c_ulonglong,POINTER(NotificationInfo)]

        self.serialize_notification = lib.serialize_notification
        self.serialize_notification.argtypes = [POINTER(NotificationInfo),POINTER(c_byte),c_ulonglong,POINTER(c_ulonglong)]

        #**************************************
        # app/client/aphy_client.h
        #**************************************

        self.aphy_client_create = lib.aphy_client_create
        self.aphy_client_create.argtypes = [c_char_p]
        self.aphy_client_create.restype = c_void_p

        self.aphy_client_destroy = lib.aphy_client_destroy
        self.aphy_client_destroy.argtypes = [c_void_p]

        self.aphy_client_get_transport = lib.aphy_client_get_transport
        self.aphy_client_get_transport.argtypes = [c_void_p,c_int]
        self.aphy_client_get_transport.restype = c_void_p

        self.aphy_client_get_fifo = lib.aphy_client_get_fifo
        self.aphy_client_get_fifo.argtypes = [c_void_p]
        self.aphy_client_get_fifo.restype = c_void_p

        self.aphy_client_get_rif = lib.aphy_client_get_rif
        self.aphy_client_get_rif.argtypes = [c_void_p]
        self.aphy_client_get_rif.restype = c_void_p

        self.aphy_client_ready = lib.aphy_client_ready
        self.aphy_client_ready.argtypes = [c_void_p,c_int]
        self.aphy_client_ready.restype = c_bool

        self.aphy_client_close = lib.aphy_client_close
        self.aphy_client_close.argtypes = [c_void_p,c_int]
        self.aphy_client_close.restype = c_bool

        self.aphy_client_register_to_events = lib.aphy_client_register_to_events
        self.aphy_client_register_to_events.argtypes = [c_void_p,c_int]
        self.aphy_client_register_to_events.restype = c_bool

        self.aphy_client_unregister_to_events = lib.aphy_client_unregister_to_events
        self.aphy_client_unregister_to_events.argtypes = [c_void_p,c_int]
        self.aphy_client_unregister_to_events.restype = c_bool

        self.aphy_client_set_event_callback = lib.aphy_client_set_event_callback
        self.aphy_client_set_event_callback.argtypes = [c_void_p,c_int,c_int, EventHandlerFunc]
        self.aphy_client_set_event_callback.restype = c_bool

        self.aphy_client_subscribe_to_notification = lib.aphy_client_subscribe_to_notification
        self.aphy_client_subscribe_to_notification.argtypes = [c_void_p,c_int,POINTER(NotificationInfo)]
        self.aphy_client_subscribe_to_notification.restype = c_bool

        self.aphy_client_unsubscribe_from_notification = lib.aphy_client_unsubscribe_from_notification
        self.aphy_client_unsubscribe_from_notification.argtypes = [c_void_p,c_int,POINTER(NotificationInfo)]
        self.aphy_client_unsubscribe_from_notification.restype = c_bool

        self.aphy_client_get_states = lib.aphy_client_get_states
        self.aphy_client_get_states.argtypes = [c_void_p,c_int,POINTER(c_int),POINTER(c_int),POINTER(c_int)]
        self.aphy_client_get_states.restype = c_bool

        self.aphy_client_set_state = lib.aphy_client_set_state
        self.aphy_client_set_state.argtypes = [c_void_p,c_int,c_int]
        self.aphy_client_set_state.restype = c_bool

        self.aphy_client_activate_rclk_in = lib.aphy_client_activate_rclk_in
        self.aphy_client_activate_rclk_in.argtypes = [c_void_p,c_int,c_int]
        self.aphy_client_activate_rclk_in.restype = c_bool

        self.aphy_client_activate_rclk_out = lib.aphy_client_activate_rclk_out
        self.aphy_client_activate_rclk_out.argtypes = [c_void_p,c_int]
        self.aphy_client_activate_rclk_out.restype = c_bool

        self.aphy_client_activate_msio = lib.aphy_client_activate_msio
        self.aphy_client_activate_msio.argtypes = [c_void_p,c_int,c_int]
        self.aphy_client_activate_msio.restype = c_bool

        self.aphy_client_run_i2c_reset = lib.aphy_client_run_i2c_reset
        self.aphy_client_run_i2c_reset.argtypes = [c_void_p,c_int,c_int,c_int]
        self.aphy_client_run_i2c_reset.restype = c_bool

        #**************************************
        # app/client/aphy_client_sync.h
        #**************************************

        self.dev_host_sync_start = lib.dev_host_sync_start
        self.dev_host_sync_start.argtypes = [c_void_p,POINTER(SyncCallbacks)]
        self.dev_host_sync_start.restype = c_bool

        self.dev_host_sync_is_running = lib.dev_host_sync_is_running
        self.dev_host_sync_is_running.argtypes = [c_void_p]
        self.dev_host_sync_is_running.restype = c_bool

        self.dev_host_sync_stop = lib.dev_host_sync_stop
        self.dev_host_sync_stop.argtypes = [c_void_p]

        self.dev_host_sync_set_callbacks = lib.dev_host_sync_set_callbacks
        self.dev_host_sync_set_callbacks.argtypes = [c_void_p,c_int]

        #**************************************
        # app/client/aphy_client_sync_types.h
        #**************************************

        self.fsm_queue_init = lib.fsm_queue_init
        self.fsm_queue_init.argtypes = [POINTER(FsmInputsQueue)]

        self.fsm_queue_close = lib.fsm_queue_close
        self.fsm_queue_close.argtypes = [POINTER(FsmInputsQueue)]

        self.fsm_queue_push = lib.fsm_queue_push
        self.fsm_queue_push.argtypes = [POINTER(FsmInputsQueue),FsmInput]
        self.fsm_queue_push.restype = c_bool

        self.fsm_queue_pop = lib.fsm_queue_pop
        self.fsm_queue_pop.argtypes = [POINTER(FsmInputsQueue),POINTER(FsmInput),c_uint]
        self.fsm_queue_pop.restype = c_bool

        self.fsm_queue_peek = lib.fsm_queue_peek
        self.fsm_queue_peek.argtypes = [POINTER(FsmInputsQueue),POINTER(FsmInput),c_uint]
        self.fsm_queue_peek.restype = c_bool

        #**************************************
        # app/api/general_api.h
        #**************************************

        self.app_client_ready = lib.app_client_ready
        self.app_client_ready.argtypes = [c_void_p,POINTER(TransactionStatus)]
        self.app_client_ready.restype = c_bool

        self.app_client_close = lib.app_client_close
        self.app_client_close.argtypes = [c_void_p,POINTER(TransactionStatus)]
        self.app_client_close.restype = c_bool

        self.app_set_state = lib.app_set_state
        self.app_set_state.argtypes = [c_void_p,c_int,POINTER(TransactionStatus)]
        self.app_set_state.restype = c_bool

        self.app_get_states = lib.app_get_states
        self.app_get_states.argtypes = [c_void_p,POINTER(c_int),POINTER(c_int),POINTER(c_int),POINTER(TransactionStatus)]
        self.app_get_states.restype = c_bool

        self.app_get_version = lib.app_get_version
        self.app_get_version.argtypes = [c_void_p,c_int,POINTER(VlnsVersion),POINTER(TransactionStatus)]
        self.app_get_version.restype = c_bool

        self.app_register_events = lib.app_register_events
        self.app_register_events.argtypes = [c_void_p,c_int,c_uint,POINTER(TransactionStatus)]
        self.app_register_events.restype = c_bool

        self.app_init_fifo = lib.app_init_fifo
        self.app_init_fifo.argtypes = [c_void_p,POINTER(TransactionStatus)]
        self.app_init_fifo.restype = c_bool

        self.app_init_fw_prog = lib.app_init_fw_prog
        self.app_init_fw_prog.argtypes = [c_void_p,c_int,c_byte,POINTER(TransactionStatus)]
        self.app_init_fw_prog.restype = c_bool

        self.app_next_fw_prog = lib.app_next_fw_prog
        self.app_next_fw_prog.argtypes = [c_void_p,POINTER(c_byte),c_ushort,POINTER(TransactionStatus)]
        self.app_next_fw_prog.restype = c_bool

        self.app_end_fw_prog = lib.app_end_fw_prog
        self.app_end_fw_prog.argtypes = [c_void_p,POINTER(TransactionStatus)]
        self.app_end_fw_prog.restype = c_bool

        self.app_read_registers = lib.app_read_registers
        self.app_read_registers.argtypes = [c_void_p,POINTER(RegInfo),c_uint,POINTER(TransactionStatus)]
        self.app_read_registers.restype = c_bool

        self.app_write_registers = lib.app_write_registers
        self.app_write_registers.argtypes = [c_void_p,POINTER(RegInfo),c_uint,POINTER(TransactionStatus)]
        self.app_write_registers.restype = c_bool

        self.app_read_acmd_registers = lib.app_read_acmd_registers
        self.app_read_acmd_registers.argtypes = [c_void_p,c_uint,c_uint,POINTER(c_uint),POINTER(TransactionStatus)]
        self.app_read_acmd_registers.restype = c_bool

        self.app_write_acmd_registers = lib.app_write_acmd_registers
        self.app_write_acmd_registers.argtypes = [c_void_p,c_uint,c_uint,POINTER(c_uint),POINTER(TransactionStatus)]
        self.app_write_acmd_registers.restype = c_bool

        self.app_read_fifo = lib.app_read_fifo
        self.app_read_fifo.argtypes = [c_void_p,c_uint,c_uint,POINTER(c_byte),POINTER(TransactionStatus)]
        self.app_read_fifo.restype = c_bool

        self.app_write_fifo = lib.app_write_fifo
        self.app_write_fifo.argtypes = [c_void_p,c_uint,c_uint,POINTER(c_byte),POINTER(TransactionStatus)]
        self.app_write_fifo.restype = c_bool

        self.app_subscribe_to_notification = lib.app_subscribe_to_notification
        self.app_subscribe_to_notification.argtypes = [c_void_p,POINTER(NotificationInfo),POINTER(TransactionStatus)]
        self.app_subscribe_to_notification.restype = c_bool

        self.app_unsubscribe_to_notification = lib.app_unsubscribe_to_notification
        self.app_unsubscribe_to_notification.argtypes = [c_void_p,POINTER(NotificationInfo),POINTER(TransactionStatus)]
        self.app_unsubscribe_to_notification.restype = c_bool

        self.app_clear_notification = lib.app_clear_notification
        self.app_clear_notification.argtypes = [c_void_p,POINTER(NotificationInfo),POINTER(TransactionStatus)]
        self.app_clear_notification.restype = c_bool

        #**************************************
        # app/api/link_api.h
        #**************************************

        self.link_get_info = lib.link_get_info
        self.link_get_info.argtypes = [c_void_p,c_int,POINTER(APhyPortLinkInfo),POINTER(TransactionStatus)]
        self.link_get_info.restype = c_bool

        self.link_get_port_config = lib.link_get_port_config
        self.link_get_port_config.argtypes = [c_void_p,c_int,POINTER(APhyPortConfig),POINTER(TransactionStatus)]
        self.link_get_port_config.restype = c_bool

        self.link_get_uplink_retransmission = lib.link_get_uplink_retransmission
        self.link_get_uplink_retransmission.argtypes = [c_void_p,c_int,POINTER(c_bool),POINTER(TransactionStatus)]
        self.link_get_uplink_retransmission.restype = c_bool

        self.link_get_rx_counters = lib.link_get_rx_counters
        self.link_get_rx_counters.argtypes = [c_void_p,c_int,POINTER(LinkRxCounters),POINTER(TransactionStatus)]
        self.link_get_rx_counters.restype = c_bool

        self.link_get_tx_counter = lib.link_get_tx_counter
        self.link_get_tx_counter.argtypes = [c_void_p,POINTER(c_uint),POINTER(TransactionStatus)]
        self.link_get_tx_counter.restype = c_bool

        self.reset_bad_link = lib.reset_bad_link
        self.reset_bad_link.argtypes = [c_void_p,c_int,POINTER(TransactionStatus)]
        self.reset_bad_link.restype = c_bool


    @staticmethod
    def get_version():
        return "1.0.22 (Generated: 28.01.2022 16.58.59)"

    def check_status(self, message, status: TransactionStatus):
        if (status.transportStatus != APP_TRANSPORT_SUCCESS_E.value) or (status.hostStatus != HOST_STATUS_SUCCESS_E.value):
            transMsg = self.get_transport_status_info(status.transportStatus)
            hostMsg = self.get_host_status_info(status.hostStatus)
            raise Exception("{0} - ({1}, {2})".format(message, transMsg, hostMsg))
