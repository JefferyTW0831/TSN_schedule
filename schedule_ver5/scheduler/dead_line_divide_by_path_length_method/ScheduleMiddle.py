#這邊方法採用最笨的排法，也就是依照flow編號排下去，編號前面的優先度較高
import copy
class ScheduleMiddle:

    def __init__(self, flow_dic, flow_paths_dic, time_table_maintainer):
        self.flow_dic = flow_dic
        self.flow_paths_dic = flow_paths_dic
        self.time_table = time_table_maintainer.time_table  #dict
        
    def schedule_middle(self):
        reschedule = {}
        for time in range(0,101):
            
            if self.time_table.get(time) != None:
                if self.time_table.get(time+1) == None:
                    self.time_table[time+1] = {}
                next_schedule = {}
                #依據當前時間所佔據在link上的Packets，取得他下一條是哪條link，並排程他近期可以占用的時間
                #某時間中某些link有packet
                for link1, packet in self.time_table[time].items():
                    #從packet內取得flow資訊
                    for link2 in self.flow_paths_dic[packet["Flow"]]:
                        #依照flow&link從path_dic取得下一條link資訊
                        if link2["Ingress"] == link1[1]:
                            #查看下個時間點的link受否有占用(查看next_schedule)
                            if next_schedule.get((link2["Ingress"], link2["Egress"])) != None:
                                #有占用的話就比較PR大小(如果當前的packet要取代已保留的，這樣的話已保留的就要在更之後去放置)
                                if packet["PiorityWeiget"] < next_schedule[(link2["Ingress"], link2["Egress"])]["PiorityWeiget"]:
                                    reschedule[(link2["Ingress"], link2["Egress"])] = {}
                                    reschedule[(link2["Ingress"], link2["Egress"])] = copy.deepcopy(next_schedule[(link2["Ingress"], link2["Egress"])])
                                    next_schedule[(link2["Ingress"], link2["Egress"])] = packet
                            else:
                                next_schedule[(link2["Ingress"], link2["Egress"])] = packet
            
            add_to_next = {}
            if reschedule:
                for re_link, re_packet in reschedule.items():
                    for next_link, next_packet in next_schedule.items():
                        #如果有發現相同link
                        if re_link == next_link:
                            if re_packet["PiorityWeiget"] < next_packet["PiorityWeiget"]:
                                reschedule[re_link], next_schedule[next_link] = next_schedule[next_link], reschedule[re_link]
                        #如果link不同，則reschedule可以排入時間表
                        else:
                           add_to_next[re_link] = re_packet
                                
                    
            else:                   
                if add_to_next:
                    next_schedule.update(add_to_next)
                for link, packet in next_schedule.items():
                    self.time_table[time+1].update({link:packet})
                
                
                
    
                                    
                            
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
      