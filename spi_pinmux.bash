#!/bin/bash

sudo apt-get install devmem2

#Bank: 0 Reg: 0x0243d058 Val: 0x00000400 -> spi1_mosi_pz5
#Bank: 0 Reg: 0x0243d020 Val: 0x00000458 -> spi1_miso_pz4
#Bank: 0 Reg: 0x0243d040 Val: 0x00000400 -> spi1_sck_pz3
#Bank: 0 Reg: 0x0243d010 Val: 0x00000400 -> spi1_cs0_pz6
#Bank: 0 Reg: 0x0243d050 Val: 0x00000400 -> spi1_cs1_pz7

sudo devmem2 0x0243d058 word 0x400
sudo devmem2 0x0243d020 word 0x458
sudo devmem2 0x0243d040 word 0x400
sudo devmem2 0x0243d010 word 0x400
sudo devmem2 0x0243d050 word 0x400

sudo cat /sys/kernel/debug/tegra_pinctrl_reg | grep -i spi1 | grep -iv qspi
