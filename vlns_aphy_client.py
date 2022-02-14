from vlns_aphy_wrapper import *
import ctypes


class VlnsAPhyClient(object):
    def __init__(self, libpath, remote):
        self.sdk = VlnsAPhySdk(libpath)
        self.remote = remote.encode('utf-8') if remote is not None else None

        sdk_version = self.sdk.aphy_sdk_version()
        print("*****************************************************************")
        print("Py Wrapper: {0} [APhySdk: {1}]".format(VlnsAPhySdk.get_version(), sdk_version.versionString))
        print("*****************************************************************")

        status = self.sdk.valens_aphy_init(True)
        if not status:
            raise Exception("Failed to init library '{0}'".format(self.sdk))

        self.client = self.sdk.aphy_client_create(self.remote)

    @staticmethod
    def create(libpath=None, remote=None):
        instance = VlnsAPhyClient(libpath, remote)       
        return instance

    def destroy(self):        
        self.sdk.aphy_client_destroy(self.client)

        destroy_result = self.sdk.valens_aphy_destroy()
        if not destroy_result:
            print("Failed to destroy library '{0}'".format(self.sdk))
    

    def print_service_versions(self, services:[]):
        for i in range(0, len(services)):
            transport_status = APP_TRANSPORT_SUCCESS_E
            transport = self.sdk.app_transport_get_or_create(self.remote, services[i], byref(transport_status))
            if transport_status.value != APP_TRANSPORT_SUCCESS_E.value:
                raise Exception("Failed to get or create app transport - {0}".format(transport_status))

            vlnsVer = VlnsVersion()
            status = TransactionStatus()
            self.sdk.app_get_version(transport, ALL_VERSIONS_E, byref(vlnsVer), byref(status))
            self.sdk.check_status("Failed to get versions of components", status)

            print("Service: {0} ***********************************".format(services[i].value))
            print("App Ver: {0}".format(vlnsVer.appVer))
            print("Lib Ver: {0}".format(vlnsVer.libVer))
            print("Drv Ver: {0}".format(vlnsVer.drvVer))
            print("FW  Ver: {0}".format(vlnsVer.fwVer))

    
    """
    Run device-host synchronization flow and waiting for system is ready.
    TODO: Implement the waiting functionality. It's not suported right now.
    """
    def run_device_host_sync(self, callbacksArg:SyncCallbacks=None, wait_timeout_seconds=10):

        if callbacksArg is None:
            self.current_callbacks = SyncCallbacks()
            self.current_callbacks.pArg = self.client
            self.current_callbacks.idle = SyncCallback(self.idle_callback)
            self.current_callbacks.error = SyncCallback(self.error_callback)
            self.current_callbacks.linkError = SyncCallbackLinkError(self.link_error_callback)
            self.current_callbacks.linkDown = SyncCallbackLinkDown(self.link_down_callback)
            self.current_callbacks.fwInitDone = SyncCallback(self.fw_init_done_callback)
        else:
            self.current_callbacks = SyncCallbacks()

        self.sdk.dev_host_sync_start(self.client, self.current_callbacks)
        time.sleep(wait_timeout_seconds)


    def idle_callback(self, pArg):
        print("Python 'idle_callback'")

    def error_callback(pArg):
        print("Python 'error_callback'")

    def link_error_callback(pArg, service, code):
        print("Python 'link_error_callback'")

    def link_down_callback(pArg, service):
        print("Python 'link_down_callback'")

    def fw_init_done_callback(pArg):
        print("Python 'fw_init_done_callback'")



    """
    Read RIF register
    """
    def read_rif_reg(self, serviceId, reg_address):

        rif_regs = (RegInfo * 1)()
        regs_array = ctypes.cast(rif_regs, ctypes.POINTER(RegInfo))
        regs_array[0].address = reg_address

        transport_status = APP_TRANSPORT_SUCCESS_E
        transport = self.sdk.app_transport_get_or_create(self.remote, serviceId, byref(transport_status))
        if transport_status.value != APP_TRANSPORT_SUCCESS_E.value:
            raise Exception("Failed to get or create app transport - {0}".format(transport_status))

        status = TransactionStatus()
        result = self.sdk.app_read_registers(transport, regs_array, c_uint(1), byref(status))
        if not result:
            self.sdk.check_status("Failed to read RIF reg", status)

        return regs_array[0].value


    """
    Write RIF register
    """
    def write_rif_reg(self, serviceId, reg_address, reg_value):

        rif_regs = (RegInfo * 1)()
        regs_array = ctypes.cast(rif_regs, ctypes.POINTER(RegInfo))
        regs_array[0].address = reg_address
        regs_array[0].value = reg_value

        transport_status = APP_TRANSPORT_SUCCESS_E
        transport = self.sdk.app_transport_get_or_create(self.remote, serviceId, byref(transport_status))
        if transport_status.value != APP_TRANSPORT_SUCCESS_E.value:
            raise Exception("Failed to get or create app transport - {0}".format(transport_status))

        status = TransactionStatus()
        result = self.sdk.app_write_registers(transport, regs_array, c_uint(1), byref(status))
        if not result:
            self.sdk.check_status("Failed to write RIF reg", status)


    """
    Read ACMD registers
    """
    def read_acmd_regs(self, serviceId, count_of_regs, start_address, regs_array):

        transport_status = APP_TRANSPORT_SUCCESS_E
        transport = self.sdk.app_transport_get_or_create(self.remote, serviceId, byref(transport_status))
        if transport_status.value != APP_TRANSPORT_SUCCESS_E.value:
            raise Exception("Failed to get or create app transport - {0}".format(transport_status))

        status = TransactionStatus()
        result = self.sdk.app_read_acmd_registers(transport, count_of_regs, start_address, regs_array, byref(status))
        if result is False:
            self.sdk.check_status("Failed to read ACMD regs", status)

    """
    Write ACMD registers
    """
    def write_acmd_regs(self, serviceId, count_of_regs, start_address, regs_array):

        transport_status = APP_TRANSPORT_SUCCESS_E
        transport = self.sdk.app_transport_get_or_create(self.remote, serviceId, byref(transport_status))
        if transport_status.value != APP_TRANSPORT_SUCCESS_E.value:
            raise Exception("Failed to get or create app transport - {0}".format(transport_status))

        status = TransactionStatus()
        result = self.sdk.app_write_acmd_registers(transport, count_of_regs, start_address, regs_array, byref(status))
        if result is False:
            self.sdk.check_status("Failed to write ACMD regs", status)
