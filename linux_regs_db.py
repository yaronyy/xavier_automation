from __future__ import unicode_literals

from builtins import hex
from builtins import object

import logging, time, sys, re

import math
import statistics


log = logging.getLogger(__name__)
if __name__ == '__main__':
    sys.path.append(re.sub(r"(.*)(\\utilities.*)$", "\g<1>", sys.path[0]))



class csiSpeedCalculator(object):

    def __init__(self, timeBase, all = None):
        self.rxParam_TimeBase = timeBase
        self.all = all
        #####################################################################################          RX PY    #############################################################

        self.rxParam_Tdco = 5
        self.rxParam_TminRX = 4
        self.rxParam_DIV = 16
        self.rxParam_Tddl = 2.1
        self.rxParam_Target_Thssettle = 115 + 6000 / self.rxParam_TimeBase
        self.rxParam_Tlprx = 1
        #################################################################################    parameters  section end ###################################################################


        self.DDLCAL_MAX_PHASE_CALCVAL_DICT = {'4500':hex(63), '4000':hex(71), '3600':hex(79), '3230':hex(87), '3000':hex(71),
                                                      '2700':hex(79), '2455':hex(87), '2250':hex(95), '2077':hex(103), '1929':hex(111),
                                                      '1800':hex(119), '1688':hex(127), '1588':hex(135), '1500':hex(143)}

        self.DDLCAL_DLL_FBK_CALCVAL_DICT = {'4500':hex(7), '4000':hex(8), '3600':hex(9), '3230':hex(10), '3000':hex(8),
                                                      '2700':hex(9), '2455':hex(10), '2250':hex(11), '2077':hex(12), '1929':hex(13),
                                                      '1800':hex(14), '1688':hex(15), '1588':hex(16),'1500': hex(17)}

        self.DDLCAL_DDL_COARSE_BANK_CALCVAL_DICT = {'4500': hex(0), '4000': hex(1), '3600': hex(1), '3230': hex(1), '3000': hex(0),
                                                      '2700': hex(1), '2455': hex(1), '2250': hex(1), '2077':hex(1), '1929': hex(2),
                                                      '1800': hex(2), '1688': hex(2), '1588': hex(2), '1500': hex(3)}

        self.OA_LANE0_HSRX_CDPHY_SEL_FAST_CALCVAL_DICT = {'4500': hex(1), '4000': hex(1), '3600': hex(1), '3230': hex(1), '3000': hex(0),
                                                      '2700': hex(0), '2455': hex(0), '2250': hex(0), '2077': hex(0), '1929': hex(0),
                                                      '1800': hex(0), '1688': hex(0), '1588': hex(0), '1500': hex(0)}

        self.OA_LANE1_HSRX_CDPHY_SEL_FAST_CALCVAL_DICT = {'4500': hex(1), '4000':hex(1), '3600': hex(1), '3230': hex(1), '3000': hex(0),
                                                      '2700': hex(0), '2455': hex(0), '2250': hex(0), '2077': hex(0), '1929': hex(0),
                                                      '1800': hex(0), '1688': hex(0), '1588': hex(0),'1500': hex(0)}

        self.OA_LANE2_HSRX_CDPHY_SEL_FAST_CALCVAL_DICT = {'4500': hex(1), '4000': hex(1), '3600': hex(1), '3230': hex(1), '3000': hex(0),
                                                      '2700': hex(0), '2455': hex(0), '2250': hex(0), '2077': hex(0), '1929': hex(0),
                                                      '1800': hex(0), '1688': hex(0), '1588': hex(0), '1500': hex(0)}

        self.OA_LANE3_HSRX_CDPHY_SEL_FAST_CALCVAL_DICT = {'4500': hex(1), '4000': hex(1), '3600': hex(1), '3230': hex(1), '3000': hex(0),
                                                      '2700': hex(0), '2455': hex(0), '2250': hex(0), '2077': hex(0), '1929': hex(0),
                                                      '1800': hex(0), '1688': hex(0), '1588': hex(0), '1500': hex(0)}

        self.OA_LANE4_HSRX_CDPHY_SEL_FAST_CALCVAL_DICT = {'4500': hex(1), '4000': hex(1), '3600': hex(1), '3230':hex(1), '3000': hex(0),
                                                      '2700': hex(0), '2455': hex(0), '2250': hex(0), '2077': hex(0), '1929': hex(0),
                                                      '1800': hex(0), '1688': hex(0), '1588': hex(0), '1500': hex(0)}


        self.OA_LANE2_HSRX_HS_CLK_DIV_CALCVAL_DICT = {'2560':hex(6), '1280': hex(5), '640':hex(4), '320': hex(3), '160': hex(2),
                                                      '80': hex(1)}

        self.HS_RX_0_THSSETTLE_REG_CALCVAL = hex(math.floor((self.rxParam_Target_Thssettle - self.rxParam_Tlprx - (
                    self.rxParam_TminRX + 3) * self.rxParam_Tdco - 2 * self.rxParam_Tdco - self.rxParam_Tdco) / self.rxParam_Tdco))

        self.HS_RX_3_FJUMP_DESKEW_REG_CALCVAL_DICT = {'4500': hex(2), '4000': hex(2), '3600': hex(2), '3230': hex(3), '3000': hex(2),
                                                      '2700': hex(2), '2455': hex(3), '2250': hex(3), '2077': hex(3), '1929': hex(3),
                                                      '1800': hex(3), '1688': hex(4), '1588': hex(4), '1500': hex(4)}

        self.MIN_EYE_OPENING_DESKEW_REG_CALCVAL_DICT = {'4500': hex(13), '4000': hex(15), '3600': hex(16), '3230': hex(18), '3000': hex(15),
                                                      '2700': hex(16), '2455': hex(18), '2250': hex(19), '2077': hex(21), '1929': hex(23),
                                                      '1800': hex(24), '1688': hex(26), '1588': hex(27), '1500': hex(29)}

        self.DDLCAL_COUNTER_REF_CALCVAL = hex(math.ceil((self.rxParam_TimeBase * 5) / (2 * self.rxParam_DIV * self.rxParam_Tddl))) if self.rxParam_TimeBase >= 1500 else None

        # self.csi_rx_local_reg_info_lut_nt = namedtuple('csi_rx_local_reg_info_lut_nt',
        #                                           'reg_name, reg_field, field_val')


        self.csi_rx_7031_reg_info = [
            ["_csi_tadp_tx_{}_PPI_STARTUP_RW_COMMON_DPHY_7_reg".format(self.all), "csi_tadp_tx_{}_DPHY_DDL_CAL_addr".format(self.all), hex(40 if self.rxParam_TimeBase > 1500 else 104)],
            ["_csi_tadp_tx_{}_PPI_RW_DDLCAL_CFG_3_reg".format(self.all), "csi_tadp_tx_{}_DDLCAL_COUNTER_REF".format(self.all), self.DDLCAL_COUNTER_REF_CALCVAL],
            ["_csi_tadp_tx_{}_PPI_RW_DDLCAL_CFG_0_reg".format(self.all), "csi_tadp_tx_{}_DDLCAL_TIMEBASE_TARGET".format(self.all), '0x5F'],
            ["_csi_tadp_tx_{}_PPI_RW_DDLCAL_CFG_1_reg".format(self.all), "csi_tadp_tx_{}_DDLCAL_MAX_PHASE".format(self.all), self.DDLCAL_MAX_PHASE_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_csi_tadp_tx_{}_PPI_RW_DDLCAL_CFG_5_reg".format(self.all), "csi_tadp_tx_{}_DDLCAL_DLL_FBK".format(self.all), self.DDLCAL_DLL_FBK_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_csi_tadp_tx_{}_PPI_RW_DDLCAL_CFG_5_reg".format(self.all), "csi_tadp_tx_{}_DDLCAL_DDL_COARSE_BANK".format(self.all), self.DDLCAL_DDL_COARSE_BANK_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_csi_tadp_tx_{}_CORE_DIG_IOCTRL_RW_AFE_LANE0_CTRL_2_8_reg".format(self.all), "csi_tadp_tx_{}_OA_LANE0_HSRX_CDPHY_SEL_FAST".format(self.all), self.OA_LANE0_HSRX_CDPHY_SEL_FAST_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_csi_tadp_tx_{}_CORE_DIG_IOCTRL_RW_AFE_LANE1_CTRL_2_8_reg".format(self.all), "csi_tadp_tx_{}_OA_LANE1_HSRX_CDPHY_SEL_FAST".format(self.all), self.OA_LANE1_HSRX_CDPHY_SEL_FAST_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_csi_tadp_tx_{}_CORE_DIG_IOCTRL_RW_AFE_LANE2_CTRL_2_8_reg".format(self.all), "csi_tadp_tx_{}_OA_LANE2_HSRX_CDPHY_SEL_FAST".format(self.all), self.OA_LANE2_HSRX_CDPHY_SEL_FAST_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_csi_tadp_tx_{}_CORE_DIG_IOCTRL_RW_AFE_LANE3_CTRL_2_8_reg".format(self.all), "csi_tadp_tx_{}_OA_LANE3_HSRX_CDPHY_SEL_FAST".format(self.all), self.OA_LANE3_HSRX_CDPHY_SEL_FAST_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_csi_tadp_tx_{}_CORE_DIG_IOCTRL_RW_AFE_LANE4_CTRL_2_8_reg".format(self.all), "csi_tadp_tx_{}_OA_LANE4_HSRX_CDPHY_SEL_FAST".format(self.all), self.OA_LANE4_HSRX_CDPHY_SEL_FAST_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_0_RW_LP_0_reg".format(self.all), "csi_tadp_tx_{}_LP_0_TTAGO_reg".format(self.all), '0x7'],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_1_RW_LP_0_reg".format(self.all), "csi_tadp_tx_{}_LP_0_TTAGO_reg".format(self.all), '0x7'],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_2_RW_LP_0_reg".format(self.all), "csi_tadp_tx_{}_LP_0_TTAGO_reg".format(self.all), '0x7'],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_3_RW_LP_0_reg".format(self.all), "csi_tadp_tx_{}_LP_0_TTAGO_reg".format(self.all), '0x7'],
            ["_csi_tadp_tx_{}_CORE_DIG_IOCTRL_RW_AFE_LANE0_CTRL_2_12_reg".format(self.all), "csi_tadp_tx_{}_OA_LANE0_HSRX_DPHY_DDL_BYPASS_EN_OVR_VAL".format(self.all), hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_csi_tadp_tx_{}_CORE_DIG_IOCTRL_RW_AFE_LANE1_CTRL_2_12_reg".format(self.all), "csi_tadp_tx_{}_OA_LANE1_HSRX_DPHY_DDL_BYPASS_EN_OVR_VAL".format(self.all), hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_csi_tadp_tx_{}_CORE_DIG_IOCTRL_RW_AFE_LANE2_CTRL_2_12_reg".format(self.all), "csi_tadp_tx_{}_OA_LANE2_HSRX_DPHY_DDL_BYPASS_EN_OVR_VAL".format(self.all), hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_csi_tadp_tx_{}_CORE_DIG_IOCTRL_RW_AFE_LANE3_CTRL_2_12_reg".format(self.all), "csi_tadp_tx_{}_OA_LANE3_HSRX_DPHY_DDL_BYPASS_EN_OVR_VAL".format(self.all), hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_csi_tadp_tx_{}_CORE_DIG_IOCTRL_RW_AFE_LANE4_CTRL_2_12_reg".format(self.all), "csi_tadp_tx_{}_OA_LANE4_HSRX_DPHY_DDL_BYPASS_EN_OVR_VAL".format(self.all), hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_csi_tadp_tx_{}_CORE_DIG_IOCTRL_RW_AFE_LANE0_CTRL_2_13_reg".format(self.all), "csi_tadp_tx_{}_OA_LANE0_HSRX_DPHY_DDL_BYPASS_EN_OVR_EN".format(self.all), hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_csi_tadp_tx_{}_CORE_DIG_IOCTRL_RW_AFE_LANE1_CTRL_2_13_reg".format(self.all), "csi_tadp_tx_{}_OA_LANE1_HSRX_DPHY_DDL_BYPASS_EN_OVR_EN".format(self.all), hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_csi_tadp_tx_{}_CORE_DIG_IOCTRL_RW_AFE_LANE2_CTRL_2_13_reg".format(self.all), "csi_tadp_tx_{}_OA_LANE2_HSRX_DPHY_DDL_BYPASS_EN_OVR_EN".format(self.all), hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_csi_tadp_tx_{}_CORE_DIG_IOCTRL_RW_AFE_LANE3_CTRL_2_13_reg".format(self.all), "csi_tadp_tx_{}_OA_LANE3_HSRX_DPHY_DDL_BYPASS_EN_OVR_EN".format(self.all), hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_csi_tadp_tx_{}_CORE_DIG_IOCTRL_RW_AFE_LANE4_CTRL_2_13_reg".format(self.all), "csi_tadp_tx_{}_OA_LANE4_HSRX_DPHY_DDL_BYPASS_EN_OVR_EN".format(self.all), hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_csi_tadp_tx_{}_CORE_DIG_IOCTRL_RW_AFE_LANE2_CTRL_2_9_reg".format(self.all), "csi_tadp_tx_{}_OA_LANE2_HSRX_HS_CLK_DIV".format(self.all), self.OA_LANE2_HSRX_HS_CLK_DIV_CALCVAL_DICT.get(self.range_key_by_speed_LANE2_CTRL_2_9, None)],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_CLK_RW_HS_RX_0_reg".format(self.all), "csi_tadp_tx_{}_HS_RX_0_TCLKSETTLE_reg".format(self.all), hex(28)],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_CLK_RW_HS_RX_0_reg".format(self.all), "csi_tadp_tx_{}_HS_RX_0_THSSETTLE_reg".format(self.all), self.HS_RX_0_THSSETTLE_REG_CALCVAL],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_0_RW_HS_RX_0_reg".format(self.all), "csi_tadp_tx_{}_HS_RX_0_THSSETTLE_reg".format(self.all), self.HS_RX_0_THSSETTLE_REG_CALCVAL],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_1_RW_HS_RX_0_reg".format(self.all), "csi_tadp_tx_{}_HS_RX_0_THSSETTLE_reg".format(self.all), self.HS_RX_0_THSSETTLE_REG_CALCVAL],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_2_RW_HS_RX_0_reg".format(self.all), "csi_tadp_tx_{}_HS_RX_0_THSSETTLE_reg".format(self.all), self.HS_RX_0_THSSETTLE_REG_CALCVAL],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_3_RW_HS_RX_0_reg".format(self.all), "csi_tadp_tx_{}_HS_RX_0_THSSETTLE_reg".format(self.all), self.HS_RX_0_THSSETTLE_REG_CALCVAL],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_0_RW_CFG_1_reg".format(self.all), "csi_tadp_tx_{}_CFG_1_DESKEW_SUPPORTED_reg".format(self.all), hex(1 if self.rxParam_TimeBase > 1500 else 0)],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_0_RW_CFG_1_reg".format(self.all), "csi_tadp_tx_{}_CFG_1_SOT_DETECTION_reg".format(self.all), hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_1_RW_CFG_1_reg".format(self.all), "csi_tadp_tx_{}_CFG_1_DESKEW_SUPPORTED_reg".format(self.all), hex(1 if self.rxParam_TimeBase > 1500 else 0)],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_1_RW_CFG_1_reg".format(self.all), "csi_tadp_tx_{}_CFG_1_SOT_DETECTION_reg".format(self.all), hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_2_RW_CFG_1_reg".format(self.all), "csi_tadp_tx_{}_CFG_1_DESKEW_SUPPORTED_reg".format(self.all), hex(1 if self.rxParam_TimeBase > 1500 else 0)],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_2_RW_CFG_1_reg".format(self.all), "csi_tadp_tx_{}_CFG_1_SOT_DETECTION_reg".format(self.all), hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_3_RW_CFG_1_reg".format(self.all), "csi_tadp_tx_{}_CFG_1_DESKEW_SUPPORTED_reg".format(self.all), hex(1 if self.rxParam_TimeBase > 1500 else 0)],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_3_RW_CFG_1_reg".format(self.all), "csi_tadp_tx_{}_CFG_1_SOT_DETECTION_reg".format(self.all), hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_CLK_RW_CFG_1_reg".format(self.all), "csi_tadp_tx_{}_CFG_1_DESKEW_SUPPORTED_reg".format(self.all), hex(1 if self.rxParam_TimeBase > 1500 else 0)],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_CLK_RW_CFG_1_reg".format(self.all), "csi_tadp_tx_{}_CFG_1_SOT_DETECTION_reg".format(self.all), hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_0_RW_HS_RX_2_reg".format(self.all), "csi_tadp_tx_{}_HS_RX_2_IGNORE_ALTERNCAL_reg".format(self.all), hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_1_RW_HS_RX_2_reg".format(self.all), "csi_tadp_tx_{}_HS_RX_2_IGNORE_ALTERNCAL_reg".format(self.all), hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_2_RW_HS_RX_2_reg".format(self.all), "csi_tadp_tx_{}_HS_RX_2_IGNORE_ALTERNCAL_reg".format(self.all), hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_3_RW_HS_RX_2_reg".format(self.all), "csi_tadp_tx_{}_HS_RX_2_IGNORE_ALTERNCAL_reg".format(self.all), hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_CLK_RW_HS_RX_2_reg".format(self.all), "csi_tadp_tx_{}_HS_RX_2_IGNORE_ALTERNCAL_reg".format(self.all), hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_0_RW_HS_RX_3_reg".format(self.all), "csi_tadp_tx_{}_HS_RX_3_FJUMP_DESKEW_reg".format(self.all),  self.HS_RX_3_FJUMP_DESKEW_REG_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_1_RW_HS_RX_3_reg".format(self.all), "csi_tadp_tx_{}_HS_RX_3_FJUMP_DESKEW_reg".format(self.all), self.HS_RX_3_FJUMP_DESKEW_REG_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_2_RW_HS_RX_3_reg".format(self.all), "csi_tadp_tx_{}_HS_RX_3_FJUMP_DESKEW_reg".format(self.all), self.HS_RX_3_FJUMP_DESKEW_REG_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_3_RW_HS_RX_3_reg".format(self.all), "csi_tadp_tx_{}_HS_RX_3_FJUMP_DESKEW_reg".format(self.all), self.HS_RX_3_FJUMP_DESKEW_REG_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_CLK_RW_HS_RX_3_reg".format(self.all), "csi_tadp_tx_{}_HS_RX_3_FJUMP_DESKEW_reg".format(self.all), self.HS_RX_3_FJUMP_DESKEW_REG_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_0_RW_HS_RX_6_reg".format(self.all), "csi_tadp_tx_{}_HS_RX_6_MIN_EYE_OPENING_DESKEW_reg".format(self.all), self.MIN_EYE_OPENING_DESKEW_REG_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_1_RW_HS_RX_6_reg".format(self.all), "csi_tadp_tx_{}_HS_RX_6_MIN_EYE_OPENING_DESKEW_reg".format(self.all), self.MIN_EYE_OPENING_DESKEW_REG_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_2_RW_HS_RX_6_reg".format(self.all), "csi_tadp_tx_{}_HS_RX_6_MIN_EYE_OPENING_DESKEW_reg".format(self.all), self.MIN_EYE_OPENING_DESKEW_REG_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_3_RW_HS_RX_6_reg".format(self.all), "csi_tadp_tx_{}_HS_RX_6_MIN_EYE_OPENING_DESKEW_reg".format(self.all), self.MIN_EYE_OPENING_DESKEW_REG_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_csi_tadp_tx_{}_CORE_DIG_DLANE_CLK_RW_HS_RX_6_reg".format(self.all), "csi_tadp_tx_{}_HS_RX_6_MIN_EYE_OPENING_DESKEW_reg".format(self.all), self.MIN_EYE_OPENING_DESKEW_REG_CALCVAL_DICT.get(self.range_key_by_speed, None)]]
        
        self.csi_rx_7044_reg_info = [
            ["_B_PPI_STARTUP_RW_COMMON_DPHY_7_reg", "DPHY_DDL_CAL_addr", hex(40 if self.rxParam_TimeBase > 1500 else 104)],
            ["_B_PPI_RW_DDLCAL_CFG_3_reg", "DDLCAL_COUNTER_REF", self.DDLCAL_COUNTER_REF_CALCVAL],
            ["_B_PPI_RW_DDLCAL_CFG_0_reg", "DDLCAL_TIMEBASE_TARGET", '0x5F'],
            ["_B_PPI_RW_DDLCAL_CFG_1_reg", "DDLCAL_MAX_PHASE", self.DDLCAL_MAX_PHASE_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_B_PPI_RW_DDLCAL_CFG_5_reg", "DDLCAL_DLL_FBK", self.DDLCAL_DLL_FBK_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_B_PPI_RW_DDLCAL_CFG_5_reg", "DDLCAL_DDL_COARSE_BANK", self.DDLCAL_DDL_COARSE_BANK_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_B_CORE_DIG_IOCTRL_RW_AFE_LANE0_CTRL_2_8_reg", "OA_LANE0_HSRX_CDPHY_SEL_FAST", self.OA_LANE0_HSRX_CDPHY_SEL_FAST_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_B_CORE_DIG_IOCTRL_RW_AFE_LANE1_CTRL_2_8_reg", "OA_LANE1_HSRX_CDPHY_SEL_FAST", self.OA_LANE1_HSRX_CDPHY_SEL_FAST_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_B_CORE_DIG_IOCTRL_RW_AFE_LANE2_CTRL_2_8_reg", "OA_LANE2_HSRX_CDPHY_SEL_FAST", self.OA_LANE2_HSRX_CDPHY_SEL_FAST_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_B_CORE_DIG_IOCTRL_RW_AFE_LANE3_CTRL_2_8_reg", "OA_LANE3_HSRX_CDPHY_SEL_FAST", self.OA_LANE3_HSRX_CDPHY_SEL_FAST_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_B_CORE_DIG_IOCTRL_RW_AFE_LANE4_CTRL_2_8_reg", "OA_LANE4_HSRX_CDPHY_SEL_FAST", self.OA_LANE4_HSRX_CDPHY_SEL_FAST_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_B_CORE_DIG_DLANE_0_RW_LP_0_reg", "LP_0_TTAGO_reg", '0x7'],
            ["_B_CORE_DIG_DLANE_1_RW_LP_0_reg", "LP_0_TTAGO_reg", '0x7'],
            ["_B_CORE_DIG_DLANE_2_RW_LP_0_reg", "LP_0_TTAGO_reg", '0x7'],
            ["_B_CORE_DIG_DLANE_3_RW_LP_0_reg", "LP_0_TTAGO_reg", '0x7'],
            ["_B_CORE_DIG_IOCTRL_RW_AFE_LANE0_CTRL_2_12_reg", "OA_LANE0_HSRX_DPHY_DDL_BYPASS_EN_OVR_VAL", hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_B_CORE_DIG_IOCTRL_RW_AFE_LANE1_CTRL_2_12_reg", "OA_LANE1_HSRX_DPHY_DDL_BYPASS_EN_OVR_VAL", hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_B_CORE_DIG_IOCTRL_RW_AFE_LANE2_CTRL_2_12_reg", "OA_LANE2_HSRX_DPHY_DDL_BYPASS_EN_OVR_VAL", hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_B_CORE_DIG_IOCTRL_RW_AFE_LANE3_CTRL_2_12_reg", "OA_LANE3_HSRX_DPHY_DDL_BYPASS_EN_OVR_VAL", hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_B_CORE_DIG_IOCTRL_RW_AFE_LANE4_CTRL_2_12_reg", "OA_LANE4_HSRX_DPHY_DDL_BYPASS_EN_OVR_VAL", hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_B_CORE_DIG_IOCTRL_RW_AFE_LANE0_CTRL_2_13_reg", "OA_LANE0_HSRX_DPHY_DDL_BYPASS_EN_OVR_EN", hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_B_CORE_DIG_IOCTRL_RW_AFE_LANE1_CTRL_2_13_reg", "OA_LANE1_HSRX_DPHY_DDL_BYPASS_EN_OVR_EN", hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_B_CORE_DIG_IOCTRL_RW_AFE_LANE2_CTRL_2_13_reg", "OA_LANE2_HSRX_DPHY_DDL_BYPASS_EN_OVR_EN", hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_B_CORE_DIG_IOCTRL_RW_AFE_LANE3_CTRL_2_13_reg", "OA_LANE3_HSRX_DPHY_DDL_BYPASS_EN_OVR_EN", hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_B_CORE_DIG_IOCTRL_RW_AFE_LANE4_CTRL_2_13_reg", "OA_LANE4_HSRX_DPHY_DDL_BYPASS_EN_OVR_EN", hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_B_CORE_DIG_IOCTRL_RW_AFE_LANE2_CTRL_2_9_reg", "OA_LANE2_HSRX_HS_CLK_DIV", self.OA_LANE2_HSRX_HS_CLK_DIV_CALCVAL_DICT.get(self.range_key_by_speed_LANE2_CTRL_2_9, None)],
            ["_B_CORE_DIG_DLANE_CLK_RW_HS_RX_0_reg", "HS_RX_0_TCLKSETTLE_reg", hex(28)],
            ["_B_CORE_DIG_DLANE_CLK_RW_HS_RX_0_reg", "HS_RX_0_THSSETTLE_reg", self.HS_RX_0_THSSETTLE_REG_CALCVAL],
            ["_B_CORE_DIG_DLANE_0_RW_HS_RX_0_reg", "HS_RX_0_THSSETTLE_reg", self.HS_RX_0_THSSETTLE_REG_CALCVAL],
            ["_B_CORE_DIG_DLANE_1_RW_HS_RX_0_reg", "HS_RX_0_THSSETTLE_reg", self.HS_RX_0_THSSETTLE_REG_CALCVAL],
            ["_B_CORE_DIG_DLANE_2_RW_HS_RX_0_reg", "HS_RX_0_THSSETTLE_reg", self.HS_RX_0_THSSETTLE_REG_CALCVAL],
            ["_B_CORE_DIG_DLANE_3_RW_HS_RX_0_reg", "HS_RX_0_THSSETTLE_reg", self.HS_RX_0_THSSETTLE_REG_CALCVAL],
            ["_B_CORE_DIG_DLANE_0_RW_CFG_1_reg", "CFG_1_DESKEW_SUPPORTED_reg", hex(1 if self.rxParam_TimeBase > 1500 else 0)],
            ["_B_CORE_DIG_DLANE_0_RW_CFG_1_reg", "CFG_1_SOT_DETECTION_reg", hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_B_CORE_DIG_DLANE_1_RW_CFG_1_reg", "CFG_1_DESKEW_SUPPORTED_reg", hex(1 if self.rxParam_TimeBase > 1500 else 0)],
            ["_B_CORE_DIG_DLANE_1_RW_CFG_1_reg", "CFG_1_SOT_DETECTION_reg", hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_B_CORE_DIG_DLANE_2_RW_CFG_1_reg", "CFG_1_DESKEW_SUPPORTED_reg", hex(1 if self.rxParam_TimeBase > 1500 else 0)],
            ["_B_CORE_DIG_DLANE_2_RW_CFG_1_reg", "CFG_1_SOT_DETECTION_reg", hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_B_CORE_DIG_DLANE_3_RW_CFG_1_reg", "CFG_1_DESKEW_SUPPORTED_reg", hex(1 if self.rxParam_TimeBase > 1500 else 0)],
            ["_B_CORE_DIG_DLANE_3_RW_CFG_1_reg", "CFG_1_SOT_DETECTION_reg", hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_B_CORE_DIG_DLANE_CLK_RW_CFG_1_reg", "CFG_1_DESKEW_SUPPORTED_reg", hex(1 if self.rxParam_TimeBase > 1500 else 0)],
            ["_B_CORE_DIG_DLANE_CLK_RW_CFG_1_reg", "CFG_1_SOT_DETECTION_reg", hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_B_CORE_DIG_DLANE_0_RW_HS_RX_2_reg", "HS_RX_2_IGNORE_ALTERNCAL_reg", hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_B_CORE_DIG_DLANE_1_RW_HS_RX_2_reg", "HS_RX_2_IGNORE_ALTERNCAL_reg", hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_B_CORE_DIG_DLANE_2_RW_HS_RX_2_reg", "HS_RX_2_IGNORE_ALTERNCAL_reg", hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_B_CORE_DIG_DLANE_3_RW_HS_RX_2_reg", "HS_RX_2_IGNORE_ALTERNCAL_reg", hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_B_CORE_DIG_DLANE_CLK_RW_HS_RX_2_reg", "HS_RX_2_IGNORE_ALTERNCAL_reg", hex(0 if self.rxParam_TimeBase > 1500 else 1)],
            ["_B_CORE_DIG_DLANE_0_RW_HS_RX_3_reg", "HS_RX_3_FJUMP_DESKEW_reg",  self.HS_RX_3_FJUMP_DESKEW_REG_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_B_CORE_DIG_DLANE_1_RW_HS_RX_3_reg", "HS_RX_3_FJUMP_DESKEW_reg", self.HS_RX_3_FJUMP_DESKEW_REG_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_B_CORE_DIG_DLANE_2_RW_HS_RX_3_reg", "HS_RX_3_FJUMP_DESKEW_reg", self.HS_RX_3_FJUMP_DESKEW_REG_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_B_CORE_DIG_DLANE_3_RW_HS_RX_3_reg", "HS_RX_3_FJUMP_DESKEW_reg", self.HS_RX_3_FJUMP_DESKEW_REG_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_B_CORE_DIG_DLANE_CLK_RW_HS_RX_3_reg", "HS_RX_3_FJUMP_DESKEW_reg", self.HS_RX_3_FJUMP_DESKEW_REG_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_B_CORE_DIG_DLANE_0_RW_HS_RX_6_reg", "HS_RX_6_MIN_EYE_OPENING_DESKEW_reg", self.MIN_EYE_OPENING_DESKEW_REG_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_B_CORE_DIG_DLANE_1_RW_HS_RX_6_reg", "HS_RX_6_MIN_EYE_OPENING_DESKEW_reg", self.MIN_EYE_OPENING_DESKEW_REG_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_B_CORE_DIG_DLANE_2_RW_HS_RX_6_reg", "HS_RX_6_MIN_EYE_OPENING_DESKEW_reg", self.MIN_EYE_OPENING_DESKEW_REG_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_B_CORE_DIG_DLANE_3_RW_HS_RX_6_reg", "HS_RX_6_MIN_EYE_OPENING_DESKEW_reg", self.MIN_EYE_OPENING_DESKEW_REG_CALCVAL_DICT.get(self.range_key_by_speed, None)],
            ["_B_CORE_DIG_DLANE_CLK_RW_HS_RX_6_reg", "HS_RX_6_MIN_EYE_OPENING_DESKEW_reg", self.MIN_EYE_OPENING_DESKEW_REG_CALCVAL_DICT.get(self.range_key_by_speed, None)]]


        #####################################################################################          TX PY    #############################################################
        def set_esc_clk_values():
            for esc_clk_div in range(2, 100):
                esc_clk = self.rxParam_TimeBase/(8*esc_clk_div)
                if 5 <= esc_clk <= 20:
                    return {'esc_clk_div':esc_clk_div,'esc_clk':esc_clk}

        self.csi_tx_T_DCO = 5
        self.csi_tx_T_DCO_MIN = 5.26
        self.csi_tx_T_DCO_MAX = 4.77
        self.csi_tx_T_DCO_MID = 5.02
        self.csi_tx_LP_FREQ = 20
        self.csi_tx_hs_clk_freq = self.rxParam_TimeBase * 500
        self.csi_tx_ui = 1000000 /( self.csi_tx_hs_clk_freq * 2)
        self.csi_tx_mult = 1.1
        self.csi_tx_tlpx = 50 * self.csi_tx_mult
        self.csi_tx_lptx_en_dly = 5
        self.csi_tx_wordclk_period = self.csi_tx_ui * 8
        self.csi_tx_lptx_io_sr0_fall_dly = 12.5
        self.csi_tx_tlptxoverlap_reg = self.csi_tx_lptx_en_dly / self.csi_tx_T_DCO_MAX
        self.csi_tx_tlp11init_dco_reg = (5 * 1000000 / ( (self.csi_tx_LP_FREQ) * 1000) / self.csi_tx_T_DCO_MAX) - 1
        self.csi_tx_tlp11end_dco_reg = (5 * 1000000 / ( (self.csi_tx_LP_FREQ) * 1000) / self.csi_tx_T_DCO_MAX) - 1
        self.csi_tx_tlpx_dco_reg = self.csi_tx_tlpx / self.csi_tx_T_DCO_MAX - 1
        self.csi_tx_hs_exit = 100 * self.csi_tx_mult
        self.csi_tx_hs_exit_reg = self.csi_tx_hs_exit  /  self.csi_tx_T_DCO_MAX - 1
        self.csi_tx_d2a_hstx_dly = 3
        self.csi_tx_clk_pre_reg = 3
        self.csi_tx_hs_prepare_dco = math.ceil(1.1 * (statistics.mean([40 + 4 * self.csi_tx_ui, 85 + 6 * self.csi_tx_ui])))
        self.csi_tx_clk_prepare = 66
        self.csi_tx_clk_zero = 257
        self.csi_tx_t3_prepare_dco = 38 + ((95-38)/2)
        self.csi_tx_t3_prepare_dco_reg = (self.csi_tx_t3_prepare_dco + self.csi_tx_lptx_io_sr0_fall_dly) / self.csi_tx_T_DCO_MID - 1
        self.csi_tx_t_hs_trail = 1.1 * (60 + 4 * self.csi_tx_ui)
        self.csi_tx_t_clk_trail = 1.1 * 60
        self.csi_tx_t_clk_post = 1.1 * (60 + 52 * self.csi_tx_ui)
        self.csi_tx_hs_zero = (145 + 10 * self.csi_tx_ui) - self.csi_tx_hs_prepare_dco
        self.csi_tx_TEOTmax =  105 + 12 * self.csi_tx_ui

        self.csi_tx_t3_prepare = 50
        self.csi_tx_t3_PROGSEQ = 14 * self.csi_tx_ui
        self.csi_tx_t3_PREAMBLE = 3050
        self.csi_tx_Cphy_word_clock_period = 7 * self.rxParam_TimeBase / 1000
        self.csi_tx_Cphy_UI = 1000 / self.rxParam_TimeBase
        self.csi_tx_tlpx = 55
        self.csi_tx_t3_PREEND = 7 * self.csi_tx_Cphy_UI
        self.csi_tx_t3_SYNC = 7 * self.csi_tx_Cphy_UI
        self.csi_tx_t3_PREBEGIN = self.csi_tx_Cphy_UI * 10
        self.csi_tx_t3_POST = 220 * self.csi_tx_Cphy_UI


        self.CLK_HS_TX_1_THSZERO_REG_CALCVAL = math.ceil(((self.csi_tx_tlpx + self.csi_tx_clk_prepare + self.csi_tx_clk_zero + 5 * self.csi_tx_T_DCO_MAX - 3 * self.csi_tx_wordclk_period ) / self.csi_tx_wordclk_period -1))

        self.HS_TX_8_TCLKPOST_REG_CALCVAL = math.ceil(self.csi_tx_t_clk_post / self.csi_tx_wordclk_period - 3)

        self.RW_HS_TX_1_THSZERO_REG_CALCVAL = math.ceil((self.csi_tx_tlpx + self.csi_tx_hs_prepare_dco + self.csi_tx_hs_zero + 5 * self.csi_tx_T_DCO_MAX - 3 * self.csi_tx_wordclk_period) / self.csi_tx_wordclk_period - 1)\
            if math.ceil((self.csi_tx_tlpx + self.csi_tx_hs_prepare_dco + self.csi_tx_hs_zero + 5 * self.csi_tx_T_DCO_MAX - 3 * self.csi_tx_wordclk_period) / self.csi_tx_wordclk_period - 1) > 0 else 0

        self.HS_TX_0_THSTRAIL_REG_CALCVAL = round( ( self.csi_tx_t_clk_trail + ((self.csi_tx_TEOTmax - self.csi_tx_t_clk_trail) / 2)) / self.csi_tx_wordclk_period - 1 + self.csi_tx_d2a_hstx_dly )

        self.HS_TX_5_THSTRAIL_DCO_REG_CALCVAL = math.ceil( ( ( self.HS_TX_0_THSTRAIL_REG_CALCVAL + 1) * self.csi_tx_wordclk_period - self.csi_tx_wordclk_period - 4 * self.csi_tx_T_DCO_MAX) /self.csi_tx_T_DCO_MAX - 1)

        self.HS_TX_9_THSPRPR_DCO_REG_CALCVAL = math.ceil( ( self.csi_tx_lptx_io_sr0_fall_dly + self.csi_tx_hs_prepare_dco) / self.csi_tx_T_DCO_MID ) - 1

        self.HS_TX_2_TCALPREAMBLE_REG_CALCVAL = ((self.csi_tx_tlpx + self.csi_tx_tlpx + self.csi_tx_t3_prepare + self.csi_tx_t3_PREAMBLE + 5 * self.csi_tx_T_DCO_MAX - 3 * self.csi_tx_Cphy_word_clock_period ) / self.csi_tx_Cphy_word_clock_period ) - 1

        self.HS_TX_10_TLP11INIT_DCO_REG_CALCVAL = round((5 * 1 / set_esc_clk_values()['esc_clk']) / (1 / 200))

        # self.csi_tx_local_reg_info_lut_nt = namedtuple('csi_tx_local_reg_info_lut_nt','reg_name, reg_field, field_val')
        self.csi_tx_local_reg_info = [
            ["_A_P{}_CORE_DIG_DLANE_CLK_RW_HS_TX_1_reg".format(self.all), "A_P{}_HS_TX_1_THSZERO_REG".format(self.all), hex(self.CLK_HS_TX_1_THSZERO_REG_CALCVAL)],
            ["_A_P{}_CORE_DIG_DLANE_CLK_RW_HS_TX_0_reg".format(self.all), "A_P{}_HS_TX_0_THSTRAIL_REG".format(self.all), hex(self.HS_TX_0_THSTRAIL_REG_CALCVAL)],
            ["_A_P{}_CORE_DIG_DLANE_CLK_RW_HS_TX_5_reg".format(self.all), "A_P{}_HS_TX_5_THSTRAIL_DCO_REG".format(self.all), hex(self.HS_TX_5_THSTRAIL_DCO_REG_CALCVAL)],
            ["_A_P{}_CORE_DIG_DLANE_CLK_RW_HS_TX_8_reg".format(self.all), "A_P{}_HS_TX_8_TCLKPOST_REG".format(self.all),hex(45)],# Old version -hex(self.HS_TX_8_TCLKPOST_REG_CALCVAL)
            ["_A_P{}_CORE_DIG_DLANE_0_RW_HS_TX_1_reg".format(self.all), "A_P{}_HS_TX_1_THSZERO_REG".format(self.all), hex(self.RW_HS_TX_1_THSZERO_REG_CALCVAL)],
            ["_A_P{}_CORE_DIG_DLANE_1_RW_HS_TX_1_reg".format(self.all), "A_P{}_HS_TX_1_THSZERO_REG".format(self.all), hex(self.RW_HS_TX_1_THSZERO_REG_CALCVAL)],
            ["_A_P{}_CORE_DIG_DLANE_2_RW_HS_TX_1_reg".format(self.all), "A_P{}_HS_TX_1_THSZERO_REG".format(self.all), hex(self.RW_HS_TX_1_THSZERO_REG_CALCVAL)],
            ["_A_P{}_CORE_DIG_DLANE_3_RW_HS_TX_1_reg".format(self.all), "A_P{}_HS_TX_1_THSZERO_REG".format(self.all), hex(self.RW_HS_TX_1_THSZERO_REG_CALCVAL)],
            ["_A_P{}_CORE_DIG_DLANE_0_RW_HS_TX_0_reg".format(self.all), "A_P{}_HS_TX_0_THSTRAIL_REG".format(self.all), hex(self.HS_TX_0_THSTRAIL_REG_CALCVAL)],
            ["_A_P{}_CORE_DIG_DLANE_1_RW_HS_TX_0_reg".format(self.all), "A_P{}_HS_TX_0_THSTRAIL_REG".format(self.all), hex(self.HS_TX_0_THSTRAIL_REG_CALCVAL)],
            ["_A_P{}_CORE_DIG_DLANE_2_RW_HS_TX_0_reg".format(self.all), "A_P{}_HS_TX_0_THSTRAIL_REG".format(self.all), hex(self.HS_TX_0_THSTRAIL_REG_CALCVAL)],
            ["_A_P{}_CORE_DIG_DLANE_3_RW_HS_TX_0_reg".format(self.all), "A_P{}_HS_TX_0_THSTRAIL_REG".format(self.all), hex(self.HS_TX_0_THSTRAIL_REG_CALCVAL)],
            ["_A_P{}_CORE_DIG_DLANE_0_RW_HS_TX_5_reg".format(self.all), "A_P{}_HS_TX_5_THSTRAIL_DCO_REG".format(self.all), hex(self.HS_TX_5_THSTRAIL_DCO_REG_CALCVAL)],
            ["_A_P{}_CORE_DIG_DLANE_1_RW_HS_TX_5_reg".format(self.all), "A_P{}_HS_TX_5_THSTRAIL_DCO_REG".format(self.all), hex(self.HS_TX_5_THSTRAIL_DCO_REG_CALCVAL)],
            ["_A_P{}_CORE_DIG_DLANE_2_RW_HS_TX_5_reg".format(self.all), "A_P{}_HS_TX_5_THSTRAIL_DCO_REG".format(self.all), hex(self.HS_TX_5_THSTRAIL_DCO_REG_CALCVAL)],
            ["_A_P{}_CORE_DIG_DLANE_3_RW_HS_TX_5_reg".format(self.all), "A_P{}_HS_TX_5_THSTRAIL_DCO_REG".format(self.all), hex(self.HS_TX_5_THSTRAIL_DCO_REG_CALCVAL)],
            ["_A_P{}_CORE_DIG_DLANE_0_RW_HS_TX_9_reg".format(self.all), "A_P{}_HS_TX_9_THSPRPR_DCO_REG".format(self.all), hex(self.HS_TX_9_THSPRPR_DCO_REG_CALCVAL)],
            ["_A_P{}_CORE_DIG_DLANE_1_RW_HS_TX_9_reg".format(self.all), "A_P{}_HS_TX_9_THSPRPR_DCO_REG".format(self.all), hex(self.HS_TX_9_THSPRPR_DCO_REG_CALCVAL)],
            ["_A_P{}_CORE_DIG_DLANE_2_RW_HS_TX_9_reg".format(self.all), "A_P{}_HS_TX_9_THSPRPR_DCO_REG".format(self.all), hex(self.HS_TX_9_THSPRPR_DCO_REG_CALCVAL)],
            ["_A_P{}_CORE_DIG_DLANE_3_RW_HS_TX_9_reg".format(self.all), "A_P{}_HS_TX_9_THSPRPR_DCO_REG".format(self.all), hex(self.HS_TX_9_THSPRPR_DCO_REG_CALCVAL)],
            ["_A_P{}_CORE_DIG_DLANE_0_RW_HS_TX_10_reg".format(self.all), "A_P{}_HS_TX_10_TLP11INIT_DCO_REG".format(self.all), hex(self.HS_TX_10_TLP11INIT_DCO_REG_CALCVAL)],
            ["_A_P{}_CORE_DIG_DLANE_1_RW_HS_TX_10_reg".format(self.all), "A_P{}_HS_TX_10_TLP11INIT_DCO_REG".format(self.all), hex(self.HS_TX_10_TLP11INIT_DCO_REG_CALCVAL)],
            ["_A_P{}_CORE_DIG_DLANE_2_RW_HS_TX_10_reg".format(self.all), "A_P{}_HS_TX_10_TLP11INIT_DCO_REG".format(self.all), hex(self.HS_TX_10_TLP11INIT_DCO_REG_CALCVAL)],
            ["_A_P{}_CORE_DIG_DLANE_3_RW_HS_TX_10_reg".format(self.all), "A_P{}_HS_TX_10_TLP11INIT_DCO_REG".format(self.all), hex(self.HS_TX_10_TLP11INIT_DCO_REG_CALCVAL)],
            ["_A_P{}_CORE_DIG_DLANE_CLK_RW_HS_TX_10_reg".format(self.all), "A_P{}_HS_TX_10_TLP11INIT_DCO_REG".format(self.all), hex(self.HS_TX_10_TLP11INIT_DCO_REG_CALCVAL)],
            ["_A_P{}_CORE_DIG_DLANE_0_RW_HS_TX_6_reg".format(self.all), "A_P{}_HS_TX_6_TLP11END_DCO_REG".format(self.all), hex(self.HS_TX_10_TLP11INIT_DCO_REG_CALCVAL)],
            ["_A_P{}_CORE_DIG_DLANE_1_RW_HS_TX_6_reg".format(self.all),"A_P{}_HS_TX_6_TLP11END_DCO_REG".format(self.all), hex(self.HS_TX_10_TLP11INIT_DCO_REG_CALCVAL)],
            ["_A_P{}_CORE_DIG_DLANE_2_RW_HS_TX_6_reg".format(self.all),"A_P{}_HS_TX_6_TLP11END_DCO_REG".format(self.all), hex(self.HS_TX_10_TLP11INIT_DCO_REG_CALCVAL)],
            ["_A_P{}_CORE_DIG_DLANE_3_RW_HS_TX_6_reg".format(self.all), "A_P{}_HS_TX_6_TLP11END_DCO_REG".format(self.all), hex(self.HS_TX_10_TLP11INIT_DCO_REG_CALCVAL)],
            ["_A_P{}_CORE_DIG_DLANE_CLK_RW_HS_TX_6_reg".format(self.all),"A_P{}_HS_TX_6_TLP11END_DCO_REG".format(self.all), hex(self.HS_TX_10_TLP11INIT_DCO_REG_CALCVAL)]]

        #####################################################################################          PLL FRAC  #############################################################

        self.Fclkin = 25
        self.VCO_min = 1000 # MHz
        self.VCO_max = 2250 # MHz
        self.SSC_mod_frequency = 31.5
        self.SSC_mod_depth = 5000
        self.esc_clk_div = set_esc_clk_values()['esc_clk_div']
        self.ecs_clock = self.rxParam_TimeBase/(8*self.esc_clk_div)

        self.PLL_output_freq = self.rxParam_TimeBase * 1e6 / 2
        self.ssc_mod_deph = 0
        self.ssc_mod_freq = 0
        self.loop_ref_frequency = self.Fclkin * 1e6
        self.P = self.set_P()
        self.Mint = self.multiplication_integer * 4
        self.N = 1
        self.pll_frac_den = 1
        self.frac_num = self.pll_frac_den * self.fractional
        self.pll_n = self.N - 1
        self.pll_mint = int(self.multiplication_integer * 4 -32)# =I8*4-32
        self.pll_m = self.pll_mint + 32
        self.pll_cpbias_cntrl = self.pll_vco_cntrl = 0
        self.pll_fracn_en = 1
        self.pll_ssc_en = 0
        self.pll_ssc_peak = round(2*self.multiplication_integer * math.fabs(self.ssc_mod_deph)*math.pow(2,16)) #=ROUND(2*I8*ABS(E8)*2^16,0)
        self.pll_stepsize = round((4*self.ssc_mod_freq*self.multiplication_integer*math.fabs(self.ssc_mod_deph)*math.pow(2,25))/self.loop_ref_frequency)# =ROUND((4*F8*I8*ABS(E8)*2^25)/M8,0)

        self.pll_frac_quot = int(self.frac_num*math.pow(2, 17)/self.pll_frac_den)# =INT(N8*2^17/Y8)
        self.pll_frac_rem = 0

        # self.csi_pll_frac_reg_info_lut_nt = namedtuple('csi_pll_frac_reg_info_lut_nt','reg_name, reg_field, field_val')
        self.csi_pll_frac_reg_info = [
            ["_A_cfg_all{}_cfg_all{}_phy_regs2".format(self.all,self.all), "A_cfg_all{}_cfg_all{}_phy_int_cntrl".format(self.all,self.all), hex(1 if self.PLL_output_freq < 350 else 0)],  # =IF(D8<350,1,0)
            ["_A_cfg_all{}_cfg_all{}_phy_regs".format(self.all,self.all), "A_cfg_all{}_cfg_all{}_phy_pll_prop_cntrl".format(self.all,self.all), hex(5)],
            ["_A_cfg_all{}_cfg_all{}_phy_regs".format(self.all,self.all), "A_cfg_all{}_cfg_all{}_phy_pll_m".format(self.all,self.all), hex(self.pll_m)],
            ["_A_cfg_all{}_cfg_all{}_phy_regs".format(self.all,self.all), "A_cfg_all{}_cfg_all{}_phy_pll_n".format(self.all,self.all), hex(self.pll_n)],
            ["_A_cfg_all{}_cfg_all{}_phy_reg4".format(self.all,self.all), "A_cfg_all{}_cfg_all{}_pll_cpbias".format(self.all,self.all), hex({1: 0, 2: 64, 4: 0, 8: 0, 16: 0, 32: 64}[self.P]) if self.P in (1, 2, 4, 8, 16, 32) else None],#=IF(OR($G$8=1,$G$8=4,$G$8=8,$G$8=16),0,IF(OR($G$8=2,$G$8=32),64,null))
            ["_A_cfg_all{}_cfg_all{}_phy_regs2".format(self.all,self.all), "A_cfg_all{}_cfg_all{}_pll_vco_cntrl".format(self.all,self.all), hex({1: 0, 2: 3*16, 4: 1*16, 8: 2*16, 16: 3*16, 32: 0}[self.P]) if self.P in (1, 2, 4, 8, 16, 32) else None],  # =IF(OR(G8=1,G8=32),0,IF(OR(G8=2,G8=16),3,IF(G8=4,1,IF(G8=8,2,null))))*16
            ["_A_C{}_CLKMGR_CFG_reg".format(self.all), "A_C{}_tx_esc_clk_division".format(self.all), hex(self.esc_clk_div)],
            ["_A_cfg_all{}_cfg_all{}_phy_frac2_reg".format(self.all,self.all), "A_cfg_all{}_cfg_all{}_phy_mint".format(self.all,self.all), hex(self.pll_mint)],
            ["_A_cfg_all{}_cfg_all{}_phy_frac1_reg".format(self.all,self.all), "A_cfg_all{}_cfg_all{}_phy_frac_quot".format(self.all,self.all), hex(self.pll_frac_quot)],
            ["_A_cfg_all{}_cfg_all{}_phy_frac2_reg".format(self.all,self.all), "A_cfg_all{}_cfg_all{}_phy_frac_rem".format(self.all,self.all), hex(0)],
            ["_A_cfg_all{}_cfg_all{}_phy_frac1_reg".format(self.all,self.all), "A_cfg_all{}_cfg_all{}_phy_frac_den".format(self.all,self.all), hex(1)],
            ["_A_cfg_all{}_cfg_all{}_phy_frac2_reg".format(self.all,self.all), "A_cfg_all{}_cfg_all{}_phy_fracn_en".format(self.all,self.all), hex(1)],
            ["_A_cfg_all{}_cfg_all{}_phy_frac2_reg".format(self.all,self.all), "A_cfg_all{}_cfg_all{}_phy_fracn_cfg_update_en".format(self.all,self.all), hex(1)]]

        #########################################################    Deskew  #############################################################

        self.csi_deskew_regs_info = [
                ["_A_cfg_all{}_cfg_all{}_deskew_between_timers".format(self.all, self.all), hex(0x500000)],
                ["_A_cfg_all{}_cfg_all{}_deskew_watchdog_timer".format(self.all, self.all), hex(0x100)],
                ["_A_cfg_all{}_cfg_all{}_deskew_duration_timer".format(self.all, self.all), hex(0x230)],
                ["_A_cfg_all{}_cfg_all{}_deskew_init_duration_timer".format(self.all, self.all), hex(0xD50)],
                ["_A_cfg_all{}_cfg_all{}_deskew_wait_duration_timer".format(self.all, self.all), hex(0xCE4)],
                ["_A_cfg_all{}_cfg_all{}_deskew_ctrl".format(self.all, self.all), hex(0x2)]]

    def set_P(self):
        for p in [1, 2, 4, 8, 16, 32]:
            self.multiplication_integer = math.floor((self.PLL_output_freq * p) / self.loop_ref_frequency * 4) / 4 # =FLOOR((D8*G8)/M8,0.25)
            self.fractional =(self.PLL_output_freq * p) / self.loop_ref_frequency - self.multiplication_integer # =(D8*G8)/M8-I8
            self.vco_frequency = self.loop_ref_frequency * (self.multiplication_integer + self.fractional) # =M8*(I8+K8)
            if self.VCO_min*1e6 <= self.vco_frequency <= self.VCO_max*1e6:
                return p

    @property
    def range_key_by_speed(self):

        if self.rxParam_TimeBase >= 4500:
            return '4500'
        if self.rxParam_TimeBase >= 4000:
            return '4000'
        if self.rxParam_TimeBase >= 3600:
            return '3600'
        if self.rxParam_TimeBase >= 3230:
            return '3230'
        if self.rxParam_TimeBase >= 3000:
            return '3000'
        if self.rxParam_TimeBase >= 2700:
            return '2700'
        if self.rxParam_TimeBase >= 2455:
            return '2455'
        if self.rxParam_TimeBase >= 2250:
            return '2250'
        if self.rxParam_TimeBase >= 2077:
            return '2077'
        if self.rxParam_TimeBase >= 1929:
            return '1929'
        if self.rxParam_TimeBase >= 1800:
            return '1800'
        if self.rxParam_TimeBase >= 1688:
            return '1688'
        if self.rxParam_TimeBase >= 1588:
            return '1588'
        if self.rxParam_TimeBase >= 1500:
            return '1500'
        return None

    @property
    def range_key_by_speed_LANE2_CTRL_2_9(self):

        if self.rxParam_TimeBase >= 2560:
            return '2560'
        if self.rxParam_TimeBase >= 1280:
            return '1280'
        if self.rxParam_TimeBase >= 640:
            return '640'
        if self.rxParam_TimeBase >= 320:
            return '320'
        if self.rxParam_TimeBase >= 160:
            return '160'
        if self.rxParam_TimeBase >= 80:
            return '80'

        else:
            return None

    # def get_csi_rx_local_reg_info(self, reg = None, field = None):
    #     return self.csi_rx_local_reg_info_lut_nt._make(*(x for x in self.csi_rx_local_reg_info if x[0] == reg and x[1] == field))
    #
    # def get_csi_tx_local_reg_info(self, reg = None, field = None):
    #
    #     return self.csi_tx_local_reg_info_lut_nt._make(*(x for x in self.csi_tx_local_reg_info if x[0] == reg and x[1] == field))
    #
    # def get_csi_pll_frac_reg_info(self, reg = None, field = None):
    #     return self.csi_pll_frac_reg_info_lut_nt._make(*(x for x in self.csi_pll_frac_reg_info if x[0] == reg and x[1] == field))


if __name__ == "__main__":

    calc = csiSpeedCalculator(1200)
    local_reg_prefix = "B_"
    remote_reg_prefix = "csi_tadp_tx_0_"
    for reg in calc.csi_rx_local_reg_info:
        reg_info = calc.get_csi_rx_local_reg_info(reg = reg[0], field = reg[1])
        print( reg_info.field_val)
        print(local_reg_prefix + reg_info.reg_name)
        print(local_reg_prefix + reg_info.reg_field + "\r\n##########REMOTE REGISTER VAL#################\r\n")
        print(reg_info.field_val)
        print(remote_reg_prefix + reg_info.reg_name)
        print(remote_reg_prefix + reg_info.reg_field + "\r\n##########LOCAL REGISTER VAL#################\r\n")

    # for reg in calc.csi_tx_local_reg_info:
    #     reg_info = calc.get_csi_tx_local_reg_info(reg = reg[0], field = reg[1])
    #     print( reg_info.tx_field_val)
    #     print(reg_info.tx_reg_name)
    #     print(reg_info.tx_reg_field + "\r\n###########################\r\n")
