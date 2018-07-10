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
# sender.py
# A demo program for lora to send message
#
# Author : sosorry
# Date   : 08/06/2016
#
# Example: $ sudo python sender.py 
#            Serial Port? /dev/ttyUSB0
#

import serial
import time
import re
import json
import packer
import lora


# GLOBAL VARIABLE
DEVICE_ID = "DV01"
#DEVICE_ID = "DV02"


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

print('----------------------------------')


try:
    while True:

        rawinput = input(">>> ")

        try:
            byte_rawinput = bytes(rawinput + "\r\n")
        except:
            byte_rawinput = bytes(rawinput + "\r\n", encoding="UTF-8")


        data = {"id":DEVICE_ID,"data":rawinput}

        cmd = "radio tx "
        _length, _payload = packer.Pack_Str( json.dumps(data) )

        if int(_length) < int(lora.MAX_PAYLOAD_LENGTH):
            print("Time: " + str(time.ctime()))
            byte_rawinput = bytes(cmd + _payload)
            ser.write(byte_rawinput)
            ser.readline()
            time.sleep(0.5 + 0.01 * int(_length))
            print("Ready to receive ACK")
            ret = ser.readline()

            if ret == "ok" or "radio_tx_ok" :
                ser.write(b'radio rx 0\r\n')
                ret = ser.readline()
                ret = ser.readline()

                if re.match('^radio_rx', str(ret).strip()):
                    payload = ret.split("  ", 1)[1]
                    _length, _payload = packer.Unpack_Str(payload)

                    _payload = json.loads(_payload)

                    if _payload["data"] == packer.ACK:
                        print("Receive ACK from " + str(_payload["id"]))
                        #break
                else:
                    for i in range(0, lora.RETRY):
                        time.sleep(i*2)
                        print("Retry %d", i)

                        ser.write(b'radio rx 0\r\n')

                        ret = ser.readline()
                        ret = ser.readline()
                        ret = ser.readline()

                        if re.match('^radio_rx', str(ret).strip()):
                            payload = ret.split("  ", 1)[1]
                            _length, _payload = packer.Unpack_Str(payload)

                            _payload = json.loads(_payload)

                            if _payload["data"] == packer.ACK:
                                print("Receive ACK from " + str(_payload["id"]))
                                break

                        data = {"id":DEVICE_ID,"data":rawinput}

                        cmd = "radio tx "
                        #_length, _payload = packer.Pack_Str(rawinput)
                        _length, _payload = packer.Pack_Str( json.dumps(data) )
                        byte_rawinput = bytes(cmd + _payload)
                        ser.write(byte_rawinput)
                        ser.readline()


                        if i == lora.RETRY - 1:
                            print("Reset serial")
                            #ser.close()
                            #time.sleep(0.2)
                            #ser = None
                            ser = lora.Init_Serial(ser)
                            break

finally:
    if ser is not None:
        ser.close()

