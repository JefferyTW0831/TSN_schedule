from .Timetable import TimeTable
class InitFlowFilter:

    def __init__(self, flow_dic, flow_paths_dic):
        self.flow_dic = flow_dic
        self.flow_paths_dic = flow_paths_dic

    #應該要將比較方法放在時間表(time_table)裡面進行，會有比較高的可調整性。(但這邊想說一次處理，先利用path_dic執行看看，之後有機會再做模組化調整)
    def init_flows_filter(self):  
        mentain_time_dict = {}
        remove = []
        time_table_maintainer = TimeTable()
        #先將時間放入各Flow的path中的first link，並計算path size
        for flow, path in self.flow_paths_dic.items():    
            time_list = self.genarate_time_slot(flow)
            time_table_maintainer.put_path_and_time_list_to_table(path, time_list)
            
            #計算path size   
            mentain_time_dict[flow] = {"Ingress":path[0]["Ingress"], "Egress":path[0]["Egress"], "PathSize":len(path), "Time":time_list} 

        #比較各flow，當Ingress及Egress相同，找到有相同first_link的兩個flow，比較兩flow內的時間，如果時間相同
        for i, (flow1, data1) in enumerate(mentain_time_dict.items()):
            for flow2, data2 in list(mentain_time_dict.items())[i+1:]:
                if data1["Ingress"] == data2["Ingress"] and data1["Egress"] == data2["Egress"] and bool(set(data1['Time']) & set(data2[0]['Time'])):
                    if flow1 not in remove: 
                        if data1["PathSize"] > data2["PathSize"]:
                            if flow1 not in remove:
                                remove.append(flow1)
                        else:
                            if flow2 not in remove:
                                remove.append(flow2)
        print("\n\n------------------------------")
        print(f"(IintFlowFilter.py)\n")
        print(f"remove_flows = ")
        for flow in remove:
            print(f"{flow}:{self.flow_paths_dic[flow][0]}")
            self.flow_paths_dic.pop(flow, None)
        print("------------------------------")
     
    #加入時間
    def genarate_time_slot(self, flow):
        time_list = {}
        start = self.flow_dic[flow]["StartTime"]
        period = self.flow_dic[flow]["Period"]
        times = self.flow_dic[flow]["Times"]
        size = self.flow_dic[flow]["Size"]
        current_time = start
        for _ in range(times):
            for times in range(size):
                time_list[current_time] = flow + "_" + str(times)
                current_time += 1
            current_time += period - size
        return time_list