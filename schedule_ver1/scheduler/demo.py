import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsLineItem, QGraphicsSimpleTextItem, QGraphicsRectItem
from PyQt5.QtGui import QPen, QColor
import random


class CustomGraphicsView(QGraphicsView):
    def __init__(self, links_dic):
        super().__init__()

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.links_dic = links_dic



        self.grid_size_x = 100
        self.grid_size_y = self.links_dic
        self.cell_width = 30
        self.cell_height = 30

        self.grid_line_color = QColor("black")
        self.cell_background_color = QColor("lightgray")

        self.draw_grid()

    def draw_grid(self):

        for i, key in enumerate(self.grid_size_y.keys()):
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

        for i in range(self.grid_size_x + 1):
            text_item = QGraphicsSimpleTextItem(str(i))
            text_item.setPos(i * self.cell_width + 10, -15)
            self.scene.addItem(text_item)


    def update_graphics_from_dict(self, data_dict):
        for flow_name, path in data_dict.items():
            random_color = self.generate_random_color()
            for link in path:
                target_key = (link["Ingress"],link["Egress"]) 
                y = list(self.links_dic.keys()).index(target_key)
                x = link["Time"]
                for time in x.keys():
                    rect = QGraphicsRectItem(time * self.cell_width, y * self.cell_height, 1 * self.cell_width, 1 * self.cell_height)
                    rect.setBrush(QColor(random_color))
                    self.scene.addItem(rect)
                    
                    text_item = QGraphicsSimpleTextItem(str(flow_name))
                    text_item.setPos(time * self.cell_width, y * self.cell_height +15)
                    self.scene.addItem(text_item)
            print(f"{flow_name}:{random_color}")
            print('\n') 
            
    def generate_random_color(self):
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        color = QColor(red, green, blue)
        return color

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = CustomGraphicsView()
    view.show()
    sys.exit(app.exec_())
