import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsLineItem, QGraphicsSimpleTextItem, QGraphicsRectItem
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtCore import QPointF
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
        collision_dict = {}
        for flow_name, path in data_dict.items():
            random_color = self.generate_random_color()
            for link in path:
                target_key = (link["Ingress"],link["Egress"]) 
                y = list(self.links_dic.keys()).index(target_key)
                x = link["Time"]
                for time in x.keys():
                    
                    if self.is_color_at_position(time * self.cell_width + 0.5, y * self.cell_height + 0.5):
                        rect = QGraphicsRectItem(time * self.cell_width, y * self.cell_height, 0.3 * self.cell_width, 0.3 * self.cell_height)
                        rect.setBrush(QColor("black"))
                        self.scene.addItem(rect)
                        if collision_dict.get(target_key) == None:
                            collision_dict[target_key] = {}
                            collision_dict[target_key][time] = []
                            collision_dict[target_key][time].append(flow_name)
                        elif collision_dict[target_key].get(time) == None:
                            collision_dict[target_key][time] = []
                            collision_dict[target_key][time].append(flow_name)
                        else:
                            collision_dict[target_key][time].append(flow_name)
                    
                    else:
                        rect = QGraphicsRectItem(time * self.cell_width, y * self.cell_height, 1 * self.cell_width, 1 * self.cell_height)
                        rect.setBrush(QColor(random_color))
                        self.scene.addItem(rect)
                        text_item2 = QGraphicsSimpleTextItem(str(flow_name))
                        text_item2.setPos(time * self.cell_width + 0.5, y * self.cell_height + 15)
                        text_item2.setBrush(QColor("White"))  # 设置字体颜色
                        self.scene.addItem(text_item2)
        print(f"----------")
        for link, time in collision_dict.items():
            print(f"link = {link}, time = {time}")
        print(f"{flow_name}:{random_color}")
        print('\n') 


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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = CustomGraphicsView()
    view.show()
    sys.exit(app.exec_())
