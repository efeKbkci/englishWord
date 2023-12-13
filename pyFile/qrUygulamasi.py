import segno
from PIL import Image
from os import remove,path
import requests

from PyQt5.QtWidgets import *
from PyQt5 import uic 
from PyQt5.QtGui import QPixmap
import resources
from qrPlace import combineWidget
from pdfPageSelector import pageSelector
from pdfBirlestir import png_to_pdf,birlestir
from sunucuIslemleri import dosyaKontrolEtme, dosyaYukleme

class successfulDialog(QDialog):

    def __init__(self):
        super().__init__()

        uic.loadUi("uiFile\Dialog_2.ui",self)

        self.okBtn.clicked.connect(lambda:self.close())

class qrSettings(QWidget):

    def __init__(self):
        super().__init__()

        uic.loadUi("uiFile\qrSettings.ui",self)

        self.text = self.qrContent.text()

        self.scale = self.qrScale.value()

        self.createQR(self.text,self.scale)

        self.okeyBtn.clicked.connect(self.qrSettings)

    def qrSettings(self):

        self.text = self.qrContent.text()

        self.scale = self.qrScale.value()

        qr = segno.make_qr(self.text)

        qr.save("qr_code.png", scale=self.scale)

        self.close()

    def createQR(self,url,scale):

        qr = segno.make_qr(url)

        qr.save("qr_code.png", scale=scale)

class MainWidget(QWidget):
    
    #TODO:Resmi doğru konuma yerleştir, pdf için ayarla

    def __init__(self):

        super(MainWidget,self).__init__()

        uic.loadUi(r"uiFile\birlestirici.ui",self)

        self.hide()

        self.combineUI = combineWidget()

        self.dialog = successfulDialog()

        self.qrSettings = qrSettings()

        self.combineUI.closeSignal[list].connect(self.combineAndFinish)

        self.getFileBtn.clicked.connect(self.getFile)

        self.getQRBtn.clicked.connect(self.getQR)

        self.combineBtn.clicked.connect(self.combineUIShow)

        self.toolButton.clicked.connect(self.qrSettingsShow)

        self.fileName = None

        self.qrName = None

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

            self.pdfPageSelector = pageSelector(self.fileName)

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

    def qrSettingsShow(self):

        self.qrSettings.show()

    def combineAndFinish(self,kordinatlar):

        self.show()

        x = kordinatlar[0]
        y = kordinatlar[1]

        if not kordinatlar[2]:

            fileName = self.fileName.split("/")[-1]
            addingFileName = f"{fileName.split('.')[0]}_qr_eklenmis.png"

            dosyaSozluk = dosyaKontrolEtme(addingFileName)
            addingFileName = dosyaSozluk["fileName"]

        else:

            fileName = self.fileName.split("/")[-1]
            addingFileName = f"{fileName.split('.')[0]}_qr_eklenmis.pdf"
            
            dosyaSozluk = dosyaKontrolEtme(addingFileName)
            addingFileName = dosyaSozluk["fileName"]

        self.qrSettings.createQR(f"http://35.246.208.82/files/bIMJ-h5qr-Z3WZ-Oo9A/{addingFileName}",self.qrSettings.scale)            

        if kordinatlar[2]:
            background = Image.open("geciciResimSilme.png")

        else:
            background = Image.open(self.fileName)

        overlay = Image.open("qr_code.png")

        background.paste(overlay, (int(x),int(y)))

        if not kordinatlar[2]:

            background.save(f"OutputFiles\\{addingFileName}")

            dosyaYukleme(f"OutputFiles\\{addingFileName}",addingFileName)
        
        else:
            remove("geciciResimSilme.png")

            background.save("geciciResimSilme.png")

            png_to_pdf("geciciResimSilme.png")

            birlestir(self.fileName,self.pageNumber,f"OutputFiles\\{addingFileName}")

            dosyaYukleme(f"OutputFiles\\{addingFileName}",addingFileName)

            remove("geciciResimSilme.png")

            remove("gecicipdf.pdf")

        try:
            del self.pdfPageSelector.pixmapObject
            del self.pdfPageSelector.pageNumber
        except AttributeError:
            pass

        self.dialog.show()

if __name__ == "__main__":

    app = QApplication([])
    widget = MainWidget()

    ekran_geo = app.desktop().screenGeometry()
    widget.move((ekran_geo.width() - widget.width()) // 2, (ekran_geo.height() - widget.height()) // 2)

    widget.show()
    app.exec_()
