import sys
import socket
import struct
import util
import time
from random import randint
from collections import namedtuple

SYN = 0 + (1 << 1) + (0 << 2) + (0 << 3) + (0 << 4) + (0 << 5)
ACK = 0 + (0 << 1) + (0 << 2) + (0 << 3) + (1 << 4) + (0 << 5)
SYN_ACK = 0 + (1 << 1) + (0 << 2) + (0 << 3) + (1 << 4) + (0 << 5)
FIN = 1 + (0 << 1) + (0 << 2) + (0 << 3) + (0 << 4) + (0 << 5)
FIN_ACK = 1 + (0 << 1) + (0 << 2) + (0 << 3) + (1 << 4) + (0 << 5)
PSH_ACK = 0 + (0 << 1) + (0 << 2) + (1 << 3) + (1 << 4) + (0 << 5)

class RawSocket(object):

    def __init__(self):
        try:
            self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
            self.rev_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            self.localhostip = util.get_localhost()[0]
            self.buffer = ''
            self.localhostport = randint(1500, 63000)
            self.tcp_seq = randint(0, (2 << 31) - 1)
            self.tcp_ack_seq = 0
            self.tcp_adwind = 20480
            # congestion control
            self.cwnd = 1
            self.slow_start_flag = True
            # Maximum Segment Size is 536
            self.mss = 536
        except socket.error, e:
            print "Error,Cannot Create Raw Socket", e
            sys.exit()
        print 'local_ip_port: ', self.localhostip, self.localhostport
    
    def ip_header(self):
        # ip header fields
        ip_ihl = 5
        ip_ver = 4
        ip_tos = 0
        ip_tot_len = 0
        ip_id = randint(0, 60000)
        ip_frag_off = 0
        ip_ttl = 255
        ip_proto = socket.IPPROTO_TCP
        ip_check = 0
        ip_saddr = socket.inet_aton(self.localhostip)
        ip_daddr = socket.inet_aton(self.remoteIP)
        ip_ihl_ver = (ip_ver << 4) + ip_ihl
        # the ! in the pack format means network order
        ip_header = struct.pack('!BBHHHBBH4s4s', ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)
        return ip_header
    
    def tcp_header(self, flags=ACK, payload=''):
        # tcp header fields
        tcp_source = self.localhostport
        tcp_dest = self.remotePORT
        tcp_seq = self.tcp_seq
        tcp_ack_seq = self.tcp_ack_seq
        tcp_doff = 5
        tcp_window = self.tcp_adwind
        tcp_check = 0
        tcp_urg_ptr = 0
        tcp_offset_res = (tcp_doff << 4) + 0
        tcp_flags = flags
        tcp_header = struct.pack('!HHLLBBHHH', tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags,  tcp_window, tcp_check, tcp_urg_ptr)
        # pseudo header fields
        source_address = socket.inet_aton(self.localhostip)
        dest_address = socket.inet_aton(self.remoteIP)
        placeholder = 0
        protocol = socket.IPPROTO_TCP
        if len(payload) % 2 != 0:
            payload += ' '
        tcp_length = len(tcp_header) + len(payload)
        
        psh = struct.pack('!4s4sBBH', source_address, dest_address, placeholder, protocol, tcp_length)
        psh = psh + tcp_header + payload

        tcp_check = util.checksum(psh)
        tcp_header = struct.pack('!HHLLBBH', tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags,  tcp_window) + struct.pack('H', tcp_check) + struct.pack('!H', tcp_urg_ptr)
        return tcp_header + payload

    def _send(self, data='', flags=ACK):
        self.buffer = data
        current_index = 0
        # Send SYN/ACK flags
        if not data:
            # send first ACK packet
            packet = self.ip_header() + self.tcp_header(flags=flags, payload=self.buffer)
            self.send_socket.sendto(packet, (self.remoteIP, self.remotePORT))
            return

        if not self.slow_start_flag:
            new_index = current_index + self.cwnd*self.mss
        
        # send packet segments for congestion control
        while True:
            if(len(self.buffer) - current_index > self.cwnd*self.mss):
                send_buffer = data[current_index:new_index]
                packet = self.ip_header() + self.tcp_header(flags=flags, payload=send_buffer)
                self.send_socket.sendto(packet, (self.remoteIP, self.remotePORT))
                # set new send buffer
                self.buffer = send_buffer[new_index:]
                current_index = new_index
                new_index = current_index + self.cwnd*self.mss
            # last segment
            else:
                send_buffer = data[current_index:]
                # send packet
                packet = self.ip_header() + self.tcp_header(flags=flags, payload=send_buffer)
                self.send_socket.sendto(packet, (self.remoteIP, self.remotePORT))
                break

    def send(self, data):
        self._send(data, flags=PSH_ACK)
        # reset buffer
        self.buffer = ''
    
    def connect(self, remoteIP, port):
        # TCP 3 handshakes
        self.remoteIP = remoteIP
        self.remotePORT = port
        print "Connected: ", self.remoteIP, self.remotePORT
        self._send(flags=SYN)
        # verify ACK
        if self.receive_ack(offset=1):
            # connection success
            self._send(flags=ACK)
            print 'TCP handshake success!'
        else:
            print 'TCP handshake failed'
            self.close('send')
            sys.exit(1)
    
    def close(self, how):
        if how == 'send':
            print 'client closed'
            self._send(flags=FIN_ACK)
            self.receive_ack()
            self._send(flags=ACK)
        
        if how == 'reply':
            print 'server closed'
            self._send(flags=FIN_ACK)
            
        self.send_socket.close()
        self.rev_socket.close()

    def receive_ack(self, offset=0):
        start_time = time.time()
        while time.time() - start_time < 60:
            tcp_seg = self._receive()
            if not tcp_seg:
                break
            # TCP handshake, verify ACK = SYN + 1
            if tcp_seg.flags & ACK and tcp_seg.ack_seq == self.tcp_seq + offset:
                self.tcp_seq = tcp_seg.ack_seq
                self.tcp_ack_seq = tcp_seg.seq + offset
                # Congestion control initial
                self.congestion_control()
                return True
        return False
    
    def _receive(self, size=20480, delay=60):
        # set basic timeout function
        self.rev_socket.settimeout(delay)
        try:
            while True:
                data = self.rev_socket.recv(size)
                ip_datagram = util.unpack_ipdata(data)
                # verify checksum, src and dest address
                if ip_datagram.dest != self.localhostip or ip_datagram.src != self.remoteIP:
                    continue
                # unpack tcp segment
                tcp_seg = util.unpack_tcpdata(ip_datagram.payload)
                if tcp_seg.dest != self.localhostport or tcp_seg.src != self.remotePORT:
                    continue
                return tcp_seg
        except socket.timeout:
            # if timeout, reset cwnd and enter slowstart mode 
            self.slow_start_flag = True
            self.congestion_control()
            return False
    
    def receive(self):
        tcp_segments = {}
        while True:
            tcp_seg = self._receive()
            # if timeout, exit system
            if not tcp_seg:
                print 'socket timeout!'
                sys.exit(1)

            # server close connection
            if tcp_seg.flags & FIN:
                self.tcp_seq = tcp_seg.ack_seq
                self.tcp_ack_seq = tcp_seg.seq + 1
                self.close('reply')
                break
            # congestion window
            if tcp_seg.flags & ACK and tcp_seg.seq not in tcp_segments and tcp_seg.payload:
                if tcp_seg.seq == self.tcp_ack_seq:
                    # congestion control
                    self.congestion_control()
                    # add TCP segments
                    tcp_segments[tcp_seg.seq] = tcp_seg.payload
                    self.tcp_seq = tcp_seg.ack_seq
                    self.tcp_ack_seq = tcp_seg.seq + len(tcp_seg.payload)
                    self._send(flags=ACK)
                # retransmit if not receive ACK
                else:
                    # reset congestion window for drop packet
                    self.slow_start_flag = True
                    self.congestion_control()
                    self._send(flags=ACK)
        
        sorted_segments = sorted(tcp_segments.items())
        data = ''
        for _, v in sorted_segments:
            data += v
        return data
    
    def congestion_control(self):
        if self.slow_start_flag:
            self.slow_start_flag = False
            self.cwnd = 1
        else:
            self.cwnd = min(2*self.cwnd, 1000)
        return


def main(argv):
    remoteIP, filename, path, remotehost = util.get_remotehost(argv[1])
    print 'remote: ',remoteIP, filename, path, remotehost
    s = RawSocket()
    # 3 handshake
    s.connect(remoteIP, 80)
    # download file
    print 'tcp handshake finished, start http request......'
    s.send(util.http_request(path, remotehost))
    data = s.receive()
    # extract content from http content
    res = data.split("\r\n\r\n", 1)[-1]

    if not data.startswith("HTTP/1.1 200 OK"):
        print 'http request failed'
        s.close('send')
        sys.exit(1)
    
    with open(filename, "w") as f:
        f.write(res)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('Illegal arguments')
    main(sys.argv)