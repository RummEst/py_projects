from pywebostv.discovery import *    # Because I'm lazy, don't do this.
from pywebostv.connection import *
from pywebostv.controls import *


def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")



# for newer models:
#    client = WebOSClient("<IP Address of TV>", secure=True)
class LG:
    def __init__(self, store, ip="192.168.1.106"):
        self.ip = ip
        self.store = store
        print("Connecting...")
        self.client = self.connect()
        self.MediaControl = MediaControl(self.client)
        self.SystemControl = SystemControl(self.client)
        self.InputControl = InputControl(self.client)
        self.TvControl = TvControl(self.client)
        print(f"\nsysINFO:\n{self.SystemControl.info()}\n")

    def connect(self):
        client = WebOSClient(self.ip)
        client.connect()
        for status in client.register(self.store):
            if status == WebOSClient.REGISTERED:
                print("Connection success")
                return client
            else:
                print("!!! Connection Error !!!")
                return None

    def help(self):
        read_file('lgTest-DOCS.txt')


def main():
    store = {'client_key': '7e818a687a15d2aa90a162ac3d1d892c'}
    tv = LG(store)
    print(tv)
    media, system, inp, channel = tv.MediaControl, tv.SystemControl, tv.InputControl, tv.TvControl
    print("\n Running in Client Mode (__main__), for documentation run \'tv.help()\'\n METHODS: media, system, inp, channel ")
    print("<end>")

if __name__ == "__main__":
    main()

