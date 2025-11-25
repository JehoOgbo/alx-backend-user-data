# Simple API

Simple HTTP API for playing with `User` model.


## Files

### `models/`

- `base.py`: base of all models of the API - handle serialization to file
- `user.py`: user model

### `api/v1`

- `app.py`: entry point of the API
- `views/index.py`: basic endpoints of the API: `/status` and `/stats`
- `views/users.py`: all users endpoints
- `auth/auth.py`: The class Auth managing basic authentication


## Setup

```
$ pip3 install -r requirements.txt
```


## Run

```
$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
```


## Routes

- `GET /api/v1/status`: returns the status of the API
- `GET /api/v1/stats`: returns some stats of the API
- `GET /api/v1/users`: returns the list of users
- `GET /api/v1/users/:id`: returns an user based on the ID
- `GET /api/v1/unauthorized`: returns an unauthorized error object
- `GET /api/v1/forbidden`: returns a forbidden error object
- `DELETE /api/v1/users/:id`: deletes an user based on the ID
- `POST /api/v1/users`: creates a new user (JSON parameters: `email`, `password`, `last_name` (optional) and `first_name` (optional))
- `PUT /api/v1/users/:id`: updates an user based on the ID (JSON parameters: `last_name` and `first_name`)

## Objectives

### 1. Error Handler: Unauthorized
What the HTTP status code for a request unauthorized? 401 of course!

Edit api/v1/app.py:

- Add a new error handler for this status code, the response must be:
  - a JSON: {"error": "Unauthorized"}
  - status code 401
  - you must use jsonify from Flask

For testing this new error handler, add a new endpoint in api/v1/views/index.py:

- Route: GET /api/v1/unauthorized
- This endpoint must raise a 401 error by using abort - Custom Error Pages

By calling abort(401), the error handler for 401 will be executed.

In the first terminal:

```
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
....

In a second terminal:

bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/unauthorized"
{
  "error": "Unauthorized"
}
bob@dylan:~$
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/unauthorized" -vvv
*   Trying 0.0.0.0...
* TCP_NODELAY set
* Connected to 0.0.0.0 (127.0.0.1) port 5000 (#0)
> GET /api/v1/unauthorized HTTP/1.1
> Host: 0.0.0.0:5000
> User-Agent: curl/7.54.0
> Accept: */*
> 
* HTTP 1.0, assume close after body
< HTTP/1.0 401 UNAUTHORIZED
< Content-Type: application/json
< Content-Length: 30
< Server: Werkzeug/0.12.1 Python/3.4.3
< Date: Sun, 24 Sep 2017 22:50:40 GMT
< 
{
  "error": "Unauthorized"
}
* Closing connection 0
bob@dylan:~$
```

### 3. Error Handler: Forbidden
What the HTTP status code for a request where the user is authenticate but not allowed to access to a resource? 403 of course!

Edit [api/v1/app.py](./api/v1/app.py):

- Add a new error handler for this status code, the response must be:
  - a JSON: {"error": "Forbidden"}
  - status code 403
  - you must use jsonify from Flask

For testing this new error handler, add a new endpoint in [api/v1/views/index.py](./api/v1/views/index.py):

    Route: `GET /api/v1/forbidden`
    This endpoint must raise a 403 error by using abort - Custom Error Pages

By calling abort(403), the error handler for 403 will be executed.

In the first terminal:

```
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
....
```

In a second terminal:

```
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/forbidden"
{
  "error": "Forbidden"
}
bob@dylan:~$
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/forbidden" -vvv
*   Trying 0.0.0.0...
* TCP_NODELAY set
* Connected to 0.0.0.0 (127.0.0.1) port 5000 (#0)
> GET /api/v1/forbidden HTTP/1.1
> Host: 0.0.0.0:5000
> User-Agent: curl/7.54.0
> Accept: */*
> 
* HTTP 1.0, assume close after body
< HTTP/1.0 403 FORBIDDEN
< Content-Type: application/json
< Content-Length: 27
< Server: Werkzeug/0.12.1 Python/3.4.3
< Date: Sun, 24 Sep 2017 22:54:22 GMT
< 
{
  "error": "Forbidden"
}
* Closing connection 0
bob@dylan:~$
```

### 4. Auth class
Now you will create a class to manage the API authentication.

- Create a folder [api/v1/auth](./api/v1/auth)
- Create an empty file [api/v1/auth/__init__.py](./api/v1/auth/__init__.py)
- Create the class Auth:
  - in the file [api/v1/auth/auth.py](./api/v1/auth/auth.py)
  - import request from flask
  - class name Auth
  - public method def require_auth(self, path: str, excluded_paths: List[str]) -> bool: that returns False - path and excluded_paths will be used later, now, you don’t need to take care of them
  - public method def authorization_header(self, request=None) -> str: that returns None - request will be the Flask request object
  - public method def current_user(self, request=None) -> TypeVar('User'): that returns None - request will be the Flask request object

This class is the template for all authentication system you will implement.

```
bob@dylan:~$ cat main_0.py
#!/usr/bin/env python3
""" Main 0
"""
from api.v1.auth.auth import Auth

a = Auth()

print(a.require_auth("/api/v1/status/", ["/api/v1/status/"]))
print(a.authorization_header())
print(a.current_user())

bob@dylan:~$ 
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 ./main_0.py
False
None
None
bob@dylan:~$
```

