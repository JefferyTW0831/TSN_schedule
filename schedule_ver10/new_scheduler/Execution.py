import sys
import csv
import network_datas.setup_inputflows_rand
import new_scheduler.Genarators as Genarators 
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication
from network_datas.setup_inputflows_rand import SetInputFlowsRand
from network_datas.InputFlow import InputFlow
from network_datas.Topology import Topology
from new_scheduler.Demo import Demo
import time
mode = {
    1:{"driving_mode":"Time", "direction":"Forward"},
    2:{"driving_mode":"Time", "direction":"Backward"},
    3:{"driving_mode":"Flow", "direction":"Forward"},
    4:{"driving_mode":"Flow", "direction":"Backward"}
}

result_driving_mode = {
    1:{"driving_mode":"Flow", "direction":"Backward"},
    2:{"driving_mode":"Flow", "direction":"Forward"},
    3:{"driving_mode":"Flow", "direction":"Forward"},
    4:{"driving_mode":"Flow", "direction":"Forward"},
    5:{"driving_mode":"Flow", "direction":"Forward"},
}

result_sort_mode = {
    1:"NCB",
    2:"PB",
    3:"STB",
    4:"JDPS",
    5:"FS"
}

class RunData:
    def __init__(self, object_chosen):
        self.object_chosen = object_chosen
        self.rand_flows = SetInputFlowsRand()
        self.input_flows = None

    def run(self):

        with open("測試_沒common_link_包假假假.csv", "w", newline='') as file:
            csv_writer = csv.writer(file)
            # 如果文件是空的，寫入標題行
            if file.tell() == 0:
                csv_writer.writerow(['次數', '原始', 'Time_前後', 'Time_後前', 'Flow_前後', 'Flow_後前'])
            else:
                csv_writer.writerow(['--------------','-------------','-我是分隔','線-----------', '--------------','--------------'])
            self.input_flows = int(input("輸入資料流數量："))
            loop_times = int(input(f"輸入執行次數 : "))
            sort_choose = self.sort_mode_chosen()
            for times in range(1, loop_times+1):
                scheduled_data = self.scheulde_working(sort_choose)
                self.write_output_flows_csv(scheduled_data, csv_writer, times)

    def scheulde_working(self, sort_choose):
        self.rand_flows.run(self.input_flows)
        
        input_flow = InputFlow()                                       
        flow_dic = input_flow.run()
        self.write_input_flows(flow_dic)
        topology = Topology(flow_dic)                                
        topology.routing()     

        scheduled_data = {}
        for i in range(1, 5):
            print(f"{mode[i]['driving_mode']}_{mode[i]['direction']}")
            scheduler = self.object_chosen(topology, "RunData", mode[i]["driving_mode"], mode[i]["direction"],sort_mode[sort_choose])
            
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
            print(i, scheduler_name, data)
            success_flows.append(data["success_flows"])
        csv_writer.writerows([success_flows])

    def sort_mode_chosen(self):
        print(f"選擇初始篩選方法:")
        print("1.原始(按照flow名稱)")
        print("2.按照權重")
        print("3.先找出衝突組合，每個組合裡擁有最多的flows的子組合將勝選")
        print("4.包容力排序")
        while True:
            try:
                chosen = int(input("請輸入1到4之間的數字："))
                if 1 <= chosen <= 4:
                    break
                else:
                    print("請輸入1到4之間的數字。")
            except ValueError:
                print("請輸入有效的數字。")
        return chosen

