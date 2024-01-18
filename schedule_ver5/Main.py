# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication
from network_datas.InputFlow import InputFlow
from network_datas.Topology import Topology
from scheduler.Scheduler_swicth import SchedulerSwitch
from new_scheduler.ObjectSwicth import ObjectSwitch
from scheduler.Demo import Demo




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

 
    #選擇方法
    version_swicth = input("1.原版  else.整合版\n")
    if version_swicth == "1":
        #---原版 施工中---#
        scheduler_choose = SchedulerSwitch(topology)
    else:
        #---整合版 施工中---#
        scheduler_choose = ObjectSwitch(topology)

    #排程結果資料取得
    scheduled_data = scheduler_choose.run()
    
   
    

    app = QApplication(sys.argv)
    view = Demo(topology.links)
    view.show()
    #結果以圖表顯示
    view.update_graphics_from_dict(scheduled_data)
    
    sys.exit(app.exec_())

main()






