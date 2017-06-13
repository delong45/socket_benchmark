#!/usr/bin/env python

import os
import sys
import socket
import optparse

class LocalSocket(object):
    def __init__(self, chunk, num, addr_dir='/var/run/socket_benchmark/'):
        self.chunk = chunk
        self.num = num
        self.addr_dir = addr_dir
        self.addr = self.addr_dir + 'socket.benchmark'
        self.sock = socket.socket(socket.AF_UNIX, socket.STREAM)

    def create_client_socket(self):
        self.sock.connect(self.addr)
        return self.sock

    def create_server_socket(self):
        if not os.path.exists(self.addr_dir):
            os.makedirs(self.addr_dir)

        try:
            os.remove(self.addr)
        except OSError:
            pass
        self.sock.bind(self.addr)
        self.sock.listen(10)

        return self.sock

    def run(self):
        pass

    def close(self):
        if self.sock:
            self.sock.close()

class NetworkSocket(object):
    def __init__(self, chunk, num, host='127.0.0.1', port=8081):
        self.chunk = chunk
        self.num = num
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.STREAM)

    def create_client_socket(self):
        self.sock.connect((self.host, self.port))

        return self.sock

    def create_server_socket(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(10)

        return self.sock

    def run(self):
        pass

    def close(self):
        if self.sock:
            self.sock.close()

def check_args(opt):
    if not opt.target or not opt.size or not opt.chunk:
        return False
    if opt.target != 'local' and opt.target != 'network':
        return False
    if opt.size != 'client' and opt.size != 'server':
        return False

    return True
                
if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-t', '--target',
                      dest='target',
                      help='local or network')
    parser.add_option('-s', '--size',
                      dest='size',
                      help='client or server')
    parser.add_option('-c', '--chunk',
                      dest='chunk', 
                      type='int',
                      help='size of chunk to transport')
    parser.add_option('-n', '--num',
                      dest='num',
                      type='int',
                      default=10000,
                      help='total number of sending time')
    options, args = parser.parse_args()

    if not check_args(options):
        sys.stderr.write('check arguments failed')
        parser.print_help()
        sys.exit(1)

    if options.target == 'local':
        local_socket = LocalSocket(options.chunk, options.num)
    else:
        network_socket = NetworkSocket(options.chunk, options.num)
