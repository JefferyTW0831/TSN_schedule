import math
import copy
from .InitFlowFilter import InitFlowFilter
from .ScheduleMiddle_copy import ScheduleMiddle

class Scheduler:
    def __init__(self, flow_dic, flow_links, flow_paths_dic) :
        self.flow_dic = flow_dic
        self.flow_links = flow_links                        
        self.flow_paths_dic = flow_paths_dic            
   
    def scheduling(self):
        #將有相同first_Link的flows依據path從小排到大，發生衝突時path較小的可優先被挑選
        init_flows = InitFlowFilter(self.flow_dic ,self.flow_paths_dic)             
        init_flows.init_flows_filter()

        schedule_middle = ScheduleMiddle(self.flow_dic, self.flow_paths_dic)
        schedule_middle.schedule_middle()


        print("\n\n------------------------------")
        print(f"(Scheduler.py)\n")
        print(f"path_dic = ")
        for flow, paths in self.flow_paths_dic.items():
            print(f"{flow}=")
            for path in paths:
                print(path)
        print("-------------------------------")
        return self.flow_paths_dic
    
    
    
    


   