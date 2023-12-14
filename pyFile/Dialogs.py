from PyQt5.QtWidgets import QDialog
from PyQt5 import uic 

class successMsg(QDialog):

    def __init__(self):
        super().__init__()

        uic.loadUi("uiFile\successMsg.ui",self)

        self.okBtn.clicked.connect(lambda:self.close())


class savingQuestion(QDialog):

    def __init__(self):
        super().__init__()

        uic.loadUi("uiFile\savingQuestion.ui",self)

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
