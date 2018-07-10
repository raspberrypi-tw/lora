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
# test_lora_recv.py
# The simple test program for lora module to receive file
#
# Author : sosorry
# Date   : 10/03/2017
#
#!/usr/bin/python
# -*- coding: UTF-8 -*-

from Logger import Logger
from Socket import Socket
from LoRa import LoRa

rn = LoRa("RN2483")
socket = Socket(rn)

while True:
    data = socket.recv()

    if len(data) == 0:
        break;

socket.close()

