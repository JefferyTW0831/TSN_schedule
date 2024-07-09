import new_scheduler.Genarators as Genarators
import new_scheduler.FogSort as FogSort
from new_scheduler.Timetable import TimeTable
from new_scheduler.full_schedule.RescheduleMiddle import RescheduleMiddle
from new_scheduler.full_schedule.SortFlow import SortFlow
from new_scheduler.full_schedule.LinkTimeDict import LinkTimeDict 
class FullSchedulerReschedule:
    def __init__(self, topology, execution, driving_mode, direction, sort_mode):
        self.flow_dic = topology.flow_dic
        self.flow_links = topology.links                        
        self.flow_paths_dic = topology.path_dic
        self.execution = execution
        self.driving_mode = driving_mode
        self.direction = direction
        self.sort_mode = sort_mode
        self.fail_flows = []    
        self.link_record = {}   
        #建立清單時間紀錄
        for link in self.flow_links:
            if self.link_record.get(link) == None:
                self.link_record.update({link:LinkTimeDict()}) 
       
        self.flow_PR_sortlist = None
        self.time_table_maintainer = TimeTable()
        self.sortflow = SortFlow(self.flow_dic, self.flow_paths_dic, self.time_table_maintainer, driving_mode, sort_mode, direction)
        self.reschedule_middle = RescheduleMiddle(self.flow_dic, self.flow_paths_dic, self.time_table_maintainer, self.link_record, driving_mode, direction, self.sort_mode)
        
        
    def scheduling(self):
      
        self.sortflow.sort_flows()
        self.flow_PR_sortlist = self.sortflow.flow_PR_sortlist
        #print(f"排序結果：{self.flow_PR_sortlist}")
        
        #包容力→Deadline/(Size*Pathlength)
        for flow in self.flow_PR_sortlist:          
            self.set_flow(flow)

        return self.time_table_maintainer.time_table

    

    def set_flow(self, flow):
        not_set = True
        self.flow_dic[flow]["StartTime"] = -1
        all_link = [(link["Ingress"], link["Egress"]) for link in self.flow_paths_dic[flow]]
        firstlink = all_link[0]
     
        #備分清單
        for link in all_link:
            self.link_record[link].original_dic = self.link_record[link].time_dic.copy()

        while not_set:

            self.flow_dic[flow]["StartTime"] += 1 
            if  self.time_table_maintainer.time_table.get(self.flow_dic[flow]["StartTime"]) != None:
                if firstlink in self.time_table_maintainer.time_table[self.flow_dic[flow]["StartTime"]].keys():
                    continue
            time_dict = Genarators.genarate_time_slot(flow, self.flow_dic)
            time_list = self.time_table_maintainer.reschedule_firstlink_to_timetable(firstlink, time_dict)
            #找到first_link可以放的位置
            if time_list:
                self.reschedule_middle.schedule_middle(flow, time_list)
                #如果排失敗
                if self.reschedule_middle.fail_flows:
                    self.time_table_maintainer.fail_flow_refilt(self.reschedule_middle.fail_flows)
                    self.reschedule_middle.fail_flows = []
                else:

                    not_set = False
      
     

    