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
        self.sorted_flows = []            
   
    def scheduling(self):
        print("\n\n------------------------------")
        print(f"(Scheduler1.py)\n")
        #排序flows
        self.flows_sort()
        init_flows = InitFlowFilter(self.flow_dic ,self.flow_paths_dic, self.time_table_maintainer)           
        init_flows.init_flows_filter()
        if self.time_table_maintainer.fail_flows:
            self.record_fail_flows(self.time_table_maintainer.fail_flows)


        schedule_middle = ScheduleMiddle(self.flow_dic, self.flow_paths_dic, self.time_table_maintainer, self.sorted_flows)
        schedule_middle.schedule_middle()
        #排程後有fail的flow，清空時間表上的fail_flow
        if schedule_middle.fail_flow:
            print(f"fail_flow_occur:{schedule_middle.fail_flow}")
            self.time_table_maintainer.fail_flow_refilt(schedule_middle.fail_flow)
            self.record_fail_flows(schedule_middle.fail_flow)


        print(f"fail flows:")
        for flow in self.fail_flows:
            print(f"{flow}")
        all_flows = len(self.flow_paths_dic)
        fail_flows = len(self.fail_flows)
        print(f"scheduled flows = {all_flows-fail_flows} flows")
        
        
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
        print(f"(Scheduler5.py)\n")
        #將有相同first_Link的flows依據path從小排到大，發生衝突時path較小的可優先被挑選
        self.sort_flow()
        init_flows = InitFlowFilter(self.flow_dic ,self.flow_paths_dic, self.time_table_maintainer)           
        init_flows.init_flows_filter(self.flow_PR_sortlist)
        if self.time_table_maintainer.fail_flows:
            self.record_fail_flows(self.time_table_maintainer.fail_flows)

        schedule_middle = ScheduleMiddle(self.flow_dic, self.flow_paths_dic, self.time_table_maintainer)
        schedule_middle.schedule_middle(self.flow_PR_sortlist)
        #排程後有fail的flow，清空時間表上的fail_flow
        if schedule_middle.fail_flow:
            print(f"fail_flow_occur:{schedule_middle.fail_flow}")
            self.time_table_maintainer.fail_flow_refilt(schedule_middle.fail_flow)
            self.record_fail_flows(schedule_middle.fail_flow)

        print(f"fail flows:")
        for flow in self.fail_flows:
            print(f"{flow}")
        all_flows = len(self.flow_paths_dic)
        fail_flows = len(self.fail_flows)
        print(f"scheduled flows = {all_flows-fail_flows} flows")
        
        return self.time_table_maintainer.time_table
    
    def record_fail_flows(self, fail_flows):
        for flow in fail_flows:
            self.fail_flows.append(flow)


    def sort_flow(self):   # this PR means deadline/path_length
        piority_dic = {}
        for flow, path in self.flow_paths_dic.items():
            deadline = self.flow_dic[flow]["Deadline"] 
            piority_dic[flow] = deadline/len(path)

        # 使用sorted函數，依據字典的值進行排序，並取得排序後的鍵值清單
        sorted_keys = sorted(piority_dic, key=piority_dic.get)
        self.flow_PR_sortlist = sorted_keys




   