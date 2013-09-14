Proxama Test Project
====================

The following project should be implemented in Python, ideally using Django but other solutions are acceptable.

Please write your code as if this project were part of your day-to-day work.

The code and any other related files should be provided either in a publicly-accessible source code repository or in a common archive format (zip or tarball).

Project Specification
---------------------

We require a stand-alone web service that will be accessed by various client applications to store and retrieve simple key/value pairs.

Each client application should have its own set of key/value pairs that can only be accessed by itself.

To achieve this, the web service should expose three APIs:

1. Register Application.

When a client application calls this API, it should receive a unique token which it should then include with any other request. This token will be used to identify the application to the web service.

2. Store data

This API should accept three parameters:

* The client's unique registration token
* A key name which should be a string 	between 1 and 20 characters long
* A value which should be a string between 0 and 100 characters long

The web service should store the key and value against the client record for future retrieval

3. Retrieve data

This API should accept the following parameters:

* The client's unique registration token
* An optional key name which should be a string between 1 and 20 characters long

If the key name is supplied and that key has been stored against the identified client, the API should return the related value.

If the key name is not supplied, all key/value pairs for the identified client should be returned.

The format of the input and output of the APIs is up to you as are the URLs.

The stored data must persist after the web service is stopped and should be available once it is restarted.

If you wish, you may also include a simple example client application to demonstrate your application working but this is not required.
