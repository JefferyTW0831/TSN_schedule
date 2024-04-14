from collections import defaultdict
import new_scheduler.Genarators as Genarators



class InitFlowFilter:
    def __init__(self, flow_dic, flow_paths_dic, time_table_maintainer, sort_mode):
        self.flow_dic = flow_dic
        self.flow_paths_dic = flow_paths_dic
        self.time_table_maintainer = time_table_maintainer
        self.sort_mode = sort_mode
   
    #應該要將比較方法放在時間表(time_table)裡面進行，會有比較高的可調整性。(但這邊想說一次處理，先利用path_dic執行看看，之後有機會再做模組化調整)
    def init_flows_filter(self, flow_PR_sortlist): 

        if self.sort_mode == 1:
            self.original()
        elif self.sort_mode == 2:
            self.weight(flow_PR_sortlist)
        #設計第三種方法：先找出衝突組合，每個組合裡擁有最多的flows的子組合將勝選
        else:
            self.gcd_weight(flow_PR_sortlist)

        
    def original(self):
        for flow, path in self.flow_paths_dic.items():  
            time_list = Genarators.genarate_time_slot(flow, self.flow_dic)
            self.time_table_maintainer.set_firstlink_to_time_table(path[0], time_list)

    def weight(self, flow_PR_sortlist):
        for flow in flow_PR_sortlist:
            first_link = self.flow_paths_dic[flow][0]
            time_list = Genarators.genarate_time_slot(flow, self.flow_dic)
            self.time_table_maintainer.set_firstlink_to_time_table(first_link, time_list)
        print(f"flow_PR_list = {flow_PR_sortlist}\n")

    def gcd_weight(self,flow_PR_sortlist):
        not_collision_group = self.find_not_collision_flows_groups()
        print(f"group = {not_collision_group}")
        for flow in not_collision_group:
            if flow in flow_PR_sortlist:
                first_link = self.flow_paths_dic[flow][0]
                time_list = Genarators.genarate_time_slot(flow, self.flow_dic)
                self.time_table_maintainer.set_firstlink_to_time_table(first_link, time_list)
                flow_PR_sortlist.remove(flow)
        for flow in flow_PR_sortlist:
            first_link = self.flow_paths_dic[flow][0]
            time_list = Genarators.genarate_time_slot(flow, self.flow_dic)
            self.time_table_maintainer.set_firstlink_to_time_table(first_link, time_list)
        print(f"\nflow_PR_list = {flow_PR_sortlist}")


    def find_not_collision_flows_groups(self):
        remaining_flows = list(self.flow_dic.keys())
        temp_dict = {}
        time = 1 
        for flow in remaining_flows:
            first_link = self.flow_paths_dic[flow][0]
            time_list = Genarators.genarate_time_slot(flow, self.flow_dic)
            if temp_dict.get((first_link["Ingress"], first_link["Egress"])) != None:
                temp_dict[(first_link["Ingress"], first_link["Egress"])].update({flow:list(time_list.keys())})
            else:
                temp_dict.update({(first_link["Ingress"], first_link["Egress"]):{flow:list(time_list.keys())}})

        #印一下細節：
        for link , flow_time in temp_dict.items():
            print(f"link = {link}")
            for flow, time in flow_time.items():
                print(f"{flow, time}")

        group = []
        #挑選出沒衝突的組合
        for link, flow_time in temp_dict.items():
            keys = list(flow_time.keys())
            for i in range(len(keys)):
                for j in range(i + 1, len(keys)):
                    key1 = keys[i]
                    key2 = keys[j]
                    list1 = flow_time[key1]
                    list2 = flow_time[key2]
                    intersection = set(list1) & set(list2)
                    if not intersection:
                        print(f"{key1} 和 {key2} 沒有共同數字")
                        group.append(key1)
                        group.append(key2)
        return group


   