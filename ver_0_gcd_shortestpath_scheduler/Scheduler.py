import math
import copy
from scheduler.GcdFlows import GcdFlows
from scheduler.ShortestPair import ShortestPair
class Scheduler:
    def __init__(self, flow_dic, path_dic) :
        
        self.flow_dic = flow_dic    #{F1:(D1, D3, "", 2, 8, 5, 2, 8), F2:(D1, D4, "", 3, 9, 4, 3, 8),...}
        self.path_dic = path_dic    #
        self.links_time_list = []   #紀錄每個所需要的link上面的資源占用狀態 = []
        self.gcd_srcflows = []
        self.gcd_dstflows = []
        self.remaining_gcd_flows_pair = {}
        self.scheduled_flows = []
        self.find_gcd_flows()       
        self.links_time_arrangement()

    #這邊用來查找有哪些flows可組成pair(size相同;period/size要呈GCD)
    def find_gcd_flows(self):
        get_gcdflows = GcdFlows(self.flow_dic, self.path_dic)
        self.gcd_srcflows, self.gcd_dstflows = get_gcdflows.run()
        print(f"gcd_srcflows = {self.gcd_srcflows}")
        print(f"gcd_dstflows = {self.gcd_dstflows}")
    
    #這邊做一下時間表管理(每個link的資源占用情況)
    def links_time_arrangement(self):
        for flow, links in self.path_dic.items():
            for link in links:
                if link not in self.links_time_list:
                    self.links_time_list.append(copy.deepcopy(link))
        #print(f"links_time_list = {self.links_time_list}")

    #這邊將進行scheduling，會分成幾個步驟做處理，目前第一步先把GCD_pair裡面查找生命周期最短的pair優先排入時間表
    def scheduling(self):  
        if not self.scheduled_flows :
            #在GCD_pairs裡面找出最短生命週期的pair
            shortest_pair = ShortestPair(self.flow_dic, self.path_dic, self.gcd_srcflows, self.gcd_dstflows)
            flows_to_scheduling = shortest_pair.shortest_life_flows_pair()
            flows_to_scheduling = shortest_pair.reconstruct_pair_flow(flows_to_scheduling)      #如果pair裡面有超過兩個flows，將會取前面兩個來塞進時間表
            flow1 = next(iter(flows_to_scheduling.keys()))[0]
            flow2 = next(iter(flows_to_scheduling.keys()))[1]
            print(f"{flow1}, {flow2}, 將會被塞入時間表裡面")
            self.put_into_shcedule_head(flow1, flow2)
            self.put_into_shcedule_tail(flow1, flow2)
            self.put_into_schedule_middle(flow1, flow2)
        else:
            pass

    def put_into_shcedule_head(self, flow1, flow2):                #flow1, flow2 只有flow的名稱資訊而已

        time_list = []                                             #獲取flow的時間frame
        scheduled = False
        for link in self.links_time_list:                          #在時間表管理中查找flow1
            if self.path_dic[flow1][0].get("Src") == link.get("Src") and self.path_dic[flow1][0].get("Dst") == link.get("Dst"):                   #找到flow1的第一個link
                start = self.flow_dic[flow1]["StartTime"]          #重新命名開始時間
                period = self.flow_dic[flow1]["Period"]            #重新命名週期
                period_times = self.flow_dic[flow1]["Times"]       #重新命名週期次數
                size = self.flow_dic[flow1]["Size"]                #重新命名flow大小
                time_list = self.generate_link_time_sequence(start, period, period_times, size, time_list)
                scheduled = self.check_schedule(time_list, flow1)
                
                if scheduled == True:
                    link["Time"] = time_list                        #這一行有問題，因為這個關係，舊有的self.links_time_list會被更改
                    self.path_dic[flow1][0]["Time"] = time_list
                    self.scheduled_flows.append(flow1)
          
        time_list = []
        scheduled = False
        for link in self.links_time_list:                           #在時間表管理中查找flow2 
            if self.path_dic[flow2][0].get("Src") == link.get("Src") and self.path_dic[flow2][0].get("Dst") == link.get("Dst"):                     #找到flow2資訊
                self.flow_dic[flow2]["StartTime"] = start + size    #偏移開始傳輸時間
                start = self.flow_dic[flow2]["StartTime"]             
                period = self.flow_dic[flow2]["Period"]            
                period_times = self.flow_dic[flow2]["Times"]      
                size = self.flow_dic[flow2]["Size"]
                time_list = self.generate_link_time_sequence(start, period, period_times, size, time_list)
                scheduled = self.check_schedule(time_list, flow2)
                if scheduled == True:
                    link["Time"] = link["Time"]+time_list
                    self.path_dic[flow2][0]["Time"] = time_list
                    self.scheduled_flows.append(flow2)

    def put_into_shcedule_tail(self, flow1, flow2): 
        time_list = []
        scheduled = False
        for link in self.links_time_list:
            if self.path_dic[flow1][-1] == link:
                period = self.flow_dic[flow1]["Period"]            #重新命名週期
                period_times = self.flow_dic[flow1]["Times"]       #重新命名週期次數
                size = self.flow_dic[flow1]["Size"]                #重新命名flow大小
                start = self.flow_dic[flow1]["StartTime"]+period-size        
                time_list = self.generate_link_time_sequence(start, period, period_times, size, time_list)
                scheduled = self.check_schedule(time_list, flow1)
                if scheduled == True:
                    link["Time"] = time_list
                    self.path_dic[flow1][-1]["Time"] = time_list
                    self.scheduled_flows.append(flow1)
        time_list = []
        scheduled = False
        for link in self.links_time_list:
            if self.path_dic[flow2][-1] == link:
                period = self.flow_dic[flow2]["Period"]            #重新命名週期
                period_times = self.flow_dic[flow2]["Times"]       #重新命名週期次數
                size = self.flow_dic[flow2]["Size"]                #重新命名flow大小
                start = self.flow_dic[flow2]["StartTime"]+period-size      
                time_list = self.generate_link_time_sequence(start, period, period_times, size, time_list)
                scheduled = self.check_schedule(time_list, flow2)
                if scheduled == True:
                    link["Time"] = time_list
                    self.path_dic[flow2][-1]["Time"] = time_list
                    self.scheduled_flows.append(flow2)
        
        print("-----------------")
        print(f"查看時間表 = ")
        for link in self.links_time_list:
            print(f"link = {link}")
        print("----------------------------")
        print(f"path_dic1 =  {self.path_dic[flow1][0]['Time']}")    #flow1第一條link
        print(f"path_dic2 =  {self.path_dic[flow2][0]['Time']}")    #flow2第一條link
        print("----------------------------")
        print(f"path_dic1 =  {self.path_dic[flow1][-1]['Time']}")   #flow1最後一條link
        print(f"path_dic2 =  {self.path_dic[flow2][-1]['Time']}")   #flow2最後一條link
        print("-----------------")
       
    def put_into_schedule_middle(self, flow1, flow2):          
        same_link = False                                       #檢查有沒有一樣的Link 
        for flow in self.path_dic[flow1]:
            if flow == self.path_dic[flow2]:
                same_link = True
            if same_link == True:                               #如果有一樣的link，deadline早的先排完
                if self.path_dic[flow1][0]["StartTime"] < self.path_dic[flow2][0]["StartTime"]:   #在時間表上的第二個時間點
                    period = self.flow_dic[flow1]["Period"]            #重新命名週期
                    period_times = self.flow_dic[flow1]["Times"]      #重新命名週期次數
                    size = self.flow_dic[flow1]["Size"]              #重新命名flow大小
                    start = self.flow_dic[flow1]["StartTime"]+size
                    time_list = self.generate_link_time_sequence(start, period, period_times, size, time_list)
                    scheduled = self.check_schedule(time_list, flow2)
                    if scheduled == True:
                        flow[2] = time_list                     #將path_dic上flow1的此link時間更新
                        for link in self.links_time_list:
                            if link[:2] == flow[:2]:
                                link[2] = time_list             #將links_time_list上的此link時間更新
                              
        
                # else:
                #     period = self.flow_dic[flow2][4]            #重新命名週期
                #     period_times = self.flow_dic[flow2][5]      #重新命名週期次數
                #     size = self.flow_dic[flow2][6]              #重新命名flow大小
                #     start = self.flow_dic[flow2][2]+size 
         
    def generate_link_time_sequence(self, start, period, period_times, size, time_list):
        current_number = start
        for add in range(0, size):
            current_number = start + add
            for _ in range(period_times):
                time_list.append(current_number)
                current_number += (period)
        return time_list

    def check_schedule(self, time_list, flow):

        for t_list in time_list:
            if t_list in self.path_dic[flow][2]:
                return False
        return True
    
    
        
