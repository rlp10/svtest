Svtest
======

Svtest is a key/value store offered as an XML-RPC webservice, along
with a command line client.

Each client registers their own ID, and can then access a key/value
store individual to that client ID.

Usage
-----

Run the server program svserver.py to start the web server.  The
default host is "localhost" and port number is 9000.  Run "svserver.py
-h" for details on how to change this.

You can then register, store and retrieve values using svclient.py or
any other XML-RPC client.  You get usage information on running the
client with "svclient.py -h".  Once you register, svclient.py saves
your client token in ~/.svtoken so you don't have to keep entering it.

Example
-------

```shell
$ ./svserver.py # starts server on localhost:9000
# In another terminal
$ ./svclient.py register # registers and saves new client ID
$ ./svclient.py store foo bar
$ ./svclient.py store ham eggs
$ ./svclient.py retrieve foo
bar
$ ./svclient.py retrieve ham
eggs
```

Testing
-------

Run "svtests.py" to run the unit tests.

Bugs
----

- new_token uses a sha244 hash of the current time to create a random
  token.  This is horribly slow and there must be a better way of
  doing it.

- svclient.py throws a horrible exception if the key does not exist
  rather than exiting gracefully

Roadmap
-------

- Commandline arguments for the client so that you can connect from a
  different host onto any port

- A real database (as opposed to a pickled file) would be used for any
  significant volume of data.  Even sqlite would be significantly
  better.

- register_token could check to see that the token used is unique and
  throw an exception if not

- There are no tests for the client and no exception handling

- There are only a few tests written for the server
