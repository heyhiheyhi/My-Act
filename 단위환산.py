import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit, QComboBox)
from PyQt5.QtCore import Qt


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self.lbl1 = QLabel('', self)
        self.lbl1.setAlignment(Qt.AlignCenter)
        self.lbl2 = QLabel('', self)
        self.lbl2.setAlignment(Qt.AlignCenter)
        self.lbl3 = QLabel('', self)
        self.lbl3.setAlignment(Qt.AlignCenter)
        self.lbl4 = QLabel('mm', self)
        self.lbl5 = QLabel('cm', self)
        self.lbl6 = QLabel('m', self)

        self.le1 = QLineEdit(self)
        self.le1.textChanged.connect(self.calculator)
        self.le2 = QLineEdit(self)
        self.le2.setReadOnly(True)

        self.cb1 = QComboBox(self)
        self.cb1.currentIndexChanged.connect(self.calculator)
        self.cb1.addItem('mm')
        self.cb1.addItem('cm')
        self.cb1.addItem('m')
        self.cb2 = QComboBox(self)
        self.cb2.currentIndexChanged.connect(self.calculator)
        self.cb2.addItem('mm')
        self.cb2.addItem('cm')
        self.cb2.addItem('m')

        grid.addWidget(self.le1, 0, 0)
        grid.addWidget(self.le2, 1, 0)
        grid.addWidget(self.lbl1, 2, 0)
        grid.addWidget(self.lbl2, 3, 0)
        grid.addWidget(self.lbl3, 4, 0)
        grid.addWidget(self.lbl4, 2, 1)
        grid.addWidget(self.lbl5, 3, 1)
        grid.addWidget(self.lbl6, 4, 1)

        grid.addWidget(self.cb1, 0, 1)
        grid.addWidget(self.cb2, 1, 1)

        self.setWindowTitle('QGridLayout')
        self.setGeometry(299, 300, 300, 200)
        self.show()

    def calculator(self):
        try:
            le1_value = float(self.le1.text())
            if self.cb1.currentIndex() == 0:
                self.lbl1.setText(str(le1_value))
                self.lbl2.setText(str(le1_value * 0.1))
                self.lbl3.setText(str(le1_value * 0.001))

                if self.cb2.currentIndex() == 0:
                    self.le2.setText(self.lbl1.text())
                elif self.cb2.currentIndex() == 1:
                    self.le2.setText(self.lbl2.text())
                elif self.cb2.currentIndex() == 2:
                    self.le2.setText(self.lbl3.text())

            elif self.cb1.currentIndex() == 1:
                self.lbl1.setText(str(le1_value * 10))
                self.lbl2.setText(str(le1_value))
                self.lbl3.setText(str(le1_value * 0.01))

                if self.cb2.currentIndex() == 0:
                    self.le2.setText(self.lbl1.text())
                elif self.cb2.currentIndex() == 1:
                    self.le2.setText(self.lbl2.text())
                elif self.cb2.currentIndex() == 2:
                    self.le2.setText(self.lbl3.text())

            elif self.cb1.currentIndex() == 2:
                self.lbl1.setText(str(le1_value * 1000))
                self.lbl2.setText(str(le1_value * 100))
                self.lbl3.setText(str(le1_value))

                if self.cb2.currentIndex() == 0:
                    self.le2.setText(self.lbl1.text())
                elif self.cb2.currentIndex() == 1:
                    self.le2.setText(self.lbl2.text())
                elif self.cb2.currentIndex() == 2:
                    self.le2.setText(self.lbl3.text())

        except ValueError:
            self.le1.setText('')
            self.le1.setPlaceholderText("숫자만 입력해 주세요")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())