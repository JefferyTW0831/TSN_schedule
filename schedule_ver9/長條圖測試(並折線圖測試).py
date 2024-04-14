import matplotlib.pyplot as plt

def three_data_bar_chart():
    # 數據
    x = [1, 2, 3, 4, 5]
    x_offsets = [-0.2, 0, 0.2]  # 每組數據的水平偏移量
    h1 = [10, 20, 30, 40, 50]   # 第一組數據高度
    h2 = [20, 10, 40, 50, 30]   # 第二組數據高度
    h3 = [15, 25, 35, 45, 55]   # 第三組數據高度

    bar_width = 0.2  # 長條圖寬度

    # 繪製長條圖
    for i, data in enumerate([h1, h2, h3]):
        x_shifted = [pos + x_offsets[i] for pos in x]  # 計算每組數據的位置
        plt.bar(x_shifted, data, width=bar_width, align='center', label=f'Data {i+1}')

    # 添加標籤和標題
    plt.xlabel('Xlabel')
    plt.ylabel('Ylaebl')
    plt.title('three_data_plot')
    plt.xticks(x)
    plt.legend()

    # 顯示圖形
    plt.show()

def bar_and_line_chart():
    # 數據
    x = [1, 2, 3, 4, 5]
    h = [10, 20, 30, 40, 50]  # 長條圖數據
    line_data = [15, 25, 35, 45, 55]  # 折線圖數據

    # 繪製長條圖
    plt.bar(x, h, color='b', label='Bar Chart')

    # 繪製折線圖
    plt.plot(x, line_data, color='r', marker='o', linestyle='-', linewidth=2, label='Line Chart')

    # 添加標籤和標題
    plt.xlabel('X軸標籤')
    plt.ylabel('Y軸標籤')
    plt.title('長條圖與折線圖')

    # 添加圖例
    plt.legend()

    # 顯示圖形
    plt.show()

def main():
    chosen = int(input("1.三筆資料長條圖  2.長條圖&折線圖繪製"))
    if chosen == 1:
        three_data_bar_chart()
    else:
        bar_and_line_chart()

main()