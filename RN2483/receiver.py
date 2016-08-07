#!/usr/bin/python
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

BAUDRATE = 57600               # the baud rate we talk to the microchip RN2483
TIMEOUT = 1

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

print("Device Opening: " + str(ser.isOpen()))
print('----------------------------------')

# signed decimal number representing the transceiver output power, 
# from -3 to 15.
print('radio set pwr 14')
ser.write(b'radio set pwr 14\r\n')
print(str(ser.readline()))

# decimal representing the operating radio bandwidth, in kHz. 
# Parameter values can be: 125, 250, 500.
print('radio set bw 250')
ser.write(b'radio set bw 250\r\n')
print(str(ser.readline()))

# decimal representing the frequency, 
# from 433000000 to 434800000 or from 863000000 to 870000000, in Hz.
print('radio set freq 868100000')
ser.write(b'radio set freq 868100000\r\n')
print(str(ser.readline()))

# pauses the LoRaWAN stack functionality to allow transceiver (radio) configuration 
# must be called before any radio transmission or reception
print('mac pause')
ser.write(b'mac pause\r\n')
print(str(ser.readline()))

#print('radio set wdt 2000')
#ser.write(b'radio set wdt 2000\r\n')
#print(str(ser.readline()))

# puts the radio into continuous Receive mode.
# from 0 to 65535, set '0' in order to enable the Continuous Reception mode
print('radio rx 0')
ser.write(b'radio rx 0\r\n')
print(str(ser.readline()))

try:
    while True:
        response = ser.readline()

        # for python3
        try:
            utf8_response = str(response, encoding="UTF-8").strip()

            if re.match('^radio_rx', utf8_response):
                print('radio rx 0')
                ser.write(b'radio rx 0\r\n')

                text = utf8_response.split("  ", 1)[1]
                print("receive: " + text + "\r\n")

        # for python2
        except:
            if re.match('^radio_rx', str(response).strip()):
                print('radio rx 0')
                ser.write(b'radio rx 0\r\n')

                text = response.split("  ", 1)[1]
                print("receive: " + text + "\r\n")

    time.sleep(1)

finally:
    ser.close()


