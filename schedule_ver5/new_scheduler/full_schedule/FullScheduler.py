from new_scheduler.Timetable import TimeTable
from new_scheduler.tense_schedule.TenseScheduler import TenseScheduler

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
        self.fail_flows = []
        self.time_table_maintainer = TimeTable() 
        self.flow_PR_sortlist = []        
        

    def scheduling(self):
        tense_scheduler = TenseScheduler(self.topology, self.execution, self.driving_mode, self.direction)
        scheduled_data = tense_scheduler.scheduling()
        print("---------------------------------------------------------------")
        print(f"init_fail = {tense_scheduler.time_table_maintainer.init_fail_flows}")
        print(f"shceule_data = {scheduled_data}")
        print("---------------------------------------------------------------")
        
        return scheduled_data
        

class FullSchedulerReschedule:
    def __init__(self) -> None:
        pass
    