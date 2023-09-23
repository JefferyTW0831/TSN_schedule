import math
from scheduler.Timetable import TimeTable
class Scheduler:
    def __init__(self, flow_dic, flow_paths_dic) :
        self.flow_dic = flow_dic                        #{F1:(D1, D3, "", 2, 8, 5, 2, 8), F2:(D1, D4, "", 3, 9, 4, 3, 8),...}
        self.flow_paths_dic = flow_paths_dic            
        self.time_table = {}                            #{(D1,D3):{}, }
        self.wait_to_schedule = []
   

    def scheduling(self):
        time_table = TimeTable()
        print("-----------------flow_paths_dic---------------------")
        for key, value in self.flow_paths_dic.items():
            print(f"key:value = {key}:{value}")
        print("------------------------------------------------------")

        for flow, path in self.flow_paths_dic.items():    #flow = F1, path=[{'Src':'D1', 'Dst':'SW1', 'Time':[]},{},{}]
            self.genarate_first_link_time(time_table, flow, path[0])
            self.genarate_last_link_time(flow, path[-1])
            print(f"每flow狀態： {flow}")
            print(f"{path}")                              #清單形式
            for num in path:                            #印出每個清單內的項目
                print(f"{num}")
        print(f"-----------------------------------------------------")
        self.schedule_middle()
        print(f"path_dic = ")
        for flow, paths in self.flow_paths_dic.items():
            print(f"{flow}=")
            for path in paths:
                print(path)
        self.put_flows_to_time_table()
        
    def genarate_first_link_time(self, time_table, flow, path):
        path["Time"] = self.genarate_time_slot(flow, 0)
        time_table.put_flows_to_time_table(path)

    def genarate_last_link_time(self, time_table, flow, path):
        path["Time"] = self.genarate_time_slot(flow, -self.flow_dic[flow]["Size"])
        time_table.put_flows_to_time_table(path)

    def genarate_time_slot(self, flow, bias):
        time_list = {}
        if bias == 0:
            start = self.flow_dic[flow]["StartTime"]
        else:
            start = self.flow_dic[flow]["StartTime"]+self.flow_dic[flow]["Period"]+bias
        period = self.flow_dic[flow]["Period"]
        times = self.flow_dic[flow]["Times"]
        size = self.flow_dic[flow]["Size"]
        current_time = start
        for _ in range(times):
            for _ in range(size):
                time_list[current_time] = flow
                current_time += 1
            current_time += period - size
        return time_list
    
    def schedule_middle(self):
        long_path_fail_flows = []
        short_path_fail_flows = []
        previous_path = {}
        for flow, paths in self.flow_paths_dic.items():
            if flow not in self.wait_to_schedule:
                for path in paths:
                    if not path.get('Time') :
                            time_list = self.genarate_active_time_slot(previous_path, flow, self.flow_dic[flow]["Size"])
                            path["Time"] = time_list
                    previous_path = path

    def genarate_active_time_slot(self, prev_path, flow, bias):
        time_list = {}
        print(f"min = {min(prev_path['Time'].keys())}")
        start =  min(prev_path["Time"].keys())+bias
        period = self.flow_dic[flow]["Period"]
        times = self.flow_dic[flow]["Times"]
        size = self.flow_dic[flow]["Size"]
        current_time = start
        for _ in range(times):
            for _ in range(size):
                time_list[current_time] = flow
                current_time += 1
            current_time += period - size
        return time_list
                
        
            


                                
                    


        


        

            
       
            
