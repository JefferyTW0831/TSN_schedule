import matplotlib.pyplot as plt

class ResourceUsagePlot:
    def __init__(self, num_links):
        self.num_links = num_links
    
    def draw_grid_lines(self, ax):
        #畫16條線
        for row in range(self.num_links + 1):                   
            ax.axhline(y=row, color='black', linewidth=2)
        #畫16條線
        for col in range(self.num_links + 1):                   
            ax.axvline(x=col, color='black', linewidth=2)

    def plot_resource_usage_top_row(self):
        fig, ax = plt.subplots()

        self.draw_grid_lines(ax)
        
        # 繪製位於第一列的藍色矩形，其中 row = 14 的矩形會被上色
        for row in range(self.num_links):
            color = 'blue' if row == 14 else 'white'
            ax.add_patch(plt.Rectangle((0, row), 1, 1, color=color))

        # 設定 x 和 y 軸的刻度    
        ax.set_xticks(range(self.num_links))
        ax.set_yticks(range(self.num_links))
        
        # 設定 x 軸刻度標籤，並進行旋轉和對齊
        ax.set_xticklabels([f'Time {i+1}' for i in range(self.num_links)], rotation=45, ha='center')
        ax.set_yticklabels([f'Link {i}' for i in range(self.num_links, 0, -1)], va='center')

        ax.set_xlim(0, self.num_links)
        ax.set_ylim(0, self.num_links)
        #默認情況下，Matplotlib 的坐標軸縱橫比是 "auto"，這意味著 Matplotlib 會根據圖形的數據範圍和繪圖區域的尺寸自動調整縱橫比。
        #使用ax.set_aspect('equal') 來保持縱橫比為 1，從而確保在繪製時不會有形狀的變形。總之，ax.set_aspect() 方法可以根據您的需求設定坐標軸的縱橫比，以確保繪製的圖形在輸出時保持正確的形狀。
        ax.set_aspect('equal') 

        ax.set_xlabel('Time')
        ax.set_ylabel('Links')
        
        ax.set_title('Resource Usage')

        plt.tight_layout()
        plt.show()


resource_plot = ResourceUsagePlot(num_links=15)                 #創建XY各15個格子
resource_plot.plot_resource_usage_top_row()
