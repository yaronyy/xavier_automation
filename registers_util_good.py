
from builtins import object
import logging
import time,sys
import configparser
from cryptography.fernet import Fernet

log = logging.getLogger(__name__)

vl1 = b'4JR-2GVRgyQGSFp_NN2ZEsY8A9yk1X5pbwkHWU_fei4='

def encrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it encrypts the file and write it
    """
    f = Fernet(key)
    # After initializing the Fernet object with the given key, let's read that file first:
    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()
    # After that, encrypting the data we just read:
    encrypted_data = f.encrypt(file_data)
    # Writing the encrypted file with the same name, so it will override the original (don't use this on sensitive information yet, just test on some junk data):
    with open(filename, "wb") as file:
        file.write(encrypted_data)
def decrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it decrypts the file and write it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    # decrypt data
    decrypted_data = f.decrypt(encrypted_data)
    # write the original file
    with open(filename, "wb") as file:
        file.write(decrypted_data)

class configparser(configparser.ConfigParser):

    def _read(self, fp, fpname):
        """Parse a sectioned configuration file.

        Each section in a configuration file contains a header, indicated by
        a name in square brackets (`[]'), plus key/value options, indicated by
        `name' and `value' delimited with a specific substring (`=' or `:' by
        default).

        Values can span multiple lines, as long as they are indented deeper
        than the first line of the value. Depending on the parser's mode, blank
        lines may be treated as parts of multiline values or ignored.

        Configuration files may include comments, prefixed by specific
        characters (`#' and `;' by default). Comments may appear on their own
        in an otherwise empty line or may be entered in lines holding values or
        section names.
        """
        elements_added = set()
        cursect = None                        # None, or a dictionary
        sectname = None
        optname = None
        lineno = 0
        indent_level = 0
        e = None                              # None, or an exception
        for lineno, line in enumerate(fp, start=1):
            comment_start = sys.maxsize
            # strip inline comments
            inline_prefixes = {p: -1 for p in self._inline_comment_prefixes}
            while comment_start == sys.maxsize and inline_prefixes:
                next_prefixes = {}
                for prefix, index in inline_prefixes.items():
                    index = line.find(prefix, index+1)
                    if index == -1:
                        continue
                    next_prefixes[prefix] = index
                    if index == 0 or (index > 0 and line[index-1].isspace()):
                        comment_start = min(comment_start, index)
                inline_prefixes = next_prefixes
            # strip full line comments
            for prefix in self._comment_prefixes:
                if line.strip().startswith(prefix):
                    comment_start = 0
                    break
            if comment_start == sys.maxsize:
                comment_start = None
            value = line[:comment_start].strip()
            if not value:
                if self._empty_lines_in_values:
                    # add empty line to the value, but only if there was no
                    # comment on the line
                    if (comment_start is None and
                        cursect is not None and
                        optname and
                        cursect[optname] is not None):
                        cursect[optname].append('') # newlines added at join
                else:
                    # empty line marks end of value
                    indent_level = sys.maxsize
                continue
            # continuation line?
            first_nonspace = self.NONSPACECRE.search(line)
            cur_indent_level = first_nonspace.start() if first_nonspace else 0
            if (cursect is not None and optname and
                cur_indent_level > indent_level):
                cursect[optname].append(value)
            # a section header or option header?
            else:
                indent_level = cur_indent_level
                # is it a section header?
                mo = self.SECTCRE.match(value)
                if mo:
                    sectname = mo.group('header')
                    if sectname in self._sections:
                        if self._strict and sectname in elements_added:
                            raise DuplicateSectionError(sectname, fpname,
                                                        lineno)
                        cursect = self._sections[sectname]
                        elements_added.add(sectname)
                    elif sectname == self.default_section:
                        cursect = self._defaults
                    else:
                        cursect = self._dict()
                        self._sections[sectname] = cursect
                        self._proxies[sectname] = SectionProxy(self, sectname)
                        elements_added.add(sectname)
                    # So sections can't start with a continuation line
                    optname = None
                # no section header in the file?
                elif cursect is None:
                    raise MissingSectionHeaderError(fpname, lineno, line)
                # an option line?
                else:
                    mo = self._optcre.match(value)
                    if mo:
                        optname, vi, optval = mo.group('option', 'vi', 'value')
                        if not optname:
                            e = self._handle_error(e, fpname, lineno, line)
                        optname = self.optionxform(optname.rstrip())
                        # if (self._strict and
                        #     (sectname, optname) in elements_added):
                        #     raise DuplicateOptionError(sectname, optname,
                        #                                fpname, lineno)
                        elements_added.add((sectname, optname))
                        # This check is fine because the OPTCRE cannot
                        # match if it would set optval to None
                        if optval is not None:
                            optval = optval.strip()
                            cursect[optname] = [optval]
                        else:
                            # valueless option handling
                            cursect[optname] = None
                    else:
                        # a non-fatal parsing error occurred. set up the
                        # exception but keep going. the exception will be
                        # raised at the end of the file and will contain a
                        # list of all bogus lines
                        e = self._handle_error(e, fpname, lineno, line)
        self._join_multiline_values()
        # if any parsing errors occurred, raise an exception
        if e:
            raise e

class RegisterInfo(object):

    def __init__(self, reg_name, reg_data):
        self.reg_data = reg_name + " = " + reg_data
        self.parseRegisterData(reg_name, reg_data)

    def parseRegisterData(self, reg_name, reg_data):

        """
                                    0      1 2 3  4  5
        Tx_Mng_Enable_Looback = h90040b50 14 1 h0 RW BIN
        """
        if len(reg_data) == 0 or len(reg_name) == 0:
            raise Exception("ERROR : Invalid parameter")

        self.name = reg_name

        reg_info = [x.strip() for x in reg_data.split()]

        # support for Hex
        if 'h' in reg_info[0]:
            reg_info[0] = reg_info[0].replace('h', '0x')
            self.addr = int(reg_info[0], 16)
        else:
            self.addr = int(reg_info[0], 10)

        self.bit = int(reg_info[1])
        self.size = int(reg_info[2])

        self.mask = int('1' * self.size, 2) << self.bit

        self.can_write = True if 'W' in reg_info[4].upper() else False
        self.can_read = True if 'R' in reg_info[4].upper() else False
        self.can_clear = True if 'SC' in reg_info[4].upper() else False

class Registers(object):

    
    def __init__(self, interface, register_file = None, dut_id = None):
        self.registers_db = configparser()
        # self.registers_db.optionxform = str
        self._if = interface
        self.ini_section = "DIRECT"
        #Just for linux,  for windows change register_file to register_file.replace('/','\\')
        decrypt(register_file, vl1)
        time.sleep(1)
        if register_file:
            self.load_registers_file(register_file)
        #Just for linux,  for windows change register_file to register_file.replace('/','\\')
        encrypt(register_file, vl1)

        self.dut_id = dut_id if not dut_id is None else -1

    def load_registers_file(self, registers_file):
        try:
            file = self.registers_db.read(registers_file, encoding="utf-8")
        except:
            file = self.registers_db.read(registers_file, encoding="latin-1")
        if len(file) == 0:
            raise ReferenceError("ERROR : system unable to load the ini file {}".format(registers_file) )

        #options = self.registers_db.options(section)

    def _get_register( self, register_name ):
        try:

            reg_data = self.registers_db.get( self.ini_section, register_name )
        except Exception as e:
            log.error( "ERROR : register name {} not found in database".format(register_name) )
            raise
        else:
            return RegisterInfo(register_name , reg_data)

    def write(self, register_name, value):
        reg = self._get_register(register_name)
        if not reg.can_write:
            if reg.can_clear:
                raise Exception("ERROR : register {} can be cleared only ".format( register_name ) )
            else:
                raise Exception("ERROR : register {} can not be written".format( register_name ) )

        reg_val = self._if.read_register( reg.addr )
        value = value & int( '1' * reg.size, 2 )   
        reg_val = (reg_val & ~reg.mask) | ( (value & int( '1' * reg.size, 2 ))<< reg.bit)

        self.register = self._if.write_register(reg.addr, reg_val)
        log.debug( "DUT {}, Register {} Addr : {}, value : {}".format( self.dut_id, register_name, reg.addr, reg_val ) )
        return reg_val

    def write_to_field(self, register_name, register_field, value):
        # find offset of register field
        reg = self._get_register(register_name)
        if not reg.can_write:
            if reg.can_clear:
                raise Exception("ERROR : register {} can be cleared only ".format( register_name ) )
            else:
                raise Exception("ERROR : register {} can not be written".format( register_name ) )

        # get info from specific field
        field = self._get_register(register_field)

        reg_val = self._if.read_register( reg.addr )
        value = value & int( '1' * field.size, 2 )
        reg_val = (reg_val & ~field.mask) | ( (value & int( '1' * field.size, 2 ))<< field.bit)

        self.register = self._if.write_register(reg.addr, reg_val)
        log.debug( "DUT {}, Register {} Addr : {}, value : {}".format( self.dut_id, register_name, reg.addr, reg_val ) )
        return reg_val

    def clear_counter( self, register_name, value = 0 ):
        reg = self._get_register(register_name)
        reg_val = self._if.read_register( reg.addr )
        reg_val = (reg_val & ~reg.mask) | ( (value & int( '1' * reg.size, 2 ))<< reg.bit)
        self._if.write_register( reg.addr, reg_val )
        log.debug( "Clear Counter Register {} Addr : {}, value : {}".format( register_name, reg.addr, reg_val ) )
        return reg_val

    def read(self, register_name ):
        
        reg = self._get_register(register_name)
        reg_val = self._if.read_register ( reg.addr )
        log.debug("DUT {} : Reading {} Register {} value : {}".format(self.dut_id, register_name , reg.addr , reg_val) )
        return ((reg_val & reg.mask) >> reg.bit)

    def write_direct( self, addr, value ):
        self._if.write_register( addr, value )

    def read_direct( self, addr):
        return self._if.read_register (addr )

    def write_sub_reg(self , register_name, bit ,size, value):
        reg = self._get_register(register_name)
        if not reg.can_write:
            raise Exception("ERROR : register {} can not be written".format( register_name ) )
        reg_val = self._if.read_register( reg.addr )
        reg_mask =  int('1' * size, 2) << (reg.bit+ bit)
        reg_val = (reg_val & ~reg_mask) | ( (value & int( '1' * size, 2 ))<< (reg.bit+ bit))
        self._if.write_register( reg.addr, reg_val )
    
    def read_sub_reg(self , register_name, bit ,size):
        reg_val = self.read(register_name)
        reg_mask =  int('1' * size, 2) << bit
        return ((reg_val & reg_mask) >> bit)

    def activate_registers_file( self, file_name ):

        hwd = open( file_name, 'r')
        reg_data = hwd.readlines()

        for line in reg_data:
            # Expected format in each line
            # TSWSOC_Block_Reset_1 = hffffffff
            reg_name, value = [x.strip() for x in line.split('=')]

            value = value if not value.startwith('&') else value[1:]    
            value = int(value[1:],16) if value.startwith('h') else int(value,10)
            self.write ( reg_name, value)
            time.sleep(0.01)

if __name__ == '__main__':
    a=0