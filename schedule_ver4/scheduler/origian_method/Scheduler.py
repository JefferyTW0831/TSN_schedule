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
        print(f"(Scheduler1.py)\n")
        #將有相同first_Link的flows依據path從小排到大，發生衝突時path較小的可優先被挑選
        init_flows = InitFlowFilter(self.flow_dic ,self.flow_paths_dic, self.time_table_maintainer)           
        init_flows.init_flows_filter()
        self.fail_flows = self.time_table_maintainer.fail_flows

        schedule_middle = ScheduleMiddle(self.flow_dic, self.flow_paths_dic, self.time_table_maintainer)
        schedule_middle.schedule_middle()

        #把時間表回傳給主程式，讓Demo顯示時間表
        for time, packet in self.time_table_maintainer.time_table.items():
            print(f"time:{time}")
            print(f"packet:{packet}")
        return self.time_table_maintainer.time_table
    
    
    
    


   