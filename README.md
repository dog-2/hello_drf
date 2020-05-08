# info

- demo code snippets when learning Django REST Framework through [video lessons](https://www.bilibili.com/video/BV1nE411J7hx)
- learning notes(Chinese) were post on [my blog](https://dog.wtf/tags/django-rest-framework/)

# env

- python: 3.7.5
- virtual env: pipenv
- django: 3.0.5
- djangorestframework: 3.11.0

# init

go to `hello_drf\` and run:

```bash
pip install pipenv
pipenv shell
pipenv sync
```

# run

cd to `hello_drf\noN_XYZ` and run:

```bash
python manage.py
```

# test API

1. cd to `hello_drf\noN_XYZ`
2. open [postman](https://www.postman.com/downloads/) and import collection file `hello_drf\noX_XYZ\noX_XYZ.postman_collection.json`
3. test imported requests in this collection
