'''
Created on 4 déc. 2018

@author: gautier
'''

import serial

def checksum(d):
    csum = sum(d[2:-2])
    csum = csum & 0xff
    d[-2] = csum
    
ser =serial.Serial('/dev/ttyUSB0', 9600)
checkFW = [0xaa, 0xb4, 0x7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0xff, 0xff, 0x00, 0xab]
#checkFW = [0xaa, 0xb4, 0x7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0xa1, 0x60, 0x00, 0xab]
setWorkingPeriod = [0xaa,0xb4,8,0x00,0x00,0,0,0,0,0,0,0,0,0,0,0xff,0xff,0x00,0xab]

checksum(setWorkingPeriod)
print(setWorkingPeriod)

ser.write(setWorkingPeriod)
state = 0
while True:
    while True:
        v = ser.read(1)
        print("received = ",hex(v[0]))
        if state == 0 and v[0] == 0xaa:
            print("state 1")
            state = 1
        elif state == 1 and v[0] == 0xc5:
            print("state 2")
            state = 2
            break
        else:
            print("state 0")
            state = 0
    v = ser.read(8)
    for e in v:
        print("answer =", hex(e))   
    break 