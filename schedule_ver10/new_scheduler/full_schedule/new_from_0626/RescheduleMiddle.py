import new_scheduler.Genarators as Genarators

class RescheduleMiddle:
    def __init__(self, flow_dic, flow_paths_dic, time_table_maintainer, link_record, driving_mode, direction, sort_mode):
        self.flow_dic = flow_dic
        self.flow_paths_dic = flow_paths_dic
        self.time_table_maintainer = time_table_maintainer
        self.fail_flows = []
        self.link_record = link_record                      #紀錄link已經使用的時間戳
        self.driving_mode = driving_mode
        self.direction = direction
        self.sort_mode = sort_mode

    def schedule_middle(self, flow, time_list):
        all_link = [(link["Ingress"], link["Egress"]) for link in self.flow_paths_dic[flow]]
        first_link = all_link[0]
        #針對每個packet
        for time in time_list:
            packet = self.time_table_maintainer.time_table[time][first_link]
            
            if self.set_flows(time, packet) == "TimeOut":
                for link in all_link:
                    self.link_record[link].time_dic = self.link_record[link].original_dic.copy()
                return
        
            
    def set_flows(self, time, packet):
        all_link = [(link["Ingress"], link["Egress"]) for link in self.flow_paths_dic[packet["Flow"]]]
        remaining_link = all_link[1:]
        #一個pakcet先走完所有link
        for link in remaining_link:
            #設定packet
            target_time = self.set_packet(time, link, packet)
            #碰到timeout
            if target_time == "TimeOut":
                return "TimeOut"
            time = target_time
    
    def set_packet(self, time, link, packet):
        target_time = time + 1 
        check_continuous_time = self.link_record[link].time_dic.get(target_time)
        
        if check_continuous_time == None :
            if target_time >= packet["Tolerant"]:
                if packet["Flow"] not in self.fail_flows:
                    self.fail_flows.append(packet["Flow"])
                return "TimeOut"  
            self.time_table_maintainer.setup_time_and_link(target_time, link, packet)
            self.link_record[link].run(target_time)

            return target_time

        elif check_continuous_time < packet["Tolerant"] and self.sort_mode == "Our":
            self.time_table_maintainer.setup_time_and_link(check_continuous_time, link, packet)
            self.link_record[link].run(check_continuous_time)
            return check_continuous_time

        else :
            if packet["Flow"] not in self.fail_flows:
                self.fail_flows.append(packet["Flow"])   

            return "TimeOut"
        
        
