
class InitFlowFilter:

    def __init__(self, flow_dic, flow_paths_dic, time_table_maintainer):
        self.flow_dic = flow_dic
        self.flow_paths_dic = flow_paths_dic
        self.time_table_maintainer = time_table_maintainer
        self.flow_PR_sortlist = []  # high to low
    #應該要將比較方法放在時間表(time_table)裡面進行，會有比較高的可調整性。(但這邊想說一次處理，先利用path_dic執行看看，之後有機會再做模組化調整)
    def init_flows_filter(self): 

        self.sort_flow()

        #先將時間放入各Flow的path中的first link，並計算path size
        for flow in self.flow_PR_sortlist:
            path = self.flow_paths_dic[flow]
            time_list = self.genarate_time_slot(flow)
            self.time_table_maintainer.first_link_set_up(flow, path[0], time_list)
    def sort_flow(self):   # this PR means deadline/path_length
        piority_dic = {}
        for flow, path in self.flow_paths_dic.items():
            deadline = self.flow_dic[flow]["Deadline"] 
            piority_dic[flow] = deadline/len(path)

        # 使用sorted函數，依據字典的值進行排序，並取得排序後的鍵值清單
        sorted_keys = sorted(piority_dic, key=piority_dic.get)
        self.flow_PR_sortlist = sorted_keys
       
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
    
    