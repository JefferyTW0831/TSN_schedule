import matplotlib.pyplot as plt

def plot_four_subplots():
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))  # 2x2的子圖表

    # 第一張子圖表
    ax = axs[0, 0]
    plot_data(ax, 1)

    # 第二張子圖表
    ax = axs[0, 1]
    plot_data(ax, 2)

    # 第三張子圖表
    ax = axs[1, 0]
    plot_data(ax, 3)

    # 第四張子圖表
    ax = axs[1, 1]
    plot_data(ax, 4)

    plt.tight_layout()  # 調整子圖的間距
    plt.show()

def plot_data(ax, plot_number):
    x = [1, 2, 3, 4, 5]
    data1 = [10, 20, 30, 40, 50]
    data2 = [20, 15, 25, 35, 45]
    data3 = [15, 25, 35, 30, 40]

    # 繪製長條圖
    ax.bar(x, data1, color='b', label='Data 1')
    ax.bar(x, data2, color='g', label='Data 2', bottom=data1)
    ax.bar(x, data3, color='r', label='Data 3', bottom=[data1[i] + data2[i] for i in range(len(data1))])

    # 添加標籤和標題
    ax.set_xlabel('X軸標籤')
    ax.set_ylabel('Y軸標籤')
    ax.set_title(f'Plot {plot_number}')

    # 添加圖例
    ax.legend()

plot_four_subplots()