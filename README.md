
# iReporter
## Project Overview
The application is meant to help address and arrest corruption within the Country by improving reporting and follow up.

To view this site : https://github.com/Muchogo/Questioner


## Technologies used.

* Python 3

* flask
* flask-restful

## [Pivotal Tacker Stories](https://www.pivotaltracker.com/n/projects/2235816)

## Current endpoints

| Method  | Endpoint  | Usage  |
|---|---|---|
|POST | api/v1/signup | Register a user.  |   
|POST | api/v1/login | Login a new user  |  
|POST | api/v1/meetups  | Create a new meetup  |   
|GET| api/v1/meetups| Get all the created meetups|
|GET| api/v1/meetups/ (meetupsId) | Get a single meetup|
|PUT|	api/v1/meetups/ (meetupsId)/location |	Update a single meetups location.|
|PUT|	api/v1/meetups/(meetupsId)/comment |	Update a single meetups comment.|
|DELETE	| api/v1/meetups/(meetupsId)/comment	| Delete a single meetups.|
## Installation guide and usage

#### **Clone the repo.**
  ```
   $ git clone https://github.com/Muchogo/Questioner
  ```

#### **Create virtual environment & Activate.**
  ```
   $ virtualenv env -p python3
   $ source env/bin/activate
   ```
#### **Install Dependancies.**
  ```
    (env)$ pip install -r requirements.txt
  ```

#### **Run the app**
```
(env)$ cd iReporter/
```

On Linux set the enviroment variables for the project
```
(env)$ export FLASK_APP=run.py
(env)$ export FLASK_DEBUG=1
(env)$ export FLASK_ENV=development
(env)$ flask run
```

#### **Run Tests**

  ```
    (env)$ pytest --cov=tests
  ```