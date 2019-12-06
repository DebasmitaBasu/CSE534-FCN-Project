import dpkt
import socket
from pprint import pprint
from struct import *
from datetime import datetime
import sys
import os
import csv

csv_input = []

def parse_tcp(buf):
    src_port, dest_port, seq, ack, offset_flags, window = unpack('! H H L L H H', buf[:16])
    offset = (offset_flags >> 12) * 4
    flag_ack = (offset_flags & 16) >> 4
    flag_psh = (offset_flags & 8) >> 3
    flag_syn = (offset_flags & 2) >> 1
    flag_fin = offset_flags & 1
    data = buf[offset:]
    tcp_seg_len = len(data)
    return src_port, dest_port, seq, ack, flag_ack, flag_psh, flag_syn, flag_fin, window, tcp_seg_len

def parse_ipv(buf):
    version_header_length = buf[0]
    header_length = (version_header_length & 15) * 4
    ttl, proto, src, dest = unpack('! 8x B B 2x 4s 4s', buf[:20])
    src = '.'.join(map(str, src))
    dest = '.'.join(map(str, dest))
    data = buf[header_length:]
    return proto, src, dest, data
    
def parse_eth(buf):
    data = buf[14:]
    return data

class Qn2_var:
    def __init__(self, seq):
        self.seq = seq     
    def add_ack(self, ack):
        self.ack = ack
    def add_window(self, window):
        self.window = window
        
class Qn2:
    def __init__(self, psh):
        self.psh = psh
        self.next_psh = -1
        self.next_psh_ack = -1
    
def parse_packs(pcap,filename):
    server_ip = None
    client_ip = None
    server_ports = []
    no_of_tcp_flows = 0
    syn_set = 0
    Qn2List = []
    repeat_seq_count = [0] * 1000
    fast_retrans = [0] * 1000
    total_packets = [0] * 1000
    total_ack_packets = [0] * 1000
    prev_ack_size = [-1] * 1000
    seq_set = [set(), set(), set()]
    ack_set = [set(), set(), set()]
    ack_dest = [{}] * 1000
    start_time = [-1] * 1000
    final_seq = [-1] * 1000
    end_time = [-1] * 1000
    total_time = [-1] * 1000
    total_bytes = [0] * 1000
    total_bytes_recv = [0] * 1000
    start_seq = [-1] * 1000
    start_seq_recv = [-1] * 1000
    cong_win = [0] * 1000
    cong_win_free = [0] * 1000
    last10cong = [[] for i in range(3)]
    psh_rec = [[] for i in range(3)]
    psh_ack_rec = [[] for i in range(3)]
    psh_next_rec = [[] for i in range(3)]
    psh_next_ack_rec = [[] for i in range(3)]
    line_count = 0
    csv_proto = 'TCP'
    for buf in pcap:
        line_count+=1
        proto, src_ip, dest_ip, ipv_data = parse_ipv(parse_eth(buf[1]))
        if proto == 17:
            csv_proto = 'UDP'
            #print('UDP')
        src_port, dest_port, seq, ack, flag_ack, flag_psh, flag_syn, flag_fin, window, tcp_seg_len = parse_tcp(ipv_data)

        if server_ip == None:
            if src_port == 80:
                server_ip = dest_ip
                client_ip = src_ip
            else:
                server_ip = src_ip
                client_ip = dest_ip

        if src_ip == server_ip:
            if src_port not in server_ports:
                server_ports.append(src_port)
                
        if dest_ip == server_ip:
            if dest_port not in server_ports:
                server_ports.append(dest_port)
        if flag_syn == 1 and src_ip == server_ip:
            syn_set += 1
            Qn2List.append(Qn2(seq+1))
        if flag_fin == 1 and src_ip == server_ip:
            syn_set -= 1
            no_of_tcp_flows += 1
        for iterat, s_port in enumerate(server_ports):
            if src_port == s_port and start_time[iterat] == -1:
                start_time[iterat] = buf[0]
                start_seq[iterat] = seq
            if dest_port == s_port and flag_fin == 1:
                final_seq[iterat] = ack
        if seq in final_seq:
            index = final_seq.index(seq)
            total_time[index] = (datetime.fromtimestamp(buf[0]) - datetime.fromtimestamp(start_time[index])).total_seconds()
            total_bytes[index] = seq - start_seq[index]
        for iterat, s_port in enumerate(server_ports):
            if dest_port == s_port:
                total_ack_packets[iterat] += 1
                if prev_ack_size[iterat] != -1:
                    if (len(last10cong[iterat]) < 1) or ((last10cong[iterat][-1] < cong_win[iterat] or last10cong[iterat][-1] >= 2*cong_win[iterat]) and len(last10cong[iterat]) < 10): 
                        last10cong[iterat].append(cong_win[iterat])
                    cong_win_free[iterat] += 1
                if ack_dest[iterat].get(ack) is None:
                    ack_dest[iterat].update({ack: 1})
                else:
                    ack_dest[iterat].update({ack: ack_dest[iterat].get(ack)+1})
                break

    throughput = 0
    for flno in range(no_of_tcp_flows):
        throughput += (total_bytes[flno]+total_packets[flno]*66+total_ack_packets[flno]*66)/total_time[flno]
    if throughput < 0:
        throughput = -throughput
    csv_input.append([filename,no_of_tcp_flows,throughput,csv_proto])
        
def read_packets(input_pcap_file,filename):
    with open(input_pcap_file, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        parse_packs(pcap,filename)
        
if __name__ == '__main__':
    path = 'input_usa'
    
    for filename in os.listdir(path):
        #read_packets("input_data\\"+filename,filename)
        read_packets("input_usa\\"+filename,filename)

    with open('stat_usa.csv', mode='w') as employee_file:
        employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in csv_input:
            print(i)
            employee_writer.writerow(i)
