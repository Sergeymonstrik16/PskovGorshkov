import sys
from random import randint
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QColor, QPixmap, QPen


class Zadacha2(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Ui.ui', self)
        self.initUI()

    def initUI(self):
        self.for_krug.setPixmap(QPixmap(501, 361))
        self.pushButton.clicked.connect(self.krug)

    def krug(self):
        x, y = [randint(10, 360) for i in range(2)]
        w, h = [randint(10, 100) for i in range(2)]
        painter = QPainter(self.for_krug.pixmap())
        pen = QPen()
        pen.setWidth(3)
        pen.setColor(QColor(255, 255, 0))
        painter.setPen(pen)
        painter.drawEllipse(x, y, w, h)
        painter.end()
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Zadacha2()
    ex.show()
    sys.exit(app.exec_())
