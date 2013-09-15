#!/usr/bin/env python2

import hashlib
import logging
import os
import os.path
import pickle
import time

from SimpleXMLRPCServer import SimpleXMLRPCServer

####################
# Data Persistence #
####################

# The data consists of a dictionary of dictionaries. The keys of the
# top level dictionary are registration tokens. The keys and values of
# the second level dictionary are keys and values to be stored by that
# user.  Each key/value pair in the second dictionary is called an
# "entry".

def default_filename():
    '''Returns the default filename from the user's home directory as a
    location to save data'''
    return os.path.expanduser("~/.svtest")

def save_data(data, filename=None):
    '''Saves the data to disk, with a default filename if none given'''
    if filename == None:
        filename = default_filename()
    pickle.dump(data, open(filename, "wb"))

def load_data(filename=None):
    '''Returns the loaded data from disk, using a default filename if none
    given'''
    if filename == None:
        filename = default_filename()
    try:
        return pickle.load(open(filename, "rb"))
    except Exception:
        return {}

################
# Registration #
################

def new_token(data):
    '''Returns a new random token, ensuring it's not already used as a
    registration key'''
    token = None
    while (token == None) or (token in data.keys()):
        token = hashlib.sha224(str(time.time())).hexdigest()
    return token

def register_token(data, token):
    '''Registers a new token against the database'''
    data[token] = {}
    return data

##############
# Store Data #
##############

def store_entry(data, token, key, value):
    '''Stores an entry against the relevant client's record'''
    data[token][key] = value
    return data

#################
# Retrieve Data #
#################

def retrieve_entry(data, token, key):
    '''Retrieves an entry from the relevant client's record'''
    return data[token][key]

###############
# Web Service #
###############

# Uses code from here: http://pymotw.com/2/SimpleXMLRPCServer/

def hello():
    '''Test function to be offered as web service'''
    return "Hello world!"

def register():
    '''Register function to be offered as web service'''
    data = load_data()
    token = new_token(data)
    data = register_token(data, token)
    save_data(data)
    return token

def store(token, key, value):
    '''Store function to be offered as web service'''
    if not (0 < len(key) < 21):
        return "Error: Key must be between 1 and 20 characters in length"
    data = load_data()
    data = store_entry(data, token, key, value)
    save_data(data)
    return True

def retrieve(token, key):
    '''Retrieve function to be offered as web service'''
    data = load_data()
    return retrieve_entry(data,token, key)

def serve_forever():
    '''Setup web server and offer API'''
    logging.basicConfig(level = logging.DEBUG)
    server = SimpleXMLRPCServer(('localhost', 9000), logRequests=True)
    server.register_function(hello)
    server.register_function(register)
    server.register_function(store)
    server.register_function(retrieve)
    server.serve_forever()

if __name__ == '__main__':
    serve_forever()
