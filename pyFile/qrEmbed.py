from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt,pyqtSignal
import sys

from Dialogs import savingQuestion

def createUI(instance=QGraphicsView):

    instance.savingQuestion = savingQuestion()

    desktop = QDesktopWidget().screenGeometry()
    ekran_genislik = desktop.width()
    ekran_yukseklik = desktop.height()

    # TODO:Dosyaya göre boyut ayarı yapılacak
    # TODO:Arka plana göre qr kod büyüklüğü ayarlanacak
    instance.setGeometry((ekran_genislik - 600) // 2, (ekran_yukseklik - 800) // 2,600,800)
    instance.setStyleSheet(
        """
        QGraphicsView {
            background-color: #F9F3CC
        }
        """
    )

    instance.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    instance.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    instance.myscene = QGraphicsScene()

    instance.setScene(instance.myscene)


class qrEmbed(QGraphicsView):

    closeSignal = pyqtSignal(list)

    def __init__(self):

        super().__init__()

        createUI(self)

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

        self.savingQuestion.exec()

        if self.savingQuestion.saveStatement:

            if hasattr(self,"overlay"):

                if self.isPDF:
                    image = self.background_image.toImage()
                    image.save("geciciResimSilme.png")

                kordinat = self.overlay.mapToParent(0,0) 
                self.closeSignal.emit([kordinat.x(),kordinat.y(),self.isPDF])

        elif self.savingQuestion.statement:
            event.accept()

        else:
            event.ignore()
        
if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = qrEmbed()
    window.show()
    sys.exit(App.exec())