# Elasticsearch App

## Requirements
1. Docker
2. Python3
3. virtualenvwrapper (optional)
4. flask
5. elasticsearch_dsl

## How To Run
### Run elasticsearch via docker container
This project uses Docker compose to setup elasticsearch environment. Please install docker first on your local machine. After installing docker, run the following on your terminal:

```sh
docker-compose up
```

The above command will pull docker image related to elasticsearch, create and run elasticsearch containers as configured on `docker-compose.yml`.

If you want to stop the docker containers you can just run:

```sh
docker-compose down
```

### Install python dependencies
We really recomend to use `virtualenvwrapper` to encapsulate your python working environment.
Please go to the official documentation to [install](https://virtualenvwrapper.readthedocs.io/en/latest/install.html).

Make a your virtual environment:
```sh
mkvirtualenv [your-env]
```

Install our project's python dependencies by running:
```sh
pip install -r requirements.txt
```
