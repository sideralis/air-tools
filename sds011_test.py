'''
Created on 4 déc. 2018

@author: gautier
'''

import serial
import time
from os.path import sys

def checksum(d):
    csum = sum(d[2:-2])
    csum = csum & 0xff
    d[-2] = csum
    
def write(action):
    checksum(action)
    print(action)
    ser.write(action)
    
def read():   
    state = 0
    while True:
        while True:
            v = ser.read(1)
            if state == 0 and v[0] == 0xaa:
                state = 1
            elif state == 1 and v[0] == 0xc5:
                state = 2
                break
            elif state == 1 and v[0] == 0xc0:
                state = 3
                break
            else:
                state = 0
        v = ser.read(8)
        break
    return state, v      
    
def analyze(state, v):
    if state == 3:
        print(time.localtime())
        print("~~~ pm2.5 = ",v[0] + (v[1]<<8), "~~~~")
        print("~~~ pm10 = ",v[2] + (v[3]<<8), "~~~~")
        print("id = ",hex(v[4]),hex(v[5]))
        return -1
    else:
        print("answer =", [hex(e) for e in v])
        return v[0]

ser =serial.Serial('/dev/ttyUSB0', 9600)

setDataReportingMode = [0xaa, 0xb4, 0x2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0xff, 0xff, 0x00, 0xab]
queryDataCommand = [0xaa, 0xb4, 0x4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0xff, 0xff, 0x00, 0xab]
setSleep = [0xaa, 0xb4, 0x6, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0xff, 0xff, 0x00, 0xab]
setWork = [0xaa, 0xb4, 0x6, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0xff, 0xff, 0x00, 0xab]
checkFW = [0xaa, 0xb4, 0x7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0xff, 0xff, 0x00, 0xab]
#checkFW = [0xaa, 0xb4, 0x7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0xa1, 0x60, 0x00, 0xab]
setWorkingPeriod = [0xaa,0xb4,8,1,0x00,0,0,0,0,0,0,0,0,0,0,0xff,0xff,0x00,0xab]

print("== set work")
write(setWork)         
s,v = read()
ans = analyze(s,v)
if ans != 6:
    print("erreur")
    
print("== Continous measurement")
write(setWorkingPeriod)             # continuous
s,v = read()
ans = analyze(s,v)
if ans != 8:
    print("erreur")

print("== set query data reporting")
write(setDataReportingMode)         # on query
s,v = read()
ans = analyze(s,v)
if ans != 2:
    print("erreur")
 
print("== set sleep")
write(setSleep)         
s,v = read()
ans = analyze(s,v)
if ans != 6:
    print("erreur")
   
while True:
    print("== waiting 4mn30s")
    time.sleep(4*60+30)
    print("== set work")
    write(setWork)         # 
    s,v = read()
    ans = analyze(s,v)
    if ans != 6:
        print("erreur")
    
    print("== waiting 30s")
    time.sleep(30)
    
    print("== query a result")
    write(queryDataCommand)         # 
    s,v = read()
    ans = analyze(s,v)
    if ans != -1:
        print("erreur")

    print("== set sleep")
    write(setSleep)         
    s,v = read()
    ans = analyze(s,v)
    if ans != 6:
        print("erreur")
    
   
    
