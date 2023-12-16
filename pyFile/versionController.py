from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QCloseEvent
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

from PyQt5.QtWidgets import QWidget
import requests
from PyQt5.QtWidgets import *
from PyQt5 import uic 

# preload_content parametresi istenen dosyanın bir anda tamamının belleğe alınmayacağını, parça parça okunup işleneceğini ifade eder. Bu parametre varsayılan olarak True'dur. Yani dosyanın tamamı bir anda belleğe alınır. 
# Büyük dosyalarla çalışırken bu parametrenin false olarak ayarlanması, dosyanın parça parça indirilerek hem yazılımın kitlenmesini engeller, hemde başka işlemler yapmamıza olanak sağlar.

# TODO: QThread not alınacak

def createUI(instance=QWidget):

    uic.loadUi(r"uiFile\updateMsg.ui",instance)

    instance.closeBtn.clicked.connect(lambda: instance.close())

    instance.cancelBtn.clicked.connect(instance.cancelUpdate)

    instance.downloadBtn.clicked.connect(instance.startDownload)

    instance.downloadBtn.hide()

    instance.closeBtn.hide()

    instance.progressBar.hide()

    instance.cancelBtn.hide()
   
class latestVersion(QThread):

    responseSignal = pyqtSignal(str)

    def run(self):

        try:
            response = requests.get("https://api.github.com/repos/efeKbkci/englishWord/releases/latest")
            response_json = response.json()
            response.raise_for_status()  # HTTP hataları için
        except HTTPError as http_err:
            self.responseSignal.emit("Hata")
            return
        except ConnectionError as conn_err:
            self.responseSignal.emit("Hata")
            return
        except Timeout as timeout_err:
            self.responseSignal.emit("Hata")
            return
        except RequestException as req_err:
            self.responseSignal.emit("Hata")
            return

        self.latest_version = response_json["tag_name"]

        with open("version.txt","r") as version_file:

            current_version = version_file.read()

            if current_version != self.latest_version:

                exe_file = response_json["assets"][0]["browser_download_url"]

                self.file_size = response_json["assets"][0]["size"]

                self.value = exe_file

            else:

                self.value = "Versiyon Güncel"

        self.responseSignal.emit(self.value)

class downloadFile(QThread):

    downloadStatus = pyqtSignal(int)

    successSignal = pyqtSignal()

    iptal = False

    def run(self):

        try:
            response = requests.get(url=self.exe_url, stream=True)
            response.raise_for_status()  # HTTP hataları için
        except HTTPError as http_err:
            self.downloadStatus.emit(-1)
            return
        except ConnectionError as conn_err:
            self.downloadStatus.emit(-1)
            return
        except Timeout as timeout_err:
            self.downloadStatus.emit(-1)
            return
        except RequestException as req_err:
            self.downloadStatus.emit(-1)
            return

        indirilen = 0

        with open(r"qrApp.exe","rb") as file: # Dosya yedeği almak, iptal sonrasında dosyası yeniden oluşturmak için gereklidir.

            self.copy_app = file.read()

        with open(r"qrApp.exe", "wb") as file:

            for data in response.iter_content(chunk_size=1024):

                if self.iptal:

                    return

                if data:

                    indirilen += len(data)
                    self.downloadStatus.emit(indirilen)
                    file.write(data)

        with open("version.txt","w") as version_file:

            version_file.write(self.latest_version)

        self.successSignal.emit()
        
class versionController(QWidget):

    successSignal = pyqtSignal(bool)

    def __init__(self):

        super().__init__()

        self.latestVersionIns = latestVersion()

        self.downloadFileIns = downloadFile()

        self.latestVersionIns.responseSignal[str].connect(self.checkUpdate)

        self.downloadFileIns.downloadStatus[int].connect(self.progressBarSlot)

        self.downloadFileIns.successSignal.connect(self.successSignalSlot)

        createUI(self)

        self.infoLabel.setText("Güncellemeler kontrol ediliyor...")

        self.latestVersionIns.start()

        self.success = False # Program her kapandığında closeEvente girse bile, yalnızca başarılı durumda başarılı sinyali yayacak
        
    def checkUpdate(self,response):

        if response == "Hata":

            self.manageBtns()

            self.infoLabel.setText("Güncelleme kontrol edilemedi, bu sayfayı kapatabilirsiniz")

        elif response != "Versiyon Güncel":

            self.FILESIZE = self.latestVersionIns.file_size

            self.progressBar.setMaximum(self.FILESIZE//1048576)

            setattr(self.downloadFileIns,"exe_url",self.latestVersionIns.value)

            setattr(self.downloadFileIns,"latest_version",self.latestVersionIns.latest_version)

            self.infoLabel.setText(F"Güncelleme mevcut, hemen indirmek ister misiniz?\nDosya boyutu : {self.FILESIZE // 1048576} MB")

            self.manageBtns(b1=True,b2=True)
        
        else:

            self.close()

            print("Versiyon Güncel")

    def startDownload(self):

        self.infoLabel.setText("Güncelleme İndiriliyor...")

        self.downloadFileIns.start()

        self.manageBtns(b3=True,b4=True)

    def cancelUpdate(self):

        with open(r"qrApp.exe","wb") as file:

            file.write(self.downloadFileIns.copy_app) # Eski dosya yeniden yüklendi

        self.downloadFileIns.iptal = True

        self.manageBtns()

        self.infoLabel.setText("Güncelleme iptal edildi, bu sayfayı kapatabilirsiniz")

    def progressBarSlot(self,value):

        if value == -1:

            self.manageBtns()

            self.infoLabel.setText("Dosya indirilirken bir hata oluştu, bu sayfayı kapatabilirsiniz")

        self.progressBar.setValue(value)
        self.progressBar.setFormat(f"{value//1048576}/{self.FILESIZE//1048576} MB")

    def successSignalSlot(self):

        self.manageBtns()

        self.infoLabel.setText("Güncelleme başarıyla yüklendi, programı kapatıp tekrar açınız.")

        self.success = True

    def manageBtns(self,b1=False,b2=False,b3=False,b4=False):

        if b1:
            self.closeBtn.show()
        else:
            self.closeBtn.hide()
        if b2:
            self.downloadBtn.show()
        else:
            self.downloadBtn.hide()
        if b3:
            self.progressBar.show()
        else:
            self.progressBar.hide()
        if b4:
            self.cancelBtn.show()
        else:
            self.cancelBtn.hide()

    def closeEvent(self, event):

        self.successSignal.emit(self.success) # Program kapatıldığı zaman, ana programda kapanacak

        return super().closeEvent(event)

if __name__ == "__main__":

    app = QApplication([])
    widget = versionController()
    widget.show()
    app.exec_()