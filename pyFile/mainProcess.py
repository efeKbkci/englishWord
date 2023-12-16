import subprocess
import os

# TODO: subprocess öğrenilecek

# .exe dosyanızı başlatın

process = subprocess.Popen([r"qrmain.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

stdout, stderr = process.communicate()

if os.path.isfile("qrApp_silme.exe"): # Güncelleme olmuştur

    print("if block")

    os.remove(r"qrmain.exe")

    os.rename("qrApp_silme.exe","qrmain.exe")
