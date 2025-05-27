

import socket
import threading
import logging
from time import sleep

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
    ticks_idle = 0 #  1 tick = 20ms
    while True:
        try:
            for timer in range(500):
                _buffer = src.recv(4096)
                if len(_buffer) == 0:
                    ticks_idle += 1
                    sleep(0.02)
                    if ticks_idle >= 50 * 60:
                        raise Exception("Timeout, dead for 1min")
                else:
                    dst.send(handle(_buffer, direction, src_address, src_port, dst_address, dst_port))
                    ticks_idle = 1
        except Exception as e:
            logging.error(repr(e) + f"src={src_address, src_port},  dst={dst_address, dst_port}")
            break
    logging.warning(f"Closing connect {src_address, src_port}! ")
    src.close()
    logging.warning(f"Closing connect {dst_address, dst_port}! ")
    dst.close()
    return


def server(local_host, local_port, remote_host, remote_port):
    logging.debug(f"\n   server(local_host={local_host}, local_port={local_port},\n   remote_host={remote_host}, remote_port={remote_port})")
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


server(getip(), 8088, "127.0.0.1", 9014)
