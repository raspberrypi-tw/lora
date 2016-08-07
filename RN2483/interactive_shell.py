#!/usr/bin/python
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|.|c|o|m|.|t|w|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# Copyright (c) 2016, raspberrypi.com.tw
# All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# interactive_shell.py
# An interactive shell for Microchip RN2483 compatible with python2/3
#
# Author : sosorry
# Date   : 08/06/2016
#
# Example: >>> sys get ver
#          RN2483 1.0.1 Dec 15 2015 09:38:09

import serial

BAUDRATE = 57600               # the baud rate we talk to the lora
TIMEOUT = 1

try:
    input = raw_input
except NameError:
    pass

serial_port = input("Serial Port? ")

# open up the FTDI serial port to get data transmitted to lora
ser = serial.Serial(serial_port, BAUDRATE, timeout=TIMEOUT)

if ser.isOpen() == False:
    ser.open()

# The default settings for the UART interface are
# 57600 bps, 8 bits, no parity, 1 Stop bit, no flow control.
ser.bytesize = 8
ser.parity   = "N"
ser.stopbits = 1
ser.timeout  = 5

print("Device Opening: " + str(ser.isOpen()))
print('----------------------------------')

try:
    while True:

        rawinput = input(">>> ")

        if rawinput == "exit":
            break

        # for python3
        try:
            byte_rawinput = bytes(rawinput + "\r\n", encoding="UTF-8")

        # for python2
        except:
            byte_rawinput = bytes(rawinput + "\r\n")

        ser.write(byte_rawinput)


        response = ser.readline()

        # for python3
        try:
            print(str(response, encoding="UTF-8"))

        # for python2
        except:
            print(str(response))

finally:
    ser.close()

