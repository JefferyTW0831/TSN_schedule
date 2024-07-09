import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('点击计数器')

        self.counter = 0
        self.label = QLabel(str(self.counter), self)

        self.btn = QPushButton('点击我', self)
        self.btn.clicked.connect(self.on_click)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.btn)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 200, 150)

    def on_click(self):
        self.counter += 1
        self.label.setText(str(self.counter))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())