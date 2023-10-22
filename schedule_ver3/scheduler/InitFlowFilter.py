class InitFlowFilter:

    def __init__(self, flow_dic, flow_paths_dic):
        self.flow_dic = flow_dic
        self.flow_paths_dic = flow_paths_dic
    
    def init_flows_filter(self):
        mentain_time_dict = {}
        remove = []
        for flow, path in self.flow_paths_dic.items():    
            time_list = self.genarate_first_link_time(flow)
            path[0]["Time"] = time_list   
            mentain_time_dict[flow] = {"Ingress":path[0]["Ingress"], "Egress":path[0]["Egress"], "PathSize":len(path)}               #data_struct
        
        for i, (flow1, data1) in enumerate(mentain_time_dict.items()):
            for flow2, data2 in list(mentain_time_dict.items())[i+1:]:
                if data1["Ingress"] == data2["Ingress"] and data1["Egress"] == data2["Egress"] and bool(set(self.flow_paths_dic[flow1][0]['Time']) & set(self.flow_paths_dic[flow2][0]['Time'])):
                    if flow1 not in remove: 
                        if data1["PathSize"] > data2["PathSize"]:
                            if flow1 not in remove:
                                remove.append(flow1)
                        else:
                            if flow2 not in remove:
                                remove.append(flow2)
        print(f"remove_flows = ")
        for flow in remove:
            print(f"{flow}:{self.flow_paths_dic[flow][0]}")
            self.flow_paths_dic.pop(flow, None)
        print("------------------------------")
     
    
    def genarate_first_link_time(self, flow):
        time_list = self.genarate_time_slot(flow, 0)

        return time_list

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
            for times in range(size):
                time_list[current_time] = flow + "_" + str(times)
                current_time += 1
            current_time += period - size
        return time_list