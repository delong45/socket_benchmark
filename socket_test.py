#!/usr/bin/env python

import os
import sys
import socket
import optparse

class LocalSocket(object):
    def __init__(self, chunk, num):
        self.chunk = chunk
        self.num = num
        self.sock = socket.socket(socket.AF_UNIX, socket.STREAM)

    def create_client_socket(self):
        pass

    def create_server_socket(self):
        pass

    def close(self):
        pass

class NetworkSocket(object):
    def __init__(self, chunk, num):
        self.chunk = chunk
        self.num = num
        self.sock = socket.socket(socket.AF_INET, socket.STREAM)

    def create_client_socket(self):
        pass

    def create_server_socket(self):
        pass

    def close(self):
        pass

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
