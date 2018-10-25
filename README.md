## Hackernews Backend:

> Built in [Python](https://www.python.org/) programming language with [Flask](http://flask.pocoo.org/) framework.

Backend file structure:
```
Backend/
    .circleci/
        config.yml
    app/
        test/
        __init__.py
        app.py
        controller.py
        database.py
    .gitignore
    Dockerfile
    README.md
    Requierements.txt
```

#### .circleci/config.yaml

The `.circleci/config.yml` file in the repository branch indicates the
use of [CircleCI](https://circleci.com/docs/2.0/about-circleci/#section=welcome)
for continuous integration.

For better understanding of the  `config.yaml` file structure, please see
[circleci-python](https://circleci.com/docs/2.0/language-python/) and
closer description on CI in our `Ops` documentation
[CI-chain](https://github.com/ProjectHackernewsGroup04/Ops#cicd-chain).

#### Structure of `app` package
Package `app` host the application and runs on http://0.0.0.0:5000.

- _init.py_ - in Python, if a sub-directory includes a __init__.py file
 it is considered a package, and can be imported.

- _app.py_ - in this module we structure our application, set routes and
 create the application object as an instance of Flask imported from the flask package.

 ```python
from flask import Flask
...
 app = Flask(__name__)
 ...
 @app.route('/')
 ...
 ```
 The @app.route decorator creates an association between the URL given
 as an argument and the function.

- _controller.py_ - here lays all the logic for each endpoint/route from the `app.py`.
Once `app.py` receives data from `Frontend`, it processes data and make
queries to the database.


- _database.py_ - this module, establishes connection to database.
```python
def get_db_conn():
    connection = client[db_name]
    return connection
```
Prepares collections in "hackernews" database hosted on MongoDB server.

To understand the sequence flow, please see System Sequence Diagram below.
![SSD](https://github.com/ProjectHackernewsGroup04/Documentation/blob/master/images/SSD.jpg)

#### User registration and login

- Passwords hashed with bcrypt.

#### Dockerfile

When running `docker-compose up --build` Docker builds images automatically
by reading the instructions from a Dockerfile.
Read more detailed about Dockerfile [here](https://docs.docker.com/engine/reference/builder/).

In the Dockerfile, we have specified which tools we want installed on
the Docker image. `RUN pip install -r requirements.txt` command
will look for the `requirements.txt` file and install the listed requirements.

_requirements.txt:_
```txt
Flask==0.12.3
pymongo
bcrypt
pytest
flask_httpauth
```
