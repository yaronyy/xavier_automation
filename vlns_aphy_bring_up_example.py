from vlns_aphy_wrapper import *
from vlns_aphy_client import *
from vlns_aphy_utils import *
import vlns_aphy_config as CFG


if __name__ == "__main__":
    start_time = datetime.datetime.now()    
    
    client = None

    try:
        
        """
        Creating APhy Python Client to access to Apps functionality.
        To work with remote server use the 'remote' arg:
        client = VlnsAPhyClient.create(remote="172.23.8.185")
        """
        client = VlnsAPhyClient.create(remote=CFG.REMOTE_MACHINE)

        """
        Start Device Host Sync flow
        """
        client.run_device_host_sync(wait_timeout_seconds=5)

        
        """
        Print verions of all components of VA7044 service
        """
        client.print_service_versions([PROC_DEV_7044_0_E])
        
        
        """
        Read Version register
        """
        version_reg_value = client.read_rif_reg(PROC_DEV_7044_0_E, 0x80000000)
        print("Version Reg: {0}".format(hex(version_reg_value)))


        """
        Write Soft register
        """
        client.write_rif_reg(PROC_DEV_7044_0_E, 0x80000F2C, 0xAABBCCDD)

        """
        Read Soft register
        """
        soft_reg_value = client.read_rif_reg(PROC_DEV_7044_0_E, 0x80000F2C)
        print("Soft Reg: {0}".format(hex(soft_reg_value)))


        try:
            input("Press any key to continue...")
        except SyntaxError:
            pass

        client.destroy()
        client = None

    except Exception as ex:        
        print("Failed to run command - {0}\n{1}".format(str(ex), Utils.format_exception(ex)))
        sys.exit(-1)
    finally:
        if client is not None:
            client.destroy()

        elapsed_time = datetime.datetime.now() - start_time
        print("\nScript finished, elapsed - {0}".format(elapsed_time))

    sys.exit(0)
