#這邊方法採用最笨的排法，也就是依照flow編號排下去，編號前面的優先度較高
class ScheduleMiddle:

    def __init__(self, flow_dic, flow_paths_dic, time_table_maintainer):
        self.flow_dic = flow_dic
        self.flow_paths_dic = flow_paths_dic
        self.time_table = time_table_maintainer.time_table  #dict
        self.fail_flow = []
    
        
    def schedule_middle(self, flow_PR_sortlist):
        self.set_deadline(flow_PR_sortlist)
        max_time = self.get_max_time()
        for time in range (max_time,-1,-1):
            if self.time_table.get(time) != None:
                for target_flow in flow_PR_sortlist:
                    for link1, packet in self.time_table[time].items():
                        if target_flow == packet["Flow"]:
                            target_time = time - 1
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
                                not_set = True
                                while not_set:
                                    if target_time <= packet["StartTime"]:
                                        if packet['Flow'] not in self.fail_flow:
                                            self.fail_flow.append(packet['Flow'])   
                                        not_set = False
                                #如果time+1沒有被建立
                                    elif self.time_table.get(target_time) == None:
                                        #建立link並將封包丟到time_slot裡面
                                        self.time_table[target_time] = {}
                                        self.time_table[target_time].update({prev_link:packet})
                                        not_set = False
                                    else:
                                        #如果time+1已被建立但是裡面沒有該link(亦即無衝突)
                                        if self.time_table[target_time].get(prev_link) == None:
                                            self.time_table[target_time][prev_link] = packet
                                            not_set = False
                                        else:
                                            target_time -= 1        
            
    def get_max_time(self):
        max_value = None
        for flow, data in self.flow_dic.items():
            flow_deadline_time = data["StartTime"]+data["Period"]*(data["Times"]-1)+data["Deadline"]
            if max_value == None or flow_deadline_time > max_value:
                max_value = flow_deadline_time
                max_flow = flow
        print(f"Max_time : {max_flow, max_value}")
        return max_value  
    
    def set_deadline(self, flow_PR_sortlist):
        deadline_dic = {}
        for target_flow in flow_PR_sortlist:
            for time, data in reversed(self.time_table.items()):
                for first_link, packet in data.items():
                    if target_flow == packet["Flow"]:
                        
                        last_link = (self.flow_paths_dic[packet["Flow"]][-1]["Ingress"], self.flow_paths_dic[packet["Flow"]][-1]["Egress"])
                        not_set = True
                        target_time = packet["Tolerant"]
                        #print(f"{packet['Flow'], packet['Packet'], target_time}")
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
                
            
         

