
class InitFlowFilter:

    def __init__(self, flow_dic, flow_paths_dic, time_table_maintainer):
        self.flow_dic = flow_dic
        self.flow_paths_dic = flow_paths_dic
        self.time_table_maintainer = time_table_maintainer
        self.flow_PR_sortlist = []  # high to low

    
    def init_flows_filter(self, flow_PR_sortlist): 
        #先將時間放入各Flow的path中的first link
        for flow in flow_PR_sortlist:  
            path = self.flow_paths_dic[flow] 
            time_dict = self.genarate_time_slot(flow)
            self.time_table_maintainer.first_link_set_up(path[0], time_dict)
            
       
    #製造開始傳輸之packets
    def genarate_time_slot(self, flow):
        time_dict = {}
        start = self.flow_dic[flow]["StartTime"]
        period = self.flow_dic[flow]["Period"]
        times = self.flow_dic[flow]["Times"]
        size = self.flow_dic[flow]["Size"]
        e2e = self.flow_dic[flow]["Deadline"]
        current_time = start
        for _ in range(times):
            for times in range(size):
                time_dict[current_time] = {"Flow":flow, "StartTime":current_time, "Packet":times, "Tolerant":current_time-size+1+e2e}
                current_time += 1
            current_time += period - size
        return time_dict
    
    def sort_flow(self):   # this PR means deadline/path_length
        piority_dic = {}
        for flow, path in self.flow_paths_dic.items():
            deadline = self.flow_dic[flow]["Deadline"] 
            piority_dic[flow] = deadline/len(path)

        # 使用sorted函數，依據字典的值進行排序，並取得排序後的鍵值清單
        sorted_keys = sorted(piority_dic, key=piority_dic.get)
        self.flow_PR_sortlist = sorted_keys

    #製造deadline之packets
    def genarate_deadline_packet(self, time_list):
        deadline_dict = {}
        for packet_data in time_list.values():
            deadline_dict.update({packet_data["Tolerant"]:packet_data})
        return deadline_dict



