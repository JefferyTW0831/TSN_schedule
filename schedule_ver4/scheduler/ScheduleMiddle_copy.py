#這邊方法採用最笨的排法，也就是依照flow編號排下去，編號前面的優先度較高
class ScheduleMiddle:

    def __init__(self, flow_dic, flow_paths_dic, time_table_maintainer):
        self.flow_dic = flow_dic
        self.flow_paths_dic = flow_paths_dic
        self.time_table = time_table_maintainer.time_table  #dict
        
    def schedule_middle(self):                  
        catch_packets_to_next_link = {}
        fail_packets = {}

        for time in range(0,101):
                #把預處理的flow加入下一條link
                if catch_packets_to_next_link:
                    if self.time_table.get(time) == None:
                        self.time_table[time] = {}
                    for link, packet in catch_packets_to_next_link.items():
                        if link not in self.time_table[time]:
                            self.time_table[time][link] = packet
                catch_packets_to_next_link = {}

                if self.time_table.get(time) != None:
                    for link1, packet in self.time_table[time].items():
                        next_link = ()
                        #取得下一條link
                        for link2 in self.flow_paths_dic[packet["Flow"]]:
                            if link2["Ingress"] == link1[1]:
                                next_link = (link2["Ingress"], link2["Egress"])
                                break
                        #如果還沒到結束路徑
                        if next_link:
                            if catch_packets_to_next_link.get(next_link) == None:
                                catch_packets_to_next_link[next_link] = packet
                            else:
                                self.reschedule_failed_packets({time+2:(next_link, packet)})

       
        

    def reschedule_failed_packets(self, fail_packets):
        for time, (next_link, packet) in fail_packets.items():
            while time < 100:  # 限制在時間範圍內，這裡假設總時間是100
                time += 1
                if self.time_table.get(time) == None:
                    self.time_table[time] = {}

                if next_link not in self.time_table[time]:
                    self.time_table[time][next_link] = packet
                    break
                
                    