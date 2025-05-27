
import socket
import reverseProxyLibO1 as rProxy
from reverseProxyLibO1 import getip



rProxy.server(getip(), 8088, "127.0.0.1", 9014)
