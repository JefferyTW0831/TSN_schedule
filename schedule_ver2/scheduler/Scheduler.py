import math
import copy

class Scheduler:
    def __init__(self, flow_dic, flow_links, flow_paths_dic) :
        self.flow_dic = flow_dic
        self.flow_links = flow_links                        #{F1:(D1, D3, "", 2, 8, 5, 2, 8), F2:(D1, D4, "", 3, 9, 4, 3, 8),...}
        self.flow_paths_dic = flow_paths_dic            
        self.remove_flows = []
        self.remaining_flows = []
        self.schedulable_flows = {}

        self.time_table = {}
       
    def scheduling(self):
        self.schedulable_flows = self.init_flows_filter()
        for flow, data in self.schedulable_flows.items():
            for links in self.flow_paths_dic[flow]:
                if links["Ingress"] == data["Link"]["Ingress"] and links["Egress"] == data["Link"]["Egress"]:   
                    print(f"可排程之flows = {flow}:{data}")
                    for time in data["Time"]:
                        if self.time_table.get(time) == None:
                            self.time_table[time] = {}
                        if self.time_table[time].get((data["Link"]["Ingress"], data["Link"]["Egress"])) == None:
                            self.time_table[time][(data["Link"]["Ingress"], data["Link"]["Egress"])] = flow
                    continue
                else:                                           #還在想要怎麼處理....依照前一個link生成一串數字並塞進去，但是這樣就寫法一樣了
                    pass
        for time, data in self.time_table.items():
            print(f"{time}:{data}")

    def init_flows_filter(self):
        mentain_time_dict = {}
        for flow, path in self.flow_paths_dic.items():    
            time_list = self.genarate_first_link_time(flow, path[0])
            mentain_time_dict[flow] = {"Link":path[0], "Time":time_list, "PathSize":len(path)}                  #data_struct
        
        for i, (flow1, data1) in enumerate(mentain_time_dict.items()):
            for flow2, data2 in list(mentain_time_dict.items())[i+1:]:
                if data1['Link'] == data2['Link'] and bool(set(data1['Time']) & set(data2['Time'])):
                    if flow1 not in self.remove_flows: 
                        if data1["PathSize"] > data2["PathSize"]:
                            if flow1 not in self.remove_flows:
                                self.remove_flows.append(flow1)
                        else:
                            if flow2 not in self.remove_flows:
                                self.remove_flows.append(flow2)

        for flow in self.remove_flows:
            mentain_time_dict.pop(flow, None)
        
        self.remaining_flows = list(mentain_time_dict.keys())

        return mentain_time_dict

    def genarate_first_link_time(self, flow, first_link):
        time_list = self.genarate_time_slot(flow, 0)

        return time_list

    def genarate_time_slot(self, flow, bias):
        time_list = []
        if bias == 0:
            start = self.flow_dic[flow]["StartTime"]
        else:
            start = self.flow_dic[flow]["StartTime"]+self.flow_dic[flow]["Period"]+bias
        period = self.flow_dic[flow]["Period"]
        times = self.flow_dic[flow]["Times"]
        size = self.flow_dic[flow]["Size"]
        current_time = start
        for _ in range(times):
            for _ in range(size):
                time_list.append(current_time)
                current_time += 1
            current_time += period - size
        return time_list

 