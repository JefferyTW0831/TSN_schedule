#這邊方法採用最笨的排法，也就是依照flow編號排下去，編號前面的優先度較高
class ScheduleMiddle:

    def __init__(self, flow_dic, flow_paths_dic, time_table_maintainer):
        self.flow_dic = flow_dic
        self.flow_paths_dic = flow_paths_dic
        self.time_table = time_table_maintainer.time_table  #dict
        self.fail_flow = []



    def schedule_middle(self):
        reschedule = {}
        #計算max_time
        max_time = self.get_max_time()

        for time in range(0,max_time):

            if self.time_table.get(time) != None:
                #依據當前時間所佔據在link上的Packets，取得他下一條是哪條link，並排程他近期可以占用的時間
                for link1, packet in self.time_table[time].items():
                    next_link = ()
                    #取得下一條link
                    for link2 in self.flow_paths_dic[packet["Flow"]]:
                        if link2["Ingress"] == link1[1]:
                            next_link = (link2["Ingress"], link2["Egress"])
                            break
                    #如果還沒到結束路徑(開始排他可以next_link最快可以占用的時間)
                    if next_link:
                        #如果time+1沒有被建立
                        if self.time_table.get(time+1) == None:
                            #建立link並將封包丟到time_slot裡面
                            self.time_table[time+1] = {}
                            self.time_table[time+1].update({next_link:packet})
                            
                        else:
                            #如果time+1已被建立但是裡面沒有該link(亦即無衝突)
                            if self.time_table[time+1].get(next_link) == None:
                                self.time_table[time+1][next_link] = packet
                            #如果time+1已被建立，且裡面有該Link存在(發生衝突)
                            else:
                                if reschedule.get(time+1) == None:
                                    reschedule[time+1] = {}
                                reschedule[time+1].update({next_link:packet})
        if reschedule:
            #print(f"\n\n重新排程：{reschedule}\n")
            self.rescheduling(reschedule)
    
    def get_max_time(self):
        max_value = None
        for flow, data in self.flow_dic.items():
            flow_deadline_time = data["StartTime"]+data["Period"]*(data["Times"]-1)+data["Deadline"]
            if max_value == None or flow_deadline_time > max_value:
                max_value = flow_deadline_time
                max_flow = flow
        print(f"Max_time : {max_flow, max_value}")
        return max_value

    def rescheduling(self, reschedule):
        print(f"\n\n重新排程：\n")
        for time, data in reschedule.items():
            print(time, data)
        remaining_schedule = {}
        for time, link_dic in reschedule.items():
            for link, packet in link_dic.items():
                set_up = True
                while set_up:
                    if self.time_table.get(time) == None:
                        self.time_table[time] = {}
                        self.time_table[time][link] = packet
                        if time >= packet["Tolerant"]:
                            if packet['Flow'] not in self.fail_flow:
                                self.fail_flow.append(packet['Flow'])   
                        set_up = False
                    else:
                        if self.time_table[time].get(link) == None:
                            self.time_table[time][link] = packet
                            if time >= packet["Tolerant"]:
                                if packet['Flow'] not in self.fail_flow:
                                    self.fail_flow.append(packet['Flow'])
                            set_up = False
                        else:
                            time += 1
                            
     
                for link2 in self.flow_paths_dic[packet["Flow"]]:
                    next_link = ()
                    if link2["Ingress"] == link[1]:
                        next_link = (link2["Ingress"], link2["Egress"])
                        break
                if next_link:
                    if remaining_schedule.get(time+1) == None:
                        remaining_schedule[time+1] = {next_link:packet}
                    else:
                        remaining_schedule[time+1].update({next_link:packet})
                       
        if remaining_schedule:
            self.rescheduling(remaining_schedule)
       # print(f"剩餘的：schedule = {remaining_schedule}")   
