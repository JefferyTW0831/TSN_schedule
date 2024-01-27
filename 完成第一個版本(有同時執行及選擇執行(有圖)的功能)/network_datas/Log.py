import json
from .InputFlow import InputFlow

class Log:
    def __init__(self, table_data):
        self.table_data = table_data
        input_flow = InputFlow()
        flow_dic = input_flow.run()
        self.max_time = self.get_max_time(flow_dic)
    
        
    def log_processor(self):
        print(f"log = ")
        for time in range(0, self.max_time):
            if self.table_data.get(time) != None:
                print("")
                print(f"Time : {time}")
                print("-------------------------")
                for link, packet in self.table_data[time].items():
                    print(f"{link} flow={packet['Flow']}")
       
                
    #不做output了，我的鍵不是int不然就是tuple，要再全部重新換成str格式會有點小麻煩
    # def log_output(self):
    #     print(f"{self.saved_table}")
    #     with open("log.json", "w") as fp:
    #         json.dump(self.saved_table, fp)
           

    def get_max_time(self, flow_dic):
        max_value = None
        for flow, data in flow_dic.items():
            flow_deadline_time = data["StartTime"]+data["Period"]*(data["Times"]-1)+data["Deadline"]
            if max_value == None or flow_deadline_time > max_value:
                max_value = flow_deadline_time
                max_flow = flow
        print(f"Max_time : {max_flow, max_value}")
        return max_value