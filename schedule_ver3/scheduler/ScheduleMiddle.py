class ScheduleMiddle:

    def __init__(self, flow_dic, flow_paths_dic):
        self.flow_dic = flow_dic
        self.flow_paths_dic = flow_paths_dic
        
    def schedule_middle(self):                  

        common_link = self.classify_links()
        print("\n\n------------------------------")
        print(f"(ScheduleMiddle.py)\n")
        for c_link, c_list in common_link.items():
            print(f"{c_link}={c_list}")
        print("-------------------------------")

        for c_link, c_list in common_link.items():                 
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