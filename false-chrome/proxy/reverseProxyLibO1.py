
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
# !/usr/bin/env python3
# Tcp Port Forwarding (Reverse Proxy)
# Author: Optimized by ChatGPT

import socket
import threading
import logging
from concurrent.futures import ThreadPoolExecutor

# Logging configuration
format = '%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=format)

# Thread pool executor for managing threads efficiently
thread_pool = ThreadPoolExecutor(max_workers=20)

def getip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
        print(f"getip() -> {IP}")
    except Exception:
        print("getip() failed, using 127.0.0.1")
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def handle(buffer, direction, src_address, src_port, dst_address, dst_port):
    '''
    Intercept the data flows between local port and the target port
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
            else:
                break
        except Exception as e:
            logging.error(repr(e))
            break
    logging.warning(f"Closing connection {src_address, src_port}!")
    src.close()
    logging.warning(f"Closing connection {dst_address, dst_port}!")
    dst.close()


def server(local_host, local_port, remote_host, remote_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((local_host, local_port))
        server_socket.listen(0x40)
        logging.info(f"Server started {local_host, local_port}")
        logging.info(f"Connect to {local_host, local_port} to get the content of {remote_host, remote_port}")

        while True:
            try:
                src_socket, src_address = server_socket.accept()
                logging.info(
                    f"[Establishing] {src_address} -> {local_host, local_port} -> ? -> {remote_host, remote_port}")

                dst_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                dst_socket.connect((remote_host, remote_port))
                logging.info(
                    f"[OK] {src_address} -> {local_host, local_port} -> {dst_socket.getsockname()} -> {remote_host, remote_port}")

                # Using thread pool to manage connections
                thread_pool.submit(transfer, dst_socket, src_socket, False)
                thread_pool.submit(transfer, src_socket, dst_socket, True)
            except KeyboardInterrupt:
                exit()
            except Exception as e:
                logging.error(repr(e))


