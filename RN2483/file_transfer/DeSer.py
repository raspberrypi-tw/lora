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
# DeSer.py
# The DeSer class is to SERialize and Deserialize data
#
# Author : sosorry
# Date   : 10/03/2017
#

import binascii, sys, os
import hashlib
from Logger import Logger

class DeSer:
    def __init__(self):
        self.name = None
        self.md5 = None
        self.hexlist = None
        self.hexlen = None

    def open(self, _src_file):
        self.hexlist = self.file_to_hex(_src_file)
        self.hexlen = len(self.hexlist)
        self.name = self.get_name(_src_file)
        self.md5 = self.md5sum(_src_file)

        return {'name':self.name,
                'md5':self.md5,
                'hexlist':self.hexlist,
                'hexlen':self.hexlen}

    def get_name(self, _src_file):
        head, tail = os.path.split(_src_file)
        return tail

    def file_to_hex(self, _src_file):
        try:
            with open(_src_file, 'rb') as f:
                hexdata = binascii.hexlify(f.read())

            hexlist = map(''.join, zip(*[iter(hexdata)]*2))
        except Exception as e:
            hexdata = None
            hexlist = None
            Logger.logr.error("Exception> %s" % (e) )

        return hexlist

    def hex_to_file(self, dst_file, hexlist):
        try:
            with open(dst_file, 'wb') as f:
                bytes = binascii.a2b_hex(''.join(hexlist))
                f.write(bytes)
        except Exception as e:
            Logger.logr.error("Exception> %s" % (e) )


    def md5sum(self, _src_file):
        return hashlib.md5(open(_src_file, 'rb').read()).hexdigest()

