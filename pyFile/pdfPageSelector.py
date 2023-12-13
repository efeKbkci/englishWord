from PyQt5.QtWidgets import *
from PyQt5 import uic 
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
import fitz

class pageSelector(QWidget):

    closeSignal = pyqtSignal()

    def __init__(self,file_path=str):
        super().__init__()

        uic.loadUi("uiFile\pdfSayfaSecme.ui",self)

        self.pixmap_list = self.getPages(file_path)

        self.spin_box.setMinimum(1)

        self.spin_box.setMaximum(len(self.pixmap_list))

        self.spin_box.valueChanged.connect(self.valueChanged)

        self.okeyBtn.clicked.connect(self.choose_and_finish)

        self.pixmapLabel.setPixmap(self.pixmap_list[self.spin_box.value()-1])

        self.pixmapLabel.setScaledContents(True)

    def valueChanged(self):

        value = self.spin_box.value()

        pixmap = self.pixmap_list[value-1]

        self.pixmapLabel.setPixmap(pixmap)

        self.pixmapLabel.setScaledContents(True)

    def getPages(self,file_path):

        qtPixmaps = list()

        doc = fitz.open(file_path)

        for i in range(doc.page_count):

            page = doc[i]

            image = page.get_pixmap()

            qt_image = QPixmap()

            qt_image.loadFromData(image.tobytes(), "PNG")

            qtPixmaps.append(qt_image)

        doc.close()

        return qtPixmaps
    
    def choose_and_finish(self):

        self.pixmapObject = self.pixmap_list[self.spin_box.value()-1]
        self.pageNumber = self.pixmap_list.index(self.pixmap_list[self.spin_box.value()-1])
        self.close()

    def closeEvent(self, event):

        self.closeSignal.emit()
        return super().closeEvent(event)

        
if __name__ == "__main__":

    app = QApplication([])
    widget = pageSelector(r"C:\Users\efkan\Downloads\efkanefekabakcii@gmail.com.pdf")
    widget.show()
    app.exec_()
