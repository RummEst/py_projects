
'''
 +-----------------------------+         +---------------------------------------------+         +--------------------------------+
 |     My Laptop (Alice)       |         |            Intermediary Server (Bob)        |         |    Internal Server (Carol)     |
 +-----------------------------+         +----------------------+----------------------+         +--------------------------------+
 | $ ssh -p 1022 carol@1.2.3.4 |<------->|    IF 1: 1.2.3.4     |  IF 2: 192.168.1.1   |<------->|       IF 1: 192.168.1.2        |
 | carol@1.2.3.4's password:   |         +----------------------+----------------------+         +--------------------------------+
 | carol@hostname:~$ whoami    |         | $ python pf.py --listen-host 1.2.3.4 \      |         | 192.168.1.2:22(OpenSSH Server) |
 | carol                       |         |                --listen-port 1022 \         |         +--------------------------------+
 +-----------------------------+         |                --connect-host 192.168.1.2 \ |
                                         |                --connect-port 22            |
                                         +---------------------------------------------+
'''

import socket
import threading
import logging


format = '%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=format)


def handle(buffer, direction, src_address, src_port, dst_address, dst_port):
    '''
    intercept the data flows between local port and the target port
    '''
    if direction:
        logging.debug(f"{src_address, src_port} -> {dst_address, dst_port} {len(buffer)} bytes")
    else:
        logging.debug(f"{src_address, src_port} <- {dst_address, dst_port} {len(buffer)} bytes")
    return buffer


def transfer(src, dst, direction):
    src_address, src_port = src.getsockname()
    dst_address, dst_port = dst.getsockname()
    while True:
        try:
            _buffer = src.recv(4096)
            if len(_buffer) > 0:
                dst.send(handle(_buffer, direction, src_address, src_port, dst_address, dst_port))
        except Exception as e:
            logging.error(repr(e))
            break
    logging.warning(f"Closing connect {src_address, src_port}! ")
    src.close()
    logging.warning(f"Closing connect {dst_address, dst_port}! ")
    dst.close()


def server(local_host, local_port, remote_host, remote_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((local_host, local_port))
    server_socket.listen(0x40)
    logging.info(f"Server started {local_host, local_port}")
    logging.info(f"Connect to {local_host, local_port} to get the content of {remote_host, remote_port}")
    while True:
        src_socket, src_address = server_socket.accept()
        logging.info(f"[Establishing] {src_address} -> {local_host, local_port} -> ? -> {remote_host, remote_port}")
        try:
            dst_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dst_socket.connect((remote_host, remote_port))
            logging.info(f"[OK] {src_address} -> {local_host, local_port} -> {dst_socket.getsockname()} -> {remote_host, remote_port}")
            s = threading.Thread(target=transfer, args=(dst_socket, src_socket, False))
            r = threading.Thread(target=transfer, args=(src_socket, dst_socket, True))
            s.start()
            r.start()
        except KeyboardInterrupt:
            exit()
        except Exception as e:
            logging.error(repr(e))


