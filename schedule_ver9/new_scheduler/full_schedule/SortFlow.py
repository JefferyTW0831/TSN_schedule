import new_scheduler.FogSort as FogSort
import new_scheduler.Genarators as Genarators

class SortFlow:
    def __init__(self, flow_dic, flow_paths_dic, time_table_maintainer, driving_mode, sort_mode, direction):
        self.flow_dic = flow_dic
        self.flow_paths_dic = flow_paths_dic
        self.time_table_maintainer = time_table_maintainer
        self.flow_PR_sortlist = None
        self.driving_mode = driving_mode
        self.sort_mode = sort_mode
        self.direction = direction
   
    def sort_flows(self): # this PR means deadline/path_length，越小越緊急，由小到大排列
        piority_dic = {}
        if self.sort_mode == "NCB":
            for flow, path in self.flow_paths_dic.items():
                peiord = self.flow_dic[flow]["Period"] 
                piority_dic[flow] = len(path)/peiord
            sorted_keys = sorted(piority_dic, key=piority_dic.get)
            self.flow_PR_sortlist = sorted_keys

            
        elif self.sort_mode == "STB":
            for flow, path in self.flow_paths_dic.items():
                period = self.flow_dic[flow]["Period"] 
                size = self.flow_dic[flow]["Size"]
                start_time = self.flow_dic[flow]["StartTime"]
                piority_dic[flow] = start_time

        elif self.sort_mode == "JDPS":
            for flow, path in self.flow_paths_dic.items():
                deadline_w = self.flow_dic[flow]["Deadline"]*0.6
                period_w = self.flow_dic[flow]["Period"]*0.3
                size_w = self.flow_dic[flow]["Size"]*0.1
                piority_dic[flow] = deadline_w + period_w + size_w

        elif self.sort_mode == "PB":
            for flow, path in self.flow_paths_dic.items():
                peiord = self.flow_dic[flow]["Period"] 
                # Weight = 原本應該是 deadline_len(path)
                piority_dic[flow] = peiord

        elif self.sort_mode == "FS":
            # for flow, path in self.flow_paths_dic.items():
            #     Deadline = self.flow_dic[flow]["Deadline"] 
            #     Start_Time = self.flow_dic[flow]["StartTime"]
            #     piority_dic[flow] = Start_Time + Deadline
            for flow, path in self.flow_paths_dic.items():
                piority_dic[flow] = len(path)
            sorted_keys = FogSort.sorting(self.flow_dic, piority_dic)
            self.flow_PR_sortlist = sorted_keys

        if self.sort_mode != "FS" and self.sort_mode != "NCB":
        # 使用sorted函數，依據字典的值進行排序，並取得排序後的鍵值清單,小到大
            sorted_keys = sorted(piority_dic, key=piority_dic.get)
            self.flow_PR_sortlist = sorted_keys
     

    def gcd_weight(self):
        not_collision_group = self.find_not_collision_flows_groups()
        print(f"無衝突組合 = {not_collision_group}")
        #取group最大尺寸
        max_group_size = 0
        new_group_list = []
        for group in not_collision_group:
            if len(group)>max_group_size:
                max_group_size = len(group)

        for group_size in range(max_group_size, 1, -1):
            for group in not_collision_group:
                if len(group) == group_size:
                    new_group_list.append(group) 
        group_sorted = sorted(new_group_list, key=lambda x: len(x), reverse=True)
        remaining_elements = [element for element in self.flow_PR_sortlist if element not in sum(group_sorted, [])]
        finished_grouped_list = group_sorted + [[element] for element in remaining_elements]
        fainal_list = []
        for inner_list in finished_grouped_list:
            for flow in inner_list:
                fainal_list.append(flow)
        self.flow_PR_sortlist = fainal_list

    def find_not_collision_flows_groups(self):
        remaining_flows = self.flow_PR_sortlist
        temp_dict = {}
        for flow in remaining_flows:
            first_link = self.flow_paths_dic[flow][0]
            time_list = Genarators.genarate_time_slot(flow, self.flow_dic)
            print(f"{flow} = {time_list.keys()}")
            if temp_dict.get((first_link["Ingress"], first_link["Egress"])) != None:
                temp_dict[(first_link["Ingress"], first_link["Egress"])].update({flow:list(time_list.keys())})
            else:
                temp_dict.update({(first_link["Ingress"], first_link["Egress"]):{flow:list(time_list.keys())}})
        # for link, flows in temp_dict.items():
        #     print(link)
        #     print(flows)
        group = []
        conflict_flag = False
        #挑選出沒衝突的組合
        for link, flow_time in temp_dict.items():
            remain_flow = list(flow_time.keys())
            while len(remain_flow) != 0:
                sub_flow = []
                sub_time = []
                #處理第一個flow
                sub_flow.append(remain_flow[0])
                #處理第一個flow的time_list
                for time in flow_time[remain_flow[0]]:
                    sub_time.append(time)
                remain_flow.pop(0)   
                for flow in remain_flow:
                    for num in flow_time[flow]:
                        if num in sub_time:
                            conflict_flag = True
                    #若無衝突發生    
                    if conflict_flag == False:
                        sub_flow.append(flow) 
                        for num in flow_time[flow]:
                            sub_time.append(num)
                    #若有衝突發生，不處理
                    else:
                        conflict_flag = False
                #僅加入有兩個元素以上的組到group裡面               
                if len(sub_flow) >1:
                    group.append([])
                    for inner_flow in sub_flow:
                        group[-1].append(inner_flow)
                        
                sub_flow.pop(0)
                
                while len(sub_flow) > 0:
                    remain_flow.remove(sub_flow[0])
                    sub_flow.pop(0)

        return group  
    
    def common_link(self):
        common_link_dict = self.count_common_link()
        sorted_data = sorted(common_link_dict.items(), key=lambda x: x[1])
        new_flow_PR_sortlist = []
        for (flow, count) in sorted_data:
            new_flow_PR_sortlist.append(flow)
        self.flow_PR_sortlist = new_flow_PR_sortlist

        # #顯示common link數量
        # for flow, count in common_link_dict.items():
        #     print(f"{flow} = {count}")
        
    def count_common_link(self):
        common_link_dict = {}
        #先選從當前目標flow開始
        for target_flow in self.flow_PR_sortlist:
            #找到當前目標flow的鏈結
            for target_link_dict in self.flow_paths_dic[target_flow][1:-1]:   
                #對於所有flow的所有路徑搜尋
                for flow, path_dict in self.flow_paths_dic.items():
                    #搜尋路徑中每個鏈結
                    for link_dict in path_dict:
                        #如果找到目標鏈結
                        if target_link_dict == link_dict and target_flow != flow:
                            #印出conflict_links
                            #print(target_flow, flow, target_link_dict)
                            if target_flow not in common_link_dict.keys():
                                common_link_dict.update({target_flow:1})
                            else:
                                common_link_dict[target_flow] += 1
        add_flow = {}
        for flow in self.flow_paths_dic.keys():
            if flow not in common_link_dict.keys():
                add_flow[flow] = 0
        for flow, common_link in add_flow.items():
            common_link_dict.update({flow:common_link})
            
        return common_link_dict