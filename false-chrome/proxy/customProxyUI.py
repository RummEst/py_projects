import tkinter as tk
import socket
from tkinter import messagebox
from time import sleep

import threading
import logging
from concurrent.futures import ThreadPoolExecutor


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

class rProxy:
    def __init__(self):
        self.local_host, self.local_port, self.remote_host, self.remote_port = get_args_gui()

        # Logging configuration
        format = '[%(levelname)s] thread-%(thread)d @ %(relativeCreated)dms -> %(message)s'
        logging.basicConfig(level=logging.DEBUG, format=format)
        logging.info(f"\n   server(local_host={self.local_host}, local_port={self.local_port},\n   remote_host={self.remote_host}, remote_port={self.remote_port})")
        # Thread pool executor for managing threads efficiently
        self.thread_pool = ThreadPoolExecutor(max_workers=20)

    def handle(self, buffer, direction, src_address, src_port, dst_address, dst_port):
        '''
        Intercept the data flows between local port and the target port
        '''
        if direction:
            logging.debug(f"{src_address, src_port} -> {dst_address, dst_port} {len(buffer)} bytes")
        else:
            logging.debug(f"{src_address, src_port} <- {dst_address, dst_port} {len(buffer)} bytes")
        return buffer

    def transfer(self, src, dst, direction):
        src_address, src_port = src.getsockname()
        dst_address, dst_port = dst.getsockname()

        ticks_idle = 0  # 1 tick = 20ms
        while ticks_idle < 50 * 5:
            try:
                _buffer = src.recv(4096)
                if len(_buffer) > 0:
                    dst.send(self.handle(_buffer, direction, src_address, src_port, dst_address, dst_port))
                else:
                    sleep(0.02)
                    ticks_idle += 1
            except Exception as e:
                logging.error(repr(e))
                logging.warning(f"Terminating {src_address, src_port} -> {dst_address, dst_port}!")
                src.close()
                dst.close()
                break
        logging.warning(f"Closing {src_address, src_port} -> {dst_address, dst_port}!")
        src.close()
        dst.close()

    def server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.local_host, self.local_port))
            server_socket.listen(0x40)
            logging.info(f"Server started {self.local_host, self.local_port}")
            logging.info(f"Connect to {self.local_host, self.local_port} to get the content of {self.remote_host, self.remote_port}")

            while True:
                try:
                    src_socket, src_address = server_socket.accept()
                    logging.info(
                        f"[Establishing] {src_address} -> {self.local_host, self.local_port} -> ? -> {self.remote_host, self.remote_port}")

                    dst_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    dst_socket.connect((self.remote_host, self.remote_port))
                    logging.info(
                        f"[OK] {src_address} -> {self.local_host, self.local_port} -> {dst_socket.getsockname()} -> {self.remote_host, self.remote_port}")

                    # Using thread pool to manage connections
                    s = self.thread_pool.submit(self.transfer, dst_socket, src_socket, False)
                    r = self.thread_pool.submit(self.transfer, src_socket, dst_socket, True)
                    sleep(0.001)
                except KeyboardInterrupt:
                    exit()
                except Exception as e:
                    logging.error(repr(e))


def get_args_gui():

    def validate_ip_or_domain(host):
        # Function to validate if the input is a valid IPv4 address or domain name
        try:
            socket.inet_aton(host)
            return True  # Valid IPv4 address
        except socket.error:
            try:
                socket.gethostbyname(host)
                return True  # Valid domain
            except socket.error:
                return False  # Invalid IP or domain

    def on_ok():
        # Function to execute when OK button is pressed
        if not validate_ip_or_domain(remote_host_entry.get()):
            messagebox.showerror("Error", "Invalid Remote Host")
            return
        if not validate_ip_or_domain(local_host_entry.get()):
            messagebox.showerror("Error", "Invalid Local Host")
            return
        results.append(local_host_entry.get())
        results.append(int(local_port_entry.get()))
        results.append(remote_host_entry.get())
        results.append(int(remote_port_entry.get()))
        window.quit()

    # Main window
    window = tk.Tk()
    window.title("Input Window")
    results = []

    # Local Host
    tk.Label(window, text="Local Host:").grid(row=0)
    local_host_entry = tk.Entry(window)
    local_host_entry.insert(0, getip())
    local_host_entry.grid(row=0, column=1)

    # Local Port
    tk.Label(window, text="Local Port:").grid(row=1)
    local_port_entry = tk.Entry(window)
    local_port_entry.insert(0, "8088")
    local_port_entry.grid(row=1, column=1)

    # Remote Host
    tk.Label(window, text="Remote Host:").grid(row=2)
    remote_host_entry = tk.Entry(window)
    remote_host_entry.insert(0, "127.0.0.1")
    remote_host_entry.grid(row=2, column=1)

    # Remote Port
    tk.Label(window, text="Remote Port:").grid(row=3)
    remote_port_entry = tk.Entry(window)
    remote_port_entry.insert(0, "9014")
    remote_port_entry.grid(row=3, column=1)

    # OK Button
    ok_button = tk.Button(window, text="OK", command=on_ok)
    ok_button.grid(row=4, columnspan=2)

    window.mainloop()
    window.destroy()
    return results

if __name__ == "__main__":
    proxy = rProxy()
    proxy.server()