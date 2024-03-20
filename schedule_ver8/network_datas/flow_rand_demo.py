import json


def main():
    with open('network_datas/flow_data.json', 'r') as json_file:
        flow_dic = json.load(json_file)
    demo_flows(flow_dic)    
    
    
    
def demo_flows(flow_dic):
    for flow, attr in flow_dic.items():
        print(f"flow = {flow}")
        print(f"attr = {attr}")
    
    
main()