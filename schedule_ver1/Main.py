from InputFlow import InputFlow
from scheduler.Scheduler import Scheduler
from Topology import Topology

#from ResourceUsagePlot import ResourceUsagePlot

def main():
    input_flow = InputFlow()                                        #讀取flow參數                       OK
    flow_dic = input_flow.run()

    topology = Topology(flow_dic)                                   #建構拓樸(假設已從CUC得到拓樸資訊)    OK
    topology.routing()                                              #得到每個flow的路徑流向

    # print(f"流字典 : ")
    # for key, value in topology.flow_dic.items():
    #     print(f"{key}: {value}")
    # print(f"鏈節字典 : ")
    # for key, value in topology.links.items():
    #     print(f"{key}: {value}")
    # print(f"路徑字典 : ")
    # for key, value in topology.path_dic.items():
    #     print(f"{key}: {value}")

    scheduler = Scheduler(topology.flow_dic, topology.path_dic)     #排程
    scheduler.scheduling()

    # print(f"流字典 : ")
    # for key, value in topology.flow_dic.items():
    #     print(f"{key}: {value}")
    # print(f"鏈節字典 : ")
    # for key, value in topology.links.items():
    #     print(f"{key}: {value}")
    # print(f"路徑字典 : ")
    # for key, value in topology.path_dic.items():
    #     print(f"{key}: {value}")












main()
