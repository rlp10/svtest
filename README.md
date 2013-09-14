Svtest
======

Usage
-----

Run the server program svserver.py to start the web server.

You can then register, store and retrieve values using svclient.py.
You can get usage information by running "svclient.py -h".

Testing
-------

Run "svtests.py" to run the unit tests.

Bugs
----

- There should be better error checking in load_data rather than just
  returning an empty dictionary whenever it catches an exception.  The
  assumption is that an exception would mean that the file doesn't
  exist yet.  If there was an exception for a different reason then
  there would be a risk of overwriting all data!

- It would be better to check the reliability of the data before the
  server is loaded rather than when the first request is made.

- new_token uses a sha244 hash of the current time to create a random
  token.  This is horribly slow and there must be a better way of
  doing it.

Roadmap
-------

- Commandline arguments could be developed in order to specify the
  host and port number of the server

- Commandline arguments for the client so that you can connect from a
  different host onto any port

- A real database (as opposed to a pickled file) would be used for any
  significant volume of data.  Even sqlite would be significantly
  better.

- register_token could check to see that the token used is unique and
  throw an exception if not

- There are no tests for the client and no exception handling

- There are only a few tests written for the server
