from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLayout, QLineEdit,
                             QSizePolicy, QToolButton, QWidget)

class Button(QToolButton):
    def __init__(self, text, parent=None):
        super(Button, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setText(text)

    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height() + 20)
        size.setWidth(max(size.width(), size.height()))
        return size

class Calculator(QWidget):
    NumDigitButtons = 10

    def __init__(self, parent=None):
        super(Calculator, self).__init__(parent)

        self.pendingAddOp = ''
        self.pendingMulOp = ''

        self.sumOp = 0.0
        self.mulOp = 0.0
        self.sumMemory = 0.0
        self.waitingForOp = True

        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMaxLength(15)

        font = self.display.font()
        font.setPointSize(font.pointSize() + 8)
        self.display.setFont(font)

        ## Create Button
        self.digitButtons = []
        for i in range(Calculator.NumDigitButtons):
            self.digitButtons.append(self.createButton(str(i), self.digitClicked))

        self.pointButton = self.createButton(".", self.pointClicked)
        self.clearAllButton = self.createButton("C", self.clearAll)
        self.backspaceButton = self.createButton("←", self.backspaceClicked)
        self.equalButton = self.createButton("=", self.equalClicked)
        self.plusButton = self.createButton("+", self.PlusMinusClicked)
        self.minusButton = self.createButton("-", self.PlusMinusClicked)
        self.mulButton = self.createButton("x", self.MulDivClicked)
        self.divButton = self.createButton("÷", self.MulDivClicked)


        ## Set Layout
        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)

        mainLayout.addWidget(self.display, 0, 0, 1, 4)
        mainLayout.addWidget(self.clearAllButton, 1, 0)
        mainLayout.addWidget(self.backspaceButton, 1, 1)
        mainLayout.addWidget(self.equalButton, 1, 2, 1, 2)

        for i in range(1, Calculator.NumDigitButtons):
            row = ((9 - i) / 3) + 2
            col = ((i - 1) % 3)
            mainLayout.addWidget(self.digitButtons[i], row, col, 1, 1)
        mainLayout.addWidget(self.digitButtons[0], 5, 0, 1, 2)

        mainLayout.addWidget(self.plusButton, 2, 3)
        mainLayout.addWidget(self.minusButton, 3, 3)
        mainLayout.addWidget(self.mulButton, 4, 3)
        mainLayout.addWidget(self.divButton, 5, 3)
        mainLayout.addWidget(self.pointButton, 5, 2)
        self.setLayout(mainLayout)

    def createButton(self, text, member):
        button = Button(text)
        button.clicked.connect(member)
        return button

    def digitClicked(self):
        clickedButton = self.sender()
        digitValue = int(clickedButton.text())

        if self.display.text() == '0' and digitValue ==0.0:
            return

        if self.waitingForOp:
            self.display.clear()
            self.waitingForOp = False

        self.display.setText(self.display.text() + str(digitValue))

    def PlusMinusClicked(self):
        clickedButton = self.sender()
        clickedOp = clickedButton.text()
        Op = float(self.display.text())

        if self.pendingMulOp:
            if not self.calculate(Op, self.pendingMulOp):
                self.abortOp()
                return
            self.display.setText(str(self.mulOp))
            Op = self.mulOp
            self.mulOp = 0.0
            self.pendingMulOp = ''

        if self.pendingAddOp:
            if not self.calculate(Op, self.pendingAddOp):
                self.abortOp()
                return
            self.display.setText(str(self.sumOp))
        else:
            self.sumOp = Op

        self.pendingAddOp = clickedOp
        self.waitingForOp = True

    def MulDivClicked(self):
        clickedButton = self.sender()
        clickedOp = clickedButton.text()
        Op = float(self.display.text())

        if self.pendingMulOp:
            if not self.calculate(Op, self.pendingMulOp):
                self.abortOp()
                return
            self.display.setText(str(self.mulOp))
        else:
            self.mulOp = Op

        self.pendingMulOp = clickedOp
        self.waitingForOp = True



    def pointClicked(self):
        if self.waitingForOp:
            self.display.setText('0')

        if "." not in self.display.text():
            self.display.setText(self.display.text() + ".")

        self.waitingForOp = False

    def backspaceClicked(self):
        if self.waitingForOp:
            return

        text = self.display.text()[:-1]
        if not text:
            text = '0'
            self.waitingForOp = True

        self.display.setText(text)

    def clear(self):
        if self.waitingForOp:
            return
        self.display.setText('0')
        self.waitingForOp = True

    def clearAll(self):
        self.sumOp = 0.0
        self.mulOp = 0.0
        self.pendingMulOp = ''
        self.pendingAddOp = ''
        self.display.setText('0')
        self.waitingForOp = True

    def equalClicked(self):
        Op = float(self.display.text())

        if self.pendingMulOp:
            if not self.calculate(Op, self.pendingMulOp):
                self.abortOp()
                return
            Op = self.mulOp
            self.mulOp = 0.0
            self.pendingMulOp = ''

        if self.pendingAddOp:
            if not self.calculate(Op, self.pendingAddOp):
                self.abortOp()
                return
            self.pendingAddOp = ''
        else:
            self.sumOp = Op

        self.display.setText(str(self.sumOp))
        self.sumOp = 0.0
        self.waitingForOp = True

    def abortOp(self):
        self.clearAll()
        self.display.setText("####")

    def calculate(self, rightOp, pendingOp):
        if pendingOp == "+":
            self.sumOp += rightOp
        elif pendingOp == "-":
            self.sumOp -= rightOp
        elif pendingOp == "x":
            self.mulOp *= rightOp
        elif pendingOp == "÷":
            if rightOp == 0.0:
                return False
            self.mulOp /= rightOp
        return True


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())