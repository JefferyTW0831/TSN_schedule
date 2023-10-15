import math
import copy

class Scheduler:
    def __init__(self, flow_dic, flow_links, flow_paths_dic) :
        self.flow_dic = flow_dic
        self.flow_links = flow_links                        #{F1:(D1, D3, "", 2, 8, 5, 2, 8), F2:(D1, D4, "", 3, 9, 4, 3, 8),...}
        self.flow_paths_dic = flow_paths_dic            
        self.time_table = {}                            #{(D1,D3):{}, }
        self.wait_to_schedule = []
   

    def scheduling(self):
        for flow, path in self.flow_paths_dic.items():    #flow = F1, path=[{'Src':'D1', 'Dst':'SW1', 'Time':[]},{},{}]
            self.genarate_first_link_time(flow, path[0])
           
   
        print(f"path_dic = ")
        for flow, paths in self.flow_paths_dic.items():
            print(f"{flow}=")
            for path in paths:
                print(path)
        return self.flow_paths_dic
        # self.put_flows_to_time_table()
    
    def genarate_first_link_time(self, flow, path):
        path["Time"] = self.genarate_time_slot(flow, 0)

   
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

 