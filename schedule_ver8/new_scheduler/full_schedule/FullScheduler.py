from new_scheduler.tense_schedule.TenseScheduler import TenseScheduler
import new_scheduler.Genarators as Genarators
#先測試TIME_FORWARD的然後將FAIL_FLOWS塞到後面
class FullSchedulerContinue:
    def __init__(self, topology, execution, driving_mode, direction):
        self.topology = topology
        self.flow_dic = topology.flow_dic
        self.flow_links = topology.links                        
        self.flow_paths_dic = topology.path_dic
        self.execution = execution
        self.driving_mode = driving_mode
        self.direction = direction
       
    def scheduling(self):
        tense_scheduler = TenseScheduler(self.topology, self.execution, self.driving_mode, self.direction)
        tense_scheduler.scheduling()
     
        for fail_flow in tense_scheduler.fail_flows:
            not_set = True
            while not_set:
                self.flow_dic[fail_flow]["StartTime"] += 1
                time_dict = Genarators.genarate_time_slot(fail_flow, self.flow_dic)
                firstlink = self.flow_paths_dic[fail_flow][0]
                #Firstlink排成功
                if tense_scheduler.time_table_maintainer.reschedule_firstlink_to_timetable(firstlink, time_dict):
                    #重製middle_fail_flows
                    tense_scheduler.schedule_middle.fail_flows = []
                    tense_scheduler.schedule_middle.schedule_middle([fail_flow])
                    if tense_scheduler.time_table_maintainer.middle_fail_flows:
                        print(f"重排{tense_scheduler.time_table_maintainer.middle_fail_flows}")
                        tense_scheduler.time_table_maintainer.fail_flow_refilt(tense_scheduler.time_table_maintainer.middle_fail_flows)   
                    #全部排OK
                    else:
                        print(f"{fail_flow}排OK")
                        not_set = False
                        
        return tense_scheduler.time_table_maintainer.time_table




    