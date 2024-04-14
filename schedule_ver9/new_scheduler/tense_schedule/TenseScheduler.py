import math
import copy
from .InitFlowFilter import InitFlowFilter
from .ScheduleMiddle import ScheduleMiddle
from new_scheduler.Timetable import TimeTable

class TenseScheduler:
    def __init__(self, topology, execution, driving_mode, direction, sort_mode) :
        self.flow_dic = topology.flow_dic
        self.flow_links = topology.links                        
        self.flow_paths_dic = topology.path_dic
        self.execution = execution
        self.driving_mode = driving_mode
        self.sort_mode = sort_mode
        self.direction = direction
        self.fail_flows = []
        self.time_table_maintainer = TimeTable() 
        self.init_flows = InitFlowFilter(self.flow_dic ,self.flow_paths_dic, self.time_table_maintainer, self.sort_mode)           
        self.schedule_middle = ScheduleMiddle(self.flow_dic, self.flow_paths_dic, self.time_table_maintainer, self.driving_mode, self.direction)
        self.flow_PR_sortlist = []           
    
    def scheduling(self):
        print("------------------------------")
        self.sort_flow()
        #將有相同first_Link的flows依據path從小排到大，發生衝突時path較小的可優先被挑選

        if self.sort_mode == 1:
            original_sortlist = list(self.flow_dic.keys())
            self.init_flows.init_flows_filter(original_sortlist)
        else:
            self.init_flows.init_flows_filter(self.flow_PR_sortlist)

        if self.time_table_maintainer.init_fail_flows:
            print(f"init_fail_flows_occur{self.time_table_maintainer.init_fail_flows}")
            for flow in self.time_table_maintainer.init_fail_flows:
                self.fail_flows.append(flow)



        if self.driving_mode == "Original":
            original_sortlist = list(self.flow_dic.keys())
            self.schedule_middle.schedule_middle(original_sortlist)
        else:
            self.schedule_middle.schedule_middle(self.flow_PR_sortlist)

        if self.time_table_maintainer.middle_fail_flows:
            print(f"middle_fail_flows_occur:{self.time_table_maintainer.middle_fail_flows}")
            self.time_table_maintainer.fail_flow_refilt(self.time_table_maintainer.middle_fail_flows)   
            for flow in self.time_table_maintainer.middle_fail_flows:
                self.fail_flows.append(flow)

        
        result_list = [key for key in self.flow_paths_dic if key not in self.fail_flows]
        print("\n結果:")
        print(f"scheduled flows =  {result_list}, total : {len(result_list)} flows")
        print(f"fail flows = {self.fail_flows}")
        print(f"-----------------------------------------------\n\n")

        if self.execution == "RunData":
        #傳scheudle_flow回去 (全部執行)
           return (result_list)
        else:
        #----把時間表回傳給主程式，讓Demo顯示時間表----
            return self.time_table_maintainer.time_table

    def sort_flow(self):   # this PR means deadline/path_length，越小越緊急，由小到大排列
        piority_dic = {}
        for flow, path in self.flow_paths_dic.items():
            deadline = self.flow_dic[flow]["Deadline"] 
            piority_dic[flow] = deadline/len(path)

        # 使用sorted函數，依據字典的值進行排序，並取得排序後的鍵值清單
        sorted_keys = sorted(piority_dic, key=piority_dic.get)
        
        self.flow_PR_sortlist = sorted_keys
        print(f"這裡顯示這裡顯示類別：{self.flow_PR_sortlist}")

             


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
        for target_flow in self.flow_dic.keys():
            #找到當前目標flow的鏈結
            for target_link_dict in self.flow_paths_dic[target_flow]:
                #對於所有flow的所有路徑搜尋
                for flow, path_dict in self.flow_paths_dic.items():
                    #搜尋路徑中每個鏈結
                    for link_dict in path_dict:
                        #如果找到目標鏈結
                        if target_link_dict == link_dict:
                            if target_flow not in common_link_dict.keys():
                                common_link_dict.update({target_flow:1})
                            else:
                                common_link_dict[target_flow] += 1
        return common_link_dict


                        
                    
                


        


    