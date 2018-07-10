#!/usr/bin/python
# -*- coding: UTF-8 -*-
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|.|c|o|m|.|t|w|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# Copyright (c) 2018, raspberrypi.com.tw
# All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# p2p_send.py
# A demo program for lora to send message compatible with python2
#
# Author : sosorry
# Date   : 08/06/2016
#
# Example: $ python p2p_send.py <device_path>
#

import serial
import time
import sys

try:
    device_path = sys.argv[1]
    lora = serial.Serial(device_path, 57600)
except:
    lora = serial.Serial("/dev/ttyUSB0", 57600)

# bw=125
print('cmd> radio set bw 125')
lora.write(b'radio set bw 125\r\n')
print(str(lora.readline()))

# pwr=15
print('cmd> radio set pwr 15')
lora.write(b'radio set pwr 15\r\n')
print(str(lora.readline()))

# sf=sf12
print('cmd> radio set sf sf12')
lora.write(b'radio set sf sf12\r\n')
print(str(lora.readline()))

print('cmd> radio set freq 433000000')
lora.write(b'radio set freq 433000000\r\n')
print(str(lora.readline()))


while True:
    print('----------------------------------')

    lora.write(b'mac pause\r\n')
    lora.readline()

    t = int(time.time())

    cmd = 'radio tx ' + str(t) + '\r\n'
    print('cmd> ' + cmd.strip())

    byte_cmd = bytes(cmd)
    #print byte_cmd
    lora.write(byte_cmd)
    lora.readline()
    ret = lora.readline().strip()
    #print "ret of tx: " + ret   # ret=ok

    time.sleep(1 + 0.01 * int(len(cmd)))

