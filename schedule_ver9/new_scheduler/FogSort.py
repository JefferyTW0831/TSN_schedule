import random

#此方法先比Deadline取早，相同者再取Period小的，又相同者再取Pathlength短的
def sorting(flow_dict, path_dict):  
    new_flow_dict = {}
    for target_flow, data in flow_dict.items():
        new_flow_dict.update({target_flow:{"Deadline":data["Deadline"]+data["StartTime"]}})
        new_flow_dict[target_flow].update({"Period":data["Period"]})
        for flow, path in path_dict.items():
            if target_flow == flow:
                new_flow_dict[target_flow].update({"Pathlength":path})
    
   # 使用sorted函數對字典的鍵進行排序
    sorted_keys = sorted(
        new_flow_dict.keys(),
        key=lambda k: (new_flow_dict[k]['Deadline'], new_flow_dict[k]['Period'], new_flow_dict[k]['Pathlength'])
    )
   

    # 創建一個新的排序後的字典
    sorted_data = {k: new_flow_dict[k] for k in sorted_keys}

    return sorted_keys






