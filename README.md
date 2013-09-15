Svtest
======

Svtest is a key/value store offered as an XML-RPC webservice, along
with a command line client.

Each client registers their own ID, and can then access a key/value store unique to them.

Usage
-----

Run the server program svserver.py to start the web server.  The
default hostname and port number are "localhost" and 9000
respectively.  Run "svserver.py -h" for details on how to change this.

You can then register, store and retrieve values using svclient.py or
any other XML-RPC client.  You get usage information on running the
client with "svclient.py -h".  Once you register ("svclient
register"), svclient.py saves your client token in ~/.svtoken so you
don't have to keep entering it.

If you register again, then it overwrites your previous token.

Example
-------

```shell
$ ./svserver.py # starts server on localhost:9000
# In another terminal
$ ./svclient.py register # registers and saves new client ID
3832ca2f087df75fdb10a72f0fe2799754532c89de6531e9710b70e8 # saved in ~/.svtoken
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

- svclient.py throws an ugly exception if the key does not exist or
  the server is uncontactable, rather than exiting gracefully

Roadmap
-------

- A real database (as opposed to a pickled file) would be used for any
  significant volume of data.  Even sqlite would be significantly
  better.

- register_token could check to see that the token used is unique and
  throw an exception if not

- There are no tests for the client

- There are only a few tests written for the server
