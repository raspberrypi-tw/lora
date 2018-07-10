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
# gateway.py
# A demo gateway program for lora to receive message
#
# Author : sosorry
# Date   : 08/06/2016
#
# Example: $ sudo python gateway.py 
#


import serial
import time
import re
import json
import packer
import lora


# GLOBAL VARIABLE
GATEWAY_ID = "GW01"


#
# start here
#

try:
    input = raw_input
except NameError:
    pass

print('----------------------------------')

ser = None
ser = lora.Init_Serial(ser)

print('cmd> radio set wdt 0')
ser.write(b'radio set wdt 0\r\n')
print(str(ser.readline()))

print('----------------------------------')


try:
    while True:
        ser.write(b'radio rx 0\r\n')
        ret = ser.readline()

        if ret == "ok" or "radio_tx_ok" :

            payload = ser.readline()

            #print payload
            if re.match('^radio_rx', str(payload).strip()):
                data = payload.split("  ", 1)[1]
                print("Time: " + str(time.ctime()))

                _length, _data = packer.Unpack_Str(data)
                print("Receive: " + _data) 
                print("Length: " + str(_length))

                ser.write(b'radio get snr\r\n')
                snr = ser.readline()
                print("SNR: " + str(snr))

                device_id = json.loads(_data)["id"]

                if device_id.startswith("DV"):
                    time.sleep(0.1 + 0.02 * int(_length))
                    print('radio tx id=' + GATEWAY_ID + ',data=ACK')

                    data = {"id":GATEWAY_ID,"data":packer.ACK}
                    _length, _ack = packer.Pack_Str( json.dumps(data) )
                    ack = "radio tx " + str(_ack)
                    ser.write(ack)
                    ret = ser.readline()

                print('----------------------------------')

finally:
    if ser is not None:
        ser.close()

