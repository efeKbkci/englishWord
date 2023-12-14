from PyQt5.QtWidgets import *
from PyQt5 import uic 
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
import fitz

def createUI(instance,file_path):

    uic.loadUi("uiFile\pdfSelectPage.ui",instance)

    instance.pixmap_list = instance.getPages(file_path)

    instance.spin_box.setMinimum(1)

    instance.spin_box.setMaximum(len(instance.pixmap_list))

    instance.spin_box.valueChanged.connect(instance.valueChanged)

    instance.okeyBtn.clicked.connect(instance.choose_and_finish)

    instance.pixmapLabel.setPixmap(instance.pixmap_list[instance.spin_box.value()-1])

    instance.pixmapLabel.setScaledContents(True)

class pdfSelectPage(QWidget):

    closeSignal = pyqtSignal()

    def __init__(self,file_path=str):

        super().__init__()

        createUI(self,file_path)

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
    widget = pdfSelectPage(r"C:\Users\efkan\Downloads\efkanefekabakcii@gmail.com.pdf")
    widget.show()
    app.exec_()
