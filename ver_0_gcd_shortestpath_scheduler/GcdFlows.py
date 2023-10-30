import math

class GcdFlows:
    def __init__(self, flow_dic, time_dic):
        self.multiple_flow_src = {} #     0   1   2   3  4  5  6  7
        self.multiple_flow_dst = {} #     Src Dst ST  PR P  T  S  D
        self.flow_dic = flow_dic    #{F1:(D1, D3, "", 2, 8, 5, 2, 8), F2:(D1, D4, "", 3, 9, 4, 3, 8),...}
        self.time_dic = time_dic    #(F1:[(D1, SW1, []), (SW1, SW2, []), (SW2, D3, [])], F2:[...], ...)
        self.size_dic_src = {}      #{('D1', 'size2'): ['F1', 'F2', 'F3'], ('D3', 'size3'): ['F4', 'F5', 'F6'], ...}
        self.size_dic_dst = {}      #{('D1', 'size2'): ['F1', 'F2', 'F3'], ('D3', 'size3'): ['F4', 'F5', 'F6'], ...}

    def run(self):
        self.find_same_equipment_flows()
        self.find_parallel_flow()
        #選出有GCD可同週期傳輸的flows
        src_gcdflows = self.check_gcd_srcflows()
        dst_gcdflows = self.check_gcd_dstflows()
        return src_gcdflows, dst_gcdflows

    def find_same_equipment_flows(self):
        reserved_src = []
        reserved_dst = []
        for flow_id, (src, dst, *remaining) in self.flow_dic.items():
            if src not in reserved_src :                           #如果src沒有在list裡面
                reserved_src.append(src)                           #將src存入
                self.multiple_flow_src[src] = []                   #若鍵不存在，則初始化清單
            self.multiple_flow_src[src].append(flow_id)
            #print(self.multiple_flow_src)
            
        for flow_id, (src, dst, *remaining) in self.flow_dic.items():
            if dst not in reserved_dst:
                reserved_dst.append(dst)
                self.multiple_flow_dst[dst] = []                   # 若鍵不存在，則初始化清單
            self.multiple_flow_dst[dst].append(flow_id)
            #print(self.multiple_flow_dst)

    #這邊會根據flow的size及period來判斷flows是否可在生命週期內同時進行
    def find_parallel_flow(self):               
        for equipment, flow_list in self.multiple_flow_src.items():
            for flow in flow_list:
                #在size_dic裡面key值為size value為儲存
                self.size_dic_src[equipment, f"size{self.flow_dic[flow]['Src']}"] = []    
            for flow in flow_list:
                self.size_dic_src[equipment, f"size{self.flow_dic[flow]['Src']}"].append(flow)
        for equipment, flow_list in self.multiple_flow_dst.items():
            for flow in flow_list:
                #在size_dic裡面key值為size value為儲存
                self.size_dic_dst[equipment, f"size{self.flow_dic[flow]['Src']}"] = []    
            for flow in flow_list:
                self.size_dic_dst[equipment, f"size{self.flow_dic[flow]['Src']}"].append(flow)
        # 需要刪除的keys(src)
        keys_to_delete = []
        for key, value in self.size_dic_src.items():
            if len(value) == 1:
                keys_to_delete.append(key)
        for key in keys_to_delete:
            del self.size_dic_src[key]
        # 需要刪除的keys(dst)    
        keys_to_delete = []
        for key, value in self.size_dic_dst.items():
            if len(value) == 1:
                keys_to_delete.append(key)
        for key in keys_to_delete:
            del self.size_dic_dst[key]

    def check_gcd_srcflows(self):
        gcd_list = []
        for keys, value in self.size_dic_src.items():
            gcd_tuple = ()                                              # 初始化tuple
            for flow in value:
                if len(gcd_tuple) == 0:
                    gcd_tuple = (flow,)
                elif math.gcd(self.flow_dic[gcd_tuple[0]]["Period"]//self.flow_dic[gcd_tuple[0]]["Size"], self.flow_dic[flow]["Period"]//self.flow_dic[flow]["Size"]) >= 2:
                    gcd_tuple = gcd_tuple + (flow,)                     # 新增flow到tuple裡面
                 
            if len(gcd_tuple) > 1:                                      # Check if there's any remaining data in gcd_tuple
                gcd_list.append(gcd_tuple)

        return gcd_list
    
    def check_gcd_dstflows(self):
        gcd_list = []
        for keys, value in self.size_dic_dst.items():
            gcd_tuple = ()                                              # 初始化tuple
            for flow in value:
                if len(gcd_tuple) == 0:
                    gcd_tuple = (flow,)
                elif math.gcd(self.flow_dic[gcd_tuple[0]]["Period"]//self.flow_dic[gcd_tuple[0]]["Size"], self.flow_dic[flow]["Period"]//self.flow_dic[flow]["Size"]) >= 2:
                    gcd_tuple = gcd_tuple + (flow,)                     # 新增flow到tuple裡面

            if len(gcd_tuple) > 1:                                      # Check if there's any remaining data in gcd_tuple
                gcd_list.append(gcd_tuple)

        return gcd_list
    
    #這邊可能要修一下





