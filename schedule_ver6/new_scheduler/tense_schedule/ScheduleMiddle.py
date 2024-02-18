class ScheduleMiddle:

    def __init__(self, flow_dic, flow_paths_dic, time_table_maintainer, driving_mode, direction):
        self.flow_dic = flow_dic
        self.flow_paths_dic = flow_paths_dic
        self.time_table_maintainer = time_table_maintainer
        self.time_table = time_table_maintainer.time_table  #dict
        self.fail_flows = []
        self.driving_mode = driving_mode
        self.direction = direction

    def schedule_middle(self, flow_PR_sortlist):
        if self.driving_mode == "Time":
            print(f"Time_{self.direction}")
            self.time_driving(flow_PR_sortlist)
        elif self.driving_mode == "Flow":
            print(f"Flow_{self.direction}")
            self.flow_driving(flow_PR_sortlist)
        else:
            flow_PR_sortlist = self.flow_dic.keys()
            self.original(flow_PR_sortlist)
            
        self.time_table_maintainer.middle_fail_flows = self.fail_flows
        

    def get_max_time(self):
        max_value = None
        for flow, data in self.flow_dic.items():
            flow_deadline_time = data["StartTime"]+data["Period"]*(data["Times"]-1)+data["Deadline"]
            if max_value == None or flow_deadline_time > max_value:
                max_value = flow_deadline_time
                max_flow = flow
        print(f"Last_flow: {max_flow} , Max_time: {max_value}")
        return max_value
    
    def time_driving(self, flow_PR_sortlist):
        max_time = self.get_max_time()
        if self.direction == "Forward":
            start, end, step = 0, max_time, 1
        else:
            self.set_deadline(flow_PR_sortlist)
            start, end, step = max_time, -1, -1

        for time in range(start, end, step):
            if self.time_table.get(time) != None:
                for target_flow in flow_PR_sortlist:
                    for link1, packet in self.time_table[time].items():
                        if target_flow == packet["Flow"]:
                            self.set_flows(time, step, link1, packet)
           
    def flow_driving(self, flow_PR_sortlist): 
        max_time = self.get_max_time()
        if self.direction == "Forward":
            start, end, step = 0, max_time, 1
        else:
            self.set_deadline(flow_PR_sortlist)
            start, end, step = max_time, -1, -1

        for target_flow in flow_PR_sortlist:
            for time in range(start, end, step):
                if self.time_table.get(time) != None:
                    for link1, packet in self.time_table[time].items():
                        if target_flow == packet["Flow"]:
                            self.set_flows(time, step, link1, packet)

    def original(self, flow_PR_sortlist):
        #計算max_time
        max_time = self.get_max_time()

        for time in range(0,max_time):
            if self.time_table.get(time) != None:
                for target_flow in self.flow_dic.keys():
                    #依據當前時間所佔據在link上的Packets，取得他下一條是哪條link，並排程他近期可以占用的時間
                    for link1, packet in self.time_table[time].items():
                        if target_flow == packet["Flow"]:
                            target_time = time + 1
                            next_link = ()
                            #取得下一條link
                            for link2 in self.flow_paths_dic[packet["Flow"]]:
                                if link2["Ingress"] == link1[1]:
                                    next_link = (link2["Ingress"], link2["Egress"])
                                    break
                            #如果還沒到結束路徑(開始排他可以next_link最快可以占用的時間)
                            if next_link:
                                not_set = True
                                while not_set:
                                    if target_time >= packet["Tolerant"]:
                                        if packet["Flow"] not in self.fail_flows:
                                            self.fail_flows.append(packet["Flow"])   
                                        not_set = False
                                    #如果time+1沒有被建立
                                    elif self.time_table.get(target_time) == None:
                                        #建立link並將封包丟到time_slot裡面
                                        self.time_table[target_time] = {}
                                        self.time_table[target_time].update({next_link:packet})
                                        not_set = False
                                    else:
                                        #如果time+1已被建立但是裡面沒有該link(亦即無衝突)
                                        if self.time_table[target_time].get(next_link) == None:
                                            self.time_table[target_time][next_link] = packet
                                            not_set = False
                                        #如果time+1已被建立，且裡面有該Link存在(發生衝突)
                                        else:
                                            target_time += 1

    def set_deadline(self, flow_PR_sortlist):
        deadline_dic = {}
        for target_flow in flow_PR_sortlist:
            for time, data in reversed(self.time_table.items()):
                for first_link, packet in data.items():
                    if target_flow == packet["Flow"]:

                        last_link = (self.flow_paths_dic[packet["Flow"]][-1]["Ingress"], self.flow_paths_dic[packet["Flow"]][-1]["Egress"])
                        not_set = True
                        target_time = packet["Tolerant"]
                        while not_set:
                            #假如table沒有deadline的時間
                            if  target_time not in deadline_dic:
                                deadline_dic.update({target_time:{last_link:packet}})
                                not_set = False
                            elif last_link not in deadline_dic[target_time]:
                                deadline_dic[target_time].update({last_link:packet})
                                not_set = False
                            #假如table有deadline時間
                            else:
                                target_time -= 1        
            #加入時間表
        for time, data in deadline_dic.items():
            if time in self.time_table:
                self.time_table[time].update(data)
            else:
                self.time_table.update({time:data})

    def set_flows(self, time, step, link1, packet):
        if self.direction == "Forward":
            next_link = self.get_next_link(link1, packet)
            self.set_packet_next(time, step, next_link, packet)
        else:
            next_link = self.get_prev_link(link1, packet)
            self.set_packet_prev(time, step, next_link, packet)
        
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
     
    def set_packet_next(self, time, step, next_link, packet):

        target_time = time + step
        if next_link:
            not_set = True
            while not_set:
                if target_time >= packet["Tolerant"]:
                    if packet["Flow"] not in self.fail_flows:
                        self.fail_flows.append(packet["Flow"])   
                    not_set = False
                #如果time+1沒有被建立
                elif self.time_table.get(target_time) == None:
                    #建立link並將封包丟到time_slot裡面
                    self.time_table[target_time] = {}
                    self.time_table[target_time].update({next_link:packet})
                    not_set = False
                else:
                    #如果time+1已被建立但是裡面沒有該link(亦即無衝突)
                    if self.time_table[target_time].get(next_link) == None:
                        self.time_table[target_time][next_link] = packet
                        not_set = False
                    #如果time+1已被建立，且裡面有該Link存在(發生衝突)
                    else:
                        target_time += step

    def set_packet_prev(self, time, step, prev_link, packet):
        target_time = time + step
        if prev_link:
            not_set = True
            while not_set:
                if target_time <= packet["StartTime"]:
                    if packet["Flow"] not in self.fail_flows:
                        self.fail_flows.append(packet["Flow"])   
                    not_set = False
                #如果time+1沒有被建立
                elif self.time_table.get(target_time) == None:
                    #建立link並將封包丟到time_slot裡面
                    self.time_table[target_time] = {}
                    self.time_table[target_time].update({prev_link:packet})
                    not_set = False
                else:
            
                    if self.time_table[target_time].get(prev_link) == None:
                        self.time_table[target_time][prev_link] = packet
                        not_set = False
               
                    else:
                        target_time += step

    