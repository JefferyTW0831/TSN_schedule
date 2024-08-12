
import new_scheduler.Genarators as Genarators



class InitFlowFilter:
    def __init__(self, flow_dic, flow_paths_dic, time_table_maintainer, sort_mode):
        self.flow_dic = flow_dic
        self.flow_paths_dic = flow_paths_dic
        self.time_table_maintainer = time_table_maintainer
        self.fail_flows = []
        self.sort_mode = sort_mode
   
    #應該要將比較方法放在時間表(time_table)裡面進行，會有比較高的可調整性。(但這邊想說一次處理，先利用path_dic執行看看，之後有機會再做模組化調整)
    def init_flows_filter(self, flow_PR_sortlist): 
    #    print(f"-------------------InitFlowFilter----------------------")
     
        # print(flow_PR_sortlist)
        
        for flow in flow_PR_sortlist:
            first_link = self.flow_paths_dic[flow][0]
            time_list = Genarators.genarate_time_slot(flow, self.flow_dic)
            set_fail = self.time_table_maintainer.set_firstlink_to_time_table(first_link, time_list)
            if set_fail:
                self.fail_flows.append(flow)
                
    #    print(f"-------------------------------------------------------")


    


    