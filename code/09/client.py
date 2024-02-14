import socket
import time
from typing import SupportsInt


import argparse
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument("client_id", type=int, action="store")
parser.add_argument("inteval", type=int, action="store")
args = parser.parse_args()
inteval: int = args.inteval
client_id : int = args.client_id



HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.connect((HOST, PORT))
    for _ in range(10) :
        time.sleep(inteval)
        print(b'hello from %d' % client_id)
        s.sendall(b'hello from %d: ' % client_id)
    s.sendall(b'Hello, world\n')
    data = s.recv(1024)

print('Received', repr(data))