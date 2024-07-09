import re

file_name = "20240626_process_time_Full"

pattern_greedy = r'_(.*)_(.*)_(?!.*_)'
pattern = r'_(.*?)_(.*?)_(?!.*_)'

match1 = re.search(pattern_greedy, file_name)

if match1:
    process_time = match1.group(1) + "_" + match1.group(2)
    print(f"Matched process_time: {process_time}")
else:
    print("No match found")

match2 = re.search(pattern, file_name)

if match2:
    process_time = match2.group(1) + "_" + match2.group(2)
    print(f"Matched process_time: {process_time}")
else:
    print("No match found")


## 貪婪模式
print(re.search('go*', 'goooooood').group()) ## 'gooooooo'


## 非貪婪模式
print(re.search('gooo*?', 'goooooood').group()) ## 'g'