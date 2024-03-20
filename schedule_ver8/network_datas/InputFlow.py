import json

class InputFlow:

    def __init__(self):
        self.max_time = None
        self.flow_dic = None
        
    def run(self):
        with open('network_datas/flow_data.json', 'r') as json_file:
            self.flow_dic = json.load(json_file)
            return self.flow_dic
        
    

