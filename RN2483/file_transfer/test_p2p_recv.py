#!/usr/bin/python
# -*- coding: UTF-8 -*-
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|.|c|o|m|.|t|w|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# Copyright (c) 2016, raspberrypi.com.tw
# All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# p2p_recv.py
# A demo program for lora to receive message compatible with python2
#
# Author : sosorry
# Date   : 08/06/2016
#
# Example: $ python p2p_recv.py <device_path>
#

import time
import serial
import sys

try:
    device_path = sys.argv[1]
    lora = serial.Serial(device_path, 57600)
except:
    lora = serial.Serial("/dev/ttyUSB0", 57600)

print('cmd> radio cw off')
lora.write(b'radio cw off\r\n')
print(str(lora.readline()))

print('cmd> radio set pwr 15')
lora.write(b'radio set pwr 15\r\n')
print(str(lora.readline()))

print('cmd> radio bw 125')
lora.write(b'radio set bw 125\r\n')
print(str(lora.readline()))

print('cmd> radio sf 12')
lora.write(b'radio set sf sf12\r\n')
print(str(lora.readline()))

print('cmd> radio freq 434100000')
lora.write(b'radio set freq 434100000\r\n')
print(str(lora.readline()))
lora.write(b'mac pause\r\n')
print(str(lora.readline()))

try:
    while True:

        lora.write(b'radio rx 0\r\n')

        if lora.readline().strip() == "ok" or "radio_tx_ok" :
            raw =  str(lora.readline().strip()) 

            if raw.startswith('radio_rx'):
                print('----------------------------------')
                ts = str(time.time())
                print(raw)

finally:
    if lora is not None:
        lora.close()
