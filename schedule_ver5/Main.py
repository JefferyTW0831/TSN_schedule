# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication
from network_datas.InputFlow import InputFlow
from network_datas.Topology import Topology
from new_scheduler.ObjectSwicth import ObjectSwitch
from new_scheduler.Demo import Demo




def main():
    input_flow = InputFlow()                                        #讀取flow參數                       OK
    flow_dic = input_flow.run()
    max_time = input_flow.cal_max_time()
    with open("input_weight.txt", "a") as file:
        for flow_name, data in input_flow.flow_dic.items():
            file.write(f"{flow_name} : {data}\n")
            file.write("\n" + "-" * 30 + "\n")

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
    # version_swicth = input("1.原版  else.整合版\n")
    # if version_swicth == "1":
    #     #---原版 施工中---#
    #     scheduler_choose = SchedulerSwitch(topology)
    # else:
    
    #     #---整合版---#
    scheduler_choose = ObjectSwitch(topology)

    #排程結果資料取得
    exe, scheduled_data = scheduler_choose.run()
    if exe == 1:
        with open("output_weight.txt", "a") as file:
            for scheduler_name, data in scheduled_data.items():
                file.write(f"{scheduler_name}\n")
                file.write(f"scheduled flows =  {data['result_list']}, total : {len(data['result_list'])} flows\n")
                file.write(f"scheduhle{scheduler_name[-1]} :\n")
                file.write(f"scheuled_flows = {data['result_list']}\n")
                file.write(f"amount = {len(data['result_list'])}\n")
                file.write("\n" + "-" * 30 + "\n")
    else:
        app = QApplication(sys.argv)
        view = Demo(topology.links, max_time)
        view.show()
        #結果以圖表顯示
        view.update_graphics_from_dict(scheduled_data)
        
        sys.exit(app.exec_())

main()






