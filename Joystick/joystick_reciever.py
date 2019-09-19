import socket
import serial

ser = serial.Serial('/dev/ttyUSB0', 460800)
#ser = serial.Serial('/dev/ttyS0', 460800)

comm_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCP_IP = "127.0.0.1" #add ip address here
TCP_PORT = 1234

while True:
    try:
        comm_sock.connect((TCP_IP, TCP_PORT))
        break
    except socket.error:
        TCP_PORT += 1

try:
    while True:
        recieved = comm_sock.recv(int(1e7))
	ser.write(recieved)
finally:
    comm_sock.close()
