my_dict = {'a': [1,2,3,4,5], 'b': [6,7,7,8,9], 'c': [10,11,12,13,14], 'd': 4}

# 获取字典的迭代器
iter_dict = iter(my_dict.items())

# 跳过第一个键值对
name, num = next(iter_dict)
print(name, num)

print(len(my_dict))

# 迭代剩余的键值对
for key, value in iter_dict:
    print(key, value)