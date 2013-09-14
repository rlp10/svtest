#!/usr/bin/env python2

import hashlib
import logging
import os
import os.path
import pickle
import unittest
import tempfile
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

# returns the default filename from the user's home directory as a
# location to save data
def default_filename():
    return os.path.expanduser("~/.svtest")

# saves the data to disk, with a default filename if none given
def save_data(data, filename=None):
    if filename == None:
        filename = default_filename()
    pickle.dump(data, open(filename, "wb"))

# returns the loaded data from disk, with a default filename if none
# given
def load_data(filename=None):
    if filename == None:
        filename = default_filename()
    try:
        return pickle.load(open(filename, "rb"))
    except Exception:
        return {}

################
# Registration #
################

# Returns a new random token, ensuring its not already used as a
# registration key
def new_token(data):
    token = None
    while (token == None) or (token in data.keys()):
        token = hashlib.sha224(str(time.time())).hexdigest()
    return token

# Registers a new token against the database
def register_token(data, token):
    data[token] = {}
    return data

##############
# Store Data #
##############

# Stores an entry against the relevant client's ID
def store_entry(data, token, key, value):
    data[token][key] = value
    return data

#################
# Retrieve Data #
#################

# Retrieves an entry from the relevant client's record
def retrieve_entry(data, token, key):
    return data[token][key]

###############
# Web Service #
###############

# Uses code from here: http://pymotw.com/2/SimpleXMLRPCServer/

def hello():
    return "Hello world!"

def register():
    data = load_data()
    token = new_token(data)
    data = register_token(data, token)
    save_data(data)
    return token

def store(token, key, value):
    if not (0 < len(key) < 21):
        return "Error: Key must be between 1 and 20 characters in length"
    data = load_data()
    data = store_entry(data, token, key, value)
    save_data(data)
    return True

def retrieve(token, key):
    data = load_data()
    return retrieve_entry(data,token, key)

def serve_forever():
    logging.basicConfig(level = logging.DEBUG)
    server = SimpleXMLRPCServer(('localhost', 9000), logRequests=True)
    server.register_function(hello)
    server.register_function(register)
    server.register_function(store)
    server.register_function(retrieve)
    server.serve_forever()

if __name__ == '__main__':
    serve_forever()
