import segno
from PyQt5.QtWidgets import *
from PyQt5 import uic

def createUI(instance):

    uic.loadUi("uiFile\qrSettings.ui",instance)

    instance.okeyBtn.clicked.connect(instance.qrSettings)

class qrSettings(QWidget):

    def __init__(self):
        super().__init__()   

        createUI(self)     

        self.text = self.qrContent.text()

        self.scale = self.qrScale.value()

        self.createQR(self.text,self.scale)

    def qrSettings(self):

        self.text = self.qrContent.text()

        self.scale = self.qrScale.value()

        qr = segno.make_qr(self.text)

        qr.save("qr_code.png", scale=self.scale)

        self.close()

    def createQR(self,url,scale):

        qr = segno.make_qr(url)

        qr.save("qr_code.png", scale=scale)