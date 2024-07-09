import new_scheduler.Genarators as Genarators
import new_scheduler.FogSort as FogSort
from new_scheduler.Timetable import TimeTable
from new_scheduler.full_schedule.RescheduleMiddle import RescheduleMiddle


class FullSchedulerReschedule:
    def __init__(self, topology, execution, driving_mode, direction, sort_mode):
        self.topology = topology
        self.flow_dic = topology.flow_dic
        self.flow_links = topology.links                        
        self.flow_paths_dic = topology.path_dic
        self.execution = execution
        self.driving_mode = driving_mode
        self.direction = direction
        self.sort_mode = sort_mode
        self.fail_flows = []
        self.time_table_maintainer = TimeTable()
        self.reschedule_middle = RescheduleMiddle(self.flow_dic, self.flow_paths_dic, self.time_table_maintainer, driving_mode, direction)
        
        
    def scheduling(self):
        self.sort_flow()
        print(f"排序結果：{self.flow_PR_sortlist}")
        #計算偏移時間(延後時間)
        timer = 0
        #包容力→Deadline/(Size*Pathlength)
        for flow in self.flow_PR_sortlist:          
            new_timer = self.resetStartTime(flow, timer)
            timer += new_timer
        
        print(f"排序方式：{self.sort_mode}")    
        return self.time_table_maintainer.time_table

    def sort_flow(self):   # this PR means deadline/path_length，越小越緊急，由小到大排列
        piority_dic = {}
        if self.sort_mode == "Our":
            for flow, path in self.flow_paths_dic.items():
                peiord = self.flow_dic[flow]["Period"] 
                piority_dic[flow] = 1/peiord
            sorted_keys = sorted(piority_dic, key=piority_dic.get)
            self.flow_PR_sortlist = sorted_keys
            
        elif self.sort_mode == "Period_per_size_based":
            for flow, path in self.flow_paths_dic.items():
                period = self.flow_dic[flow]["Period"] 
                size = self.flow_dic[flow]["Size"]
                piority_dic[flow] = period/size
        elif self.sort_mode == "JDPS_Flow_Sorting":
            for flow, path in self.flow_paths_dic.items():
                deadline_w = self.flow_dic[flow]["Deadline"]*0.6
                period_w = self.flow_dic[flow]["Period"]*0.3
                size_w = self.flow_dic[flow]["Size"]*0.1
                piority_dic[flow] = deadline_w + period_w + size_w
        elif self.sort_mode == "Period_based":
            for flow, path in self.flow_paths_dic.items():
                peiord = self.flow_dic[flow]["Period"] 
                # Weight = 原本應該是 deadline_len(path)
                piority_dic[flow] = peiord
        elif self.sort_mode == "Deadline_based":
            # for flow, path in self.flow_paths_dic.items():
            #     Deadline = self.flow_dic[flow]["Deadline"] 
            #     Start_Time = self.flow_dic[flow]["StartTime"]
            #     piority_dic[flow] = Start_Time + Deadline
            for flow, path in self.flow_paths_dic.items():
                piority_dic[flow] = len(path)
            sorted_keys = FogSort.sorting(self.flow_dic, piority_dic)
            self.flow_PR_sortlist = sorted_keys

        if self.sort_mode != "Deadline_based" and self.sort_mode != "Our":
        # 使用sorted函數，依據字典的值進行排序，並取得排序後的鍵值清單,小到大
            sorted_keys = sorted(piority_dic, key=piority_dic.get)
            self.flow_PR_sortlist = sorted_keys
  
    def gcd_weight(self):
        not_collision_group = self.find_not_collision_flows_groups()
        not_collision_group = list(set(not_collision_group))
        for flow in not_collision_group:
            if flow in self.flow_PR_sortlist:
                self.flow_PR_sortlist.remove(flow)
        self.flow_PR_sortlist[:0] = not_collision_group

    def find_not_collision_flows_groups(self):
        remaining_flows = list(self.flow_dic.keys())
        temp_dict = {}
        for flow in remaining_flows:
            first_link = self.flow_paths_dic[flow][0]
            time_list = Genarators.genarate_time_slot(flow, self.flow_dic)
            if temp_dict.get((first_link["Ingress"], first_link["Egress"])) != None:
                temp_dict[(first_link["Ingress"], first_link["Egress"])].update({flow:list(time_list.keys())})
            else:
                temp_dict.update({(first_link["Ingress"], first_link["Egress"]):{flow:list(time_list.keys())}})
        group = []
        sub_flow = []
        sub_time = []
        conflict_flag = False
        #挑選出沒衝突的組合
        for link, flow_time in temp_dict.items():
            remain_flow = list(flow_time.keys())
            while len(remain_flow) != 0:
                sub_flow = []
                sub_time = []
                sub_flow.append(remain_flow[0])
                sub_time.append(flow_time[remain_flow[0]])
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
                #僅加入有兩個元素以上的阻道group裡面               
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
                            if target_flow not in common_link_dict.keys():
                                common_link_dict.update({target_flow:1})
                            else:
                                common_link_dict[target_flow] += 1
        return common_link_dict
        
    def resetStartTime(self, flow, timer):
        not_set = True
        self.flow_dic[flow]["StartTime"] = -1
        all_link = [(link["Ingress"], link["Egress"]) for link in self.flow_paths_dic[flow]]
        firstlink = all_link[0]
        while not_set:
            self.flow_dic[flow]["StartTime"] += 1 
            timer += 1
            time_dict = Genarators.genarate_time_slot(flow, self.flow_dic)
            time_list = self.time_table_maintainer.reschedule_firstlink_to_timetable(firstlink, time_dict)
            if time_list:
                self.reschedule_middle.schedule_middle(flow, time_list)
                if self.reschedule_middle.fail_flows:
                    self.time_table_maintainer.fail_flow_refilt(self.reschedule_middle.fail_flows)
                    self.reschedule_middle.fail_flows = []
                else:
                    not_set = False
        return timer

    