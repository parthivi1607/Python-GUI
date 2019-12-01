import socket
import sys
import cv2
import pickle
import numpy as np
import struct
import zlib

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.connect((socket.gethostname(), 8486))
connection = client_socket.makefile('wb')

data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))

while True:
    while len(data) < payload_size:
        print("Recv: {}".format(len(data)))
        data += client_socket.recv(4096)

    print("Done Recv: {}".format(len(data)))
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print("msg_size: {}".format(msg_size))

    while len(data) < msg_size:
        data += client_socket.recv(4096)

    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame=pickle.loads(frame_data)
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    cv2.imshow('ImageWindow',frame)
    cv2.waitKey(1)
