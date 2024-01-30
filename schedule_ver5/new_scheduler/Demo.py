import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsLineItem, QGraphicsSimpleTextItem, QGraphicsRectItem
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtCore import QPointF
import random


class Demo(QGraphicsView):
    def __init__(self, links_dic, max_time):
        super().__init__()

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.links_dic = links_dic

        self.grid_size_x = max_time+1
        self.grid_size_y = self.links_dic
        self.cell_width = 30
        self.cell_height = 30

        self.grid_line_color = QColor("black")
        self.flow_color = {}

        self.draw_grid()

    def draw_grid(self):

        for i in range(len(self.grid_size_y.keys()) + 1):
            line = QGraphicsLineItem(0, i * self.cell_height, self.grid_size_x * self.cell_width, i * self.cell_height)
            pen = QPen(self.grid_line_color)
            line.setPen(pen)
            self.scene.addItem(line)

        for i in range(self.grid_size_x + 1):
            line = QGraphicsLineItem(i * self.cell_width, 0, i * self.cell_width, len(self.grid_size_y) * self.cell_height)
            pen = QPen(self.grid_line_color)
            line.setPen(pen)
            self.scene.addItem(line) 

        for i, key in enumerate(self.grid_size_y.keys()):
            text_item = QGraphicsSimpleTextItem(str(f"{key}"))
            text_item.setPos(-70, i * self.cell_height + 10)
            self.scene.addItem(text_item)

        for i in range(self.grid_size_x):
            text_item = QGraphicsSimpleTextItem(str(i))
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

    def generate_random_color(self):
        red = random.randint(1, 250)
        green = random.randint(1, 250)
        blue = random.randint(1, 250)
        color = QColor(red, green, blue)
        return color
    


    def flow_color_set(self, flow_name):
        if flow_name in self.flow_color.keys():
            return self.flow_color[flow_name]
        else:
            random_color = self.generate_random_color()
            self.flow_color[flow_name] = random_color
            return random_color





if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = Demo()
    view.show()
    sys.exit(app.exec_())