class RunDemo:
    def __init__(self, object_chosen):
        self.object_chosen = object_chosen
        self.rand_flows = SetInputFlowsRand()
        

    def run(self):
        auto_manu_chosen = self.auto_manual_chosen()
        if auto_manu_chosen == 2:
            input_flows = int(input("輸入資料流數量："))
            self.rand_flows.run(input_flows)
            input_flow = InputFlow()                             
            flow_dic = input_flow.run()
        else:
            input_flow = InputFlow()                             
            flow_dic = input_flow.run_manual()
        topology = Topology(flow_dic)                             
        topology.routing() 

        sort_choose = self.sort_chosen()
        mode_choose = self.mode_chosen()
        #紀錄資料流資訊  
        # for flow, data in flow_dic.items():
        #     print(f"{flow}:{data}") 


        start_time = time.perf_counter()
        scheduler = self.object_chosen(topology, 2, mode[mode_choose]["driving_mode"], mode[mode_choose]["direction"], result_sort_mode[sort_choose])
        # print(f"原始排序:{flow_dic.keys()}")
        scheduled_data = scheduler.scheduling()
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"執行時間: {execution_time} 秒")
        flow, max_time = Genarators.get_last_time(scheduled_data)
        print(f"最後flow = {flow}, 最後時間 = {max_time}")
         
        app = QApplication(sys.argv)
        view = Demo(topology.links, max_time)
        view.show()
        #結果以圖表顯示
        view.update_graphics_from_dict(scheduled_data)
        
        sys.exit(app.exec_())
    
    def mode_chosen(self):
        method = None
        print("Choose a method:")
        for key, value in mode.items():
            print(f"{key}:{value}")
        while True:
            try:
                method = int(input("請輸入1到4之間的數字："))
                if 1 <= method <= 4:
                    break
                else:
                    print("請輸入1到4之間的數字。")
            except ValueError:
                print("請輸入有效的數字。")
        
        return method

    def sort_chosen(self):
        print(f"選擇初始篩選方法:")
        for key, value in result_sort_mode.items():
            print(f"{key}:{value}")
        while True:
            try:
                chosen = int(input("請輸入1到5之間的數字："))
                if 1 <= chosen <= 5:
                    break
                else:
                    print("請輸入1到5之間的數字。")
            except ValueError:
                print("請輸入有效的數字。")
        return chosen
    def auto_manual_chosen(self):
        print("選擇執行:")
        print("1.套用手動生成資料流的檔案")
        print("2.輸入資料流數量隨機生成")
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
    
class RunMatPlotLibTense:
    def __init__(self, object_chosen):
        self.object_chosen = object_chosen
        self.rand_flows = SetInputFlowsRand()
    
    def run(self):
        write_file_name = input("輸入檔案名稱：")
        data = self.schedule_working_times_part()
        data = self.change_dict_to_csv_dict(data)
        self.write_csv(write_file_name, data)

    def schedule_working_times_part(self):
        main_dict = {}
        loop_times = 100
        for times in range(1, loop_times+1):
            input_flow_num_dict = {}
            for input_flow_amount in range (100, 300, 40):
                print(f"{times} : {input_flow_amount}")
                sort_dict = self.schedule_working_times_and_sort_mode_part(input_flow_amount)
                input_flow_num_dict[f"{input_flow_amount}"] = sort_dict
            main_dict[times] = input_flow_num_dict
        return main_dict

    def schedule_working_times_and_sort_mode_part(self, input_flow_amount):
        sort_dict = {}
        self.rand_flows.run(input_flow_amount)
        for num in range(1, len(result_sort_mode)+1):
            input_flow = InputFlow()                                       
            flow_dic = input_flow.run()
            topology = Topology(flow_dic)                                
            topology.routing() 
            scheduler = self.object_chosen(topology, "RunData", result_driving_mode[num]["driving_mode"], result_driving_mode[num]["direction"],result_sort_mode[num])
            scheduled_flows = scheduler.scheduling()
            sort_dict[f"{result_sort_mode[num]}"] = scheduled_flows
        return sort_dict
    
    def change_dict_to_csv_dict(self, data):
        new_dict = {}
        print("\n\n\n")
        print(data)
        for target_sort_types in result_sort_mode.values():
            if target_sort_types not in new_dict:
                new_dict.update({target_sort_types:{}})
            for times, input_flows_dict in data.items():
                for input_flows_amount, sort_types_dict in input_flows_dict.items():
                    if input_flows_amount not in new_dict[target_sort_types]:
                        new_dict[target_sort_types].update({input_flows_amount:{}})
                    new_dict[target_sort_types][input_flows_amount].update({times:sort_types_dict[target_sort_types]})
        return new_dict

    def write_csv(self, write_file_name, data):
        
        with open(f"{write_file_name}_Tense.csv", "w", newline='') as file:
            csv_writer = csv.writer(file)
            if file.tell() == 0:
                csv_writer.writerow(['次數', 'flows'])
            else:
                print(f"檔案已存在!")
                return
            for sort_name, input_flows_dict in data.items():
                csv_writer.writerow([sort_name])
                for input_flow, sort_data in input_flows_dict.items():
                    csv_writer.writerow([input_flow, f"flows"])
                    for times, flows in sort_data.items():
                        write_list = []
                        write_list.append(times)
                        write_list.append(flows)
                        csv_writer.writerow(write_list)
        print(f"\n\n{write_file_name}_Tense.csv 已保存")

