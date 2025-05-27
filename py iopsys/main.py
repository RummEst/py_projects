

import json
import sys
import subprocess
import socket
import os
from websocket import create_connection

class JUCI_API:
    def __init__(self, credentials):
        self.host, self.username, self.password = credentials
        print("Authenticating...")
        self.key = self.ubusAuth()
        if not self.key:
            print("Auth failed!")
            sys.exit(1)
        print("Got key: %s" % self.key)


    def ubusAuth(self):
        ws = create_connection("ws://" + self.host, header=["Sec-WebSocket-Protocol: ubus-json"])
        req = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "call",
                "params": [
                    "00000000000000000000000000000000",
                    "session",
                    "login",
                    {"username": self.username, "password": self.password},
                ],
                "id": 666,
            }
        )
        ws.send(req)
        response = json.loads(ws.recv())
        ws.close()
        try:
            key = response.get("result")[1].get("ubus_rpc_session")
        except IndexError:
            return None
        return key


    def ubusCall(self, namespace, argument, params={}):
        ws = create_connection("ws://" + self.host, header=["Sec-WebSocket-Protocol: ubus-json"])
        req = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "call",
                "params": [self.key, namespace, argument, params],
                "id": 666,
            }
        )
        ws.send(req)
        response = json.loads(ws.recv())
        ws.close()
        print(response)
        try:
            result = response.get("result")[1]
        except IndexError:
            if response.get("result")[0] == 0:
                return True  #  ?????
            return None
        return result

    def _getClients(self):
        return self.ubusCall("router.network", "clients")

    def _getWirelessRAW(self):
        return self.ubusCall("router.wireless", "stas")

    def _refreshMACdict(self):
        self.macDict = {}
        clients = self._getClients()
        for cl in clients:
            cl_data = clients[cl]
            self.macDict[cl_data["macaddr"]] = cl_data["hostname"]

    def _getWirelessClients(self):
        self._refreshMACdict()
        wClients = {}
        wCl_data = list(self._getWirelessRAW().values())
        for d in wCl_data:
            wClients[(self.macDict[d['macaddr']])[:11]] = d['rssi']
        return {key: value for key, value in sorted(wClients.items())}



if __name__ == "__main__":
    creds = ["192.168.1.1", "user", "DC5DV7WVLD"]
    juci = JUCI_API(creds)
    print(juci.key)




