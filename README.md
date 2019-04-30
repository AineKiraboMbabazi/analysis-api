
[![Build Status](https://travis-ci.org/AineKiraboMbabazi/analysis-api.svg?branch=users)](https://travis-ci.org/AineKiraboMbabazi/analysis-api)
[![Coverage Status](https://coveralls.io/repos/github/AineKiraboMbabazi/analysis-api/badge.svg?branch=master)](https://coveralls.io/github/AineKiraboMbabazi/analysis-api?branch=master)

## Analysis-api
Analysis-api is a backend api that is used for the analysis of myfarm data.

## Motivation
This API was designed to handle the backend operations for the farm data analysis system.

## Tech/framework used


<b>Built with</b>
- [Flask](http://flask.pocoo.org/docs/1.0/)
- [Python3](https://docs.python.org/3/)
- [MYSQL](https://www.mysql.com/)


## Features

|Endpoint   |  HTTP Method  |CRUD Method   |Result   |  
|---|---|---|---|
| / |GET   |INDEX   |  Loads the home page |
| /index  |GET   |INDEX   |  Loads the home page |
| /api/v1/auth/signup  |POST   |SIGNUP   |  Creates a user | 
| /api/v1/auth/login  |POST   |LOGIN   |   User login|  
| /api/v1/auth/forgot_password  |POST   |  RESET PASSWORD |   Reset Password|  
| /api/v1/users  |GET   |READ   |   Get all users| 
| /api/v1/users/<int:userId>  |GET   |READ   |   Get single user|
| /api/v1/users/cancel/<int:userId>  |PUT   |EDIT   |   Cancel single user|
| /api/v1/users/name/<int:userId>  |PUT   |EDIT   |   Update user name|
| /api/v1/users/user_role/<int:userId>  |PUT   |EDIT   |   Update user role|
| /api/v1/users/delete/<int:userId>  |PUT   |EDIT   |   Delete user |
| /api/v1/users/pending  |GET   |READ   |   Get all pending user accounts| 
| /api/v1/associations  |POST   |CREATE   |  Creates an association | 
| /api/v1/associations  |GET   |READ   |  Gets all associations |
| /api/v1/associations/<int:associationId> |GET   |READ   |  Fetch a single association | 
| /api/v1/associations/pending  |GET   |READ   |  Fetch pending associations |
| /api/v1/associations/approve/<int:associationId> |PUT   |EDIT   |  Approve association creation | 
| /api/v1/associations/cancel/<int:associationId> |PUT   |EDIT   |  cancel association  | 
| /api/v1/associations/name/<int:associationId> |PUT   |EDIT   |  Update association name  |
| /api/v1/associations/delete/<int:associationId> |PUT   |EDIT   |  Delete association   | 
| /api/v1/governments  |POST   |CREATE   |  Creates an government | 
| /api/v1/governments  |GET   |READ   |  Get all governments |
| /api/v1/govrnments/<int:governmentId> |GET   |READ   |  Fetch a single government |
| /api/v1/governments/pending  |GET   |READ   |  Fetch pending governments | 
| /api/v1/governments/approve/<int:governmentId> |PUT   |EDIT   |  Approve government creation | 
| /api/v1/governments/cancel/<int:governmentId> |PUT   |EDIT   |  cancel government  |
| /api/v1/governments/name/<int:governmentId> |PUT   |EDIT   |  Update government name  |
| /api/v1/governments/delete/<int:governmentId> |PUT   |EDIT   |  Delete government   | 

## Installation
Clone the repo
```
git clone https://github.com/AineKiraboMbabazi/analysis-api
```
Create virtualenv
```
virtualenv env
```
Install dependencies
```
pip3 install -r requirements.txt
```
Run application
```
python3 run.py
```

## Tests 
To run tests
```
python3 -m unittest
```

## How to use?
After running the project in your terminal
- Install postman
[Postman installation guide for Ubuntu](http://ubuntuhandbook.org/index.php/2018/09/install-postman-app-easily-via-snap-in-ubuntu-18-04/)

## Author
Software Engineer: Ainekirabo Mbabazi
#### Developer Stack
Python, Flask, Django

## License

MyFarm © [Ainekirabo Mbabazi]()
