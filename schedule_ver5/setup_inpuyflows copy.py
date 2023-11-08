import json

def is_valid_flow(flow):
    required_keys = ["Src", "Dst", "StartTime", "Period", "Times", "Size", "Deadline"]
    return isinstance(flow, dict) and all(key in flow for key in required_keys)   #booling
                                            #鍵名稱需要完全一致(順序也是)

def is_valid_flow_data(data):
    return all(is_valid_flow(flow) for flow in data.values()) #booling

# 定義數據
flow_data = {
        "F1": {
            "Src": "D1",
            "Dst": "D3",
            "StartTime": 0,
            "Period": 6,
            "Times": 9,
            "Size": 2,
            "Deadline": 6
        },
        "F2": {
            "Src": "D2",
            "Dst": "D6",
            "StartTime": 2,
            "Period": 10,
            "Times": 8,
            "Size": 2,
            "Deadline": 10
        },
        "F3": {
            "Src": "D1",
            "Dst": "D7",
            "StartTime": 4,
            "Period": 12,
            "Times": 6,
            "Size": 2,
            "Deadline": 12
        },
        "F4": {
            "Src": "D3",
            "Dst": "D2",
            "StartTime": 5,
            "Period": 9,
            "Times": 8,
            "Size": 3,
            "Deadline": 9
        },
        "F5": {
            "Src": "D3",
            "Dst": "D5",
            "StartTime": 3,
            "Period": 18,
            "Times": 5,
            "Size": 3,
            "Deadline": 18
        },
        "F6": {
            "Src": "D3",
            "Dst": "D7",
            "StartTime": 1,
            "Period": 15,
            "Times": 6,
            "Size": 3,
            "Deadline": 15
        },
        "F7": {
            "Src": "D6",
            "Dst": "D1",
            "StartTime": 0,
            "Period": 12,
            "Times": 5,
            "Size": 2,
            "Deadline": 12
        },
        "F8": {
            "Src": "D5",
            "Dst": "D3",
            "StartTime": 4,
            "Period": 8,
            "Times": 7,
            "Size": 2,
            "Deadline": 8
        },
        "F9": {
            "Src": "D6",
            "Dst": "D4",
            "StartTime": 6,
            "Period": 6,
            "Times": 8,
            "Size": 2,
            "Deadline": 6
        },
        "F10": {
            "Src": "D5",
            "Dst": "D3",
            "StartTime": 4,
            "Period": 12,
            "Times": 5,
            "Size": 3,
            "Deadline": 12
        },
        "F11": {
            "Src": "D7",
            "Dst": "D4",
            "StartTime": 2,
            "Period": 10,
            "Times": 6,
            "Size": 2,
            "Deadline": 8
        },
        "F12": {
            "Src": "D7",
            "Dst": "D6",
            "StartTime": 1,
            "Period": 12,
            "Times": 8,
            "Size": 3,
            "Deadline": 12
        }
    }

if is_valid_flow_data(flow_data):
    try:
        with open('flow_data.json', 'w') as json_file:
            json.dump(flow_data, json_file)
        print("數據成功存成'flow_data.json'")
    except Exception as e:
        print(f"存檔失敗：{e}")
else:
    print("數據格式有誤，無法存成json檔案")

