## Hackernews Backend:

> Built in Python programming language with Flask framework.

#### Structure of `app` directory

- _app.py_ -
- _controller.py_ -
- _database.py_ -

To understand the sequence flow, please see System Sequence Diagram below.
![SSD](https://github.com/ProjectHackernewsGroup04/Documentation/blob/master/images/SSD.jpg)

#### User registration and login

- Passwords hashed with bcrypt.

#### .circleci/config.yaml

The `.circleci/config.yml` file in the repository branch indicates the
use of [CircleCI](https://circleci.com/docs/2.0/about-circleci/#section=welcome)
for continuous integration.

For better understanding of the  `config.yaml` file structure, please see
[circleci-python](https://circleci.com/docs/2.0/language-python/) and
closer description on CI in our `Ops` documentation
[CI-chain](https://github.com/ProjectHackernewsGroup04/Ops#cicd-chain).

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
