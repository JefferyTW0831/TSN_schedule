# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication
from InputFlow import InputFlow
from scheduler.Scheduler import Scheduler
from Topology import Topology
from scheduler.demo import CustomGraphicsView

#from ResourceUsagePlot import ResourceUsagePlot

def main():
    input_flow = InputFlow()                                        #讀取flow參數                       OK
    flow_dic = input_flow.run()

    topology = Topology(flow_dic)                                   #建構拓樸(假設已從CUC得到拓樸資訊)    OK
    topology.routing()                                              #得到每個flow的路徑流向

    scheduler = Scheduler(topology.flow_dic ,topology.links, topology.path_dic)     #排程
    
    flow_path_dic = scheduler.scheduling()
    app = QApplication(sys.argv)
    view = CustomGraphicsView()

    view.update_graphics_from_dict(flow_path_dic)

    sys.exit(app.exec_())

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
