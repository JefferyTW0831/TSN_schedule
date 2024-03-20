from new_scheduler.Execution import RunData
from new_scheduler.Execution import RunDemo
from new_scheduler.full_schedule.FullScheduler import FullSchedulerContinue
from new_scheduler.full_schedule.FullScheduler import FullSchedulerReschedule
from new_scheduler.tense_schedule.TenseScheduler import TenseScheduler

objective = {
    1:TenseScheduler,
    2:FullSchedulerContinue,
    3:FullSchedulerReschedule
}

class ObjectiveSwitch:
    def __init__(self):
        pass 

    def run(self):
        chosen = self.print_object_message()
        #方法選擇
        scheduler = ExeSwitch(objective[chosen])
        scheduler.run()

    def print_object_message(self):
        print("Choose a method:")
        print("1.依照參數盡可能排最多的流")
        print("2.可變動開始傳輸時間，盡可能盡早傳完所有的流(接著排)")
        print("2.可變動開始傳輸時間，盡可能盡早傳完所有的流(重排)")
        while True:
            try:
                chosen = int(input("請輸入1到3之間的數字："))
                if 1 <= chosen <= 3:
                    break
                else:
                    print("請輸入1到3之間的數字。")
            except ValueError:
                print("請輸入有效的數字。")
        return chosen
    
execution = {
    1:RunData,
    2:RunDemo
}

class ExeSwitch:
    def __init__(self, object_chosen):
        self.object_chosen = object_chosen

    def run(self):
        chosen = self.print_execution_message()
        
        execution[chosen](self.object_chosen).run()
    
    def print_execution_message(self):
        print("選擇執行方式(full_schedule目前要一個一個測，所以不要用全部執行):")
        print("1.全部執行")
        print("2.則一方法執行(會跑圖)")
        while True:
            try:
                chosen = int(input("請輸入1到2之間的數字："))
                if 1 <= chosen <= 2:
                    break
                else:
                    print("請輸入1到2之間的數字。")
            except ValueError:
                print("請輸入有效的數字。")
        return chosen

