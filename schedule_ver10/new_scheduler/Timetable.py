#flow_packet = {1:F1_0, 2:F1_1,....}
class TimeTable:
    
    def __init__(self):
        self.time_table = {}
        self.init_fail_flows = []
        self.middle_fail_flows = []
        self.init_fail_flows_info = []
    
    #對應middle.py def set_next_packet
    def setup_time_and_link(self, time, link, packet):
        if self.time_table.get(time) == None:
            self.time_table[time] = {}
            self.time_table[time].update({link:packet})
        elif self.time_table[time].get(link) == None:
            self.time_table[time][link] = packet 
        else:
            #該link的目標時間點已有packet正在傳輸，衝突發生
            return False
        return True

    def set_firstlink_to_time_table(self, firstlink, time_dict):
        temp_dict = {}                  
        for time, flow_packet_dict in time_dict.items():
            flow = flow_packet_dict["Flow"]
            temp_dict[time] = {}
            #若此時間尚未被建立
            if self.time_table.get(time) == None:                   
                temp_dict[time][(firstlink["Ingress"], firstlink["Egress"])] = flow_packet_dict
            #時間已建立，firstlink尚未建立：無衝突firstlink問題，直接放置flow_packet
            elif self.time_table.get(time) != None:
                if self.time_table[time].get((firstlink["Ingress"], firstlink["Egress"])) == None:
                    temp_dict[time][(firstlink["Ingress"], firstlink["Egress"])] = flow_packet_dict
            #時間已建立firstlink也建立完畢，將會有link_time_collision
                else:
                    temp_dict = {}
                    break
        #成功設定first_link
        if temp_dict:
            for time in temp_dict.keys():
                if time in self.time_table:     
                    self.time_table[time].update(temp_dict[time])
                else:
                    self.time_table[time] = temp_dict[time]
            return False
        else:
            return True
    
    #複製的 偷工減料一下 之後看怎麼整合
    def reschedule_firstlink_to_timetable(self, firstlink, time_dict):
        temp_dict = {}                  
        for time, flow_packet_dict in time_dict.items():
            flow = flow_packet_dict["Flow"]
            temp_dict[time] = {}
            #若此時間尚未被建立
            if self.time_table.get(time) == None:                   
                temp_dict[time][firstlink] = flow_packet_dict
            #時間已建立，firstlink尚未建立：無衝突firstlink問題，直接放置flow_packet
            elif self.time_table.get(time) != None:
                if self.time_table[time].get(firstlink) == None:
                    temp_dict[time][firstlink] = flow_packet_dict
            #時間已建立firstlink也建立完畢，將會有link_time_collision
                else:
                    temp_dict = {}
                    break
        if temp_dict:
            for time in temp_dict.keys():
                if time in self.time_table:     
                    self.time_table[time].update(temp_dict[time])
                else:
                    self.time_table[time] = temp_dict[time]
            return list(temp_dict.keys())
        else:
            return False

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
        #刪除空的時間戳
        empty_time_slot = []
        for time, data in self.time_table.items():
            if not data :
                empty_time_slot.append(time)
        for time in empty_time_slot:
            self.time_table.pop(time)
                  
        
        


