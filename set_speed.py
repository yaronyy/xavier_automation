import datetime
from vlns_aphy_utils import *
import vlns_aphy_config as CFG
from vlns_aphy_client import *
import sys
import time

########
import argparse
from registers_util import Registers
from linux_regs_db import csiSpeedCalculator

db_file_path = os.path.split(os.path.abspath(__file__))[0].split('lib')[0] + '/db_files'
registers_44 = Registers('DIRECT', db_file_path + '/MeronSnk.ini')
registers_31 = Registers('DIRECT', db_file_path + '/MeronSrc.ini')

SERVICE_DICT = {'local': PROC_DEV_7044_0_E,
                '0': PROC_DEV_7031_0_E,
                '1': PROC_DEV_7031_1_E,
                '2': PROC_DEV_7031_2_E,
                '3': PROC_DEV_7031_3_E}

def parse_params():
    # run_cmd = 'python3 xavier_automation/it_set_speed.py -s 1450 -a 0 -rm 1 -sy'
    parser = argparse.ArgumentParser( description='Valens QPack automation CLI' )
    parser.add_argument( '-s', '--speed', type=str, required=True, help='speed for csi') # 80-2500
    parser.add_argument( '-a', '--all', type=str, required=False, help='number of all', default='0') #0/1
    parser.add_argument( '-rm', '--remote', type=str, required=True, help='phy number of remote 7031') #0/1/2/3
    parser.add_argument( '-sy', '--sync',action='store_true', help='run device host sync (should be after reset)')
    args = parser.parse_args()
    return args


def set_tx_phy_speed(client, speed, config_file,remote='local', all=0):
    """
    set the speed on the tx phy by registers
    At the beginning the function initializes a list of registers that comes from the config_file.
    :param client: host client
    :param speed: speed to set.
    :param config_file: file path that contain registers to initialize.
    :param remote: NOT USED - The number remote over channel(Aphy link). (options(str) : 'local'/'0'/'1'/'2'/'3')
    :param all: Number of the connected all.(options(int) : 0/1)
    :return: None
    """

    print('\n\n\nwrite_regs_from_file TX')
    write_regs_from_file(client, config_file)

    calc = csiSpeedCalculator(speed,all)
    write_regs_from_list(client,calc.csi_tx_local_reg_info)
    write_regs_from_list(client,calc.csi_pll_frac_reg_info)

    print('\n\n\nwrite_regs_from_list last *2 reg_list -tx_phy_speed')
    reg_list = [['_A_C{}_PHY_RSTZ_reg'.format(all),    7],
                ['_A_C{}_CSI2_RESETN_reg'.format(all), 1]]
    write_regs_from_list(client,reg_list)

    print('write_regs desckew_registers -tx_phy_speed')
    write_regs_from_list(client,calc.csi_deskew_regs_info)


def set_rx_phy_speed(client, speed, config_file,remote='local', all=0):
    """
    set the speed on the rx phy by registers
    At the beginning the function initializes a list of registers that comes from the config_file.
    :param client: host client.
    :param speed: speed to set.
    :param config_file: file path that contain registers to initialize.
    :param remote: The number remote over channel(Aphy link). (options(str) : 'local'/'0'/'1'/'2'/'3')
    :param all: Number of the connected all.(options(int) : 0/1)
    :return: None
    """
    print('\n\n\nwrite_regs_from_file RX -rx_phy_speed')
    write_regs_from_file(client, config_file,remote)

    calc = csiSpeedCalculator(speed,all)
    rx_regs = calc.csi_rx_7044_reg_info if remote == 'local' else calc.csi_rx_7031_reg_info
    write_regs_from_list(client,rx_regs,remote)

    print('\n\n\nwrite_regs last *2 reg_list -rx_phy_speed')
    prefix ='_B_' if remote == 'local' else '_csi_tadp_tx_{}_'.format(all)
    reg_list = [[prefix + 'PHY_SHUTDOWNZ_reg'          , 1],
                [prefix + 'meron_src_csi_swreset_n_reg', 0x1ff]]
    write_regs_from_list(client,reg_list,remote)


def write_regs_from_list(client, registers,remote='local'):
    """
    Get list that contain registers and write to the registers.
    example_list = [[r,v],[[r,v],[[r,f,v],[r,f,v],[r,f,v]....]
    :param client:host client.
    :param registers:list of [[register, (field), value],[register, (field), value],...]
    :param remote: The number remote over channel(Aphy link). (options(str) : 'local'/'0'/'1'/'2'/'3')
    :return: None
    """
    for item in registers:
        # if len ==2 -> item[0]=register ,item[1]=value
        if len(item) == 2:
            write_register(client, item[0], item[1],remote)
        # else len == 3 -> item[0]=register ,item[1]=field ,item[2]=value
        else:
            write_to_field(client, item[0], item[1], item[2],remote)


