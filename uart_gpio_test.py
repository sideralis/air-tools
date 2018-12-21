'''
Created on 19 déc. 2018

@author: gautier
'''

import serial
import sys
import time

x = 1234;

def rand():
    global x
    x ^= ((x << 13) & 0xffffffff);
    x ^= ((x >> 17) & 0xffffffff);
    x ^= ((x << 5) & 0xffffffff);
    return x & 0xff;
  
def synchro(ser):
    # Synchro
    rx = ser.read(1)
    while rx[0] != 0x55:
        rx = ser.read(1)
    ser.write([0xaa])
      
def test_tx_air(ser):
    print("Waiting for data")    

    for _ in range(1000):        
        # We are now synchro, let's really start the test.
        for ref in range(100):
            # Get data
            rx = ser.read(19)
            # Check data
            c = ref
            for d in rx:
                if d != c:
                    print("Error! got {} and expected {}".format(d,c))
                    print([int(d) for d in rx])
                    sys.exit()
                c = c + 1
            print("test_inc", ref)
    
        for ref in range(100):
            # Get data
            rx = ser.read(19)
            # Check data
            c = ref
            for d in rx:
                if d != 0:
                    print("Error! got {} and expected 0".format(d))
                    print([int(d) for d in rx])
                    sys.exit()
            print("test_0", ref)
    
        for ref in range(100):
            # Get data
            rx = ser.read(19)
            # Check data
            c = ref
            for d in rx:
                if d != 0xff:
                    print("Error! got {} and expected 0xff".format(d))
                    print([int(d) for d in rx])
                    sys.exit()
            print("test_1", ref)
    
        for ref in range(100):
            # Get data
            rx = ser.read(19)
            # Check data
            c = ref
            for d in rx:
                if d != 0xaa:
                    print("Error! got {} and expected 0xaa".format(d))
                    print([int(d) for d in rx])
                    sys.exit()
            print("test_aa", ref)
    
        for ref in range(100):
            # Get data
            rx = ser.read(19)
            # Check data
            c = ref
            for d in rx:
                if d != 0x55:
                    print("Error! got {} and expected 0x55".format(d))
                    print([int(d) for d in rx])
                    sys.exit()
            print("test_55", ref)
    
        for ref in range(100):
            # Get data
            rx = ser.read(19)
            # Check data
            for d in rx:
                c = rand()
                if d != c:
                    print("Error! got {} and expected {}".format(d,c))
                    print([int(d) for d in rx])
                    sys.exit()
            print("test_rnd", ref)
        
def test_rx_air(ser):
    time.sleep(0.5)
    
    data_tx = [0]*10  
    for ref in range(100):
        ser.write(data_tx)
        time.sleep(0.05)
        print("test_0", ref) 
        
    data_tx = [0xff]*10  
    for ref in range(100):
        ser.write(data_tx)
        time.sleep(0.05)
        print("test_1", ref) 

    data_tx = [0xaa]*10  
    for ref in range(100):
        ser.write(data_tx)
        time.sleep(0.05)
        print("test_aa", ref) 

    data_tx = [0x55]*10  
    for ref in range(100):
        ser.write(data_tx)
        time.sleep(0.05)
        print("test_55", ref) 
        
    
def main():
    ser =serial.Serial('/dev/ttyUSB1', 9600)
    
    synchro(ser)
#    test_tx_air(ser)
    test_rx_air(ser)
    
if __name__ == '__main__':    
    main()