class LinkTimeDict:
    def __init__(self):
        self.time_dic = {}
        self.original_dic = {}

    def run(self, value):
        self.add_value(value)
   

    def add_value(self, value):
        # 皆有
        if (value + 1 in self.time_dic) and (value - 1 in self.time_dic):
            self.time_dic[value] = self.time_dic[value + 1]
            self.set_prev_times(value)
        # 後有
        elif value + 1 in self.time_dic:
            self.time_dic[value] = self.time_dic[value + 1]
        # 皆無
        else:
            self.time_dic[value] = value + 1
            # 前有
            if value - 1 in self.time_dic:
                self.set_prev_times(value)
    
    # 找連續 prev_time    
    def set_prev_times(self, value):
        offset = 1
        while True:
            if value - offset in self.time_dic:
                self.time_dic[value - offset] = self.time_dic[value]
                offset += 1
            else:
                break
    




if __name__ == "__main__":
    link_dict = LinkTimeDict()
    while True:
        user_input = input("輸入一個數值 (或輸入 'exit' 離開)：")
        if user_input.lower() == "exit":
            break
        try:
            value = int(user_input)
            link_dict.run(value)
        except ValueError:
            print("請輸入有效的整數。")
