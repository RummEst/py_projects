from pywebostv.discovery import *    # Because I'm lazy, don't do this.
from pywebostv.connection import *
from pywebostv.controls import *


store = {'client_key': '7e818a687a15d2aa90a162ac3d1d892c'}



#for newer models:
#    client = WebOSClient("<IP Address of TV>", secure=True)

client = WebOSClient("192.168.1.106")
client.connect()
for status in client.register(store):
    if status == WebOSClient.PROMPTED:
        print("Please accept the connect on the TV!")
    elif status == WebOSClient.REGISTERED:
        print("Registration successful!")

# Keep the 'store' object because it contains now the access token
# and use it next time you want to register on the TV.
print(store)   # {'client_key': 'ACCESS_TOKEN_FROM_TV'}

