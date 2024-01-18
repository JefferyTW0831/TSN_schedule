#----添加要新增的排程方法----
from new_scheduler.tense_schedule.SchedulerSwitch import SchedulerSwitch as tense_schedule
#--------------------------

schedule_goal_list = {
    1:tense_schedule,
    #"2":full_schedule
}




class ObjectSwitch:
    def __init__(self, topology):
      self.topology = topology
        
    
    def run(self):
        scheduled_data = None
        object_chosen = self.print_message()
        
        #方法選擇
        scheduler = schedule_goal_list[object_chosen](self.topology)
        #資料回傳
        scheduled_data = scheduler.run()
        
    
        return scheduled_data
        
        
    def print_message(self):
        print("Choose a method:")
        print("1.tense_schedule")
        print("2.full_schedule")
        while True:
            try:
                method = int(input("請輸入1到2之間的數字："))
                if 1 <= method <= 2:
                    break
                else:
                    print("請輸入1到5之間的數字。")
            except ValueError:
                print("請輸入有效的數字。")
      
        
        return method
        

