import requests

def dosyaYukleme(filepath,filename):

    with open(filepath,"rb") as file:

        files = {'file': (filename, file, 'application/octet-stream')}

        try:
            requests.post("https://qrsorgu.com.tr/upload",files=files)
        except:
            return "Hata"
        
def dosyaKontrolEtme(filename):

    try:
        response = requests.get(f"https://qrsorgu.com.tr/control/{filename}")
    except:
        return "Hata"

    return response.json()
