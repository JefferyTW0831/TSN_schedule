import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QFileDialog
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PyQt5 QPainter Example')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.chart_widget = ChartWidget(self)
        layout.addWidget(self.chart_widget)

        save_button = QPushButton('Save Chart', self)
        save_button.clicked.connect(self.save_chart)
        layout.addWidget(save_button)

    def save_chart(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Chart", "", "PNG Files (*.png);;All Files (*)", options=options)
        if file_path:
            self.chart_widget.save_chart(file_path)

class ChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(800, 600)

    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_chart(painter)

    def draw_chart(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.black)
        painter.setBrush(QColor(200, 200, 200))
        
        # Draw a simple bar chart
        for i in range(5):
            painter.drawRect(50 + i*100, 400, 50, -i*50 - 50)

    def save_chart(self, file_path):
        pixmap = QPixmap(self.size())
        self.render(pixmap)
        pixmap.save(file_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())