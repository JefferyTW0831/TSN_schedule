#這邊方法採用最笨的排法，也就是依照flow編號排下去，編號前面的優先度較高
class ScheduleMiddle:

    def __init__(self, flow_dic, flow_paths_dic, time_table_maintainer):
        self.flow_dic = flow_dic
        self.flow_paths_dic = flow_paths_dic
        self.time_table = time_table_maintainer.time_table  #dict
        self.fail_flow = []
        
    def schedule_middle(self):
        reschedule = {}
        self.set_deadline()
      
        for time in range (201,-1,-1):
            if self.time_table.get(time) != None:
                for link1, packet in self.time_table[time].items():
                    prev_link = ()
                    #取得上一條link
                    for link2 in self.flow_paths_dic[packet["Flow"]]:
                        if link2["Egress"] == link1[0]:
                            #假如找到first_link要取消掉
                            if link2 == self.flow_paths_dic[packet["Flow"]][0]:
                                break
                            prev_link = (link2["Ingress"], link2["Egress"])
                            break
                    #如果還沒到結束路徑(開始排他可以next_link最快可以占用的時間)
                    if prev_link:
                        #如果time+1沒有被建立
                        if self.time_table.get(time-1) == None:
                            #建立link並將封包丟到time_slot裡面
                            self.time_table[time-1] = {}
                            self.time_table[time-1].update({prev_link:packet})
                        else:
                            #如果time+1已被建立但是裡面沒有該link(亦即無衝突)
                            if self.time_table[time-1].get(prev_link) == None:
                                self.time_table[time-1][prev_link] = packet
                            else:
                                if reschedule.get(time-1) == None:
                                    reschedule[time-1] = {}
                                reschedule[time-1].update({prev_link:packet})
                    
        if reschedule:
            self.rescheduling(reschedule)
       


    def rescheduling(self, reschedule):
        
        remaining_schedule = {}
        for time, link_dic in reschedule.items():
            for link, packet in link_dic.items():
                set_up = True
                while set_up:
                    if self.time_table.get(time) == None:
                        self.time_table[time] = {}
                        self.time_table[time][link] = packet
                        if time <= packet["StartTime"]:
                                if packet['Flow'] not in self.fail_flow:
                                    self.fail_flow.append(packet['Flow'])  
                        set_up = False
                    else:
                        if self.time_table[time].get(link) == None:
                            self.time_table[time][link] = packet
                            if time <= packet["StartTime"]:
                                if packet['Flow'] not in self.fail_flow:
                                    self.fail_flow.append(packet['Flow'])  
                        
                            set_up = False
                        else:
                            time -= 1
     
                for link2 in self.flow_paths_dic[packet["Flow"]]:
                    prev_link = ()
                    if link2["Egress"] == link[0]:
                        if link2 == self.flow_paths_dic[packet["Flow"]][0]:
                            break
                        prev_link = (link2["Ingress"], link2["Egress"])
                        break
                
                if prev_link:
                    print(f"繼續重排：{time}, {prev_link}, {packet}")
                    if remaining_schedule.get(time-1) == None:
                        remaining_schedule[time-1] = {prev_link:packet}
                    else:
                        remaining_schedule[time-1].update({prev_link:packet})
                       
        if remaining_schedule:
            self.rescheduling(remaining_schedule)




        
    
    def set_deadline(self):
        deadline_dic = {}
        reschedule_flows = {}
       
        for time, data in self.time_table.items():
            for first_link, packet in data.items():
                last_link = (self.flow_paths_dic[packet["Flow"]][-1]["Ingress"], self.flow_paths_dic[packet["Flow"]][-1]["Egress"])
                #假如table沒有deadline的時間
                if  packet["Tolerant"] not in deadline_dic:
                    deadline_dic.update({packet["Tolerant"]:{last_link:packet}})
                elif last_link not in deadline_dic[packet["Tolerant"]]:
                    deadline_dic[packet["Tolerant"]].update({last_link:packet})
                else:
                    if reschedule_flows.get(last_link) == None:
                        reschedule_flows[last_link] = []
                    reschedule_flows[last_link].append(packet)
        #加入時間表
        for time, data in deadline_dic.items():
            if time in self.time_table:
                self.time_table[time].update(data)
            else:
                self.time_table.update({time:data})
        #重新考慮
        if reschedule_flows:
            for link, packet in reschedule_flows.items():
                print(link, packet)
            self.deadline_reschedule(reschedule_flows)

    def deadline_reschedule(self, reschedule):
        for link, packets_list in reschedule.items():
            for packet in packets_list:

                #packet未排好
                Set = False 
                for time in range(packet['Tolerant'], packet["StartTime"],-1):

                    if self.time_table.get(time) == None:
                        self.time_table.update({time:{}})
      
                    if link not in self.time_table[time].keys():
                        self.time_table[time][link] = packet
                        Set = True
                        break
                #如果packet還是沒排程到
                if Set == False and packet["Flow"] not in self.fail_flow:
                    print(" NOT SET!!")
                    self.fail_flow.append(packet["Flow"])

