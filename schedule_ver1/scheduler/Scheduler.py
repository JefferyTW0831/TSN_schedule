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

    def schedule_middle(self):#  未完,要符合流一定要先走到前一個路徑才能走到後一個路徑、在同一條路徑上不能有兩個flow同時佔據(這個規則好難想)
        time_occupy_list = []
        common_link = self.classify_links()
        for c_link, c_list in common_link.items():
            for flow in c_list:                    #F1, F2, F3            
                for flow_name, flow_path in self.flow_paths_dic:
                    for link in flow_path:         #link = {"Ingress", "Egress", "Time"}
                        if c_link[0] == link["Ingress"] and c_link[1] == link["Egress"]:
                            time_occupy_list = self.genarate_time_slot(self, flow, time_occupy_list)

    def genarate_time_slot(self, flow, time_occupy_list):
        






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






    def schedule_middle_2(self):
        previous_path = {}
        for flow_name, flow_path in self.flow_paths_dic.items():
            for link in flow_path:
                if not link.get('Time') :
                    time_list = self.genarate_active_time_slot(previous_path, flow_name, self.flow_dic[flow_name]["Size"])
                    link["Time"] = time_list
                previous_path = link
            if self.check_self_constraints(link) == False:
                self.wait_to_schedule.append(flow_name)
          

    def genarate_active_time_slot(self, prev_path, flow, bias):
        time_list = {}
        start =  min(prev_path["Time"].keys())+bias
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
    
    def check_self_constraints(self, paths):
        time_dict_list = [dic.get("Time", {}) for dic in paths]
        key_counts = Counter(key for time_dict in time_dict_list for key in time_dict)
        duplicate_keys = [key for key, count in key_counts.items() if count > 1]
        if duplicate_keys:
            return False
        else:
            return True
        
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

            
       
            
