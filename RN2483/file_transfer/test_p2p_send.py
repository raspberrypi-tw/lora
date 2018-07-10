import serial
import time

lora = serial.Serial("/dev/ttyUSB0", 57600)

lora.write(b'radio cw off\r\n')
lora.readline()

lora.write(b'radio set bw 125\r\n')
lora.readline()

lora.write(b'radio set sf sf12\r\n')
lora.readline()

lora.write(b'radio set freq 434100000\r\n')
lora.readline()

while True:
    lora.write(b'mac pause\r\n')
    lora.readline()

    t = int(time.time())

    byte_cmd = bytes('radio tx ' + str(t) + '\r\n')
    print "send ", t
    lora.write(byte_cmd)
    lora.readline()
    lora.readline()

