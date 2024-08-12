def sort(input_flows):
    sort_list <- sort_by_sorting_fasion(input_flows)
    sort_list <- sort_by_common_egress_port_impact(sort_list)
    sort_list <- non_conflict_chosen(sortlist)
    return sort_list

def main(input_flows):
    fail_flow_list = []
    final_sort_list = sort(input_flows)
    for flow in input_flows:
        set_StartTime(flow)
        set_Deadline(flow)
        fail_flow <- backward_scheduling(flow)
        if fail_flow == True:
            fail_flow_list <- fail_flow




