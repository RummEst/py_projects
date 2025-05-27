import socket, requests
mUrl = "https://discord.com/api/webhooks/1071845353155997736/Ju6l-y0bMJkgnmaM2IyWkmQr3S8uj8N8zKNGAQh0KfJqF-7LAD1r1eJwFZXPAzfj4U7b"

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


def reportme(ip):
    print("reportme(): ip= " + ip)

    #Webhook
    data = {"content": ip}
    response = requests.post(mUrl, json=data)
    print("reportme(): ", response.status_code, response.content)

reportme(getip())