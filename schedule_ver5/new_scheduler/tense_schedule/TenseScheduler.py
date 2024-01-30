import math
import copy
from .InitFlowFilter import InitFlowFilter
from .ScheduleMiddle import ScheduleMiddle
from new_scheduler.Timetable import TimeTable

class TenseScheduler:
    def __init__(self, topology, execution, driving_mode, direction) :
        self.flow_dic = topology.flow_dic
        self.flow_links = topology.links                        
        self.flow_paths_dic = topology.path_dic
        self.execution = execution
        self.driving_mode = driving_mode
        self.direction = direction
        self.fail_flows = []
        self.time_table_maintainer = TimeTable() 
        self.flow_PR_sortlist = []           
    
    def scheduling(self):
        print("------------------------------")
      
        self.sort_flow()
        #將有相同first_Link的flows依據path從小排到大，發生衝突時path較小的可優先被挑選
        init_flows = InitFlowFilter(self.flow_dic ,self.flow_paths_dic, self.time_table_maintainer, self.driving_mode)           
        init_flows.init_flows_filter(self.flow_PR_sortlist)
        if self.time_table_maintainer.init_fail_flows:
            print(f"init_fail_flows_occur{self.time_table_maintainer.init_fail_flows}")
            for flow in self.time_table_maintainer.init_fail_flows:
                self.fail_flows.append(flow)

       
        schedule_middle = ScheduleMiddle(self.flow_dic, self.flow_paths_dic, self.time_table_maintainer, self.driving_mode, self.direction)
        schedule_middle.schedule_middle(self.flow_PR_sortlist)
        if self.time_table_maintainer.middle_fail_flows:
            print(f"middle_fail_flows_occur:{self.time_table_maintainer.middle_fail_flows}")
            self.time_table_maintainer.fail_flow_refilt(self.time_table_maintainer.middle_fail_flows)   
            for flow in self.time_table_maintainer.middle_fail_flows:
                self.fail_flows.append(flow)

        success_flows = len(self.flow_paths_dic)-len(self.fail_flows)
        result_list = [key for key in self.flow_paths_dic if key not in self.fail_flows]
        print(f"scheduled flows =  {result_list}, total : {success_flows} flows")
        
        if self.execution == 1:
        #傳scheudle_flow回去 (全部執行)
           return (result_list, success_flows)
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
        # for key in sorted_keys:
        #     print(f"{key}:{piority_dic[key]}")
        self.flow_PR_sortlist = sorted_keys
        


    