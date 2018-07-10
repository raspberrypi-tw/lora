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
# Socket.py
# The Socket class, to make Samba and LoRa be abstracted
#
# Author : sosorry
# Date   : 10/03/2017
#

from Logger import Logger
from DeSer import DeSer
from SQLite3 import SQLite3

class Socket:
    def __init__(self, arg):
        self.db = SQLite3('lora.db')
        self.ds = DeSer()
        self.arg = arg


    def open(self, _src_file):
        #try:
        fd = self.ds.open(_src_file)
        self.db.add_file(fd)
        self.db.create_hex(fd)

        return fd


    def send_syn(self, fd):
        ack = self.arg.send_data(_type='a', _data=fd)

        return ack


    def send_ack(self):
        return self.arg.send_ack()


    def recv(self):
        data = self.arg.recv_data()

        # type 'a'
        if data['type'] == 'a':
            self.db.add_file(data['fd'])
            self.send_ack()

            return str(data)

        # type 'b'
        elif data['type'] == 'b':
            if  len(data['hex']) != 0:
                ack = self.db.insert_hex(_md5=data['md5'], _id=data['_id'], _hex=data['hex'])
                snr = self.arg.get_snr()
                self.db.update_snr(_md5=data['md5'], _id=data['_id'], _snr=snr)

                if ack == True:
                    self.send_ack()

                return str(data)

            # data(hex) is empty
            # do hex to file
            else:
                md5 = data['md5']
                dst_file = self.db.get_name(md5)
                hexlist = self.db.get_hexlist(md5)
                Logger.logr.info("variable> dst_file:%s" % (dst_file) )
                Logger.logr.info("variable> hexlist:%s" % (str(hexlist)) )
                self.ds.hex_to_file(dst_file=dst_file, hexlist=hexlist)
                self.db.update_average_snr(md5)
                self.db.update_ts(md5)

                return data['hex']


    def send_data(self, fd):
        md5 = fd['md5']
        try:
            (_id, hex, ts) = self.db.next_hex(md5)

            if hex is not None:
                ack = self.arg.send_data(_type='b', _data={'_id':_id, 'md5':md5, 'hex':hex})
            else:
                ack = self.arg.send_data(_type='b', _data={})

            if ack == True:
                self.db.delete_hex(_id=_id, _md5=md5)
                return True
            else:
                return False
        except Exception as e:
            # SMB
            name = fd['name']
            ack = self.arg.send_data(name)
            self.db.update_ts(md5)
            Logger.logr.info("Exception> %s" % (e) )

            return False


    def resend_all(self):
        md5S = self.db.not_empty()

        for md5 in md5S:
            fd = {'md5':md5}
            ack = socket.send_data(fd)

            while ack == True:
                ack = self.send_data(fd)

    def next(self, fd):
        pass

    def close(self):
        cmd = 'socket.close()'
        Logger.logr.info("function> %s" % (cmd))
        self.arg.close()


