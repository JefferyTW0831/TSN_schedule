from new_scheduler.tense_schedule.TenseScheduler import TenseScheduler
from new_scheduler.full_schedule.RescheduleMiddle import RescheduleMiddle
import new_scheduler.Genarators as Genarators

#execution = 全部執行 or 跑圖
#driving_mode = time or flow
#direction = 順 or 逆
#先測試TIME_FORWARD的然後將FAIL_FLOWS塞到後面
class FullSchedulerContinue:
    def __init__(self, topology, execution, driving_mode, direction, sort_mode):
        self.topology = topology
        self.flow_dic = topology.flow_dic
        self.flow_links = topology.links                        
        self.flow_paths_dic = topology.path_dic
        self.sort_mode = sort_mode
        self.execution = execution
        self.driving_mode = driving_mode
        self.direction = direction
        self.tense_scheduler = TenseScheduler(self.topology, self.execution, self.driving_mode, self.direction, self.sort_mode)
        
    def scheduling(self):
        timer = 0
        self.tense_scheduler.scheduling()
        piority_dic = {}
        self.direction = "Forward"
        if self.sort_mode == "Our":
            for flow, path in self.flow_paths_dic.items():
                starttime = self.flow_dic[flow]["StartTime"]
                period = self.flow_dic[flow]["Period"] 
                size = self.flow_dic[flow]["Size"]
                piority_dic[flow] = 1/period
            sorted_list = sorted(piority_dic, key=piority_dic.get)
            final_list = [x for x in sorted_list if x in self.tense_scheduler.fail_flows]
            self.tense_scheduler.fail_flows = final_list
            
        self.reschedule_middle = RescheduleMiddle(self.flow_dic, self.flow_paths_dic, self.tense_scheduler.time_table_maintainer, self.driving_mode, self.direction)
        print(f"更動StartTime清單：{self.tense_scheduler.fail_flows}")
        for fail_flow in self.tense_scheduler.fail_flows:
            not_set = True
            print(f"{fail_flow} 自ST: T{self.flow_dic[fail_flow]['StartTime']}")
            while not_set:
                self.flow_dic[fail_flow]["StartTime"] += 1
                timer += 1
                time_dict = Genarators.genarate_time_slot(fail_flow, self.flow_dic)
                firstlink = self.flow_paths_dic[fail_flow][0]
                time_list = self.tense_scheduler.time_table_maintainer.reschedule_firstlink_to_timetable(firstlink, time_dict)
                #Firstlink排成功
                if time_list:
                    self.reschedule_middle.schedule_middle(fail_flow, time_list)
                    if self.reschedule_middle.fail_flows:
                        print(f"{fail_flow}的ST設置於{self.flow_dic[fail_flow]['StartTime']}時，超過deadline")
                        self.tense_scheduler.time_table_maintainer.fail_flow_refilt(self.reschedule_middle.fail_flows)   
                        self.reschedule_middle.fail_flows = []
                    else:
                        not_set = False
            print(f"延後至: T{self.flow_dic[fail_flow]['StartTime']} ")    
        print(f"總延遲：T{timer}")        
        return self.tense_scheduler.time_table_maintainer.time_table



    