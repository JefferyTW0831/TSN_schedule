import json
import os
import random


def is_valid_flow(flow):
    required_keys = ["Src", "Dst", "StartTime", "Period", "Times", "Size", "Deadline"]
    return isinstance(flow, dict) and all(key in flow for key in required_keys)   #booling
                                            #鍵名稱需要完全一致(順序也是)

def is_valid_flow_data(data):
    return all(is_valid_flow(flow) for flow in data.values()) #booling

def main():
    flow_data = rand_set_flows()
    
    if is_valid_flow_data(flow_data):
        try:
           
            with open("flow_data_manual.json", 'w') as json_file:
                json.dump(flow_data, json_file, indent=2)
            print("數據成功存成'flow_data.json'")
        except Exception as e:
            print(f"存檔失敗：{e}")
    else:
        print("數據格式有誤，無法存成json檔案")

def rand_set_flows():
    flow_data = {}
    amount = int(input("請輸入要隨機產生多少flows:"))
    
    for flow in range(1, amount+1):
        flow_data.update(rand_attribute(flow))
    return flow_data

def rand_attribute(flow):
    flow = "F" + f"{flow}"
    flow_dic = {}
    devices = ["D1", "D2", "D3", "D4", "D5", "D6", "D7"]
    src_rand = random.choice(devices)
    dst_rand = random.choice(devices)
    while dst_rand == src_rand:
        dst_rand = random.choice(devices)
        
    start_time_rand = random.randint(0, 5)    # 0, 20
    period_rand = random.randint(10, 20)      # 15, 25
    times_rand = random.randint(5, 7)         # 5, 7
    size_rand = random.randint(2, 3)          # 2, 3
    deadline_rand = random.randint(10, 15)    # 15,20
    while deadline_rand > period_rand:
        deadline_rand = random.randint(10, 15)# 15,20
    flow_dic = {flow:{"Src":src_rand, "Dst":dst_rand, "StartTime":start_time_rand, "Period":period_rand, "Times":times_rand, "Size":size_rand, "Deadline":deadline_rand}}
    return flow_dic

if __name__ == "__main__":
    main()