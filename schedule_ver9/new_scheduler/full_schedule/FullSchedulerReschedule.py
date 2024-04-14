import new_scheduler.Genarators as Genarators
from new_scheduler.Timetable import TimeTable
from new_scheduler.tense_schedule.ScheduleMiddle import ScheduleMiddle

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
        self.time_table_maintainer = TimeTable()
        self.schedule_middle = ScheduleMiddle(self.flow_dic, self.flow_paths_dic, self.time_table_maintainer, self.driving_mode, self.direction)
        
    def scheduling(self):
        self.sort_flow()
        #包容力→Deadline/(Size*Pathlength)
        for flow in self.flow_PR_sortlist:
            time_list = self.resetStartTime(flow)
            
        print(f"排序方式：{self.sort_mode}")    
        return self.time_table_maintainer.time_table


    def sort_flow(self):   # this PR means deadline/path_length，越小越緊急，由小到大排列
       
        piority_dic = {}
        if self.sort_mode == "Original_Sort":
            original_sortlist = list(self.flow_dic.keys())
            self.flow_PR_sortlist = original_sortlist
        elif self.sort_mode == "包容力_Sort":
            for flow, path in self.flow_paths_dic.items():
                period = self.flow_dic[flow]["Period"] 
                size = self.flow_dic[flow]["Size"]
                piority_dic[flow] = period/size
            sorted_keys = sorted(piority_dic, key=piority_dic.get)
            self.flow_PR_sortlist = sorted_keys
            print(f"這裡顯示資料流排序：{self.flow_PR_sortlist}")
        else:
            for flow, path in self.flow_paths_dic.items():
                deadline = self.flow_dic[flow]["Deadline"] 
                piority_dic[flow] = deadline/len(path)
        # 使用sorted函數，依據字典的值進行排序，並取得排序後的鍵值清單
            sorted_keys = sorted(piority_dic, key=piority_dic.get)
            self.flow_PR_sortlist = sorted_keys
            print(f"這裡顯示資料流排序：{self.flow_PR_sortlist}")

        
    def resetStartTime(self, flow):
        not_set = True
        self.flow_dic[flow]["StartTime"] = -1
        while not_set:
            self.flow_dic[flow]["StartTime"] += 1 
            print(f"排{self.flow_dic[flow]['StartTime']}中")
            time_dict = Genarators.genarate_time_slot(flow, self.flow_dic)
            firstlink = self.flow_paths_dic[flow][0]
            if self.time_table_maintainer.reschedule_firstlink_to_timetable(firstlink, time_dict):
                self.schedule_middle.fail_flows = []
                self.schedule_middle.schedule_middle([flow])
                if self.time_table_maintainer.middle_fail_flows:
                        print(f"重排{self.time_table_maintainer.middle_fail_flows}")
                        self.time_table_maintainer.fail_flow_refilt(self.time_table_maintainer.middle_fail_flows)
                          
                    #全部排OK
                else:
                    print(f"{flow}排OK")
                    not_set = False
           
                
        
        



        
