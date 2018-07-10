# LoRa RN2483

## Intro
In this repo, we will show how to use RN2483.
1. P2P
2. Gateway
3. File Transfer

## Environment
Two sets of Raspberry Pi [3B](https://www.raspberrypi.com.tw/10684/55/)/[3B+](https://www.raspberrypi.com.tw/19429/57/) + SanDisk 32G microSD + [RN2483](https://www.raspberrypi.com.tw/14724/1420/) + 2018-06-27-raspbian-stretch.img 

## Prerequisite
### Install required package and Python module
```shell
$ sudo apt-get update
$ sudo apt-get install -y samba samba-common smbclient samba-common-bin smbclient cifs-utils python-dev python-pip libpcap-dev libnet1-dev vim sqlite3
$ sudo pip install flask requests pysmb
```

## Usage
### 1. P2P (host1 & host2)
```
host1$ cd ~/lora/RN2483/p2p
host1$ python p2p_send.py
===
cmd> radio set bw 125
ok

cmd> radio set pwr 15
ok

cmd> radio set sf sf12
ok

cmd> radio set freq 433000000
ok

----------------------------------
cmd> radio tx 1531203143
----------------------------------
cmd> radio tx 1531203145
----------------------------------
cmd> radio tx 1531203148
----------------------------------
cmd> radio tx 1531203150
===


host2$ cd ~/lora/RN2483/p2p
host2$ python p2p_recv.py
===
python p2p_recv.py 
cmd> radio cw off
RN2903 0.9.8 Feb 14 2017 20:17:03

cmd> radio set pwr 15
ok

cmd> radio set bw 125
ok

cmd> radio set sf 12
ok

cmd> radio set freq 433000000
ok

4294967245

----------------------------------
radio_rx  1531203143
----------------------------------
radio_rx  1531203148
----------------------------------
radio_rx  1531203150
===
```

### 2. Gateway (host1 & host2)
```
host1$ cd ~/lora/RN2483/gateway
host1$ python gateway.py
===
cmd> radio cw off
RN2903 0.9.8 Feb 14 2017 20:17:03

cmd> radio set pwr 14
ok

cmd> radio set bw 125
ok

cmd> radio set sf sf12
ok

cmd> radio set cr 4/5
ok

cmd> radio set freq 433000000
invalid_param

cmd> mac pause
4294967245

cmd> radio set wdt 0
ok

----------------------------------
Time: Tue Jul 10 06:27:56 2018
Receive: {"data": "hello world", "id": "DV01"}
Length: 37
SNR: -11

radio tx id=GW01,data=ACK
RAW: 013035367b2264617461223a20223036222c20226964223a202247573031227d
===


host2$ cd ~/lora/RN2483/gateway
host2$ python sender_ack.py 
===
----------------------------------
cmd> radio cw off
RN2903 0.9.8 Feb 14 2017 20:17:03

cmd> radio set pwr 14
ok

cmd> radio set bw 125
ok

cmd> radio set sf sf12
ok

cmd> radio set cr 4/5
ok

cmd> radio set freq 433000000
invalid_param

cmd> mac pause
4294967245

----------------------------------
>>> hello world
RAW: 013037347b2264617461223a202268656c6c6f20776f726c64222c20226964223a202244563031227d

Time: Tue Jul 10 06:27:54 2018
Ready to receive ACK
Receive ACK from GW01
===
```

### 3. File Transfer (host1 & host2)
```
host1$ cd ~/lora/RN2483/file_transfer
host1$ python test_lora_recv.py
===
INFO:root: cmd> radio cw off (2018-07-10 06:48:40; LoRa.py:64)
INFO:root: RN2903 0.9.8 Feb 14 2017 20:17:03
 (2018-07-10 06:48:40; LoRa.py:66)
INFO:root: cmd> radio set pwr 12 (2018-07-10 06:48:40; LoRa.py:69)
INFO:root: ok
 (2018-07-10 06:48:40; LoRa.py:71)
INFO:root: cmd> radio set bw 125 (2018-07-10 06:48:40; LoRa.py:74)
INFO:root: ok
 (2018-07-10 06:48:40; LoRa.py:76)
INFO:root: cmd> radio set sf sf12 (2018-07-10 06:48:40; LoRa.py:79)
INFO:root: ok
 (2018-07-10 06:48:40; LoRa.py:81)
INFO:root: cmd> radio set cr 4/5 (2018-07-10 06:48:40; LoRa.py:84)
INFO:root: ok
 (2018-07-10 06:48:40; LoRa.py:86)
INFO:root: cmd> radio set freq 433000000 (2018-07-10 06:48:40; LoRa.py:89)
INFO:root: ok
 (2018-07-10 06:48:40; LoRa.py:91)
INFO:root: cmd> mac pause (2018-07-10 06:48:40; LoRa.py:94)
INFO:root: 4294967245
 (2018-07-10 06:48:40; LoRa.py:96)
INFO:root: cmd> radio set wdt 0 (2018-07-10 06:48:40; LoRa.py:103)
INFO:root: ok
 (2018-07-10 06:48:40; LoRa.py:105)
INFO:root: cmd> radio rx 0 (2018-07-10 06:48:40; LoRa.py:109)
INFO:root: cmd> radio rx 0 (2018-07-10 06:48:45; LoRa.py:109)
INFO:root: variable> time:Tue Jul 10 06:48:48 2018 (2018-07-10 06:48:48; LoRa.py:118)
INFO:root: action> receive: _length:120, _data:{"type": "a", "data": {"hexlen": 343, "name": "lena8rgb.jpg", "md5": "e3a8b6ca70a414853a4a32ee3a7bac19"}, "id": "G0003"} (2018-07-10 06:48:48; LoRa.py:121)
INFO:root: variable> {'start': '1531205328.21', 'hexlen': 343, 'name': u'lena8rgb.jpg', 'md5': u'e3a8b6ca70a414853a4a32ee3a7bac19'} (2018-07-10 06:48:48; SQLite3.py:49)
INFO:root: sql> DROP TABLE IF EXISTS MD5e3a8b6ca70a414853a4a32ee3a7bac19 (2018-07-10 06:48:48; SQLite3.py:53)
INFO:root: sql> CREATE TABLE IF NOT EXISTS MD5e3a8b6ca70a414853a4a32ee3a7bac19 (_id INTEGER PRIMARY KEY AUTOINCREMENT, hex TEXT, snr TEXT, ts TEXT); (2018-07-10 06:48:48; SQLite3.py:59)
INFO:root: cmd> radio tx id=G0003,data=ACK (2018-07-10 06:48:48; LoRa.py:144)
RAW: 013035387b2264617461223a20223036222c20226964223a20224730303033227d

INFO:root: cmd> radio set wdt 0 (2018-07-10 06:48:48; LoRa.py:103)
INFO:root: ok
 (2018-07-10 06:48:48; LoRa.py:105)
INFO:root: cmd> radio rx 0 (2018-07-10 06:48:48; LoRa.py:109)
INFO:root: cmd> radio rx 0 (2018-07-10 06:48:50; LoRa.py:109)
INFO:root: variable> time:Tue Jul 10 06:48:55 2018 (2018-07-10 06:48:55; LoRa.py:118)
INFO:root: action> receive: _length:121, _data:{"type": "b", "_id": 1, "hex": "ff,d8,ff,e0,00,10,4a,46,49,46", "id": "G0003", "md5": "e3a8b6ca70a414853a4a32ee3a7bac19"} (2018-07-10 06:48:55; LoRa.py:121)
INFO:root: variable> valeues:{'_id': 1, 'hex': u'ff,d8,ff,e0,00,10,4a,46,49,46', 'ts': '1531205335.12'} (2018-07-10 06:48:55; SQLite3.py:104)
INFO:root: cmd> radio get snr (2018-07-10 06:48:55; LoRa.py:155)
INFO:root: variable> snr:8 (2018-07-10 06:48:55; LoRa.py:158)
INFO:root: sql> UPDATE MD5e3a8b6ca70a414853a4a32ee3a7bac19 SET snr='8' WHERE _id = '1'; (2018-07-10 06:48:55; SQLite3.py:157)
INFO:root: cmd> radio tx id=G0003,data=ACK (2018-07-10 06:48:55; LoRa.py:144)
RAW: 013035387b2264617461223a20223036222c20226964223a20224730303033227d
...
===


host2$ cd ~/lora/RN2483/file_transfer
host2$ python test_lora_send.py
===
INFO:root: cmd> radio cw off (2018-07-10 06:48:40; LoRa.py:64)
INFO:root: RN2903 0.9.8 Feb 14 2017 20:17:03
 (2018-07-10 06:48:40; LoRa.py:66)
INFO:root: cmd> radio set pwr 12 (2018-07-10 06:48:40; LoRa.py:69)
INFO:root: ok
 (2018-07-10 06:48:40; LoRa.py:71)
INFO:root: cmd> radio set bw 125 (2018-07-10 06:48:40; LoRa.py:74)
INFO:root: ok
 (2018-07-10 06:48:40; LoRa.py:76)
INFO:root: cmd> radio set sf sf12 (2018-07-10 06:48:40; LoRa.py:79)
INFO:root: ok
 (2018-07-10 06:48:40; LoRa.py:81)
INFO:root: cmd> radio set cr 4/5 (2018-07-10 06:48:40; LoRa.py:84)
INFO:root: ok
 (2018-07-10 06:48:40; LoRa.py:86)
INFO:root: cmd> radio set freq 433000000 (2018-07-10 06:48:40; LoRa.py:89)
INFO:root: ok
 (2018-07-10 06:48:40; LoRa.py:91)
INFO:root: cmd> mac pause (2018-07-10 06:48:40; LoRa.py:94)
INFO:root: 4294967245
 (2018-07-10 06:48:40; LoRa.py:96)
INFO:root: cmd> radio set wdt 0 (2018-07-10 06:48:40; LoRa.py:103)
INFO:root: ok
 (2018-07-10 06:48:40; LoRa.py:105)
INFO:root: cmd> radio rx 0 (2018-07-10 06:48:40; LoRa.py:109)
INFO:root: cmd> radio rx 0 (2018-07-10 06:48:45; LoRa.py:109)
INFO:root: variable> time:Tue Jul 10 06:48:48 2018 (2018-07-10 06:48:48; LoRa.py:118)
INFO:root: action> receive: _length:120, _data:{"type": "a", "data": {"hexlen": 343, "name": "lena8rgb.jpg", "md5": "e3a8b6ca70a414853a4a32ee3a7bac19"}, "id": "G0003"} (2018-07-10 06:48:48; LoRa.py:121)
INFO:root: variable> {'start': '1531205328.21', 'hexlen': 343, 'name': u'lena8rgb.jpg', 'md5': u'e3a8b6ca70a414853a4a32ee3a7bac19'} (2018-07-10 06:48:48; SQLite3.py:49)
INFO:root: sql> DROP TABLE IF EXISTS MD5e3a8b6ca70a414853a4a32ee3a7bac19 (2018-07-10 06:48:48; SQLite3.py:53)
INFO:root: sql> CREATE TABLE IF NOT EXISTS MD5e3a8b6ca70a414853a4a32ee3a7bac19 (_id INTEGER PRIMARY KEY AUTOINCREMENT, hex TEXT, snr TEXT, ts TEXT); (2018-07-10 06:48:48; SQLite3.py:59)
INFO:root: cmd> radio tx id=G0003,data=ACK (2018-07-10 06:48:48; LoRa.py:144)
RAW: 013035387b2264617461223a20223036222c20226964223a20224730303033227d
...
===
```

## Buy LoRa RN2483 Module
[[產品] LoRa LRM001(USB/UART) – Microchip RN2483](https://www.raspberrypi.com.tw/14724/1420/)

## Reference
[Learn LoRa with Python and Raspberry Pi](https://www.slideshare.net/raspberrypi-tw/learn-lora-with-python-and-raspberry-pi)
