# Notes

## Introduction
After reading the task requirements, the following assumptions were made: 
This HTTP Proxy has two main goals
- automatically handle JWT signing for any requests 
- monitor and log all requests

This can be used for both development and for production. Whereas the usage of production depends on the actual use-case
and might not be considered very secure/helpful. One of the reasons for this is the fact, that only a user attribute and a
current date is included in the payload, but not actual the request payload. 

Hence, the code was developed with the usage for development in mind.

However, a few things were unclear or were not mentioned to test the knowledge of the applicant and decisions were 
required. 

The decisions made are based on best practice/educated guesses and are outlined below for quick reference.


## Workflow
As there was no prior experience in writing an HTTP Proxy Handler in python (only worked with ready made solutions 
or integrations) a bit of research was invested into possible solutions.

- Is there a library to solve this issue, that is relatively simple and does not create too much overhead
- Python Module Integrations that help with HTTP handling
- Up-to-date JWT Python Library

The library search was not very successful, there are many, but neither satisfied the criteria of:
- Small
- Up-to-date
- Code Coverage

After a quick few searches it became apparent that the in-built python ```BaseHTTPRequestHandler``` (via the http module)
is the best choice. The offical documentation page provided all information required, as well as looking at examples 
it became pretty clear,how to develop the entire process.

The JWT Token was not a problem at all, as I had written a custom JWT-like integration for another project, that had 
slightly higher requirements (Pentests at that time also showed that the integration was securely implemented). As these
requirements are not given here and the basic JWT concept is pretty simple, the only question was to find an easy to use
and maintained library in python, that makes use of secure cryptographic libraries. A quick google search provided: 
```pyJWT```.

For forwarding any requests to the actual endpoint I went with my personal go-to-choice of HTTP requests via the ```requests```
library. 

Because the usage of date and time formats is very limited in this task, I decided against using libraries such as 
```Arrow``` or ```Delorean``` and stuck with the normal ```datetime``` module of python.





## Questions

***1. How is the user (that is used in the JWT payload) provided?***
I decided, that it is provided via a "user" attribute in the Request Body JSON. 
However, I implemented a setting ```JWT_USER_IDENTIFIER``` for you to set the identifier, as it might be
```username``` or ```user_id``` etc. 

***2. What should happen, if there is no user provided?***
No comments were written about error handling, as the user is required for the JWT token, I decided to abort the process
and send back a 422 status code as per RFC.
This breaks the process and might actually be handled by the receiving server such as "Invalid JWT signing" or similar, 
but I figured to save the network requests costs from the Proxy to the endpoint, we can stop right here and not waste
resources. 
However, the downsite is, the implementation in the client for handling JWT token errors can not be tested.
Therefore, I implemented a setting for you to use ```DROP_JWT_ERROR``` to either drop or allow these requests.

***3. SSL Certificate Handling***
SSL is ignored, self-signed or invalid ssl certificates are not checked with the requests library. There is a "catch-all"
implementation. 

***4. What Header information should be forwarded?***
As it was not specified, which information should be present in the proxy request, apart from the JWT
I decided, to just forward the IP address of the requester


## Libraries Used
- https://requests.readthedocs.io/en/master/
- https://pyjwt.readthedocs.io/
- https://docs.makotemplates.org/
- https://github.com/MongoEngine/mongoengine 
- https://redis-py.readthedocs.io/en/stable/
- https://python-rq.org/docs/workers/

### Python Stuff
- https://docs.python.org/3/library/http.server.html#module-http.server
- https://docs.python.org/3/library/secrets.html

### Endpoint
- https://reqres.in/api/login