class RunMatPlotLibTense_Original:
    def __init__(self, object_chosen):
        self.object_chosen = object_chosen
        self.rand_flows = SetInputFlowsRand()
    
    def run(self):
        write_file_name = input("輸入檔案名稱：")
        data = self.schedule_working_driving_mode_part()
        self.write_csv(write_file_name, data)

    def schedule_working_driving_mode_part(self):
        main_dict = {}
        for schedulers in range(1, 5):
            input_flow_num_dict = {}
            for input_flow_amount in range (20, 120, 20):
                sort_dict = self.schedule_working_times_and_sort_mode_part(schedulers, input_flow_amount)
                input_flow_num_dict[f"{input_flow_amount}"] = sort_dict

            mode_key = f"{result_sort_mode[schedulers]}"
            main_dict[mode_key] = input_flow_num_dict
           
        return main_dict
                    
        #原先直接DEMO圖        
        # self.plot_chart(mode_dict)
    
    def schedule_working_times_and_sort_mode_part(self, schedulers, input_flows):
        sort_dict = {}
        loop_times = 100
        for times in range(1, loop_times+1):
            sort_dict[times] = {}
            self.rand_flows.run(input_flows)
            input_flow = InputFlow()                                       
            flow_dic = input_flow.run()
            topology = Topology(flow_dic)                                
            topology.routing()     

            scheduler = self.object_chosen(topology, "RunData", result_driving_mode[schedulers]["driving_mode"], result_driving_mode[schedulers]["direction"],result_sort_mode[schedulers])
            scheduled_flows = scheduler.scheduling()
        
            sort_dict[times] = scheduled_flows
        
        return sort_dict
    
    def write_csv(self, write_file_name, data):
        
        with open(f"{write_file_name}_Tense.csv", "w", newline='') as file:
            csv_writer = csv.writer(file)
            if file.tell() == 0:
                csv_writer.writerow(['次數', 'flows'])
            else:
                print(f"檔案已存在!")
                return
            for sort_name, input_flows_dict in data.items():
                csv_writer.writerow([sort_name])
                for input_flow, sort_data in input_flows_dict.items():
                    csv_writer.writerow([input_flow, f"flows"])
                    for times, flows in sort_data.items():
                        write_list = []
                        write_list.append(times)
                        write_list.append(flows)
                        csv_writer.writerow(write_list)
        print(f"\n\n{write_file_name}_Tense.csv 已保存")

