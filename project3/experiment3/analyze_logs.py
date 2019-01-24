import os
import numpy as np

tcps = ["DropTail_Reno", "DropTail_Sack1", "RED_Reno", "RED_Sack1"]
cwd = os.getcwd()

def calculate(fname):
    packets_received = packets_sent = 0
    sent_pkt_time = {}
    start_time = 0.0
    sum_delay = 0.0

    for line in open(fname):
        event, time, fromNode, toNode, pkt_type, pkt_size, flags, fid, src_addr, dst_addr, seq_num, pkt_id = line.split()
        time = float(time)
        # packets received
        if pkt_type == "ack" and event == "r" and toNode == "0":
            packets_received += 1
            delay = float(time) - sent_pkt_time[seq_num]
            sum_delay += delay
        # packets sent
        if pkt_type == "tcp" and event == "-" and fromNode == "0":
            packets_sent += 1
            sent_pkt_time[seq_num] = float(time)
        # timestamp
        if time - start_time >= 1:
            # output zero row
            if start_time == 0:
                yield 0, 0, 0
            # calculate throughput in Mbps, latency
            throughput = (packets_received * 8 * 1040) / (time - start_time) / 1000000
            latency = sum_delay / packets_received
            # reset 
            packets_received = packets_sent = 0
            sum_delay = 0
            start_time = time
            yield int(time), throughput, latency


def output():
    # throughput, drop_rate, latency
    tp_table = np.empty([21, 5])
    la_table = np.empty([21, 5])
    # loop the files
    for i in range(len(tcps)):
        # logs file in data
        fname = os.path.join(cwd, "data", "exp3_%s.tr" % (tcps[i]))
        for j, throughput, latency in calculate(fname):
            # print tcps[i], j,throughput, latency
            # fill throughput to tp_table
            if i == 0:
                tp_table[j][0] = j
                la_table[j][0] = j
            tp_table[j][i+1] = float(throughput)
            la_table[j][i+1] = float(latency)
    # Write table to file
    with open('plots/throughput.csv', 'wb') as f:
        np.savetxt(f, tp_table, delimiter=",")
    with open('plots/latency.csv', 'wb') as f:
        np.savetxt(f, la_table, delimiter=",")


if __name__ == '__main__':
    output()
