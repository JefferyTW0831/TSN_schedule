import math
import copy
from collections import Counter
class Scheduler:
    def __init__(self, flow_dic, flow_links, flow_paths_dic) :
        self.flow_dic = flow_dic
        self.flow_links = flow_links                        #{F1:(D1, D3, "", 2, 8, 5, 2, 8), F2:(D1, D4, "", 3, 9, 4, 3, 8),...}
        self.flow_paths_dic = flow_paths_dic            
        self.time_table = {}                            #{(D1,D3):{}, }
        self.wait_to_schedule = []
   

    def scheduling(self):
        # print("-----------------flow_paths_dic---------------------")
        # for key, value in self.flow_paths_dic.items():
        #     print(f"key:value = {key}:{value}")
        # print("------------------------------------------------------")

        for flow, path in self.flow_paths_dic.items():    #flow = F1, path=[{'Src':'D1', 'Dst':'SW1', 'Time':[]},{},{}]
            self.genarate_first_link_time(flow, path[0])
            self.genarate_last_link_time(flow, path[-1])
        self.schedule_middle()
        # self.collision_flows()
        # print(f"path_dic = {self.flow_paths_dic}")
        print(f"path_dic = ")
        for flow, paths in self.flow_paths_dic.items():
            print(f"{flow}=")
            for path in paths:
                print(path)
        # self.put_flows_to_time_table()
    
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

    
    def schedule_middle(self):              # 未完,要符合流一定要先走到前一個路徑才能走到後一個路徑、在同一條路徑上不能有兩個flow同時佔據(這個規則好難想)
        common_link = self.classify_links()
        for c_link, c_list in common_link.items():                # F1, F2, F3   
            self.common_path_bubble_sort(c_list)
            self.genarate_active_time_slot(c_link, c_list)

    
    def common_path_bubble_sort(self, c_list):  #如何sort?  要判斷目前這條link後面還有幾個link要傳，瞭解之後取剩餘Link最多的flow優先排
        for i in range(len(c_list)-1):
            for j in range(len(c_list)-1-i):
                if len(self.flow_paths_dic[c_list[j]]) < len(self.flow_paths_dic[c_list[j+1]]):
                     c_list[j], c_list[j + 1] = c_list[j + 1], c_list[j]
   

    def genarate_active_time_slot(self, link, flow_list):
        link_time_occupy_list = []          # 用來查看link上的占用其況
        for flow in flow_list:
            prev_links_occupied = []            # 用來查看flow在先前links所占用的時間點(防止前一個Link還沒傳到 就已經出現在後一個link的情況)
            for time_filled_link in self.flow_paths_dic[flow]:
                if time_filled_link["Time"]:
                    for time in time_filled_link["Time"].keys():
                        prev_links_occupied.append(time)
            if link_time_occupy_list:
                for time in link_time_occupy_list:
                    if time not in prev_links_occupied:
                        prev_links_occupied.append(time)
            #print(f"看一下該flow目前排定的link時間的占用情況：{flow} , {prev_links_occupied}")
            for not_filled_link in self.flow_paths_dic[flow]:
                if not_filled_link["Ingress"] == link[0] and not_filled_link["Egress"] == link[1]:
                    link_time_occupy_list = self.insert_continuous_values(prev_links_occupied, self.flow_dic[flow]["Size"])
                    for time in link_time_occupy_list:
                        not_filled_link["Time"][time] = flow
            break

    def insert_continuous_values(self, sequence, continuous_length):
        sequence = sorted(sequence)
        print(f"印一下 = {sequence}")
        result_sequence = []
        i = 0
        while i < len(sequence):
            result_sequence.append(sequence[i])
            if i < len(sequence) - 1 and sequence[i + 1] - sequence[i] > 1:
                # 找到缺失的連續範圍
                for j in range(1, continuous_length + 1):
                    result_sequence.append(sequence[i] + j)
            i += 1
        result_sequence = list(set(result_sequence)-set(sequence))
        return result_sequence

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
        print(f"common_link = {common_link}")
        return common_link


    # def schedule_middle_2(self):
    #     previous_path = {}
    #     for flow_name, flow_path in self.flow_paths_dic.items():
    #         for link in flow_path:
    #             if not link.get('Time') :
    #                 time_list = self.genarate_active_time_slot(previous_path, flow_name, self.flow_dic[flow_name]["Size"])
    #                 link["Time"] = time_list
    #             previous_path = link
    #         if self.check_self_constraints(link) == False:
    #             self.wait_to_schedule.append(flow_name)
          

    # def genarate_active_time_slot(self, prev_path, flow, bias):
    #     time_list = {}
    #     start =  min(prev_path["Time"].keys())+bias
    #     period = self.flow_dic[flow]["Period"]
    #     times = self.flow_dic[flow]["Times"]
    #     size = self.flow_dic[flow]["Size"]
    #     current_time = start
    #     for _ in range(times):
    #         for _ in range(size):
    #             time_list[current_time] = flow
    #             current_time += 1
    #         current_time += period - size
    #     return time_list
    
    # def check_self_constraints(self, paths):
    #     time_dict_list = [dic.get("Time", {}) for dic in paths]
    #     key_counts = Counter(key for time_dict in time_dict_list for key in time_dict)
    #     duplicate_keys = [key for key, count in key_counts.items() if count > 1]
    #     if duplicate_keys:
    #         return False
    #     else:
    #         return True
        
    # def collision_flows(self):
    #     path_manager = {}
    #     for link_path, link_values in self.flow_links.items():  #(D1, SW1) =  {}
    #         for path_flow, path_paths in self.flow_paths_dic.items(): 
    #             for path in path_paths: #list = [{"Ingress":"D1", "Egress":"SW1", "Time":{}}, ...]
    #                 if link_path[0] == path["Ingress"] and link_path[1] == path["Egress"]:
    #                     path_manager.update(path)
                

        


    # def put_flows_to_time_table(self):
    #     wait_flag = False
    #     self.wait_to_schedule = []
    #     for flow, paths in self.flow_paths_dic.items():     # paths = Path_list = [{},{},{}], {'Src', 'Dst', 'Time'}
    #         for path in paths:
                
    #             #如果沒有此link
    #             if self.time_table.get((path['Ingress'], path['Egress'])) == None:  
    #                 #新link，添加到時間表裡面
    #                 self.time_table[(path['Ingress'], path['Egress'])] = copy.deepcopy(path['Time'])
    #             #如果有此link
    #             else:
    #                 #比對time，查看是否有發生碰撞
    #                 all_common = set(path['Time'].items()) & set(self.time_table[(path['Ingress'], path['Egress'])].items()) 
    #                 common_time_slot = set(path['Time'].keys()) & set(self.time_table[(path['Ingress'], path['Egress'])].keys())
    #                 if all_common :
    #                     pass 
    #                 elif common_time_slot or wait_flag == True:
    #                     #發生碰撞，將此path先放到等待陣列
    #                     wait_flag = True
    #                 else:
    #                     self.time_table[(path['Ingress'], path['Egress'])].update(path['Time']) 
    #         if wait_flag == True:
    #                 wait_flag = False
    #                 self.wait_to_schedule.append(flow)    

    #     print(f"time_table = ")
    #     for (src, dst), time in self.time_table.items():
    #         print(f"{(src, dst)}:{time}")
    #     print(f"wait_to_schedule = {self.wait_to_schedule}")
    #     print(f"----------------------------------------------------------------")

            
       
            
