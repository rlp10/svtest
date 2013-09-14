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

#########
# Proxy #
#########

def get_proxy():
    return xmlrpclib.ServerProxy('http://localhost:9000')

############
# Commands #
############

def register():
    proxy = get_proxy()
    token = proxy.register()
    save_token(token)

def store(key, value):
    token = load_token()
    proxy = get_proxy()
    proxy.store(token, key, value)

def retrieve(key):
    token = load_token()
    proxy = get_proxy()
    print proxy.retrieve(token, key)

##########################
# Command Line Arguments #
##########################

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='commands')

# register command
register_parser = subparsers.add_parser('register', help='Register for new token (Warning: Overwrites existing token!)')
register_parser.set_defaults(func=lambda args: register())

# store command
store_parser = subparsers.add_parser('store', help='Stores a key/value entry')
store_parser.add_argument('key', help='Key')
store_parser.add_argument('value', help='Value')
store_parser.set_defaults(func=lambda args: store(args.key, args.value))

# retrieve command
retrieve_parser = subparsers.add_parser('retrieve', help="Retrieve the value from the specified entry")
retrieve_parser.add_argument('key', help='Key')
retrieve_parser.set_defaults(func=lambda args: retrieve(args.key))

if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
