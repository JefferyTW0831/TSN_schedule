import math
import copy
from .InitFlowFilter import InitFlowFilter
from .ScheduleMiddle import ScheduleMiddle
from scheduler.Timetable import TimeTable

class Scheduler:
    def __init__(self, flow_dic, flow_links, flow_paths_dic) :
        self.flow_dic = flow_dic
        self.flow_links = flow_links                        
        self.flow_paths_dic = flow_paths_dic
        self.fail_flows = []
        self.time_table_maintainer = TimeTable() 
        self.flow_PR_sortlist = []           
   
    def scheduling(self):
        print("\n\n------------------------------")
        print(f"(Scheduler2.py)\n")

        self.sort_flow()
        #將有相同first_Link的flows依據path從小排到大，發生衝突時path較小的可優先被挑選
        init_flows = InitFlowFilter(self.flow_dic ,self.flow_paths_dic, self.time_table_maintainer)           
        init_flows.init_flows_filter(self.flow_PR_sortlist)
        self.fail_flows = self.time_table_maintainer.fail_flows
       
  
        schedule_middle = ScheduleMiddle(self.flow_dic, self.flow_paths_dic, self.time_table_maintainer)
        schedule_middle.schedule_middle(self.flow_PR_sortlist)
        if schedule_middle.fail_flow:
            print(f"fail_flow_occur:{schedule_middle.fail_flow}")
            self.time_table_maintainer.fail_flow_refilt(schedule_middle.fail_flow)
            
        if schedule_middle.fail_flow:    
            for flow in schedule_middle.fail_flow:
                self.fail_flows.append(flow)
    
        for flow in self.fail_flows:
            print(f"{flow}")
        all_flows = len(self.flow_paths_dic)
        fail_flows = len(self.fail_flows)
        print(f"scheduled flows = {all_flows-fail_flows} flows")
        

        #把時間表回傳給主程式，讓Demo顯示時間表
     
        return self.time_table_maintainer.time_table
    
    
    
    def sort_flow(self):   # this PR means deadline/path_length，越小越緊急，由小到大排列
        piority_dic = {}
        for flow, path in self.flow_paths_dic.items():
            deadline = self.flow_dic[flow]["Deadline"] 
            piority_dic[flow] = deadline/len(path)

        # 使用sorted函數，依據字典的值進行排序，並取得排序後的鍵值清單
        sorted_keys = sorted(piority_dic, key=piority_dic.get)
        self.flow_PR_sortlist = sorted_keys
        


   