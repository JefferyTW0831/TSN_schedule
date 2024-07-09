
def count_missing_numbers_in_range(numbers, start, end):
    # 生成範圍內的所有數字集合
    full_set = set(range(start, end + 1))
    
    # 將數字清單轉換為集合
    number_set = set(numbers)
    
    # 計算範圍內缺失的數字集合
    missing_numbers = full_set - number_set
    
    # 返回缺失數字的個數
    return len(missing_numbers)

# 示例用法
numbers = [1, 2, 3, 7, 9]
start = 3
end = 8
print(count_missing_numbers_in_range(numbers, start, end))  # 輸出: 3