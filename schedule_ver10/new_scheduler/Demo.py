import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsLineItem, QGraphicsSimpleTextItem, QGraphicsRectItem, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtGui import QPen, QColor, QPixmap, QPainter
from PyQt5.QtCore import Qt,QPointF
import random


class Demo(QMainWindow):
    def __init__(self, links_dic, max_time):
        super().__init__()

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.links_dic = links_dic

        self.grid_size_x = max_time+1
        self.grid_size_y = self.links_dic
        self.cell_width = 30
        self.cell_height = 30

        self.grid_line_color = QColor("black")
        self.flow_color = {}
        self.color_count = 0
        self.draw_grid()
        self.initUI()
        

    def initUI(self):
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        layout.addWidget(self.view)
        # 添加保存按钮
        self.save_button = QPushButton('Save Chart', self)
        self.save_button.clicked.connect(self.save_chart)
        layout.addWidget(self.save_button)
        
        self.setCentralWidget(central_widget)  # 設置中心小部件

    def draw_grid(self):
        #繪製格線_y軸
        for i in range(len(self.grid_size_y.keys()) + 1):
            line = QGraphicsLineItem(0, i * self.cell_height, self.grid_size_x * self.cell_width, i * self.cell_height)
            pen = QPen(self.grid_line_color)
            line.setPen(pen)
            self.scene.addItem(line)
        #繪製格線_x軸
        for i in range(self.grid_size_x + 1):
            line = QGraphicsLineItem(i * self.cell_width, 0, i * self.cell_width, len(self.grid_size_y) * self.cell_height)
            pen = QPen(self.grid_line_color)
            line.setPen(pen)
            self.scene.addItem(line) 
        #標記_y軸項目(鏈結名稱)
        for i, key in enumerate(self.grid_size_y.keys()):
            text = f"{key}"
            text_item = QGraphicsSimpleTextItem(str(f"{key}"))
            text_item.setPos(-70, i * self.cell_height + 10)
            if text[2] == 'D':
                text_item.setBrush(QColor("Red"))  # 设置字体颜色
            if text[-4] == 'D' or text[-5] == 'D':
                text_item.setBrush(QColor("Green"))  # 设置字体颜色
            self.scene.addItem(text_item)
        #標記_x軸項目(時間點)
        for i in range(self.grid_size_x):
            text_item = QGraphicsSimpleTextItem(str(f"{i}"))
            text_item.setPos(i * self.cell_width + 10, -15)
            self.scene.addItem(text_item)

    def update_graphics_from_dict(self, data_dict):
        collision_dict = {}
        for time, links in data_dict.items():
            
            for link, packet_data in links.items():
                color = self.flow_color_set(packet_data["Flow"])
                y = list(self.links_dic.keys()).index(link)

                #沒有衝突狀況發生，正常印出顏色
                rect = QGraphicsRectItem(time * self.cell_width, y * self.cell_height, 1 * self.cell_width, 1 * self.cell_height)
                rect.setBrush(QColor(color))
                self.scene.addItem(rect)
                text_item2 = QGraphicsSimpleTextItem(str(packet_data["Flow"])+'_'+str(packet_data["Packet"]))
                text_item2.setPos(time * self.cell_width + 0.5, y * self.cell_height + 15)
                text_item2.setBrush(QColor("White"))  # 设置字体颜色
                self.scene.addItem(text_item2)

        print("\n\n-----------------------------------")
        print("(Demo.py)\n")
        print(f"collision flows=")
        for link, time in collision_dict.items():
            print(f"{link}:{time}")
        print("-----------------------------------")

    def is_color_at_position(self, x, y):
        items = self.scene.items(QPointF(x, y))
        for item in items:
            if isinstance(item, QGraphicsRectItem):
                return True
        return False
 
    def flow_color_set(self, flow_name):
        if flow_name in self.flow_color.keys():
            return self.flow_color[flow_name]
        else:
            random_color = self.generate_random_color()
            self.flow_color[flow_name] = random_color
            return random_color
   
    def generate_random_color(self):
        self.color_count += 5
        red = (self.color_count*10)%250
        green = (self.color_count*21)%250
        blue = (self.color_count*27)%250
        color = QColor(red, green, blue)
        return color

    def save_chart(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Chart", "", "PNG Files (*.png);;All Files (*)", options=options)
        if file_path:
            self.save_scene_to_image(file_path)

    def save_scene_to_image(self, file_path):
        # 设置画布大小为场景的边界
        rect = self.scene.itemsBoundingRect()
        image = QPixmap(int(rect.width()), int(rect.height()))
        image.fill(Qt.white)  # 可选：填充背景为白色
        painter = QPainter(image)
        self.scene.render(painter)
        painter.end()
        image.save(file_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = Demo()
    view.show()
    sys.exit(app.exec_())
