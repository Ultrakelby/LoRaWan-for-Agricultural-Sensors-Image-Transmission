# UART protocols
from machine import UART, Pin
import time
import utime
import os
import sys

print("Initialize UART")

counter = 0

# create an input pin on pin #2, This will Signal RTS from the Jetson Pin 11
p2 = Pin(2, Pin.IN)

# create an input pin on pin #7, This will Signal CTS from the Wireless Stick Pin GPIO21
p7 = Pin(7, Pin.IN)

# create an output pin on pin #3, This will Signal CTS to the Jetson
p3 = Pin(3, Pin.OUT)
p3.value(1)

# create an output pin on pin #10, This will Signal RTS to Wireless Stick Pin GPI22
p10 = Pin(10, Pin.OUT)
p10.value(0)

uart0 = UART(0,baudrate=9600,bits=8,parity=None,stop=1,tx=Pin(0),rx=Pin(1))
uart1 = UART(1,baudrate=9600,bits=8,parity=None,stop=1,tx=Pin(8),rx=Pin(9))

time.sleep(1)

rxData = bytes()
data = []# Creats a list

def main():
    p3.value(1) # Sends CTS to the Jetson
    print("Waiting for RTS from Jetson.\nPin2 Value: {0}".format(p2.value()))
    
    while not p2.value() == 1: #Wait for RTS from Jetson
        pass
    
    while True:
            try:
                while p2.value() == 1:#uart0.any() > 0:
                    if uart0.any() > 0:
                        rxData = uart0.read()
                        #data.append(rxData.decode('utf-8')) # Saves Received data into a string of chars
                        data.append(rxData) # Saves Received data into a string of bits
                        print(rxData)
                        #print(rxData.decode('utf-8')) # Optional, displays rxData in strings
                        time.sleep(0.1)
                        p3.value(0)
                        p10.value(0)
                p3.value(0)
                break
            except KeyboardInterrupt:
                #print('\n')
                print(''.join(data)) # Joins bit array into a combined list of arrays
                print('Program Interrupted')   
                p3.value(0)
                p10.value(0)
                print("Pin3 Value: {0}".format(p3.value()))
    #print(b''.join(data))
     
    while True: # Second UART to send to esp32
        global counter
        p10.value(0)
        #print(len(data))
        try:
            for i in range(0, len(data), 1):
                p10.value(1)
                while not p7.value() == 1: #Wait for CTS from Wireless Stick
                        pass
                print("Sending",counter)
                counter = counter+1
                uart1.write(data[i])
                uart1.write('\n')
                p10.value(1)
                time.sleep(0.010)
            break
        except KeyboardInterrupt:
            print('Program Interrupted')
            p10.value(1)
            sys.exit()
        p10.value(0)
        p3.value(0)
        print('Program Ended')
"""
# Below is a test of the UART between the Pico and the Heltec Wireless Stick
counter = 0
data = "ffd8abcd"
while True:
    p10.value(0)
    while not p7.value() == 1: #Wait for CTS from Wireless Stick
        pass
    print("Sending",counter)
    counter = counter+1
    uart1.write(data)
    uart1.write('\n')
    time.sleep(0.5)
"""
if __name__ == '__main__':
    main()