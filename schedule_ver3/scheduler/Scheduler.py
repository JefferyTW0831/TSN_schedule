import math
import copy
from .InitFlowFilter import InitFlowFilter
from .ScheduleMiddle import ScheduleMiddle

class Scheduler:
    def __init__(self, flow_dic, flow_links, flow_paths_dic) :
        self.flow_dic = flow_dic
        self.flow_links = flow_links                        #{F1:(D1, D3, "", 2, 8, 5, 2, 8), F2:(D1, D4, "", 3, 9, 4, 3, 8),...}
        self.flow_paths_dic = flow_paths_dic            
   
    def scheduling(self):
        init_flows = InitFlowFilter(self.flow_dic ,self.flow_paths_dic)
        init_flows.init_flows_filter()

        schedule_middle = ScheduleMiddle(self.flow_dic, self.flow_paths_dic)
        schedule_middle.schedule_middle()

        print(f"path_dic = ")
        for flow, paths in self.flow_paths_dic.items():
            print(f"{flow}=")
            for path in paths:
                print(path)
        return self.flow_paths_dic
    
    
    
    


   