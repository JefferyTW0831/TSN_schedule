import matplotlib.pyplot as plt
import csv

mode_dict = {
    1:"Time_Forward",
    2:"Time_Backward",
    3:"Flow_Forward",
    4:"Flow_Backward"
}  

input_flows_amount_dict = {
    1:"20",
    2:"40",
    3:"60",
    4:"80",
    5:"100"
}

def main():
    read_file()

def read_file():
    file_name = input("輸入檔案名稱：")
    with open(f"{file_name}.csv", newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        main_dict = read_msg(csv_reader)
        plot_chart(main_dict)                
        
def read_msg(csv_reader):
    main_dict = {}
    max_times = 100
    print_flag = 0
    for row in csv_reader:
        if row[0] in mode_dict.values():
            target_mode = row[0]
            main_dict[f"{target_mode}"] = {}
            #print(f"排序名稱：{target_mode}")
        elif row[1] == "flows":
            target_input_flows = row[0]
            main_dict[f"{target_mode}"][f"{target_input_flows}"] = {}
            #print(f"輸入資料流數量：{target_input_flows}")
            print_flag = 0
        else:
            if print_flag == 0:
                print_flag = 1
            target_times = row[0]
            main_dict[f"{target_mode}"][f"{target_input_flows}"][f"{target_times}"] = row[1:]
    
    return main_dict
    # # print測試(資料結構)
    # for mode, input_dict in main_dict.items():
    #     print(f"圖表主題(方法依據) = {mode}")
    #     for input_flows, data_dict in input_dict.items():
    #         print(f"輸入資料流數量 = {input_flows}")
    #         for times, data in data_dict.items():
    #             print(f"{times} = {data}")
            
def plot_chart(main_dict):

    fig, ax = plt.subplots(2,2,constrained_layout = True)
    subplot_indices = [(i, j) for i in range(2) for j in range(2)]

    for mode_name, (i,j) in zip(main_dict, subplot_indices):
        map_list = []
        ax[i,j].set_title(mode_name)
        input_flow_amount = [int(amount) for amount in main_dict[mode_name].keys()]

        for input_flow in input_flow_amount:
            avg_flow_list = []
            for times, scheduled_flows in main_dict[mode_name][f'{input_flow}'].items():
                if avg_flow_list == []:
                    avg_flow_list = [int(x) for x in scheduled_flows]
                else :
                    int_scheduled_flows = [int(x) for x in scheduled_flows]
                    pairs = zip(avg_flow_list, int_scheduled_flows)
                    avg_flow_list = [x + y for x, y in pairs]
            max_times = len(main_dict[mode_name][f'{input_flow}'])
            avg_flow_list = [flow / max_times for flow in avg_flow_list]
            map_list.append(avg_flow_list)
        #map_list = [(20)[sort1, sort2, sort3,sort4(flows)], (40)[...],...]
        #trans = [(sort1)[20,40,60,80,100], (sort2)[20,40,60,80,100]]
        transposed_list = list(map(list, zip(*map_list)))
        h1 = transposed_list[0]
        h2 = transposed_list[1]
        h3 = transposed_list[2]
        h4 = transposed_list[3]
        x_offsets = [-3,-1, 1, 3]
        bar_width = 2
        for idx, data in enumerate([h1, h2, h3, h4]):
            x_shifted = [pos + x_offsets[idx] for pos in input_flow_amount]  # 計算每組數據的位置
            ax[i,j].bar(x_shifted, data, width=bar_width, align='center')

    plt.show()
main()