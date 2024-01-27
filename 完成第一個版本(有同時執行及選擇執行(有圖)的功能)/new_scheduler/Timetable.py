#flow_packet = {1:F1_0, 2:F1_1,....}
class TimeTable:
    
    def __init__(self):
        self.time_table = {}
        self.fail_flows = []

    
    def fail_flow_refilt(self, fail_flow):
        pop_dic = {}
        for flow in fail_flow:
            for time, data in self.time_table.items():
                    
                for link, packet in data.items():
                    if flow == packet["Flow"]:
                        #print(f"time = {time}, link = {link}   flow = {flow}")
                        if pop_dic.get(time)==None:
                            pop_dic[time] = []
                        pop_dic[time].append(link)
        for time, data in self.time_table.items():
            for time_p, links in pop_dic.items():
                for link in links:
                    if time == time_p and link in data.keys():
                        self.time_table[time].pop(link)
                       # print(f"del   {time} {link}   packet")
                  
        
        


