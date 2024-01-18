
class InitFlowFilter:

    def __init__(self, flow_dic, flow_paths_dic, time_table_maintainer, driving_mode):
        self.flow_dic = flow_dic
        self.flow_paths_dic = flow_paths_dic
        self.time_table_maintainer = time_table_maintainer
        self.driving_mode = driving_mode

    #應該要將比較方法放在時間表(time_table)裡面進行，會有比較高的可調整性。(但這邊想說一次處理，先利用path_dic執行看看，之後有機會再做模組化調整)
    def init_flows_filter(self, flow_PR_sortlist): 

        #先將時間放入各Flow的path中的first link，並計算path size
        if self.driving_mode == "Original":
            print("Original")
            for flow, path in self.flow_paths_dic.items():    
                time_list = self.genarate_time_slot(flow)
                self.time_table_maintainer.first_link_set_up(path[0], time_list)
        else:
            print("SORT")
            for flow in flow_PR_sortlist:
                path = self.flow_paths_dic[flow]
                time_list = self.genarate_time_slot(flow)
                self.time_table_maintainer.first_link_set_up(path[0], time_list)
            
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
    
    