from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt,pyqtSignal
import sys

class DialogKutusu(QDialog):

    def __init__(self):
        super().__init__()

        uic.loadUi("uiFile\Dialog.ui",self)

        self.statement = False

        self.saveStatement = False        

        self.cancelBtn.clicked.connect(self.btnClick)
        self.okeyBtn.clicked.connect(self.btnClick)

    def btnClick(self):

        btn = self.sender()

        if btn.text() != "Kaydetmeden Çık":

            self.saveStatement = True

        else:

            self.saveStatement = False

        self.statement = True

        self.close()

    def closeEvent(self, event):

        return super().closeEvent(event)

class combineWidget(QGraphicsView):

    closeSignal = pyqtSignal(list)

    def __init__(self):
        super().__init__()

        self.dialog = DialogKutusu()

        desktop = QDesktopWidget().screenGeometry()
        ekran_genislik = desktop.width()
        ekran_yukseklik = desktop.height()


        # TODO:Dosyaya göre boyut ayarı yapılacak
        # TODO:Arka plana göre qr kod büyüklüğü ayarlanacak
        self.setGeometry((ekran_genislik - 600) // 2, (ekran_yukseklik - 800) // 2,600,800)
        self.setStyleSheet(
            """
            QGraphicsView {
                background-color: #F9F3CC
            }
            """
        )

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.myscene = QGraphicsScene()

        self.setScene(self.myscene)

    def images(self,qrImage,backgroundImage):

        if type(backgroundImage) == str:
            self.isPDF = False
            self.background_image = QPixmap(backgroundImage)

        else:
            self.isPDF = True
            self.background_image = backgroundImage

        #else durumunda zaten qpixmap'tir

        background = self.myscene.addPixmap(self.background_image)

        self.fitInView(background)

        self.overlay = self.myscene.addPixmap(QPixmap(qrImage))
        self.overlay.setParentItem(background)
        self.overlay.setFlag(QGraphicsItem.ItemIsMovable)
        self.overlay.setFlag(QGraphicsItem.ItemIsSelectable)

    def closeEvent(self,event):

        # Not al

        self.dialog.exec()

        if self.dialog.saveStatement:

            if hasattr(self,"overlay"):

                if self.isPDF:
                    image = self.background_image.toImage()
                    image.save("geciciResimSilme.png")

                kordinat = self.overlay.mapToParent(0,0) 
                self.closeSignal.emit([kordinat.x(),kordinat.y(),self.isPDF])

        elif self.dialog.statement:
            event.accept()

        else:
            event.ignore()

        
if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = combineWidget()
    window.show()
    sys.exit(App.exec())