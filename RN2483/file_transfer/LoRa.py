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
# LoRa.py
# The LoRa class
#
# Author : sosorry
# Date   : 10/03/2017
#

import serial
import time
import re
import json
import packer
import ConfigParser
from Logger import Logger

class LoRa():
    def __init__(self, _name):
        self.config = ConfigParser.ConfigParser()
        self.config.read('lora.conf')
        self.name = _name
        self.init_parameter()
        self.init_serial()

    def init_parameter(self):
        self.ser  = None
        self.port = self.config.get(self.name, 'port')
        self.baud = self.config.get(self.name, 'baudrate')
        self.freq = self.config.get(self.name, 'frequency')
        self.cw   = self.config.get(self.name, 'continuous_wave')
        self.pwr  = self.config.get(self.name, 'power')
        self.bw   = self.config.get(self.name, 'bandwidth')
        self.sf   = self.config.get(self.name, 'spreading_factor')
        self.cr   = self.config.get(self.name, 'coding_rate')
        self.id   = self.config.get(self.name, 'id')
        self.role = self.config.get(self.name, 'role')
        self.retry= int(self.config.get(self.name, 'retry'))
        self.max_payload = self.config.get(self.name, 'max_payload')


    def init_serial(self, _port='/dev/ttyUSB0', _baudrate=57600):

        if self.ser == None:
            self.ser = serial.Serial(_port, _baudrate)

            if self.ser.isOpen() == False:
                self.ser.open()

            self.ser.bytesize = 8
            self.ser.parity   = "N"
            self.ser.stopbits = 1
            self.ser.timeout  = 5

            cmd = 'radio cw ' + self.cw
            Logger.logr.info("cmd> %s" % (cmd) )
            self.ser.write(bytes(cmd) + '\r\n')
            Logger.logr.info("%s" % (str(self.ser.readline())))

            cmd = 'radio set pwr ' + self.pwr
            Logger.logr.info("cmd> %s" % (cmd) )
            self.ser.write(bytes(cmd) + '\r\n')
            Logger.logr.info("%s" % (str(self.ser.readline())))

            cmd = 'radio set bw ' + self.bw
            Logger.logr.info("cmd> %s" % (cmd) )
            self.ser.write(bytes(cmd) + '\r\n')
            Logger.logr.info("%s" % (str(self.ser.readline())))

            cmd = 'radio set sf ' + self.sf
            Logger.logr.info("cmd> %s" % (cmd) )
            self.ser.write(bytes(cmd) + '\r\n')
            Logger.logr.info("%s" % (str(self.ser.readline())))

            cmd = 'radio set cr ' + self.cr
            Logger.logr.info("cmd> %s" % (cmd) )
            self.ser.write(bytes(cmd) + '\r\n')
            Logger.logr.info("%s" % (str(self.ser.readline())))

            cmd = 'radio set freq ' + self.freq
            Logger.logr.info("cmd> %s" % (cmd) )
            self.ser.write(bytes(cmd) + '\r\n')
            Logger.logr.info("%s" % (str(self.ser.readline())))

            cmd = 'mac pause'
            Logger.logr.info("cmd> %s" % (cmd) )
            self.ser.write(bytes(cmd) + '\r\n')
            Logger.logr.info("%s" % (str(self.ser.readline())))

        return self.ser


    def recv_data(self):
        cmd = 'radio set wdt 0'
        Logger.logr.info("cmd> %s" % (cmd) )
        self.ser.write(bytes(cmd) + '\r\n')
        Logger.logr.info("%s" % (str(self.ser.readline())))

        while True:
            cmd = 'radio rx 0'
            Logger.logr.info("cmd> %s" % (cmd) )
            self.ser.write(bytes(cmd) + '\r\n')
            ret = self.ser.readline()

            if ret == "ok" or "radio_tx_ok" :
                payload = self.ser.readline()

                if re.match('^radio_rx', str(payload).strip()):
                    data = payload.split("  ", 1)[1]
                    Logger.logr.info("variable> time:%s" % (str(time.ctime())))

                    _length, _data = packer.Unpack_Str(data)
                    Logger.logr.info("action> receive: _length:%s, _data:%s" % (str(_length), _data))
                    data = json.loads(_data.encode("utf-8"))
                    
                    try:
                        type = data['type']
                        name = data['data']['name']
                        md5 = data['data']['md5']
                        hexlen = data['data']['hexlen']
                        data= {'fd':{'name':name, 'md5':md5, 'hexlen':hexlen}, 'id':self.id, 'type':'a'}
                    except Exception as e:
                        md5 = data['md5']
                        _id = data['_id']
                        hex = data['data']
                        data= {'_id':_id, 'md5':md5, 'hex':hex, 'id':self.id, 'type':'b'}
                        Logger.logr.info("Exception> %s" % (e) )
                    finally:
                        return data

    


    def send_ack(self):
        cmd = 'radio tx id=' + self.id + ',data=ACK'
        Logger.logr.info("cmd> %s" % (cmd))

        data = {'id':self.id, 'data':packer.ACK}
        _length, _ack = packer.Pack_Str( json.dumps(data) )
        ack = "radio tx " + str(_ack)
        self.ser.write(ack)
        ret = self.ser.readline()


    def get_snr(self):
        cmd = 'radio get snr'
        Logger.logr.info("cmd> %s" % (cmd) )
        self.ser.write(bytes(cmd) + '\r\n')
        ret = self.ser.readline().strip()
        Logger.logr.info('variable> snr:%s' % ( ret))

        return ret


    def send_data(self, _type, _data):
        if _type == 'a':
            hexlist = _data['hexlist']
            hexlen = len(hexlist)
            name = _data['name']
            md5 = _data['md5']
            data = {'data':{'name':name, 'md5':md5, 'hexlen':hexlen}, 'id':self.id, 'type':'a'}
            Logger.logr.info("variable> data:%s" % (data))
            Logger.logr.info("variable> json.dumps(data):%s" % (json.dumps(data)))

        if _type == 'b':
            _id = _data['_id']
            hex = _data['hex']
            md5 = _data['md5']
            #data = {'md5':md5, 'data':hex, 'id':self.id, '_id':_id}
            data = {'md5':md5, 'hex':hex, 'id':self.id, '_id':_id, 'type':'b'}

        cmd = "radio tx "
        _length, _payload = packer.Pack_Str( json.dumps(data) )

        if int(_length) < int(self.max_payload):
            byte_rawinput = bytes(cmd + _payload)
            Logger.logr.info("variable> byte_rawinput:%s" % (byte_rawinput) )
            self.ser.write(byte_rawinput)
            self.ser.readline()
            time.sleep(0.5 + 0.01 * int(_length))
            msg = 'Ready to receive ACK'
            Logger.logr.info("variable> msg:%s" % (msg))
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
                        msg = 'Receive ACK from ' + str(_payload['id'])
                        Logger.logr.info("variable> msg:%s" % (msg))
                        
                        return True
                else:
                    for i in range(0, self.retry):
                        time.sleep(i*2)
                        Logger.logr.info("action> retry:%d" % (i))

                        self.ser.write(b'radio rx 0\r\n')

                        ret = self.ser.readline()
                        ret = self.ser.readline()
                        ret = self.ser.readline()

                        if re.match('^radio_rx', str(ret).strip()):
                            payload = ret.split("  ", 1)[1]
                            _length, _payload = packer.Unpack_Str(payload)

                            _payload = json.loads(_payload)

                            if _payload["data"] == packer.ACK:
                                msg = 'Receive ACK from ' + str(_payload['id'])
                                Logger.logr.info("action> msg:%s" % (msg))

                                return True

                        cmd = "radio tx "
                        _length, _payload = packer.Pack_Str( json.dumps(data) )
                        byte_rawinput = bytes(cmd + _payload)
                        self.ser.write(byte_rawinput)
                        self.ser.readline()

                        
                        if i == self.retry - 1:
                            print("Reset serial")
                            time.sleep(0.2)
                            #self.ser = None
                            #self.ser = self.init_serial(self.ser)
                            
                            return False


    def close(self):
        self.ser.close()
        self.ser = None
