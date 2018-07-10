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
# test_lora_send.py
# The simple test program for lora module to send file
#
# Author : sosorry
# Date   : 10/03/2017
#

from Logger import Logger
from Socket import Socket
from LoRa import LoRa

rn = LoRa("RN2483")
socket=Socket(rn)
fd=socket.open("lena8rgb.jpg")
ack=socket.send_syn(fd)

while ack == True:
    ack = socket.send_data(fd)

socket.close()
