import sys
import socket
import re
import Queue
from lxml import etree
import login


hostname = 'cs5700f18.ccs.neu.edu'
visited_links = []
Q = Queue.Queue()
flag_list = []


def main(argv):
    # 001273551 2S59JFFO
    USERNAME = argv[1]
    PASSWORD = argv[2]
    # login to fakebook
    sessionid, csrftoken = login.login(USERNAME, PASSWORD)
    # Begin crawl
    root = '/fakebook/'
    crawl(root, sessionid, csrftoken)


def crawl(root, sessionid, csrftoken):
    Q.put(root)
    visited_links.append(root)
    # Breath first search
    while not Q.empty():
        current = Q.get()
        response = request(current, sessionid, csrftoken)
        if response:
            selector = etree.HTML(response)
            # get all valid link
            links = selector.xpath("//a[contains(@href, '/fakebook/')]/@href")
            flags = selector.xpath("//h2[@class='secret_flag']/text()")
            if flags:
                flag = flags[0].split(': ')[1]
                print flag
                flag_list.append(flag)
                with open('secret_flags', 'a') as f:
                    f.write(flag + '\n')
                # The number of secret flags
                if len(flag_list) == 5:
                    break
            for link in links:
                if link not in visited_links:
                    visited_links.append(link)
                    if link not in Q.queue:
                        Q.put(link)


def request(link, sessionid, csrftoken):
    lines = [
        'GET %s HTTP/1.1' % link,
        'Host: ccs5700f18.ccs.neu.edu',
        'User-Agent: PostmanRuntime/7.3.0',
        'cookie: %s; %s\r\n' % (sessionid, csrftoken),
    ]
    message = '\r\n'.join(lines) + '\r\n\r\n'
    response = login.send_msg(message)
    # parse response
    status = response.split(' ', 2)[1]
    # switch status
    if status == '200':
        return response
    elif status == '301':
        location = re.search(r'Location: http://ccs5700f18.ccs.neu.edu(.*)', response).group(1)
        return request(location, sessionid, csrftoken)
    elif status in ['403', '404']:
        return None
    elif status == '500':
        return request(link, sessionid, csrftoken)
    else:
        return None


if __name__ == '__main__':
    main(sys.argv)
