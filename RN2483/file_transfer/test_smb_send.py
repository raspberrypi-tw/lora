#!/usr/bin/python
# -*- coding: UTF-8 -*-

from Socket import Socket
from Samba import Samba

smb = Samba('SMB')
socket = Socket(smb)
fd = socket.open("lena8rgb.jpg")
socket.send_data(fd)
socket.close()
