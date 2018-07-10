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
# Samba.py
# The Samba class
#
# Author : sosorry
# Date   : 10/03/2017
#

from samba import smb
from smb import *
from smb.SMBConnection import *
import ConfigParser
from Logger import Logger

class Samba:
    def __init__(self, _name):
        self.config = ConfigParser.ConfigParser()
        self.config.read('lora.conf')
        self.name = _name
        self.init_parameter()
        self.init_conn()


    def init_parameter(self):
        self.conn         = None
        self.username     = self.config.get(self.name, 'username')
        self.password     = self.config.get(self.name, 'password')
        self.machine_name = self.config.get(self.name, 'machine_name')
        self.server_name  = self.config.get(self.name, 'server_name')
        self.server_ip    = self.config.get(self.name, 'server_ip')
        self.domain_name  = self.config.get(self.name, 'domain_name')
        self.remote_folder= self.config.get(self.name, 'remote_folder')

 
    def init_conn(self):
        self.conn = SMBConnection(self.username, self.password, self.machine_name, self.server_name, 
                                  domain=self.domain_name, use_ntlm_v2=True, is_direct_tcp=True)
        self.conn.connect(self.server_ip, 445)
        shares = self.conn.listShares()


    def send_data(self, _name):
        with open(_name, 'rb') as file:
            self.conn.storeFile(self.remote_folder, _name, file)


    def close(self):
        self.conn.close()