class RunMatPlotLibTense_Original_32:
    
    def __init__(self, object_chosen):
        self.object_chosen = object_chosen
        self.rand_flows = SetInputFlowsRand()
    
    def run(self):
        write_file_name = input("輸入檔案名稱：")
        data = self.schedule_working_part_one()
        self.write_csv(write_file_name, data)

    def schedule_working_part_one(self):
        mode_dict = {}
        for schedulers in range(1, 5):
            input_flow_num_dict = {}
            for input_flow_amount in range (20, 120, 20):
                sort_dict = self.schedule_working_part_two(schedulers, input_flow_amount)
                input_flow_num_dict[f"{input_flow_amount}"] = sort_dict

            mode_key = f"{mode[schedulers]['driving_mode']}_{mode[schedulers]['direction']}"
            mode_dict[mode_key] = input_flow_num_dict
        
        return mode_dict
                    
        #原先直接DEMO圖        
        # self.plot_chart(mode_dict)
    
    def schedule_working_part_two(self, schedulers, input_flows):
        sort_dict = {}
        loop_times = 100
        for times in range(1, loop_times+1):
            sort_dict[times] = {}
            self.rand_flows.run(input_flows)
            for sort_num in range(1, 5):

                input_flow = InputFlow()                                       
                flow_dic = input_flow.run()
                topology = Topology(flow_dic)                                
                topology.routing()     

                scheduler = self.object_chosen(topology, "RunData", mode[schedulers]["driving_mode"], mode[schedulers]["direction"],sort_mode[sort_num])
                scheduled_flows = scheduler.scheduling()
                sort_key = f"{sort_mode[sort_num]}"
                print(f"目前排程：{sort_mode[sort_num]}")
                sort_dict[times].update({sort_key:scheduled_flows})
            

        return sort_dict
    
    def write_csv(self, write_file_name, data):
        
        with open(f"{write_file_name}_Tense.csv", "w", newline='') as file:
            csv_writer = csv.writer(file)
            if file.tell() == 0:
                csv_writer.writerow(['次數', '原始排序', 'Weight排序', 'GCD排序', '包容力排序'])
            else:
                print(f"檔案已存在!")
                return
            for mode_name,  input_flows in data.items():
                csv_writer.writerow([mode_name])
                for flows, sort_data in input_flows.items():
                    csv_writer.writerow([flows, f"flows"])
                    for times, sort_types in sort_data.items():
                        write_list = []
                        write_list.append(times)
                        for scheduled_flows in list(sort_types.values()):
                            write_list.append(scheduled_flows)
                        
                        csv_writer.writerow(write_list)
        print(f"\n\n{write_file_name}_Tense.csv 已保存")
    
class RunMatPlotLibReschedule:
    def __init__(self, object_chosen):
        self.object_chosen = object_chosen
        self.rand_flows = SetInputFlowsRand()
        self.input_flows = None
    
    def run(self):
        write_file_name = input("輸入檔案名稱：")
        data, process = self.schedule_working_part_one()
        data = self.change_dict_to_csv_dict(data)
        process = self.change_dict_to_csv_dict(process)
        self.write_csv(write_file_name, data)
        self.write_csv(f"{write_file_name}_process_time", process)

    def schedule_working_part_one(self):
        main_dict = {}
        process_main_dict = {}
        loop_times = 20
        for times in range(1, loop_times+1):
            input_flow_num_dict = {}
            process_input_flow_num_dict = {}
            for input_flow_amount in range (100, 300, 40):
                print(f"{times} : {input_flow_amount}")
                sort_dict, process_dict = self.schedule_working_part_two(input_flow_amount)
                input_flow_num_dict[f"{input_flow_amount}"] = sort_dict
                process_input_flow_num_dict[f"{input_flow_amount}"] = process_dict
            main_dict[times] = input_flow_num_dict
            process_main_dict[times] = process_input_flow_num_dict
        return main_dict, process_main_dict

    def schedule_working_part_two(self, input_flows):
        sort_dict = {}
        process_dict = {}
        self.rand_flows.run(input_flows)
        for num in range(1, len(result_sort_mode)+1):
            input_flow = InputFlow()                                       
            flow_dic = input_flow.run()
            topology = Topology(flow_dic)                                
            topology.routing() 
            start_time = time.perf_counter()
            scheduler = self.object_chosen(topology, 2, result_driving_mode[num]["driving_mode"], result_driving_mode[num]["direction"],result_sort_mode[num])
            scheduled_time_table = scheduler.scheduling()
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            flow, max_time = Genarators.get_last_time(scheduled_time_table)
            sort_dict[f"{result_sort_mode[num]}"] = max_time
            process_dict[f"{result_sort_mode[num]}"] = execution_time
            print(f"排序:{result_sort_mode[num]}, 數目:{input_flows}, 執行時間:{execution_time}")

        return sort_dict, process_dict
            
    def change_dict_to_csv_dict(self, data):
        new_dict = {}
        for target_sort_types in result_sort_mode.values():
            if target_sort_types not in new_dict:
                new_dict.update({target_sort_types:{}})
            for times, input_flows_dict in data.items():
                for input_flows_amount, sort_types_dict in input_flows_dict.items():
                    if input_flows_amount not in new_dict[target_sort_types]:
                        new_dict[target_sort_types].update({input_flows_amount:{}})
                    new_dict[target_sort_types][input_flows_amount].update({times:sort_types_dict[target_sort_types]})
        return new_dict

    def write_csv(self, write_file_name, data):
        
        with open(f"{write_file_name}_Full.csv", "w", newline='') as file:
            csv_writer = csv.writer(file)
            if file.tell() == 0:
                csv_writer.writerow(['次數', 'time'])
            else:
                print(f"檔案已存在!")
                return
            for sort_name, input_flows_dict in data.items():
                csv_writer.writerow([sort_name])
                for input_flow, sort_data in input_flows_dict.items():
                    csv_writer.writerow([input_flow, f"flows"])
                    for times, flows in sort_data.items():
                        write_list = []
                        write_list.append(times)
                        write_list.append(flows)
                        csv_writer.writerow(write_list)
        print(f"\n\n{write_file_name}_Full.csv 已保存")

