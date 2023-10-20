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
        # print("-----------------flow_paths_dic---------------------")
        # for key, value in self.flow_paths_dic.items():
        #     print(f"key:value = {key}:{value}")
        # print("------------------------------------------------------")
        self.init_flows_filter()
        
        for flow, path in self.flow_paths_dic.items():    #flow = F1, path=[{'Src':'D1', 'Dst':'SW1', 'Time':[]},{},{}]
            self.genarate_first_link_time(flow, path[0])
            #self.genarate_last_link_time(flow, path[-1])
        self.schedule_middle()
        # self.collision_flows()
        # print(f"path_dic = {self.flow_paths_dic}")
        print(f"path_dic = ")
        for flow, paths in self.flow_paths_dic.items():
            print(f"{flow}=")
            for path in paths:
                print(path)
        return self.flow_paths_dic
        # self.put_flows_to_time_table()
    def init_flows_filter(self):
        mentain_time_dict = {}
        for flow, path in self.flow_paths_dic.items():    
            time_list = self.genarate_first_link_time_EX(flow, path[0])
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
            self.flow_paths_dic.pop(flow, None)
    
    def genarate_first_link_time_EX(self, flow, first_link):
        time_list = self.genarate_time_slot_EX(flow, 0)

        return time_list

    def genarate_time_slot_EX(self, flow, bias):
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
    
    def genarate_first_link_time(self, flow, path):
        path["Time"] = self.genarate_time_slot(flow, 0)

    def genarate_last_link_time(self, flow, path):
        path["Time"] = self.genarate_time_slot(flow, -self.flow_dic[flow]["Size"])

    def genarate_time_slot(self, flow, bias):
        time_list = {}
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
                time_list[current_time] = flow
                current_time += 1
            current_time += period - size
        return time_list

    
    def schedule_middle(self):              # 未完,要符合流一定要先走到前一個路徑才能走到後一個路徑、在同一條路徑上不能有兩個flow同時佔據
        common_link = self.classify_links()
        for c_link, c_list in common_link.items():                # F1, F2, F3   
            self.common_path_bubble_sort(c_list)
            self.genarate_active_time_slot(c_link, c_list)
            
    def classify_links(self):
        common_link = {}
        for flow_name, flow_path in self.flow_paths_dic.items():
            for link in flow_path:
                if not link.get('Time'):
                    key = (link["Ingress"], link["Egress"])
                    if key not in common_link:
                        common_link[(link["Ingress"], link["Egress"])] = []
                        common_link[(link["Ingress"], link["Egress"])].append(flow_name)
                    else:
                        common_link[(link["Ingress"], link["Egress"])].append(flow_name)
    
        return common_link

    
    def common_path_bubble_sort(self, c_list):  #如何sort?  要判斷目前這條link後面還有幾個link要傳，瞭解之後取剩餘Link最多的flow優先排
        for i in range(len(c_list)-1):
            for j in range(len(c_list)-1-i):
                if len(self.flow_paths_dic[c_list[j]]) < len(self.flow_paths_dic[c_list[j+1]]):
                     c_list[j], c_list[j + 1] = c_list[j + 1], c_list[j]
   

    def genarate_active_time_slot(self, link, flow_list):
        
        link_time_occupy_list = []              # 用來查看link上的占用其況
        for flow in flow_list:
            #取得衝突時間資訊(將結合link_time_occupy_list到prev_links_occupied以利同時檢查衝突)
            prev_links_occupied = []            # 用來查看flow在先前links所占用的時間點(防止前一個Link還沒傳到 就已經出現在後一個link的情況)
            for time_filled_link in self.flow_paths_dic[flow]:
                if time_filled_link["Time"]:
                    for time in time_filled_link["Time"].keys():
                        prev_links_occupied.append(time)
            if link_time_occupy_list:           #查看有沒有其他flow已經占用某些時間點，如果有的話也要加入prev_links_occupied來同時檢查衝突問題
                for time in link_time_occupy_list:
                    if time not in prev_links_occupied:
                        prev_links_occupied.append(time)
           
            for not_filled_link in self.flow_paths_dic[flow]:
                if not_filled_link["Ingress"] == link[0] and not_filled_link["Egress"] == link[1]:
                    print(f"flow = {flow}, link = {not_filled_link}")
                    insert_list = (self.insert_continuous_values(prev_links_occupied, self.flow_dic[flow]["Size"]))
                    for time in insert_list:
                        link_time_occupy_list.append(time)
                        not_filled_link["Time"][time] = flow
                    not_filled_link["Time"] = dict(sorted(not_filled_link["Time"].items()))
 
    def insert_continuous_values(self, sequence, continuous_length):    
        occupied_time_slot = sorted(sequence)
        result_sequence = []
      
        i = 0
        while i < len(occupied_time_slot):                                                  #這邊判斷的地方不能用 len(occupied_time_slot)
            result_sequence.append(occupied_time_slot[i])
            if i < len(occupied_time_slot) - 1 and occupied_time_slot[i + 1] - occupied_time_slot[i] > 1:
                # 找到缺失的連續範圍
                for j in range(1, continuous_length + 1):
                    result_sequence.append(occupied_time_slot[i] + j)
            i += 1
        result_sequence = list(set(result_sequence)-set(occupied_time_slot))
        return result_sequence


   