### 4. Define which routes don't need authentication

Update the method def require_auth(self, path: str, excluded_paths: List[str]) -> bool: in [Auth](./api/v1/auth/auth.py) that returns True if the path is not in the list of strings excluded_paths:

- Returns True if path is None
- Returns True if excluded_paths is None or empty
- Returns False if path is in excluded_paths
- You can assume excluded_paths contains string path always ending by a /
- This method must be slash tolerant: `path=/api/v1/status` and `path=/api/v1/status/` must be returned False if excluded_paths contains /api/v1/status/

```
bob@dylan:~$ cat main_1.py
#!/usr/bin/env python3
""" Main 1
"""
from api.v1.auth.auth import Auth

a = Auth()

print(a.require_auth(None, None))
print(a.require_auth(None, []))
print(a.require_auth("/api/v1/status/", []))
print(a.require_auth("/api/v1/status/", ["/api/v1/status/"]))
print(a.require_auth("/api/v1/status", ["/api/v1/status/"]))
print(a.require_auth("/api/v1/users", ["/api/v1/status/"]))
print(a.require_auth("/api/v1/users", ["/api/v1/status/", "/api/v1/stats"]))

bob@dylan:~$
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 ./main_1.py
True
True
True
False
False
True
True
bob@dylan:~$
```

### 5. Request validation!

Now you will validate all requests to secure the API:

Update the method def authorization_header(self, request=None) -> str: in [api/v1/auth/auth.py](./api/v1/auth/auth.py):

- If request is None, returns None
- If request doesn’t contain the header key Authorization, returns None
- Otherwise, return the value of the header request Authorization

Update the file [api/v1/app.py](./api/v1/app.py):

- Create a variable auth initialized to None after the CORS definition
- Based on the environment variable AUTH_TYPE, load and assign the right instance of authentication to auth
  - if auth:
    - import Auth from api.v1.auth.auth
    - create an instance of Auth and assign it to the variable auth

Now the biggest piece is the filtering of each request. For that you will use the Flask method before_request

- Add a method in [api/v1/app.py](./api/v1/app.py) to handler before_request
  - if auth is None, do nothing
  - if request.path is not part of this list ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/'], do nothing - you must use the method require_auth from the auth instance
  - if auth.authorization_header(request) returns None, raise the error 401 - you must use abort
  - if auth.current_user(request) returns None, raise the error 403 - you must use abort

In the first terminal:

```
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=auth python3 -m api.v1.app
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
....
```

In a second terminal:

```
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/status"
{
  "status": "OK"
}
bob@dylan:~$
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/status/"
{
  "status": "OK"
}
bob@dylan:~$
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/users"
{
  "error": "Unauthorized"
}
bob@dylan:~$
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/users" -H "Authorization: Test"
{
  "error": "Forbidden"
}
bob@dylan:~$
```

### 6. Basic Auth
Create a class [BasicAuth](./api/v1/auth/basic_auth.py) that inherits from Auth. For the moment this class will be empty.

Update [api/v1/app.py](./api/v1/app.py) for using BasicAuth class instead of Auth depending of the value of the environment variable AUTH_TYPE, If AUTH_TYPE is equal to basic_auth:

- import BasicAuth from api.v1.auth.basic_auth
- create an instance of BasicAuth and assign it to the variable auth

Otherwise, keep the previous mechanism with auth an instance of Auth.

In the first terminal:

```
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=basic_auth python3 -m api.v1.app
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
....
```

In a second terminal:

```
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/status"
{
  "status": "OK"
}
bob@dylan:~$
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/status/"
{
  "status": "OK"
}
bob@dylan:~$
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/users"
{
  "error": "Unauthorized"
}
bob@dylan:~$
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/users" -H "Authorization: Test"
{
  "error": "Forbidden"
}
bob@dylan:~$
```

### Basic - Base64 part
Add the method `def extract_base64_authorization_header(self, authorization_header: str) -> str:` in the class [BasicAuth](./api/v1/auth/basic_auth.py) that returns the Base64 part of the Authorization header for a Basic Authentication:

- Return None if authorization_header is None
- Return None if authorization_header is not a string
- Return None if authorization_header doesn’t start by Basic (with a space at the end)
- Otherwise, return the value after Basic (after the space)
- You can assume authorization_header contains only one Basic

```
bob@dylan:~$ cat main_2.py
#!/usr/bin/env python3
""" Main 2
"""
from api.v1.auth.basic_auth import BasicAuth

a = BasicAuth()

print(a.extract_base64_authorization_header(None))
print(a.extract_base64_authorization_header(89))
print(a.extract_base64_authorization_header("ALX"))
print(a.extract_base64_authorization_header("Basic ALX"))
print(a.extract_base64_authorization_header("Basic SG9sYmVydG9u"))
print(a.extract_base64_authorization_header("Basic SG9sYmVydG9uIFNjaG9vbA=="))
print(a.extract_base64_authorization_header("Basic1234"))

bob@dylan:~$
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 ./main_2.py
None
None
None
ALX
SG9sYmVydG9u
SG9sYmVydG9uIFNjaG9vbA==
None
bob@dylan:~$
```

File: [api/v1/auth/basic_auth.py](./api/v1/auth/basic_auth.py)


