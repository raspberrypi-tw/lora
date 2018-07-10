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
# lora.py
# A lora function to initial RN2483
#
# Author : sosorry
# Date   : 10/03/2017
#

import serial
import time
import re
import json
import packer

BAUDRATE = 57600               # the baud rate we talk to the microchip RN2483
RETRY = 3
MAX_PAYLOAD_LENGTH = 121
PORT = "/dev/ttyUSB0"


def Init_Serial(ser):

    if ser == None:
        ser = serial.Serial(PORT, BAUDRATE)

        if ser.isOpen() == False:
            ser.open()

        ser.bytesize = 8
        ser.parity   = "N"
        ser.stopbits = 1
        ser.timeout  = 5

        print('cmd> radio cw off')
        ser.write(b'radio cw off\r\n')
        print(str(ser.readline()))

        #print('cmd> radio set pwr -3')
        #ser.write(b'radio set pwr -3\r\n')
        print('cmd> radio set pwr 14')
        ser.write(b'radio set pwr 14\r\n')
        print(str(ser.readline()))

        print('cmd> radio set bw 125')
        ser.write(b'radio set bw 125\r\n')
        #print('cmd> radio set bw 500')
        #ser.write(b'radio set bw 500\r\n')
        print(str(ser.readline()))

        print('cmd> radio set sf sf12')
        ser.write(b'radio set sf sf12\r\n')
        #print('cmd> radio set sf sf7')
        #ser.write(b'radio set sf sf7\r\n')
        print(str(ser.readline()))

        print('cmd> radio set cr 4/5')
        ser.write(b'radio set cr 4/5\r\n')
        print(str(ser.readline()))

        #print('cmd> radio set freq 868100000')
        #ser.write(b'radio set freq 868100000\r\n')
        #print(str(ser.readline()))
        print('cmd> radio set freq 433000000')
        ser.write(b'radio set freq 433000000\r\n')
        print(str(ser.readline()))

        print('cmd> mac pause')
        ser.write(b'mac pause\r\n')
        print(str(ser.readline()))

    return ser


