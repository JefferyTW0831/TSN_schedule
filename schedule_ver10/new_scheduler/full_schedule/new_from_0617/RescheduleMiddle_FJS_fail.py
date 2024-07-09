import new_scheduler.Genarators as Genarators
from new_scheduler.full_schedule.LinkTimeDict import LinkTimeDict 
class RescheduleMiddle:
    def __init__(self, flow_dic, flow_paths_dic, time_table_maintainer, driving_mode, direction):
        self.flow_dic = flow_dic
        self.flow_paths_dic = flow_paths_dic
        self.time_table_maintainer = time_table_maintainer
        self.fail_flows = []
        self.link_record = {}                           #紀錄link已經使用的時間戳
        
        self.driving_mode = driving_mode
        self.direction = direction

    def schedule_middle(self, flow, time_list):
        
        all_link = [(link["Ingress"], link["Egress"]) for link in self.flow_paths_dic[flow]]
        remaining_link = all_link[1:]
        next_start = self.flow_dic[flow]["Size"]
        #設定暫存link_time_dic資訊
        temp_time_dict = {}
        for period_start in time_list[::next_start]:
            #第N個period
            up_count = 1  
            change_link_start = period_start
            for link in remaining_link:
                if self.link_record.get(link) == None:
                    self.link_record.update({link:LinkTimeDict()})
                #第N條link
                link_start = change_link_start+up_count
                link_deadline = link_start + self.flow_dic[flow]["Deadline"]-len(remaining_link)
                for count in range(0,next_start):
                    #第N個packet
                    packet = self.time_table_maintainer.time_table[period_start+count][all_link[0]]  
                    #packet預計要放的時間
                    time = self.link_record[link].time_dic.get(link_start+count)

                    #排入時間表(確定可排入) 
                    #有空時間直接排
                    if  time == None:
                        time = link_start+count
                        self.time_table_maintainer.setup_time_and_link(time, link, packet) 
                    #延後到可排的時間排入
                    elif time < link_deadline:
                        self.time_table_maintainer.setup_time_and_link(time, link, packet) 
                    #超過deadline(不排入時間表，取消排程)                
                    else:
                        return 
                    if count == 0:
                        change_link_start = time

                    #設定暫存link_time_dic資訊
                    if link not in temp_time_dict:
                        temp_time_dict[link] = []
                    else:
                        temp_time_dict[link].append(time)
                up_count += 1
        #若沒有return，更新LinkTimeDict
        for link, time_list in temp_time_dict.items():
            for time in time_list:
                self.link_record[link].run(time)




  