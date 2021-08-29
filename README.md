# order-management

## Table of contents
* [General info](#general-info)
* [Setup](#setup)
* [Tests](#tests)
* [Celery](#celery)
* [Postman collection](#postman-collection)

## General info
Test task for Light IT

## Setup
To run this project locally, make the following:

```
$ python3.8 -m venv venv
$ source venv/bin/activate
$ (env)$ pip install -r requirements.txt
$ (env)$ python manage.py migrate
```

## Tests
To run the tests ```python manage.py test```

## Celery
To start worker ```celery -A order_management_project worker -l info```

To start beat ```celery -A order_management_project beat -l info```

## Postman collection
Postman collection link: https://www.getpostman.com/collections/cb53fb7c5c923d63e804