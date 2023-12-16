import segno
from PIL import Image
from os import remove,path
import requests
import os

from PyQt5.QtWidgets import *
from PyQt5 import uic 
from PyQt5.QtGui import QPixmap
import resources

from qrEmbed import qrEmbed
from pdfSelectPage import pdfSelectPage
from pdfPutTogether import png_to_pdf,putTogether
from qrSettings import qrSettings
from versionController import versionController

from sunucuIslemleri import dosyaKontrolEtme, dosyaYukleme
from  urlNameFixing import nameFixing

from Dialogs import successMsg

def createUI(instance=QWidget):

    uic.loadUi("uiFile\qrApp.ui",instance)

    instance.getFileBtn.clicked.connect(instance.getFile)

    instance.getQRBtn.clicked.connect(instance.getQR)

    instance.combineBtn.clicked.connect(instance.combineUIShow)

    instance.toolButton.clicked.connect(lambda:instance.qrSettings.show())

    instance.versionController.successSignal[bool].connect(instance.updateStatus)

    instance.versionController.show()

class qrApp(QWidget):
    
    #TODO:Resmi doğru konuma yerleştir, pdf için ayarla

    def defineModuls(self):

        self.combineUI = qrEmbed()

        self.dialog = successMsg()

        self.qrSettings = qrSettings()

        self.versionController = versionController()

    def __init__(self):

        super(qrApp,self).__init__()

        self.defineModuls()

        createUI(self)

        self.combineUI.closeSignal[list].connect(self.combineAndFinish)

        self.fileName = None

        self.qrName = None

    def updateStatus(self,status):

        print(status)

        if status: # Güncelleme olmuş, sistem yeniden başlatılacak

            print("if bloğu")

            self.close()

            print("İndirme başarılı")
        
        else: # Güncelleme yok veya başarısız, uygulama eski sürümden devam edecek

            print("Else bloğu")

            if os.path.isfile("qrApp_silme.exe"):

                print("İndirme başarısız")

                os.remove("qrApp_silme.exe")

            self.show()

    def fileExplorer(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Dosya Seç", "", "All Files (*)", options=options)

        return fileName

    def getFile(self):

        self.fileName = self.fileExplorer()

        if not self.fileName:

            return

        if path.getsize(self.fileName) > 5242880:

            self.filePathLabel.setText("Dosya 5 megabyte'dan büyük olamaz!")

            self.fileName = ""

            return
        
        dosya_adı, uzanti = path.splitext(self.fileName)

        if not uzanti in [".pdf",".png",".jpg",".jpeg"]:

            self.filePathLabel.setText("Dosya formatı bunlardan biri olmalı -> pdf, png, jpg, jpeg")

            self.fileName = ""

            return

        self.filePathLabel.setText(self.fileName)

        if self.fileName.endswith(".pdf"):

            self.hide()

            self.pdfPageSelector = pdfSelectPage(self.fileName)

            self.pdfPageSelector.closeSignal.connect(self.pdfPageSlot)

            self.pdfPageSelector.show()

    def getQR(self):

        self.qrName = self.fileExplorer()
        
        if not self.qrName.split("/")[-1] == "qr_code.png":

            self.qrPathLabel.setText("Uygulama dizininizde bulunan 'qr_code.png' dosyasını seçiniz.")

            self.qrName = ""

            return
        
        self.qrPathLabel.setText(self.qrName)

        self.qrPrevious.setPixmap(QPixmap(self.qrName))

        self.qrPrevious.setScaledContents(True)

    def pdfPageSlot(self):

        self.show()

        if hasattr(self.pdfPageSelector,"pixmapObject"): # Tamam'a basıldıysa sayfa seçilmiştir, aksi takdirde seçilmemiştir
            self.pixmapObject = self.pdfPageSelector.pixmapObject
            self.pageNumber = self.pdfPageSelector.pageNumber

        else:
            self.pixmapObject = None
            self.filePathLabel.setText("")            

    def combineUIShow(self):

        if not self.qrName or not self.fileName:
            print("Dosyalar Eksik")
            return # popup eklenebilir
        
        if self.fileName.endswith(".pdf"):
            self.combineUI.images(self.qrName,self.pixmapObject)

        else:
            self.combineUI.images(self.qrName,self.fileName)

        self.combineUI.show()

        self.hide()

    def combineAndFinish(self,kordinatlar):

        self.show()

        x = kordinatlar[0]
        y = kordinatlar[1]

        # URL Adı Tanımlama / Hatalı harfleri yok etme

        fileName = nameFixing(self.fileName)

        if not kordinatlar[2]:

            addingFileName = f"{fileName.split('.')[0]}_qr_eklenmis.{fileName.split('.')[1]}" 
            # jpeg uzantılı bir dosyayı .png olarak kaydettiğimiz için, sunucuya boş, bilgisayarımızda olmayan bir dosya gönderiyorduk.

        else:

            addingFileName = f"{fileName.split('.')[0]}_qr_eklenmis.pdf"

        dosyaSozluk = dosyaKontrolEtme(addingFileName)

        if dosyaSozluk == "Hata":
            self.connectionError()

        addingFileName = dosyaSozluk["fileName"]

        self.qrSettings.createQR(f"https://qrsorgu.com.tr/files/bIMJ-h5qr-Z3WZ-Oo9A/{addingFileName}",self.qrSettings.scale)            

        if kordinatlar[2]:
            background = Image.open("geciciResimSilme.png")

        else:
            background = Image.open(self.fileName)

        overlay = Image.open("qr_code.png")

        background.paste(overlay, (int(x),int(y)))

        if not kordinatlar[2]:

            background.save(f"OutputFiles\\{addingFileName}")
            
            if dosyaYukleme(f"OutputFiles\\{addingFileName}",addingFileName) == "Hata":
                self.connectionError()
        
        else:
            remove("geciciResimSilme.png")

            background.save("geciciResimSilme.png")

            png_to_pdf("geciciResimSilme.png")

            putTogether(self.fileName,self.pageNumber,f"OutputFiles\\{addingFileName}")

            if dosyaYukleme(f"OutputFiles\\{addingFileName}",addingFileName):
                self.connectionError()

            remove("geciciResimSilme.png")

            remove("gecicipdf.pdf")

        try:
            del self.pdfPageSelector.pixmapObject
            del self.pdfPageSelector.pageNumber
        except AttributeError:
            pass

        self.dialog.show()

    def connectionError(self):

        msg = QMessageBox()
        msg.setText("Bir bağlantı hatası meydana geldi, lütfen internet bağlantınızı kontrol edin.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

        self.close()

if __name__ == "__main__":

    app = QApplication([])
    widget = qrApp()

    ekran_geo = app.desktop().screenGeometry()
    widget.move((ekran_geo.width() - widget.width()) // 2, (ekran_geo.height() - widget.height()) // 2)

    app.exec_()
