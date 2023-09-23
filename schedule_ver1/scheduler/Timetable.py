import copy
class TimeTable:
    def __init__(self):
        self.time_table = {}
       

    def put_flows_to_time_table(self, flow_paths_dic):
        wait_flag = False
        self.wait_to_schedule = []
        for flow, paths in flow_paths_dic.items():     # paths = Path_list = [{},{},{}], {'Src', 'Dst', 'Time'}
            for path in paths:
                
                #如果沒有此link
                if self.time_table.get((path['Ingress'], path['Egress'])) == None:  
                    #新link，添加到時間表裡面
                    self.time_table[(path['Ingress'], path['Egress'])] = copy.deepcopy(path['Time'])
                #如果有此link
                else:
                    #比對time，查看是否有發生碰撞
                    all_common = set(path['Time'].items()) & set(self.time_table[(path['Ingress'], path['Egress'])].items()) 
                    common_time_slot = set(path['Time'].keys()) & set(self.time_table[(path['Ingress'], path['Egress'])].keys())
                    if all_common :
                        pass 
                    elif common_time_slot or wait_flag == True:
                        #發生碰撞，將此path先放到等待陣列
                        wait_flag = True
                    else:
                        self.time_table[(path['Ingress'], path['Egress'])].update(path['Time']) 
            if wait_flag == True:
                    wait_flag = False
                    self.wait_to_schedule.append(flow)    

        print(f"time_table = ")
        for (src, dst), time in self.time_table.items():
            print(f"{(src, dst)}:{time}")
        print(f"wait_to_schedule = {self.wait_to_schedule}")
        print(f"----------------------------------------------------------------")    
