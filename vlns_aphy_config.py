import datetime
import os
import sys
from vlns_aphy_utils import *


TOOL_DIR = os.path.dirname(os.path.realpath(__file__))
TESTS_DATA_DIR = "data"
TEST_RESULTS_DIR = "results"
VA70XX_APPS_DIR = "/home/lab/va70xx-apps"

VA7044_FW_FILE = os.path.join(TESTS_DATA_DIR, "va7044_signed_full.hex")
VA7031_FW_FILE = os.path.join(TESTS_DATA_DIR, "va7031.hex")
VA7031_FW_DUMP_FILE = os.path.join(TESTS_DATA_DIR, "va7031_dump.hex")
VA7031_FW_DUMP_RESULT_FILE = os.path.join(TOOL_DIR, "tmp.va7031_dump_result.hex")
VA7031_I2C_BUS = "/aardvark/i2c-0"
VA7031_EEPROM_I2C_ADDRESS = "50"

LINUX_I2C_BUS = "/dev/i2c-8"

VA7044_I2C_PAIR = "2f-2f"
VA7031_I2C_PAIR = "1f-1f"

FLASH_BLOCK_SIZES = [256, 1024, 3072]
EEPROM_FLASH_BLOCK_SIZES = [256]


#REMOTE_MACHINE = "172.23.8.185"
REMOTE_MACHINE = None


def check_path(object_path:str):
    if not os.path.exists(object_path):
        raise Exception("Couldn't find the object '{0}'".format(object_path))

def check_config():
    if not os.path.isdir(TEST_RESULTS_DIR):
        os.mkdir(TEST_RESULTS_DIR)
    if not os.path.isdir(TESTS_DATA_DIR):
        raise Exception("tests data directory doesn't exist")
    if not os.access(VA7044_FW_FILE, os.R_OK):
        raise Exception("va7044 firmware doesn't exist or can't be read")
    if not os.access(VA7031_FW_FILE, os.R_OK):
        raise Exception("va7031 firmware doesn't exist or can't be read")

if __name__ == "__main__":
    start_time = datetime.datetime.now()   

    try:

        check_path(TOOL_DIR)
        check_path(TESTS_DATA_DIR)
        check_path(VA7044_FW_FILE)
        check_path(VA7031_FW_FILE)
        check_path(VA7031_FW_DUMP_FILE)
        
        print("[SUCCESS]")

    except Exception as ex:        
        error = "Failed to run test - {0}\n{1}".format(str(ex), Utils.format_exception(ex))
        print(error)
        sys.exit(-1)
    finally:        
        elapsed_time = datetime.datetime.now() - start_time
        print("\nScript finished, elapsed - {0}".format(elapsed_time))

    sys.exit(0)
