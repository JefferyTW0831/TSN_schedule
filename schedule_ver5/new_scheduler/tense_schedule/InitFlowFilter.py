
class InitFlowFilter:
    def __init__(self, flow_dic, flow_paths_dic, time_table_maintainer, driving_mode):
        self.flow_dic = flow_dic
        self.flow_paths_dic = flow_paths_dic
        self.time_table_maintainer = time_table_maintainer
        self.driving_mode = driving_mode
        self.temp_dict = {}
   
    #應該要將比較方法放在時間表(time_table)裡面進行，會有比較高的可調整性。(但這邊想說一次處理，先利用path_dic執行看看，之後有機會再做模組化調整)
    def init_flows_filter(self, flow_PR_sortlist): 

        #將排序好的flows依序把時間放入各Flow的first_link, 並排入時間表，
        # if self.driving_mode == "Original":
            # for flow, path in self.flow_paths_dic.items():    
            #     time_list = self.genarate_time_slot(flow)
            #     self.time_table_maintainer.first_link_set_up(path[0], time_list)
        # else:
            for flow in flow_PR_sortlist:
                first_link = self.flow_paths_dic[flow][0]
                time_list = self.genarate_time_slot(flow)
                self.first_link_set_up(first_link, time_list)

        #設計第三種方法：先找出衝突組合，每個組合裡擁有最多的flows的子組合將勝選，目前要寫的話需要大改(因為現在是直接把生成的time與flow丟入到時間表才判斷，等到下一個flow要丟到時間表才會知道有沒有衝突)
            # self.find_collision_flows_groups()

    #加入時間
    #Flow = 名稱, Packet = 封包編號, piority = 最大容忍時間/路徑長度(結果越小優先)
    def genarate_time_slot(self, flow):
        time_list = {}
        start = self.flow_dic[flow]["StartTime"]
        period = self.flow_dic[flow]["Period"]
        times = self.flow_dic[flow]["Times"]
        size = self.flow_dic[flow]["Size"]
        e2e = self.flow_dic[flow]["Deadline"]
        current_time = start
        for instance in range(times):
            for packet_num in range(size):
                time_list[current_time] = {"Flow":flow, "StartTime":current_time,  "Packet":packet_num, "Tolerant":current_time-size+1+e2e}
                current_time += 1
            current_time += period - size
        return time_list
    
    #這邊邏輯也要改，等到篩好之後才直接丟進time_table
    def first_link_set_up(self, path, time_dict):
        temp_dict = {}                  
        for time, flow_packet_dict in time_dict.items():
            flow = flow_packet_dict["Flow"]
            temp_dict[time] = {}
            #若此時間尚未被建立
            if self.time_table_maintainer.time_table.get(time) == None:                   
                temp_dict[time][(path["Ingress"], path["Egress"])] = flow_packet_dict
            #時間已建立，path尚未建立：無衝突Path問題，直接放置flow_packet
            elif self.time_table_maintainer.time_table.get(time) != None:
                if self.time_table_maintainer.time_table[time].get((path["Ingress"], path["Egress"])) == None:
                    temp_dict[time][(path["Ingress"], path["Egress"])] = flow_packet_dict
            #時間已建立path也建立完畢，將會有link_time_collision，先預設排序較後面的flowname優先及較低，需先去除
                else:
                    temp_dict = {}
                    self.time_table_maintainer.init_fail_flows.append(flow)
                    break
        if temp_dict:
            for time in temp_dict.keys():
                if time in self.time_table_maintainer.time_table:     
                    self.time_table_maintainer.time_table[time].update(temp_dict[time])
                else:
                    self.time_table_maintainer.time_table[time] = temp_dict[time]

    def find_collision_flows_groups(self):
        remaining_flows = list(self.flow_dic.keys())
        temp_dict = {}
        time = 1 
        for flow in remaining_flows:
            first_link = self.flow_paths_dic[flow][0]
            time_list = self.genarate_time_slot(flow)
            temp_dict.update({flow:{(first_link["Ingress"], first_link["Egress"]):list(time_list.keys())}})
        
        for flow, data in temp_dict.items():
            print(f"flow = {flow}")
            print(f"{data}")



            
    
        