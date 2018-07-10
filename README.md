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
### 1. P2P
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

### 2. Gateway
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
===
```


## Buy LoRa RN2483 Module
[[產品] LoRa LRM001(USB/UART) – Microchip RN2483](https://www.raspberrypi.com.tw/14724/1420/)

## 
[Learn LoRa with Python and Raspberry Pi](https://www.slideshare.net/raspberrypi-tw/learn-lora-with-python-and-raspberry-pi)
