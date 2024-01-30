#----添加要新增的排程方法----
from new_scheduler.tense_schedule.SchedulerSwitch import SchedulerSwitch as tense_schedule
from new_scheduler.full_schedule.SchedulerSwitch import SchedulerSwitch as full_schedule
#--------------------------

objective_list = {
    1:tense_schedule,
    2:full_schedule
}

class ObjectSwitch:
    def __init__(self, topology):
      self.topology = topology
        
    def run(self):
        scheduled_data = None
        object_chosen = self.print_object_message()
        execution_chosen = self.print_execution_message()
          
        #方法選擇
        scheduler = objective_list[object_chosen](self.topology, execution_chosen)
        #資料回傳
        scheduled_data = scheduler.run()
        if execution_chosen == 1:
            return 1, scheduled_data
        else:
            return 2, scheduled_data
        
    def print_object_message(self):
        print("Choose a method:")
        print("1.依照參數盡可能排最多的流")
        print("2.可變動開始傳輸時間，盡可能盡早傳完所有的流")
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
    
    def print_execution_message(self):
        print("選擇執行方式(full_schedule目前要一個一個測，所以不要用全部執行):")
        print("1.全部執行")
        print("2.則一方法執行(會跑圖)")
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

        

