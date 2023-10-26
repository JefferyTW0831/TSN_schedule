class ScheduleMiddle:

    def __init__(self, flow_dic, flow_paths_dic):
        self.flow_dic = flow_dic
        self.flow_paths_dic = flow_paths_dic
        
    def schedule_middle(self):                  

        common_link = self.classify_links()
        print("\n\n------------------------------")
        print(f"(ScheduleMiddle.py)\n")
        for c_link, c_list in common_link.items():
            print(f"{c_link}={c_list}")
        print("-------------------------------")

        for c_link, c_list in common_link.items():
            if len(c_list) > 1:
                self.common_path_bubble_sort(c_link, c_list)
        self.genarate_active_time_slot(common_link)                                                         #感覺還是要另一個方式整理出來
        
    def classify_links(self):
        common_link = {}
        remove = []
        for flow_name, flow_path in self.flow_paths_dic.items():
            for link in flow_path:
                if not link.get('Time'):
                    key = (link["Ingress"], link["Egress"])
                    if key not in common_link:
                        common_link[(link["Ingress"], link["Egress"])] = []
                        common_link[(link["Ingress"], link["Egress"])].append(flow_name)
                    else:
                        common_link[(link["Ingress"], link["Egress"])].append(flow_name)

        return common_link
    
    def common_path_bubble_sort(self, c_link, c_list):  
        #依照path剩餘links數，較短的先排
        for i in range(len(c_list)-1):
            for j in range(len(c_list)-1-i):
                #EX. F3:path=5, F1:path=3
                remaining_j =  self.search_key_index(c_link, c_list[j])
                remaining_j_1 = self.search_key_index(c_link, c_list[j+1])
                if remaining_j > remaining_j_1:
                     c_list[j], c_list[j + 1] = c_list[j + 1], c_list[j]

    def search_key_index(self, link, flow):
        for index, link_dict in enumerate(self.flow_paths_dic[flow]):
            if link[0] == link_dict["Ingress"] and link[1] == link_dict["Egress"]:
                return len(self.flow_paths_dic[flow])-index-1


    def genarate_active_time_slot(self, common_link):
        not_organize_link = {}
        for link, flow_list in common_link.items():
            for flow in flow_list:
                for path in self.flow_paths_dic[flow]:
                    if link[0] == path["Egress"]:
                        prev_link_time = path["Time"]           
                        #prev_link_time沿用到要設定的link上(之後視情況多變數存)
                        this_link_time = self.time_add_one_bias(prev_link_time)
                        
                    if link[0] == path["Ingress"] and link[1] == path["Egress"]:
                        if not this_link_time:
                            not_organize_link[flow] = path
                        else:
                            path["Time"] = this_link_time
        for flow, link in not_organize_link.items():
            for path in self.flow_paths_dic[flow]:
                if link["Ingress"] == path["Egress"]:
                    prev_link_time = path["Time"]
                    this_link_time = self.time_add_one_bias(prev_link_time)
                if link["Ingress"] == path["Ingress"] and link["Egress"] == path["Egress"]:
                    path["Time"] = this_link_time
                    
    def time_add_one_bias(self, prev_time_dict):
        this_time_dict = {}
        for time, flow_size_bias in prev_time_dict.items():
            this_time_dict[int(time)+1] = flow_size_bias
        return this_time_dict
        
                
                    