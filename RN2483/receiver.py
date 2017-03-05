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
# receiver.py
# A demo program for lora to receive message compatible with python2/3
#
# Author : sosorry
# Date   : 08/06/2016
#
# Example: $ sudo python receiver.py
#            Serial Port? /dev/ttyAMA0
#


import serial
import time
import re
import json
import packer

BAUDRATE = 57600               # the baud rate we talk to the microchip RN2483
MAX_PAYLOAD_LENGTH = 121

#
# start here
#

try:
    input = raw_input
except NameError:
    pass

serial_port = input("Serial Port? ")

# open up the FTDI serial port to get data transmitted to lora
ser = serial.Serial(serial_port, BAUDRATE)

if ser.isOpen() == False:
    ser.open()

# The default settings for the UART interface are
# 57600 bps, 8 bits, no parity, 1 Stop bit, no flow control.
ser.bytesize = 8
ser.parity   = "N"
ser.stopbits = 1
ser.timeout  = 5


print('----------------------------------')

print('cmd> radio cw off')
ser.write(b'radio cw off\r\n')
print(str(ser.readline()))

# signed decimal number representing the transceiver output power,
# from -3 to 15.
print('cmd> radio set pwr 14')
ser.write(b'radio set pwr 14\r\n')
print(str(ser.readline()))

# decimal representing the operating radio bandwidth, in kHz.
# Parameter values can be: 125, 250, 500.
print('cmd> radio set bw 250')
ser.write(b'radio set bw 250\r\n')
print(str(ser.readline()))

# decimal representing the frequency,
# from 433000000 to 434800000 or from 863000000 to 870000000, in Hz.
print('cmd> radio set freq 868100000')
ser.write(b'radio set freq 868100000\r\n')
print(str(ser.readline()))

# pauses the LoRaWAN stack functionality to allow transceiver (radio) configuration
# must be called before any radio transmission or reception
print('cmd> mac pause')
ser.write(b'mac pause\r\n')
print(str(ser.readline()))

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

            if re.match('^radio_rx', str(payload).strip()):
                data = payload.split("  ", 1)[1]
                _length, _data = packer.Unpack_Str(data)
                print("Time: " + str(time.ctime()))
                print("Receive: " + _data) 

                ser.write(b'radio get snr\r\n')
                snr = ser.readline()
                print("SNR: " + str(snr))

                time.sleep(0.1 + 0.02 * int(_length))
                print('radio tx ACK')
                _length, _ack = packer.Pack_Str(packer.ACK)
                ack = "radio tx " + str(_ack)
                ser.write(ack)
                ret = ser.readline()
                print('----------------------------------')

finally:
    ser.close()

