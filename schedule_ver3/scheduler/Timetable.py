class TimeTable:
    
    def __init__(self):
        self.time_table = {}

    def put_path_and_time_list_to_table(self, path, time_list):
        for time, flow_packet in time_list.items():
            #若此時間尚未被建立
            if self.time_table.get(time) != None:                   
                self.time_table[time] = {}
                self.time_table[time][path] = flow_packet
            #時間已建立，path尚未建立：無衝突Path問題，直接放置flow_packet
            elif self.time_table[time].get(path) != None:
                self.time_table[time][path] = flow_packet
            #時間已建立path也建立完畢，將會有link_time_collision
            else:
                





    def put_large_data_to_table(self):



