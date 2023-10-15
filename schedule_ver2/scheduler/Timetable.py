import copy


#目前用不到，最後再用
class TimeTable:
    def __init__(self):
        self.time_table = {}
        self.wait_to_schedule = []
       

    def put_flows_to_time_table(self, flow, path, time_slot):
        wait_flag = False
        #如果沒有此link
        if self.time_table.get((path['Ingress'], path['Egress'])) == None:  
            #新link，添加到時間表裡面
            self.time_table[(path['Ingress'], path['Egress'])] = time_slot
        #如果有此link
        else:
            #比對time，查看是否有發生碰撞
            all_common = set(time_slot) & set(self.time_table[(path['Ingress'], path['Egress'])].items()) 
            common_time_slot = set(time_slot) & set(self.time_table[(path['Ingress'], path['Egress'])].keys())
            if all_common :
                pass 
            elif common_time_slot or wait_flag == True:
                #發生碰撞，將此path先放到等待陣列
                wait_flag = True
            else:
                self.time_table[(path['Ingress'], path['Egress'])].update(time_slot) 
        if wait_flag == True:
            wait_flag = False
            self.wait_to_schedule.append(flow)    

        print(f"time_table = ")
        for (src, dst), time in self.time_table.items():
            print(f"{(src, dst)}:{time}")
        print(f"wait_to_schedule = {self.wait_to_schedule}")
        print(f"----------------------------------------------------------------")    
