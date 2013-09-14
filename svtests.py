#!/usr/bin/env python2

import tempfile
import unittest
from svserver import *

class SvtestTests(unittest.TestCase):

    # checks that data is identical when saved to disk and then
    # reloaded.  A temporary file is used and automatically deleted
    def test_data_persistence(self):
        test_data = { 'id1': {'A': 'Apple', 'B': 'Banana'},
                      'id2': {'foo': 'bar', 'ham': 'eggs'}}
        temp_file = tempfile.NamedTemporaryFile()
        save_data(test_data, filename=temp_file.name)
        new_data = load_data(temp_file.name)
        self.failUnless(test_data == new_data)

    # Test register token with 1000 unique tokens. Due to the
    # definition of a python dictionary, this would fail if there was
    # a collision between identical keys
    def test_register_100_tokens(self):
        data = {}
        for count in range(0,100):
            data = register_token(data, new_token(data))
        self.failUnless(len(data.keys()) == 100)

    # Test registering, storing an entry and retrieving it again
    def test_data_round_trip(self):
        data = {}
        token = new_token(data)
        data = register_token(data, token)
        key = "foo"
        value = "spam"
        data = store_entry(data, token, key, value)
        self.failUnless(retrieve_entry(data, token, key) == "spam")

if __name__ == '__main__':
    unittest.main()
