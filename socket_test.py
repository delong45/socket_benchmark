#!/usr/bin/env python

import os
import sys
import optparse

class LocalSocket(object):
    pass

class NetworkSocket(object):
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
    options, args = parser.parse_args()

    if not check_args(options):
        sys.stderr.write('check arguments failed')
        parser.print_help()
        sys.exit(1)
