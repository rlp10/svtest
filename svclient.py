#!/usr/bin/env python2

import argparse
import os
import os.path
import xmlrpclib

#####################
# Token persistence #
#####################

def token_filename():
    return os.path.expanduser("~/.svtoken")

def save_token(token):
    with open(token_filename(), "w") as token_file:
        token_file.write(token)

def load_token():
    with open(token_filename(), "r") as token_file:
        return token_file.read()

def del_token():
    os.remove(token_filename())

############
# Commands #
############

def register(proxy):
    token = proxy.register()
    save_token(token)
    print token

def store(proxy, key, value):
    token = load_token()
    proxy.store(token, key, value)

def retrieve(proxy, key):
    token = load_token()
    print proxy.retrieve(token, key)

##########################
# Command Line Arguments #
##########################

def parse_args():

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='commands')

    # host and port configuration
    parser.add_argument('--host', default='localhost', help='hostname of server')
    parser.add_argument('--port', default=9000, type=int, help='port number of server')

    # register command
    register_parser = subparsers.add_parser('register', help='Register for new token (Warning: Overwrites existing token!)')
    register_parser.set_defaults(func=lambda args: register(args.proxy))

    # store command
    store_parser = subparsers.add_parser('store', help='Stores a key/value entry')
    store_parser.add_argument('key', help='Key')
    store_parser.add_argument('value', help='Value')
    store_parser.set_defaults(func=lambda args: store(args.proxy, args.key, args.value))

    # retrieve command
    retrieve_parser = subparsers.add_parser('retrieve', help="Retrieve the value from the specified entry")
    retrieve_parser.add_argument('key', help='Key')
    retrieve_parser.set_defaults(func=lambda args: retrieve(args.proxy, args.key))

    args = parser.parse_args()
    return args

########
# Main #
########

def main():
    args = parse_args()
    proxy_address = 'http://{}:{}'.format(args.host, args.port)
    args.proxy = xmlrpclib.ServerProxy(proxy_address)
    args.func(args)

if __name__ == '__main__':
    main()
