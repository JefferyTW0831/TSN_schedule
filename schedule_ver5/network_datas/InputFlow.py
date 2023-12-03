import json

class InputFlow:

    def __init__(self):
        pass
        
        
    def run(self):
        with open('c:\\Users\\jeffe\\OneDrive\\桌面\\雲端硬碟資料夾\\report\\地安\\TSN_schedule\\schedule_ver5\\network_datas\\flow_data.json', 'r') as json_file:
            flow_dic = json.load(json_file)
            return flow_dic
