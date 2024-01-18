#----添加要新增的排程方法----
from scheduler.tense_schedule.origin_method.Scheduler import Scheduler as original
from scheduler.tense_schedule.weight_time_domain_forward.Scheduler import Scheduler as weight_time_domain_forward
from scheduler.tense_schedule.weight_time_domian_backward.Scheduler import Scheduler as weight_time_domian_backward
from scheduler.tense_schedule.weight_flow_domain_forward.Scheduler import Scheduler as weight_flow_domain_forward
from scheduler.tense_schedule.weight_flow_domain_backward.Scheduler import Scheduler as weight_flow_domain_backward
#--------------------------

schedule_method_list = {
    "1":original,
    "2":weight_time_domain_forward,
    "3":weight_time_domian_backward,
    "4":weight_flow_domain_forward,
    "5":weight_flow_domain_backward
}

class SchedulerSwitch:
    def __init__(self, topology):
      self.topology = topology
        
    
    def run(self):
        scheduled_data = None
        method_chosen = self.print_message()
        
        #方法選擇
        scheduler = schedule_method_list[method_chosen](self.topology.flow_dic ,self.topology.links, self.topology.path_dic)
        #資料回傳
        scheduled_data = scheduler.scheduling()
        
    
        return scheduled_data
        
        
    def print_message(self):
        print("Choose a method:")
        print("1.Original")
        print("2.weight_sorting_time_domain(forward)")
        print("3.weight_sorting_time_domain(backward)")
        print("4.weight_sorting_flow_domain(forward)")
        print("5.weight_sorting_flow_domain(backward)")
        method = input("Choose a scheduling method:")
        
        return method
        

