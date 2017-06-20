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
        self.msg = ''
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

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

    def run_client(self):
        sock = self.create_client_socket()
        for i in range(self.num):
            sock.sendall(self.msg)
            data = s.recv(1024)
        self.close()

    def run_server(self):
        sock = self.create_server_socket()
        conn, addr = sock.accept()
        while True:
            data = conn.recv(self.chunk)
            if not data:
                break
            conn.send('server received your message.')
        conn.close()

    def run(self, size):
        if size == 'client':
            self.run_client()
        else:
            self.run_server()
        self.close()

    def close(self):
        if self.sock:
            self.sock.close()

class NetworkSocket(object):
    def __init__(self, chunk, num, host='127.0.0.1', port=8081):
        self.chunk = chunk
        self.num = num
        self.host = host
        self.port = port
        self.msg = ''
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def create_client_socket(self):
        self.sock.connect((self.host, self.port))
        return self.sock

    def create_server_socket(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(10)

        return self.sock

    def run_client(self):
        sock = self.create_client_socket()
        for i in range(self.num):
            sock.sendall(self.msg)
            data = s.recv(1024)
        self.close()

    def run_server(self):
        sock = self.create_server_socket()
        conn, addr = sock.accept()
        while True:
            data = conn.recv(self.chunk)
            if not data:
                break
            conn.send('server received your message.')
        conn.close()

    def run(self, size):
        if size == 'client':
            self.run_client()
        else:
            self.run_server()
        self.close()

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
    parser.add_option('-H', '--host',
                      dest='host',
                      default='127.0.0.1',
                      help='host of network socket')
    parser.add_option('-P', '--port',
                      dest='port',
                      type='int',
                      default=8081,
                      help='port of network socket')
    options, args = parser.parse_args()

    if not check_args(options):
        sys.stderr.write('check arguments failed')
        parser.print_help()
        sys.exit(1)

    if options.target == 'local':
        local_socket = LocalSocket(options.chunk, options.num)
        try:
            local_socket.run(options.size)
        except Exception, e:
            sys.stderr.write(str(e))
            local_socket.close()
            sys.exit(2)
    else:
        network_socket = NetworkSocket(options.chunk, options.num, options.host, options.port)
        try:
            network_socket.run(options.size)
        except Exception, e:
            sys.stderr.write(str(e))
            network_socket.close()
            sys.exit(3)
