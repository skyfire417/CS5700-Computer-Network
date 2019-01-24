import socket
import argparse
import ssl

parser = argparse.ArgumentParser(description='crazy arguments')

parser.add_argument('-p', action='store', dest='PORT', type=int, default=None)
parser.add_argument('-s', action='store_true', dest='SSL', default=False)
parser.add_argument('HOST', action='store', type=str)
parser.add_argument('NEUID', action='store', type=str)

HOST = parser.parse_args().HOST
PORT = parser.parse_args().PORT
SSL = parser.parse_args().SSL
NEUID = parser.parse_args().NEUID
BUFSIZ = 4096

# PORT number
if PORT is None and SSL:
    PORT = 27994
elif PORT is None and not SSL:
    PORT = 27993

#  print PORT, SSL, HOST, NEUID

def main():
    # Create TCP client, no SSL
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)

    if not SSL:
        client.connect(server_address)
        # HELLO message
        client.send('cs5700fall2018 HELLO %s\n' % NEUID)
        # recieve_msg start
        receive_msg(client, server_address)
    # Create SSL TCP client
    else:
        # print 'SSL test...'
        ssl_client = ssl.wrap_socket(client, ssl_version=ssl.PROTOCOL_TLSv1)
        ssl_client.connect(server_address)
        ssl_client.send('cs5700fall2018 HELLO %s\n' % NEUID)
        receive_msg(ssl_client, server_address)


def receive_msg(client, server_address):
    while True:
        answer = client.recv(BUFSIZ)
        answerList = answer.split(' ')
        command = answerList[1]

        if command == 'STATUS':
            op = answerList[2] + ' ' + answerList[3] + ' ' + answerList[4]
            result = int(eval(op))
            client.send('cs5700fall2018 %s\n' % result)
        else:
            print command
            client.close()
            return


if __name__=="__main__":
    main()
