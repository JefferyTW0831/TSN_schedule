#flow_packet = {1:F1_0, 2:F1_1,....}
class TimeTable:
    
    def __init__(self):
        self.time_table = {}
        self.fail_flows = []

    def first_link_set_up(self, path, time_dict):
        temp_dict = {}                  
        
        for time, flow_packet_dict in time_dict.items():
            flow = flow_packet_dict["Flow"]
            temp_dict[time] = {}
            #若此時間尚未被建立
            if self.time_table.get(time) == None:                   
                temp_dict[time][(path["Ingress"], path["Egress"])] = flow_packet_dict
            #時間已建立，path尚未建立：無衝突Path問題，直接放置flow_packet
            elif self.time_table.get(time) != None:
                if self.time_table[time].get((path["Ingress"], path["Egress"])) == None:
                    temp_dict[time][(path["Ingress"], path["Egress"])] = flow_packet_dict
            #時間已建立path也建立完畢，將會有link_time_collision，先預設排序較後面的flowname優先及較低，需先去除
                else:
                    temp_dict = {}
                    self.fail_flows.append(flow)
                    break

        if temp_dict:
            for time in temp_dict.keys():
                if time in self.time_table:     
                    self.time_table[time].update(temp_dict[time])
                else:
                    self.time_table[time] = temp_dict[time]

    def fail_flow_refilt(self, fail_flow):
        pop_dic = {}

        for flow in fail_flow:
            for time, data in self.time_table.items():
                    
                for link, packet in data.items():
                    if flow == packet["Flow"]:
                        #print(f"time = {time}, link = {link}   flow = {flow}")
                        if pop_dic.get(time)==None:
                            pop_dic[time] = []
                        pop_dic[time].append(link)
                            
        for time, data in self.time_table.items():
            for time_p, links in pop_dic.items():
                for link in links:
                    if time == time_p and link in data.keys():
                        self.time_table[time].pop(link)
                       # print(f"del   {time} {link}   packet")
                  
        
        


