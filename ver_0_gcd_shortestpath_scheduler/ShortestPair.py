

class ShortestPair:
    def __init__(self, flow_dic, path_dic, gcd_srcflows, gcd_dstflows):
        self.flow_dic = flow_dic
        self.path_dic = path_dic
        self.gcd_srcflows = gcd_srcflows
        self.gcd_dstflows = gcd_dstflows
    
    def shortest_life_flows_pair(self):
        src_shortest_pair = {}
        dst_shortest_pair = {}

        if len(self.gcd_srcflows) > 0:
            for flow in self.gcd_srcflows:
                life_time = max(self.flow_dic[flow[0]]["Times"]*self.flow_dic[flow[0]]["Deadline"], self.flow_dic[flow[1]]["Times"]*self.flow_dic[flow[1]]["Deadline"])
                if len(src_shortest_pair) == 0:
                    src_shortest_pair[flow] = life_time
                elif life_time < min(src_shortest_pair.values()):
                    src_shortest_pair.clear()  # 清除之前的最小值
                    src_shortest_pair[flow] = life_time

        if len(self.gcd_dstflows) > 0:
            for flow in self.gcd_dstflows:
                life_time = max(self.flow_dic[flow[0]]["Times"]*self.flow_dic[flow[0]]["Deadline"], self.flow_dic[flow[1]]["Times"]*self.flow_dic[flow[1]]["Deadline"])
                if len(dst_shortest_pair) == 0:
                    dst_shortest_pair[flow] = life_time
                    
                elif life_time < min(src_shortest_pair.values()):
                    dst_shortest_pair.clear()  # 清除之前的最小值
                    dst_shortest_pair[flow] = life_time

        if src_shortest_pair and dst_shortest_pair :
            if min(src_shortest_pair.values()) < min(dst_shortest_pair.values()):
                return src_shortest_pair
            elif min(src_shortest_pair.values()) > min(dst_shortest_pair.values()):
                return dst_shortest_pair
        elif src_shortest_pair:
            return src_shortest_pair
        else:
            return dst_shortest_pair

    def reconstruct_pair_flow(self, pair_flow):
        if len(next(iter(pair_flow.keys()))) > 2: 
            key = next(iter(pair_flow.keys()))[:2]
            value = next(iter(pair_flow.values()))
            pair_flow = {key: value}
        return pair_flow