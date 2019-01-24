import sys
import socket
import re
from lxml import etree


def login(USERNAME, PASSWORD):
    # Get request_1
    lines = [
        'GET /accounts/login/?next=/fakebook/ HTTP/1.1',
        'Host: cs5700f18.ccs.neu.edu',
    ]
    request_1 = '\r\n'.join(lines) + '\r\n\r\n'
    response = send_msg(request_1)
    csrftoken = re.search(r'(csrftoken=.*); expires', response).group(1)
    sessionid = re.search(r'(sessionid=.*); expires', response).group(1)
    # POST request_2
    lines = [
        'POST /accounts/login/?next=/fakebook/ HTTP/1.1',
        'Host: ccs5700f18.ccs.neu.edu',
        'User-Agent: PostmanRuntime/7.3.0',
        'Content-Type: application/x-www-form-urlencoded',
        'content-length: 89',
        'cookie: %s; %s\r\n' % (sessionid, csrftoken),
        'username=%s&password=%s&csrfmiddlewaretoken=%s' % (USERNAME, PASSWORD, csrftoken.split('=')[1])
    ]
    request_2 = '\r\n'.join(lines)
    response = send_msg(request_2)
    # invalid username or password
    if response == 'timeout timeout':
        sys.exit('Invalid username or password!')
    sessionid = re.search(r'(sessionid=.*); expires', response).group(1)
    return sessionid, csrftoken


def send_msg(message):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10) 
        hostname = 'cs5700f18.ccs.neu.edu'
        s.connect((hostname, 80))
        s.send(message)
        response = s.recv(10240)
        s.close()
        return response
    except:
        return 'timeout timeout'
