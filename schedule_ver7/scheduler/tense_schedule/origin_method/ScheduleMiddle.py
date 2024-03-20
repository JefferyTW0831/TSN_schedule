#這邊方法採用最笨的排法，也就是依照flow編號排下去，編號前面的優先度較高
class ScheduleMiddle:

    def __init__(self, flow_dic, flow_paths_dic, time_table_maintainer):
        self.flow_dic = flow_dic
        self.flow_paths_dic = flow_paths_dic
        self.time_table = time_table_maintainer.time_table  #dict
        self.fail_flow = []
        
    def schedule_middle(self):
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
                                        if packet['Flow'] not in self.fail_flow:
                                            self.fail_flow.append(packet['Flow'])   
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
      
    def get_max_time(self):
        max_value = None
        for flow, data in self.flow_dic.items():
            flow_deadline_time = data["StartTime"]+data["Period"]*(data["Times"]-1)+data["Deadline"]
            if max_value == None or flow_deadline_time > max_value:
                max_value = flow_deadline_time
                max_flow = flow
        print(f"Max_time : {max_flow, max_value}")
        return max_value