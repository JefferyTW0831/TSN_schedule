import math
import copy
class Scheduler:
    def __init__(self, flow_dic, flow_paths_dic) :
        self.flow_dic = flow_dic                        #{F1:(D1, D3, "", 2, 8, 5, 2, 8), F2:(D1, D4, "", 3, 9, 4, 3, 8),...}
        self.flow_paths_dic = flow_paths_dic            
        self.time_table = {}                            #{(D1,D3):{}, }
        self.wait_to_schedule = []
   

    def scheduling(self):
        print("-----------------flow_paths_dic---------------------")
        for key, value in self.flow_paths_dic.items():
            print(f"key:value = {key}:{value}")
        print("------------------------------------------------------")

        for flow, path in self.flow_paths_dic.items():    #flow = F1, path=[{'Src':'D1', 'Dst':'SW1', 'Time':[]},{},{}]
            self.genarate_first_link_time(flow, path[0])
            self.genarate_last_link_time(flow, path[-1])
            print(f"每flow狀態： {flow}")
            print(f"{path}")                              #清單形式
            for num in path:                            #印出每個清單內的項目
                print(f"{num}")
        print(f"-----------------------------------------------------")
        self.put_flows_to_time_table()
        self.schedule_middle()
        print(f"path_dic = ")
        for flow, paths in self.flow_paths_dic.items():
            print(f"{flow}=")
            for path in paths:
                print(path)
        self.put_flows_to_time_table()
      
        
        
    def genarate_first_link_time(self, flow, path):
        path["Time"] = self.genarate_time_slot(flow, 0)

    def genarate_last_link_time(self, flow, path):
        path["Time"] = self.genarate_time_slot(flow, -self.flow_dic[flow]["Size"])

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
    
    def put_flows_to_time_table(self):
        wait_flag = False
        self.wait_to_schedule = []
        for flow, paths in self.flow_paths_dic.items():     # paths = Path_list = [{},{},{}], {'Src', 'Dst', 'Time'}
            for path in paths:
                
                #如果沒有此link
                if self.time_table.get((path['Src'], path['Dst'])) == None:  
                    #新link，添加到時間表裡面
                    self.time_table[(path['Src'], path['Dst'])] = copy.deepcopy(path['Time'])
                #如果有此link
                else:
                    #比對time，查看是否有發生碰撞
                    all_common = set(path['Time'].items()) & set(self.time_table[(path['Src'], path['Dst'])].items()) 
                    common_time_slot = set(path['Time'].keys()) & set(self.time_table[(path['Src'], path['Dst'])].keys())
                    if all_common :
                        pass 
                    elif common_time_slot or wait_flag == True:
                        #發生碰撞，將此path先放到等待陣列
                        wait_flag = True
                    else:
                        self.time_table[(path['Src'], path['Dst'])].update(path['Time']) 
            if wait_flag == True:
                    wait_flag = False
                    self.wait_to_schedule.append(flow)    

        print(f"time_table = ")
        for (src, dst), time in self.time_table.items():
            print(f"{(src, dst)}:{time}")
        print(f"wait_to_schedule = {self.wait_to_schedule}")
        print(f"----------------------------------------------------------------")    

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
                
        
            


                                
                    


        


        

            
       
            
