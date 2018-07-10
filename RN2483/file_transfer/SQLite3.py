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
# SQLite3.py
# The SQLite3 class, to store transactions of file transfer.(not using prepare statement!)
#
# Author : sosorry
# Date   : 10/03/2017
#

import time
import sqlite3
from Logger import Logger

class SQLite3():
    def __init__(self, db):
        self.name = self.__class__.__name__
        self.conn = sqlite3.connect(db)
        self.init_sqlite3()

    def init_sqlite3(self):
        cmd = 'SELECT name FROM sqlite_master WHERE type="table";'
        cursor = self.conn.cursor()
        cursor.execute(cmd)

        if len(cursor.fetchall()) == 0:
            cmd = 'CREATE TABLE file (_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, md5 TEXT, hexlen TEXT, start TEXT, end TEXT, snr TEXT);'
            Logger.logr.info("sql> %s" % (cmd) )
            cursor.execute(cmd)
            self.conn.commit()

    def add_file(self, fd):
        # add table
        hexlen = fd['hexlen']
        name = fd['name']
        md5 = fd['md5']
        ts = str(time.time())

        cursor = self.conn.cursor()
        values = {'name':name, 'md5':md5, 'hexlen':hexlen, 'start':ts}
        cursor.execute('INSERT INTO file (name, md5, hexlen, start) VALUES (:name, :md5, :hexlen, :start);', values)
        Logger.logr.info("variable> %s" % (str(values)) )
        self.conn.commit()

        cmd = 'DROP TABLE IF EXISTS MD5' + str(md5)
        Logger.logr.info("sql> %s" % (cmd) )
        cursor = self.conn.cursor()
        cursor.execute(cmd)
        self.conn.commit()

        cmd = 'CREATE TABLE IF NOT EXISTS MD5' + str(md5) + ' (_id INTEGER PRIMARY KEY AUTOINCREMENT, hex TEXT, snr TEXT, ts TEXT);'
        Logger.logr.info("sql> %s" % (cmd) )
        cursor = self.conn.cursor()
        cursor.execute(cmd)
        self.conn.commit()


    def create_hex(self, fd):
        hexlist = fd['hexlist']
        hexlen = len(hexlist)
        name = fd['name']
        md5 = fd['md5']

        try:
            cursor = self.conn.cursor()
            chipS = [hexlist[x:x+10] for x in range(0, hexlen, 10)]

            for chip in chipS:
                values = {'hex':','.join(chip), 'ts':str(time.time())}
                cursor.execute('INSERT INTO MD5' + str(md5) + ' (hex, ts) VALUES (:hex, :ts);', values)

            values = {'hex':'', 'ts':str(time.time())}
            cursor.execute('INSERT INTO MD5' + str(md5) + ' (hex, ts) VALUES (:hex, :ts);', values)

            self.conn.commit()

        except Exception as e:
            Logger.logr.error("Exception> %s" % (e) )


    def next_hex(self, _md5):
        cmd = 'SELECT _id as _id, hex as hex, ts as ts FROM MD5' + str(_md5) + ' ORDER BY _id ASC LIMIT 1;'
        Logger.logr.info("sql> %s" % (cmd) )
        cursor = self.conn.cursor()
        cursor.execute(cmd)
        f = cursor.fetchone()
        Logger.logr.info("variable> fetchone:%s" % (str(f)) )
        return f

    def insert_hex(self, _md5, _id, _hex):
        ts = str(time.time())
        values = {'_id':_id, 'hex':_hex, 'ts':ts}
        cursor = self.conn.cursor()

        try:
            cursor.execute('INSERT OR IGNORE INTO MD5' + str(_md5) + ' (_id, hex, ts) VALUES (:_id, :hex, :ts);', values)
            Logger.logr.info("variable> valeues:%s" % (str(values)) )
            self.conn.commit()
            return True
        except Exception as e:
            Logger.logr.info("Exception> %s" % (e) )
            return False


    def delete_hex(self, _id, _md5):
        cursor = self.conn.cursor()
        cmd = "DELETE FROM MD5" + str(_md5) + " WHERE _id = '%s' " % _id
        Logger.logr.info("sql> %s" % (cmd) )
        cursor.execute(cmd)
        self.conn.commit()

        return True


    def get_name(self, _md5):
        cmd = "SELECT _id as _id, name as name FROM file WHERE md5 = '%s' ORDER BY _id DESC LIMIT 1;" % _md5
        Logger.logr.info("sql> %s" % (cmd) )
        cursor = self.conn.cursor()
        cursor.execute(cmd)
        f = cursor.fetchone()
        Logger.logr.info("variable> fatchone:%s" % (str(f)) )

        if f is not None:
            return f[1]
        else:
            return


    def get_hexlist(self, _md5):
        cmd = 'SELECT _id, hex, ts FROM MD5' + str(_md5) + ' ORDER BY _id ASC;'
        Logger.logr.info("sql> %s" % (cmd) )
        cursor = self.conn.cursor()
        cursor.execute(cmd)
        fetchall = cursor.fetchall()

        ### fixme
        hexlist = []
        for row in fetchall:
            hexlist.extend( row[1].split(',') )

        if hexlist is not None:
            return hexlist
        else:
            return


    def update_snr(self, _md5, _id, _snr):
        cursor = self.conn.cursor()
        cmd = "UPDATE MD5" + str(_md5) + " SET snr='%s' WHERE _id = '%s';" % (str(_snr), str(_id))
        Logger.logr.info("sql> %s" % (cmd) )
        cursor.execute(cmd)
        self.conn.commit()

        return True


    def update_average_snr(self, _md5):
        cursor = self.conn.cursor()
        cmd = 'SELECT snr as snr FROM MD5' + str(_md5)
        cursor.execute(cmd)
        fetchall = cursor.fetchall()

        result = sum(int(i[0]) for i in fetchall) 
        length = len(fetchall)
        Logger.logr.info("variable> result:%s, length:%s" % (result, length) )
        average_snr = float(result)/float(length)
        cursor = self.conn.cursor()
        cmd = "UPDATE file SET snr='%s' WHERE md5='%s' ORDER BY _id DESC LIMIT 1;" % (str(average_snr), str(_md5))
        Logger.logr.info("sql> %s" % (cmd) )
        cursor.execute(cmd)
        self.conn.commit()

        return True


    def update_ts(self, _md5):
        ts = time.time()
        cmd = "UPDATE file SET end='%s' WHERE md5='%s' ORDER BY _id DESC LIMIT 1;" % (str(ts), str(_md5))
        Logger.logr.info("sql> %s" % (cmd) )
        cursor = self.conn.cursor()
        cursor.execute(cmd)
        self.conn.commit()

        return True
