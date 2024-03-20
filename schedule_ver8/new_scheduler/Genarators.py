def get_max_time(flow_dic):
    max_value = None
    for flow, data in flow_dic.items():
        flow_deadline_time = data["StartTime"]+data["Period"]*(data["Times"]-1)+data["Deadline"]
        if max_value == None or flow_deadline_time > max_value:
            max_value = flow_deadline_time
            max_flow = flow
    print(f"Last_flow: {max_flow} , Max_time: {max_value}")
    return max_value
    
#加入時間
#Flow = 名稱, Packet = 封包編號, piority = 最大容忍時間/路徑長度(結果越小優先)
def genarate_time_slot(flow, flow_dic):
    time_list = {}
    start = flow_dic[flow]["StartTime"]
    period = flow_dic[flow]["Period"]
    times = flow_dic[flow]["Times"]
    size = flow_dic[flow]["Size"]
    e2e = flow_dic[flow]["Deadline"]
    current_time = start
    for instance in range(times):
        for packet_num in range(size):
            time_list[current_time] = {"Flow":flow, "StartTime":current_time,  "Packet":packet_num, "Tolerant":current_time-size+1+e2e}
            current_time += 1
        current_time += period - size
    return time_list