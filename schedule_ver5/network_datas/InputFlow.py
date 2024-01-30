import json

class InputFlow:

    def __init__(self):
        self.max_time = None
        self.flow_dic = None
        
    def run(self):
        with open('network_datas/flow_data.json', 'r') as json_file:
            self.flow_dic = json.load(json_file)
            return self.flow_dic
        
    def cal_max_time(self):
        max_value = None
        for flow, data in self.flow_dic.items():
            flow_deadline_time = data["StartTime"]+data["Period"]*(data["Times"]-1)+data["Deadline"]
            if max_value == None or flow_deadline_time > max_value:
                max_value = flow_deadline_time
        return max_value