def write_regs_from_file(client, file_name,remote='local'):
    """
    The function writes to registers/fields in from given file.
    :param client:host client.
    :param file_name: name of the file to read registers from
    :param remote: The number remote over channel(Aphy link). (options(str) : 'local'/'0'/'1'/'2'/'3')
    :return: None
    For example : writes to registers/fields from file config_file.txt.
    usage example : MNG_SCRIPT_UTILITIES.write_regs_from_file(client,'config_file.txt','local')
    """
    #Check if the file exist
    if not os.path.exists(file_name):
        raise IOError("File {} Not exists".format(file_name))
    # Read all line of config file.
    with open(file_name, 'r') as f:
        lines = f.readlines()
    print("File name: {}".format(file_name))
    for indx, line in enumerate(lines):
        # if exist just one ',' in line -> line contain: register, value
        if line.count(',') == 1:
            reg, val = line.split(',')
            write_register(client, eval(reg), eval(val), remote)
        # if NOT exist just one ',' in line(There should be two ',' in line) -> line contain: register, field, value
        else:
            reg, field, val = line.split(',')
            write_to_field(client, eval(reg), eval(field), eval(val),remote)

def start_deskew(client, all=0,remote='local'):
    """
    start deskew by set register _A_cfg_all{}_cfg_all{}_deskew_ctrl to 3.
    :param client:host client.
    :param all: Number of the connected all.(options(int) : 0/1)
    :param remote: The number remote over channel(Aphy link). (options(str) : 'local'/'0'/'1'/'2'/'3')
    :return: None
    """
    reg_list = [["_A_cfg_all{}_cfg_all{}_deskew_ctrl".format(all, all),0x3]]
    write_regs_from_list(client, reg_list,remote)


def write_register(client,register_name, value, remote='local'):
    """
    Write to register: local(7044)/remote(7031)
    :param client:host client.
    :param register_name: The name of the register
    :param value: Value to set. (int or hex)
    :param remote: The number remote over channel(Aphy link). (options(str) : 'local'/'0'/'1'/'2'/'3')
    :return: None
    """
    if value is None:
        return
    elif isinstance(value,str):
        value = int(value,16)
    # Choose service by local(7044)/remote(7031)
    service = SERVICE_DICT[remote]
    register, dut = (registers_44, '44') if remote == 'local' else (registers_31, '31')
    reg = register._get_register(register_name)
    print("\n++write_to_register , reg:{}, val {} hex_val {} D {}".format(register_name,value, hex(value),dut))
    client.write_rif_reg(service, reg.addr, value)


def write_to_field(client, register_name, register_field, value, remote='local'):
    """
    Write to field of register: local(7044)/remote(7031)
    :param client:host client.
    :param register_name: The name of the register
    :param register_field: The name of the field
    :param value: Value to set. (int or hex)
    :param remote: The number remote over channel(Aphy link). (options(str) : 'local'/'0'/'1'/'2'/'3')
    :return: None
    """
    if value is None:
        return
    elif isinstance(value, str):
        value = int(value,16)
    # Choose service by local(7044)/remote(7031)
    service = SERVICE_DICT[remote]
    # Choose Registers object by local(7044)/remote(7031)
    register, dut = (registers_44, '44') if remote == 'local' else (registers_31, '31')
    reg = register._get_register(register_name)
    field = register._get_register(register_field)
    reg_val = client.read_rif_reg(service, reg.addr)
    # manipulates value according (mask): value, field, register.
    value = value & int('1' * field.size, 2)
    reg_val = (reg_val & ~field.mask) | ((value & int('1' * field.size, 2)) << field.bit)
    print("\n++write_to_field reg:{} reg_val:{} field: {}, hex_field_val {} D {}".format(register_name,reg_val, register_field, hex(value),dut))
    client.write_rif_reg(service, reg.addr, int(reg_val))


if __name__ == "__main__":
    run_cmd = 'python3 xavier_automation/set_speed.py -s 1450 -a 0 -rm 1 -sy'
    args = parse_params()
    speed, remote, all ,sync = int(args.speed), args.remote, int(args.all), args.sync

    print('Set speed {} all{} remote {} sync {}'.format(speed,all,remote,sync))
    config_file_path = os.path.split(os.path.abspath(__file__))[0] + '/config_files'
    cfg_file_7044 = config_file_path + '/7044_all0_without_init.txt'
    cfg_file_7031 = config_file_path + '/7031_as_DUT.txt'

    start_time = datetime.datetime.now()
    client = None
    try:
        client = VlnsAPhyClient.create(remote=CFG.REMOTE_MACHINE)
        if sync:
            print('\n run_device_host_sync \n')
            client.run_device_host_sync(wait_timeout_seconds=10)
            time.sleep(3)
        print("\n\n\n\n\n\n =============== set_tx_phy_speed========\n\n\n\n\n")
        set_tx_phy_speed(client=client, speed=speed, config_file=cfg_file_7044, all=0)
        print("\n\n\n\n\n\n =============== set_rx_phy_speed========n\n\n\n\n\n")
        set_rx_phy_speed(client=client, speed=speed, config_file=cfg_file_7031,remote=remote, all=0)
        if speed >= 1500:
            start_deskew(client=client, all=0,remote='local')

    except Exception as ex:        
        print("Failed to run command - {0}\n{1}".format(str(ex), Utils.format_exception(ex)))
        sys.exit(-1)
    finally:
        if client is not None:
            print("$$$$$$$$$$$ start destroy $$$$$$$$$$$$$$$$$$$")
            client.destroy()
            print("$$$$$$$$$$$ end destroy $$$$$$$$$$$$$$$$$$$")

        elapsed_time = datetime.datetime.now() - start_time
        print("\nScript finished, elapsed - {0}".format(elapsed_time))

    sys.exit(0)

