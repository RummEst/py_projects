import pygetwindow as gw
import socket
from datetime import datetime

def toggleReoWin():
    reoWin = gw.getWindowsWithTitle('Reolink')[0]
    print("Toggle reoWin")
    if reoWin.isMaximized:
        reoWin.minimize()
    elif not reoWin.isMaximized:
        reoWin.maximize()
    else:
        print("toggleReoWin() -> Error")

# Define the server address and port
SERVER_IP = '192.168.1.139'
SERVER_PORT = 8064

def main():
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Bind the socket to the address and port
        server_socket.bind((SERVER_IP, SERVER_PORT))

        # Listen for incoming connections (max 1 connection at a time)
        server_socket.listen(1)
        print(f'Server listening on {SERVER_IP}:{SERVER_PORT}')

        while True:
            # Wait for a connection
            connection, client_address = server_socket.accept()
            try:
                print(f'Connection from {client_address}')

                # Receive the data in small chunks and print it
                while True:
                    data = connection.recv(1024)
                    if data:
                        print('Received:', data.decode('utf-8'))
                        if data.decode('utf-8') == "reo":
                            toggleReoWin()
                            timestamp = str(datetime.utcnow().strftime('%H:%M:%S.%f')[:-3])
                            connection.send(timestamp.encode())
                    else:
                        # No more data from the client
                        break
            finally:
                # Clean up the connection
                connection.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
