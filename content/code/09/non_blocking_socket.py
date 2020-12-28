import socket, select
from contextlib import contextmanager




@contextmanager
def epoll_context(*args, ** kwargs):
    epoll = select.epoll()
    epoll.register(*args, **kwargs)

    try:
        yield epoll
    finally:
        epoll.unregister(args[0])
        epoll.close()


EOL = b'\n\n'
response = b'Hello world'
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()

    while True:
        conn, address = server.accept()
        with conn:
            req = b''
            while EOL not in req:
                req += conn.recv(1024)
                print('-' * 50 + '\n')
                print(req.decode())
                print('-' * 50 + '\n')
                break

            conn.send(response)

 
