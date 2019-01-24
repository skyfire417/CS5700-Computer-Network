import socket
from urlparse import urlparse
import sys
import struct
from collections import namedtuple

IP_datagram = namedtuple('IP_datagram',['src', 'dest', 'payload'])
TCP_segment = namedtuple('TCP_segment',['src', 'dest', 'seq', 'ack_seq', 'adwind', 'flags', 'mss','payload'])
SYN_ACK = 0 + (1 << 1) + (0 << 2) + (0 << 3) + (1 << 4) + (0 << 5)

def get_localhost():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    host = s.getsockname()
    s.close()
    return host

def get_remotehost(url):
    parsed_url = urlparse(url)
    # exit if not http
    if parsed_url.scheme.lower() != 'http':
        print 'Not supported protocol'
        sys.exit(1)
    remotehost = parsed_url.netloc
    filename = parsed_url.path.split('/')[-1] if parsed_url.path else "index.html"
    filename = 'index.html' if not filename else filename
    remoteIP = socket.gethostbyname(remotehost)
    path = '/' if not parsed_url.path else parsed_url.path
    return remoteIP, filename, path, remotehost

def http_request(path, remotehost):
    lines = [
        'GET %s HTTP/1.1' % path,
        'Host: %s' % remotehost
    ]
    data = '\r\n'.join(lines) + '\r\n\r\n'
    return data

def checksum(msg):
    s = 0
    # loop taking 2 characters at a time
    for i in range(0, len(msg), 2):
        w = ord(msg[i]) + (ord(msg[i+1]) << 8 ) 
        s = s + w
    s = (s >> 16) + (s & 0xffff)
    s = s + (s >> 16)
    # complement and mask to 4 byte short
    s = ~s & 0xffff
    return s

def unpack_ipdata(data):
    # parse IPv4 datagram
    ip_header_data = struct.unpack('!BBHHHBBH4s4s', data[:20])
    
    src = ip_header_data[8]
    dest = ip_header_data[9]
    payload = data[20:]
    
    src = socket.inet_ntoa(src)
    dest = socket.inet_ntoa(dest)
    return IP_datagram(src, dest, payload)

def unpack_tcpdata(data):
    # parse tcp header data
    tcp_header_data = struct.unpack('!HHLLBBHHH', data[:20])
    tcp_src = tcp_header_data[0]
    tcp_dest = tcp_header_data[1]
    tcp_seq = tcp_header_data[2]
    tcp_ack_seq = tcp_header_data[3]
    tcp_adwind = tcp_header_data[6]
    # parse TCP flags
    tcp_flags = tcp_header_data[5]
    # Maximum Segment Size
    tcp_mss = None

    payload = data[20:]
    return TCP_segment(tcp_src, tcp_dest, tcp_seq, tcp_ack_seq, tcp_adwind, tcp_flags, tcp_mss, payload)


