import sys
import csv
import time
import network_datas.setup_inputflows_rand
import new_scheduler.Genarators as Genarators 
from PyQt5.QtWidgets import QApplication
from network_datas.InputFlow import InputFlow
from network_datas.Topology import Topology
from new_scheduler.Demo import Demo

mode = {
    1:{"driving_mode":"Original", "direction":"Forward"},
    2:{"driving_mode":"Time", "direction":"Forward"},
    3:{"driving_mode":"Time", "direction":"Backward"},
    4:{"driving_mode":"Flow", "direction":"Forward"},
    5:{"driving_mode":"Flow", "direction":"Backward"}
}

class RunData:
    def __init__(self, object_chosen):
        self.object_chosen = object_chosen

    def run(self):
        with open("測試_沒common_link_W.csv", "w", newline='') as file:
            csv_writer = csv.writer(file)
            # 如果文件是空的，寫入標題行
            if file.tell() == 0:
                csv_writer.writerow(['次數', '原始', 'Time_前後', 'Time_後前', 'Flow_前後', 'Flow_後前'])
            else:
                csv_writer.writerow(['--------------','-------------','-我是分隔','線-----------', '--------------','--------------'])
            loop_times = int(input(f"輸入執行次數 : "))
            sort_mode = self.sort_mode_chosen()
            for times in range(1, loop_times+1):
                scheduled_data = self.scheulde_working(sort_mode)
                self.write_output_flows_csv(scheduled_data, csv_writer, times)

    def scheulde_working(self, sort_mode):
        network_datas.setup_inputflows_rand.main()
        
        input_flow = InputFlow()                                       
        flow_dic = input_flow.run()
        self.write_input_flows(flow_dic)
        topology = Topology(flow_dic)                                
        topology.routing()     

        scheduled_data = {}
        for i in range(1, 6):
            print(f"{mode[i]['driving_mode']}_{mode[i]['direction']}")
            scheduler = self.object_chosen(topology, 1, mode[i]["driving_mode"], mode[i]["direction"],sort_mode)
            
            result_list = scheduler.scheduling()
            
            scheduled_data[f"scheduler{i}"] = {"result_list": result_list, "success_flows": len(result_list)}
        return scheduled_data
    
    def write_input_flows(self, flow_dic):
        with open("input_weight.txt", "a") as file:
            for flow_name, data in flow_dic.items():
                file.write(f"{flow_name} : {data}\n")
                file.write("\n" + "-" * 30 + "\n")

    def write_output_flows_csv(self, scheduled_data, csv_writer, loop_times):
        success_flows = []
        success_flows.append(loop_times)
        # 數據行
        for i, (scheduler_name, data) in enumerate(scheduled_data.items(), start=1):
            success_flows.append(len(data['result_list']))
        csv_writer.writerows([success_flows])

    def sort_mode_chosen(self):
        print(f"選擇初始篩選方法:")
        print("1.原始(按照flow名稱)")
        print("2.按照權重")
        print("3.先找出衝突組合，每個組合裡擁有最多的flows的子組合將勝選")
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

class RunDemo:
    def __init__(self, object_chosen):
        self.object_chosen = object_chosen

    def run(self):
        input_flow = InputFlow()                                       
        flow_dic = input_flow.run()
        topology = Topology(flow_dic)                             
        topology.routing() 

        sort_mode = self.sort_mode_chosen()
        chosen = self.choose_method()
        
        scheduler = self.object_chosen(topology, 2, mode[chosen]["driving_mode"], mode[chosen]["direction"], sort_mode)
        scheduled_data = scheduler.scheduling()
        max_time = Genarators.get_max_time(topology.flow_dic)
        
        app = QApplication(sys.argv)
        view = Demo(topology.links, max_time)
        view.show()
        #結果以圖表顯示
        view.update_graphics_from_dict(scheduled_data)
        
        sys.exit(app.exec_())
    
    def choose_method(self):
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


    def sort_mode_chosen(self):
        print(f"選擇初始篩選方法:")
        print("1.原始(按照flow名稱)")
        print("2.按照權重")
        print("3.先找出衝突組合，每個組合裡擁有最多的flows的子組合將勝選")
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

    