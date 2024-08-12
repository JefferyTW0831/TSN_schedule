# -*- coding: utf-8 -*-
import random


def main():
    data = {
    "F2": {"Deadline": 10, "Period": 15, "Pathlength": 4},
    "F4": {"Deadline": 10, "Period": 12, "Pathlength": 3},
    "F5": {"Deadline": 12, "Period": 15, "Pathlength": 4},    
    "F1": {"Deadline": 12, "Period": 18, "Pathlength": 4}, 
    "F3": {"Deadline": 10, "Period": 15, "Pathlength": 3},
    
    }

    # 使用sorted函數對字典的鍵進行排序
    sorted_keys = sorted(
        data.keys(),
        key=lambda k: (data[k]['Deadline'], data[k]['Period'], data[k]['Pathlength'])
    )

    # 創建一個新的排序後的字典
    sorted_data = {k: data[k] for k in sorted_keys}
    custom_sort(sorted_data)

# 打印結果
def custom_sort(sorted_data):
    print(sorted_data)

main()