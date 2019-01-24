import os
import numpy as np

tcps = ["Reno_Reno", "Newreno_Reno", "Vegas_Vegas", "Newreno_Vegas"]
cwd = os.getcwd()

def calculate(fname):
    # fid=2
    packets_received_1 = packets_sent_1 = packets_dropped_1 =0
    # fid=3
    packets_received_2 = packets_sent_2 = packets_dropped_2 =0
    sent_pkt_time_1 = sent_pkt_time_2 = {}
    start_time = 0.0
    end_time = 10.0
    sum_delay_1 = sum_delay_2 = 0.0

    for line in open(fname):
        event, time, fromNode, toNode, pkt_type, pkt_size, flags, fid, src_addr, dst_addr, seq_num, pkt_id = line.split()
        # packets received
        if pkt_type == "ack" and event == "r":
            if toNode == "0" and fid == "2":
                packets_received_1 += 1
                delay = float(time) - sent_pkt_time_1[seq_num]
                sum_delay_1 += delay
            if toNode == "4" and fid == "3":
                packets_received_2 += 1
                delay = float(time) - sent_pkt_time_2[seq_num]
                sum_delay_2 += delay
        # packets dropped
        if pkt_type == "tcp" and event == "d":
            if fid == "2":
                packets_dropped_1 += 1
            if fid == "3":
                packets_dropped_2 += 1
        # packets sent
        if pkt_type == "tcp" and event == "-":
            if fromNode == "0" and fid == "2":
                packets_sent_1 += 1
                sent_pkt_time_1[seq_num] = float(time)
            if fromNode == "4" and fid == "3":
                packets_sent_2 += 1
                sent_pkt_time_2[seq_num] = float(time)

    # calculate throughput in Mbps
    throughput_1 = (packets_received_1 * 8 * 1040) / (end_time - start_time) / 1000000
    throughput_2 = (packets_received_2 * 8 * 1040) / (end_time - start_time) / 1000000
    # calculate drop rate
    drop_rate_1 = float(packets_dropped_1) / packets_sent_1
    drop_rate_2 = float(packets_dropped_2) / packets_sent_2
    # calculate latency
    latency_1 = sum_delay_1 / packets_received_1
    latency_2 = sum_delay_2 / packets_received_2
    return throughput_1, throughput_2, drop_rate_1, drop_rate_2, latency_1, latency_2


def output():
    # throughput, drop_rate, latency
    tp_table = np.empty([10, 9])
    dr_table = np.empty([10, 9])
    la_table = np.empty([10, 9])

    tp_table[:,0] = np.arange(1,11)
    dr_table[:,0] = np.arange(1,11)
    la_table[:,0] = np.arange(1,11)
    # loop the files
    for i in range(len(tcps)):
        for j in range(1, 11):
            # logs file in data
            fname = os.path.join(cwd, "data", "exp2_%s_%dMB.tr" % (tcps[i], j))
            throughput_1, throughput_2, drop_rate_1, drop_rate_2, latency_1, latency_2 = calculate(fname)
            # print "throughput:", tcps[i], j, throughput_1, throughput_2
            # print "drop_rate:", tcps[i], j, drop_rate_1, drop_rate_2
            # print "latency:", tcps[i], j, latency_1, drop_rate_2
            # fill throughput to tp_table
            tp_table[j-1][2*i+1] = float(throughput_1)
            tp_table[j-1][2*i+2] = float(throughput_2)
            dr_table[j-1][2*i+1] = float(drop_rate_1)
            dr_table[j-1][2*i+2] = float(drop_rate_2)
            la_table[j-1][2*i+1] = float(latency_1)
            la_table[j-1][2*i+2] = float(latency_2)

    # print tp_table
    # print dr_table
    # print la_table
    # Write table to file
    with open('plots/throughput.csv', 'wb') as f:
        np.savetxt(f, tp_table, delimiter=",")
    with open('plots/drop_rate.csv', 'wb') as f:
        np.savetxt(f, dr_table, delimiter=",")
    with open('plots/latency.csv', 'wb') as f:
        np.savetxt(f, la_table, delimiter=",")

if __name__ == '__main__':
    output()




