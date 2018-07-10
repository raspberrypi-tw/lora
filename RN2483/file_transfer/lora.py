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
# The LoRa RN2483 class to implement RN2483 LoRa functions
#
# Author : sosorry
# Date   : 10/03/2017
#

import serial
import time
import re
import json
import packer
import RN2483

class RN2483:

    def __init__(self, port):
        self.ser = None
        self.port = port
        self.baudrate = 57600
        self.retry = 5
        self.max_payload_length = 255


    def Init_Serial(self):

        if self.ser == None:
            self.ser = serial.Serial(self.port, self.baudrate)

            if self.ser.isOpen() == False:
                self.ser.open()

            self.ser.bytesize = 8
            self.ser.parity   = "N"
            self.ser.stopbits = 1
            self.ser.timeout  = 5

            print('cmd> radio cw off')
            self.ser.write(b'radio cw off\r\n')
            print(str(self.ser.readline()))

            print('cmd> radio set pwr 14')
            self.ser.write(b'radio set pwr 14\r\n')
            print(str(self.ser.readline()))

            print('cmd> radio set bw 125')
            self.ser.write(b'radio set bw 125\r\n')
            print(str(self.ser.readline()))

            print('cmd> radio set sf sf12')
            self.ser.write(b'radio set sf sf12\r\n')
            print(str(self.ser.readline()))

            print('cmd> radio set cr 4/5')
            self.ser.write(b'radio set cr 4/5\r\n')
            print(str(self.ser.readline()))

            print('cmd> radio set freq 434100000')
            self.ser.write(b'radio set freq 434100000\r\n')
            print(str(self.ser.readline()))

            print('cmd> mac pause')
            self.ser.write(b'mac pause\r\n')
            print(str(self.ser.readline()))

        return self.ser



    def Send_and_Wait_ACK(self, data):
        cmd = "radio tx "
        _length, _payload = packer.Pack_Str( json.dumps(data) )


        if int(_length) < int(self.max_payload_length):
            print("Time: " + str(time.ctime()))
            byte_rawinput = bytes(cmd + _payload)
            print "====="
            print(byte_rawinput)
            print "====="
            self.ser.write(byte_rawinput)
            self.ser.readline()
            time.sleep(0.5 + 0.01 * int(_length))
            print("Ready to receive ACK")
            ret = self.ser.readline()

            if ret == "ok" or "radio_tx_ok" :
                self.ser.write(b'radio rx 0\r\n')
                ret = self.ser.readline()
                ret = self.ser.readline()

                if re.match('^radio_rx', str(ret).strip()):
                    payload = ret.split("  ", 1)[1]
                    _length, _payload = packer.Unpack_Str(payload)

                    _payload = json.loads(_payload)


                    if _payload["data"] == packer.ACK:
                        print("Receive ACK from " + str(_payload["id"]))
                        #break
                else:
                    for i in range(0, self.retry):
                        time.sleep(i*2)
                        print("Retry %d", i)

                        self.ser.write(b'radio rx 0\r\n')

                        ret = self.ser.readline()
                        ret = self.ser.readline()
                        ret = self.ser.readline()

                        if re.match('^radio_rx', str(ret).strip()):
                            payload = ret.split("  ", 1)[1]
                            _length, _payload = packer.Unpack_Str(payload)

                            _payload = json.loads(_payload)

                            if _payload["data"] == packer.ACK:
                                print("Receive ACK from " + str(_payload["id"]))
                                break


                        cmd = "radio tx "
                        #_length, _payload = packer.Pack_Str(rawinput)
                        _length, _payload = packer.Pack_Str( json.dumps(data) )
                        byte_rawinput = bytes(cmd + _payload)
                        self.ser.write(byte_rawinput)
                        self.ser.readline()


                        if i == self.retry - 1:
                            print("Reset serial")
                            self.ser.close()
                            time.sleep(0.2)
                            self.ser = None
                            self.ser = self.Init_Serial(self.ser)
                            break


