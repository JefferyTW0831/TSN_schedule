#----添加要新增的排程方法----
from scheduler.origian_method.Scheduler import Scheduler as original
from scheduler.dead_line_divide_by_path_length_method.Scheduler import Scheduler as deadline_per_path
#--------------------------

schedule_method_list = {
    "1":original,
    "2":deadline_per_path

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
        print("2.Deadline divided by path length")
        method = input("Choose a scheduling method:")
        
        return method
        

