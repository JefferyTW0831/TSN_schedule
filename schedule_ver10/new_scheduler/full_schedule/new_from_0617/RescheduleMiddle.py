import new_scheduler.Genarators as Genarators

class RescheduleMiddle:
    def __init__(self, flow_dic, flow_paths_dic, time_table_maintainer, driving_mode, direction):
        self.flow_dic = flow_dic
        self.flow_paths_dic = flow_paths_dic
        self.time_table_maintainer = time_table_maintainer
        self.fail_flows = []
        self.link_record = {}
        self.driving_mode = driving_mode
        self.direction = direction

    def schedule_middle(self, flow, time_list):
        max_time = Genarators.get_max_time(self.flow_dic)
        start, end, step = int(time_list[0]), max_time, 1
            
        for time in time_list:
            if self.time_table_maintainer.time_table.get(time)!=None:
                for link, packet in self.time_table_maintainer.time_table[time].items():
                    if flow == packet["Flow"] and link == (self.flow_paths_dic[flow][0]["Ingress"], self.flow_paths_dic[flow][0]["Egress"]):
                        if self.set_flows(time, link, packet) == "TimeOut":
                            return


    def set_flows(self, time, link1, packet):
        all_link = [(link["Ingress"], link["Egress"]) for link in self.flow_paths_dic[packet["Flow"]]]
        start, deadline = packet["StartTime"], packet["Tolerant"]

        if self.link_timeout_check(packet, all_link, start, deadline) == "TimeOut":
            self.fail_flows.append(packet["Flow"])
            return 

       
        next_link = self.get_next_link(link1, packet)
        while next_link:
            target_time = self.set_next_packet(time, next_link, packet)
            if  target_time == "TimeOut":
                return 
            time = target_time
            next_link = self.get_next_link(next_link, packet)

    def link_timeout_check(self, packet, all_link, start, deadline):
        
        for link in all_link:
            if self.link_record.get(link) != None:
                num_in_range = deadline-start+1
                count_in_range = sum(1 for num in range(start, deadline + 1) if num in self.link_record)
                empty_count = num_in_range-count_in_range
                if empty_count < self.flow_dic[packet["Flow"]]["Size"]:
                    return "TimeOut"

    def get_next_link(self, link1, packet):
        next_link = ()
        for link2 in self.flow_paths_dic[packet["Flow"]]:
            if link2["Ingress"] == link1[1]:
                next_link = (link2["Ingress"], link2["Egress"])
                break
        return next_link
    
    #嘗試排入packet，沒辦法排入則往下一個時間點嘗試排入
    def set_next_packet(self, time, next_link, packet):
        target_time = time + 1 
        not_set = True
        while not_set:
            if target_time >= packet["Tolerant"]:
                if packet["Flow"] not in self.fail_flows:
                    self.fail_flows.append(packet["Flow"])   
                return "TimeOut"
            else:
                #檢查有無衝突的Packet
                if self.time_table_maintainer.setup_time_and_link(target_time, next_link, packet):
                    if self.link_record.get(next_link) == None:
                        self.link_record.update({next_link:[]})
                    self.link_record[next_link].append(target_time)
                    return target_time
                #發生衝突，查看下一個時間點
                else:
                    target_time += 1

  