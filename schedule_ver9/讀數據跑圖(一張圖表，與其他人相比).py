import matplotlib.pyplot as plt
import csv
import re
sort_mode_list = []
input_flows_amount_list = []

def main():
    read_file()

def read_file():
    file_name = input("輸入檔案名稱：")
    with open(f"{file_name}.csv", newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        main_dict = read_msg(csv_reader)
        plot_chart(main_dict, file_name)                
        
def read_msg(csv_reader):
    main_dict = {}
    print_flag = 0
    for row in csv_reader:
        if len(row)<2:
            target_mode = row[0]
            sort_mode_list.append(target_mode)
            main_dict[f"{target_mode}"] = {}
            #print(f"排序名稱：{target_mode}")
        elif f"flows" in row:
            target_input_flows = row[0]
            if target_input_flows not in input_flows_amount_list:
                input_flows_amount_list.append(target_input_flows)
            main_dict[f"{target_mode}"][f"{target_input_flows}"] = {}
            #print(f"輸入資料流數量：{target_input_flows}")
            print_flag = 0
        else:
            if print_flag == 0:
                print_flag = 1
            target_times = row[0]

            main_dict[f"{target_mode}"][f"{target_input_flows}"][f"{target_times}"] = row[1]
    
    
    # print測試(資料結構)
    for mode, input_dict in main_dict.items():
        print(f"圖表主題(方法依據) = {mode}")
        for input_flows, data_dict in input_dict.items():
            print(f"輸入資料流數量 = {input_flows}")
            print(f"排程資料流 = {data_dict}\n\n")
            
    return main_dict      


def plot_chart(main_dict, file_name):

    data_list = []
    for sort_name, input_flow_dict in main_dict.items():
        avg_flow_list = []
        for input_flow_amount, times_dict  in input_flow_dict.items():
            avg_flow = 0
            for times, scheduled_flows in times_dict.items():
                max_times = len(times_dict)
                avg_flow += float(scheduled_flows)
            avg_flow_list.append(avg_flow/max_times)
        data_list.append(avg_flow_list)
        print(sort_name)
        print(avg_flow_list)
    
    plt.figure(num = file_name, figsize=(7,5))
    print(f"\n開啟檔案：{file_name}")
    h1 = data_list[0]
    h2 = data_list[1]
    h3 = data_list[2]
    h4 = data_list[3]
    h5 = data_list[4]
    x = list(input_flows_amount_list)
    plt.tick_params(axis='both', which='major', labelsize=14)
    plt.plot(x, h1, color='r', marker='*', linestyle='-', linewidth=1, label="Ours")
    plt.plot(x, h2, color='g', marker='D', linestyle='-', linewidth=1, label=sort_mode_list[1])
    plt.plot(x, h3, color='b', marker='s', linestyle='-', linewidth=1, label=sort_mode_list[2])
    plt.plot(x, h4, color='m', marker='p', linestyle='-', linewidth=1, label=sort_mode_list[3])
    plt.plot(x, h5, color='c', marker='o', linestyle='-', linewidth=1, label=sort_mode_list[4])
    plt.xlabel('input_flows',fontsize=14)
    underscore_indices = [i for i, c in enumerate(file_name) if c == '_']
    if len(underscore_indices) >= 3:
        process_time = file_name[underscore_indices[-3] + 1 : underscore_indices[-1]]
    else:
        process_time = None
    if process_time == "process_time":
        plt.ylabel('Runtime(sec)',fontsize=14)
        
    elif file_name[-4:] == "Full":
        plt.ylabel('Total_Schedule_Time',fontsize=14)
    else:
        plt.ylabel('Scheduled_Flows',fontsize=14)
    plt.legend(fontsize=14)
    plt.show()

main()