class RunMatPlotLibReschedule_Original_32:
    def __init__(self, object_chosen):
        self.object_chosen = object_chosen
        self.rand_flows = SetInputFlowsRand()
        self.input_flows = None
    
    def run(self):
        write_file_name = input("輸入檔案名稱：")
        data = self.schedule_working_part_one()
        self.write_csv(write_file_name, data)

    def schedule_working_part_one(self):
        mode_dict = {}
        
        for schedulers in range(1, 5):
            input_flow_num_dict = {}
            for input_flow_amount in range (20, 120, 20):
                sort_dict = self.schedule_working_part_two(schedulers, input_flow_amount)
                input_flow_num_dict[f"{input_flow_amount}"] = sort_dict

            mode_key = f"{mode[schedulers]['driving_mode']}_{mode[schedulers]['direction']}"
            mode_dict[mode_key] = input_flow_num_dict
        
        
        return mode_dict

    def schedule_working_part_two(self, schedulers, input_flows):
        sort_dict = {}
        loop_times = 100
        for times in range(1, loop_times+1):
            sort_dict[times] = {}
            self.rand_flows.run(input_flows)
            for sort_num in range(1, 5):
                self.rand_flows.run(input_flows)
            
                input_flow = InputFlow()                                       
                flow_dic = input_flow.run()
                topology = Topology(flow_dic)                                
                topology.routing()     

                scheduler = self.object_chosen(topology, 2, mode[schedulers]["driving_mode"], mode[schedulers]["direction"],sort_mode[sort_num])
                scheduled_time_table = scheduler.scheduling()
                flow, max_time = Genarators.get_last_time(scheduled_time_table)
                sort_key = f"{sort_mode[sort_num]}"
                #這邊再看仔細一下資料結構
                sort_dict[times].update({sort_key:max_time})
            

        return sort_dict
    
    def write_csv(self, write_file_name, data):
        
        with open(f"{write_file_name}_Full.csv", "w", newline='') as file:
            csv_writer = csv.writer(file)
            if file.tell() == 0:
                csv_writer.writerow(['次數', '原始排序', 'Weight排序', 'GCD排序', '包容力排序'])
            else:
                print(f"檔案已存在!")
                return
            for mode_name,  input_flows in data.items():
                csv_writer.writerow([mode_name])
                for flows, sort_data in input_flows.items():
                    csv_writer.writerow([flows, f"flows"])
                    for times, sort_types in sort_data.items():
                        write_list = []
                        write_list.append(times)
                        for scheduled_flows in list(sort_types.values()):
                            write_list.append(scheduled_flows)
                        
                        csv_writer.writerow(write_list)
        print(f"\n\n{write_file_name}_Full.csv 已保存")