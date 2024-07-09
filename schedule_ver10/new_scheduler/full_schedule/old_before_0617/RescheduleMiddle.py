import new_scheduler.Genarators as Genarators

class RescheduleMiddle:
    def __init__(self, flow_dic, flow_paths_dic, time_table_maintainer, driving_mode, direction):
        self.flow_dic = flow_dic
        self.flow_paths_dic = flow_paths_dic
        self.time_table_maintainer = time_table_maintainer
        self.fail_flows = []
        self.driving_mode = driving_mode
        self.direction = direction

    def schedule_middle(self, flow, time_list):
    #    print(f"------------------------Schedule_Middle-----------------------")
        if self.driving_mode == "Time":
    #        print(f"Time_{self.direction}")
            self.time_driving(flow, time_list)
        elif self.driving_mode == "Flow":
    #        print(f"Flow_{self.direction}")
            self.flow_driving(flow, time_list)
        else:
            print("模式指定失敗")

    def time_driving(self, flow, time_list):
        max_time = Genarators.get_max_time(self.flow_dic)
        if self.direction == "Forward":
            start, end, step = 0, max_time, 1
        else:
            self.set_deadline(flow, time_list)
            start, end, step = max_time, -1, -1

        for time in range(start, end, step):
            if self.time_table_maintainer.time_table.get(time) != None:
                for link1, packet in self.time_table_maintainer.time_table[time].items():
                    if flow == packet["Flow"]:
                        self.set_flows(time, step, link1, packet)
           
    def flow_driving(self, flow, time_list): 
        max_time = Genarators.get_max_time(self.flow_dic)
        if self.direction == "Forward":
            start, end, step = 0, max_time, 1
        else:
            self.set_deadline(flow, time_list)
            start, end, step = max_time, -1, -1

        for time in range(start, end, step):
            if self.time_table_maintainer.time_table.get(time) != None:
                for link1, packet in self.time_table_maintainer.time_table[time].items():
                    if flow == packet["Flow"]:
                        self.set_flows(time, step, link1, packet)

    def set_deadline(self, flow, time_list):
        deadline_dic = {}
        for time_stamp in reversed(time_list):
            for time, data in (self.time_table_maintainer.time_table.items()):
                for first_link, packet in data.items():
                    if time_stamp == time and flow == packet["Flow"]:
                        last_link = (self.flow_paths_dic[packet["Flow"]][-1]["Ingress"], self.flow_paths_dic[packet["Flow"]][-1]["Egress"])
                        not_set = True
                        target_time = packet["Tolerant"]
                        while not_set:
                            #假如table沒有deadline的時間
                            if  target_time not in self.time_table_maintainer.time_table :
                                if target_time not in deadline_dic:
                                    deadline_dic[target_time] = {}
                                    deadline_dic[target_time].update({last_link:packet})
                                    not_set = False
                                elif last_link not in  deadline_dic[target_time]:
                                    deadline_dic[target_time].update({last_link:packet})
                               
                            #假如table有deadline的時間
                            elif last_link not in self.time_table_maintainer.time_table[target_time] :
                                if target_time not in deadline_dic:
                                    deadline_dic[target_time] = {}
                                    deadline_dic[target_time].update({last_link:packet})
                                    not_set = False
                                elif last_link not in  deadline_dic[target_time]:
                                    deadline_dic[target_time].update({last_link:packet})

            
                            target_time-=1
 
                                    
            #加入時間表
        for time, data in deadline_dic.items():
            if time in self.time_table_maintainer.time_table:
                self.time_table_maintainer.time_table[time].update(data)
            else:
                self.time_table_maintainer.time_table.update({time:data})

    def set_flows(self, time, step, link1, packet):
        if self.direction == "Forward":
            next_link = self.get_next_link(link1, packet)
            self.set_next_packet(time, step, next_link, packet)
        else:
            next_link = self.get_prev_link(link1, packet)
            self.set_prev_packet(time, step, next_link, packet)
        
    def get_next_link(self, link1, packet):
        next_link = ()
        for link2 in self.flow_paths_dic[packet["Flow"]]:
            if link2["Ingress"] == link1[1]:
                next_link = (link2["Ingress"], link2["Egress"])
                break
        return next_link
       
    def get_prev_link(self, link1, packet):
        prev_link = ()
        for link2 in self.flow_paths_dic[packet["Flow"]]:
            if link2["Egress"] == link1[0]:
                #假如找到first_link要取消掉
                if link2 == self.flow_paths_dic[packet["Flow"]][0]:
                    break
                prev_link = (link2["Ingress"], link2["Egress"])
                break
        return prev_link
     
    def set_next_packet(self, time, step, next_link, packet):

        target_time = time + step
        
        if next_link:
            not_set = True
            while not_set:
                if target_time >= packet["Tolerant"]:
                    if packet["Flow"] not in self.fail_flows:
                        self.fail_flows.append(packet["Flow"])   
                    not_set = False
                #如果time+1沒有被建立
                elif self.time_table_maintainer.time_table.get(target_time) == None:
                    #建立link並將封包丟到time_slot裡面
                    self.time_table_maintainer.time_table[target_time] = {}
                    self.time_table_maintainer.time_table[target_time].update({next_link:packet})
                    not_set = False
                else:
                    #如果time+1已被建立但是裡面沒有該link(亦即無衝突)
                    if self.time_table_maintainer.time_table[target_time].get(next_link) == None:
                        self.time_table_maintainer.time_table[target_time][next_link] = packet
                        not_set = False
                    #如果time+1已被建立，且裡面有該Link存在(發生衝突)
                    else:
                        target_time += step

    def set_prev_packet(self, time, step, prev_link, packet):
        target_time = time + step
        if prev_link:
            not_set = True
            while not_set:
                if target_time <= packet["StartTime"]:
                    if packet["Flow"] not in self.fail_flows:
                        self.fail_flows.append(packet["Flow"])   
                    not_set = False
                #如果time+1沒有被建立
                elif self.time_table_maintainer.time_table.get(target_time) == None:
                    #建立link並將封包丟到time_slot裡面
                    self.time_table_maintainer.time_table[target_time] = {}
                    self.time_table_maintainer.time_table[target_time].update({prev_link:packet})
                    not_set = False
                else:
            
                    if self.time_table_maintainer.time_table[target_time].get(prev_link) == None:
                        self.time_table_maintainer.time_table[target_time][prev_link] = packet
                        not_set = False
               
                    else:
                        target_time += step

    