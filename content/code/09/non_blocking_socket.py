import socket, select
from contextlib import contextmanager
from typing import Dict



@contextmanager
def epoll_context(*args, ** kwargs):
    epoll = select.epoll()
    epoll.register(*args, **kwargs)
    try:
        yield epoll
    finally:
        epoll.unregister(args[0])
        epoll.close()


EOL = b'\n'
QUIT = b'quit\n'
EMPTY = b''
response = b'Hello world'
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server


def init_connection(server: socket.socket, connections: Dict[int, socket.socket], requests : Dict[int, bytes], responses : Dict[int, bytes], epoll: select.epoll):

    conn: socket.socket
    conn, addr = server.accept()
    conn.setblocking(False)
    print(f"New Connection: {addr}")

    fd = conn.fileno()

    epoll.register(fd, select.EPOLLIN)
    connections[fd] = conn
    requests[fd] = b''
    responses[fd] = b''

def receive_request(fileno: int,  connections: Dict[int, socket.socket], requests : Dict[int, bytes], responses : Dict[int, bytes], epoll: select.epoll):

    requests[fileno] += connections[fileno].recv(1024)

    print(f"new updated {fileno} {requests[fileno]}")

    if requests[fileno] == QUIT or requests[fileno] == EMPTY:
        print('[{:02d}] exit or hung up'.format(fileno))
        epoll.unregister(fileno)
        connections[fileno].close()
        del connections[fileno], requests[fileno], responses[fileno]

    elif EOL in requests[fileno]:
        epoll.modify(fileno, select.EPOLLOUT)
        msg = requests[fileno][:-1]
        print("[{:02d}] says: {}".format(fileno, msg))
        responses[fileno] = b'ACK\n'
        requests[fileno] = b''

def send_response(fileno: int,  connections: Dict[int, socket.socket],  responses : Dict[int, bytes], epoll: select.epoll):
    """Send a response to a client."""
    byteswritten = connections[fileno].send(responses[fileno])
    responses[fileno] = responses[fileno][byteswritten:]
    epoll.modify(fileno, select.EPOLLIN)



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server, epoll_context(server.fileno(), select.EPOLLIN) as epoll:
    server.bind((HOST, PORT))
    server.setblocking(False)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    server.listen(5)

    print("Listening")
    connections : Dict[int, socket.socket] = {}


    requests : Dict[int, bytes]= {}
    responses: Dict[int, bytes] = {}
    server_fd = server.fileno()

    while True:
        events = epoll.poll(0)
        print("waiting..")
        for fileno, event in events:
            if fileno == server_fd:
                init_connection(server, connections, requests, responses, epoll)
            elif event & select.EPOLLIN:
                receive_request(fileno, connections, requests, responses, epoll)
            elif event & select.EPOLLOUT:
                send_response(fileno, connections, responses, epoll)

 
