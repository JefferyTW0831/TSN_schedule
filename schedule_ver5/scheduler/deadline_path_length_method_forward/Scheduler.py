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
   
    def scheduling(self):
        print("\n\n------------------------------")
        print(f"(Scheduler2.py)\n")
        #將有相同first_Link的flows依據path從小排到大，發生衝突時path較小的可優先被挑選
        init_flows = InitFlowFilter(self.flow_dic ,self.flow_paths_dic, self.time_table_maintainer)           
        init_flows.init_flows_filter()
        self.fail_flows = self.time_table_maintainer.fail_flows
       
  
        schedule_middle = ScheduleMiddle(self.flow_dic, self.flow_paths_dic, self.time_table_maintainer)
        schedule_middle.schedule_middle()
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
    
    
    
    


   