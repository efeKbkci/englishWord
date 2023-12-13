import requests

def dosyaYukleme(filepath,filename):

    with open(filepath,"rb") as file:

        files = {'file': (filename, file, 'application/octet-stream')}

        response = requests.post("http://35.246.208.82/upload",files=files)

def dosyaKontrolEtme(filename):

    response = requests.get(f"http://35.246.208.82/control/{filename}")

    return response.json()
