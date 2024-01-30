#----添加要新增的排程方法----
from new_scheduler.tense_schedule.TenseScheduler import TenseScheduler


#--------------------------
mode = {
    1:{"driving_mode":"Original", "direction":"Forward"},
    2:{"driving_mode":"Time", "direction":"Forward"},
    3:{"driving_mode":"Time", "direction":"Backward"},
    4:{"driving_mode":"Flow", "direction":"Forward"},
    5:{"driving_mode":"Flow", "direction":"Backward"}
}

class SchedulerSwitch:
    def __init__(self, topology, execution):
      self.topology = topology
      self.execution = execution
    
    def run(self):
        scheduled_data = None
        #---全部執行---(純看數據用_無資料回傳)#
        scheduled_data = {}
        if self.execution == 1:
            for i in range(1, 6):
                print(f"{mode[i]['driving_mode']}_{mode[i]['direction']}")
                scheduler = TenseScheduler(self.topology, self.execution, mode[i]["driving_mode"], mode[i]["direction"])
                result_list, success_flows = scheduler.scheduling()
                scheduled_data[f"scheduler{i}"] = {"result_list": result_list, "success_flows": success_flows}
        else:
            # ---選擇方法---(跑圖用_須依照數字多開終端執行(記得把main的DEMO打開))#
            method_chosen = self.print_message()
            
            #方法選擇
            scheduler = TenseScheduler(self.topology, self.execution, mode[method_chosen]["driving_mode"], mode[method_chosen]["direction"])
            #資料回傳
            scheduled_data = scheduler.scheduling()

        return scheduled_data
    
    def print_message(self):
        method = None
        print("Choose a method:")
        print("1.original")
        print("2.time_driven_forward")
        print("3.time_driven_backward")
        print("4.flow_driven_forward")
        print("5.flow_driven_backward")
        while True:
            try:
                method = int(input("請輸入1到5之間的數字："))
                if 1 <= method <= 5:
                    break
                else:
                    print("請輸入1到5之間的數字。")
            except ValueError:
                print("請輸入有效的數字。")
        
        return method

