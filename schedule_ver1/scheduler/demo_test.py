import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsLineItem, QGraphicsSimpleTextItem, QGraphicsRectItem
from PyQt5.QtGui import QPen, QColor

class CustomGraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()

        # 设置场景
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # 设置网格参数
        self.grid_size_x = 100
        self.grid_size_y = 11
        self.cell_width = 30
        self.cell_height = 30

        # 设置颜色
        self.grid_line_color = QColor("black")
        self.cell_background_color = QColor("lightgray")

        # 绘制网格
        self.draw_grid()

    def draw_grid(self):
        # 绘制水平线
        for i in range(self.grid_size_y + 1):
            line = QGraphicsLineItem(0, i * self.cell_height, self.grid_size_x * self.cell_width, i * self.cell_height)
            pen = QPen(self.grid_line_color)
            line.setPen(pen)
            self.scene.addItem(line)

        # 绘制垂直线
        for i in range(self.grid_size_x + 1):
            line = QGraphicsLineItem(i * self.cell_width, 0, i * self.cell_width, self.grid_size_y * self.cell_height)
            pen = QPen(self.grid_line_color)
            line.setPen(pen)
            self.scene.addItem(line)

        # 添加文字标签
        for i in range(self.grid_size_y):
            text_item = QGraphicsSimpleTextItem(str(f"Line{i}"))
            text_item.setPos(-40, i * self.cell_height + 10)
            self.scene.addItem(text_item)

        for i in range(self.grid_size_x + 1):
            text_item = QGraphicsSimpleTextItem(str(i))
            text_item.setPos(i * self.cell_width + 10, -15)
            self.scene.addItem(text_item)

        # 设置单元格背景颜色
        for i in range(self.grid_size_y):
            for j in range(self.grid_size_x):
                rect = self.scene.addRect(j * self.cell_width, i * self.cell_height, self.cell_width, self.cell_height)
                rect.setBrush(self.cell_background_color)

    def update_graphics_from_dict(self, data_dict):
    
        for rect_info in data_dict.get("rectangles", []):
            x = rect_info.get("x", 0)
            y = rect_info.get("y", 0)
            width = rect_info.get("width", 1)
            height = rect_info.get("height", 1)

            rect = QGraphicsRectItem(x * self.cell_width, y * self.cell_height, width * self.cell_width, height * self.cell_height)
            rect.setBrush(QColor(rect_info.get("color", "blue")))
            self.scene.addItem(rect)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = CustomGraphicsView()
    view.show()

    data_dict = {
        "rectangles": [
            {"x": 2, "y": 2, "width": 3, "height": 2, "color": "red"},
            {"x": 5, "y": 5, "width": 2, "height": 3, "color": "green"},
        ]
    }

    view.update_graphics_from_dict(data_dict)

    sys.exit(app.exec_())
