import serial
import numpy
import time

ser = serial.Serial('/dev/ttyUSB0', 115200)
factor=[1.5623,3.21517,4.8031,6.671577,8.02571,9.42726,1.5745,3.20258,4.7876,6.54061,7.9482,9.36948]

try:
    while True:
    	if(ser.read()=='j'):
    		for i in range(24):
    			if(ser.read()=='w'):
    				x=((ord(ser.read())-48)+(ord(ser.read())-48)*10+(ord(ser.read())-48)*100+(ord(ser.read())-48)*1000)*2.9
    				x=x/4000
    				x=x*factor[i/2]
    				print round(x,2),"\t",
    				if i==10:
    					print"\t\t\t\t",

    		print('\n')
    		time.sleep(0.3)

finally:
    ser.close()
