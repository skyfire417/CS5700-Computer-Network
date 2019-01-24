import os
import numpy as np

tcps = ["Tahoe", "Reno", "NewReno", "Vegas"]
cwd = os.getcwd()

def calculate(fname):
    packets_received = packets_sent = packets_dropped =0
    sent_pkt_time = {}
    start_time = 0.0
    end_time = 10.0
    sum_delay = 0.0

    for line in open(fname):
        event, time, fromNode, toNode, pkt_type, pkt_size, flags, fid, src_addr, dst_addr, seq_num, pkt_id = line.split()
        # packets received
        if pkt_type == "ack" and event == "r" and toNode == "0":
            packets_received += 1
            delay = float(time) - sent_pkt_time[seq_num]
            sum_delay += delay
        # packets dropped
        if pkt_type == "tcp" and event == "d":
            packets_dropped  += 1
        # packets sent
        if pkt_type == "tcp" and event == "-" and fromNode == "0":
            packets_sent += 1
            sent_pkt_time[seq_num] = float(time)

    
    # calculate throughput in Mbps
    # print packets_received, packets_dropped, packets_sent, sum_delay
    throughput = (packets_received * 8 * 1040) / (end_time - start_time) / 1000000 
    drop_rate = float(packets_dropped) / packets_sent
    latency = sum_delay / packets_received
    return throughput, drop_rate, latency


def output():
    # throughput, drop_rate, latency
    tp_table = np.empty([10, 5])
    dr_table = np.empty([10, 5])
    la_table = np.empty([10, 5])

    tp_table[:,0] = np.arange(1,11)
    dr_table[:,0] = np.arange(1,11)
    la_table[:,0] = np.arange(1,11)
    # loop the files
    for i in range(len(tcps)):
        for j in range(1, 11):
            # logs file in data
            fname = os.path.join(cwd, "data", "exp1_%s_%dMB.tr" % (tcps[i], j))
            throughput, drop_rate, latency = calculate(fname)
            # print "throughput:", tcps[i], j, throughput
            # print "drop_rate:", tcps[i], j, drop_rate
            # print "latency:", tcps[i], j, latency
            # fill throughput to tp_table
            tp_table[j-1][i+1] = float(throughput)
            dr_table[j-1][i+1] = float(drop_rate)
            la_table[j-1][i+1] = float(latency)

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



