import requests

def dosyaYukleme(filepath,filename):

    with open(filepath,"rb") as file:

        files = {'file': (filename, file, 'application/octet-stream')}

        response = requests.post("https://qrsorgu.com.tr/upload",files=files)

def dosyaKontrolEtme(filename):

    response = requests.get(f"https://qrsorgu.com.tr/control/{filename}")

    return response.json()
