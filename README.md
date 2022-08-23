# Homzhub Services

A Django web application/server for the SITA apps.


## Installation

#### Installing Python 3.8 on Ubuntu from Source

```console
sudo apt update
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev
wget https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz
tar -xf Python-3.10.0.tgz
cd Python-3.10.0
./configure --enable-optimizations
make -j $(nproc)
sudo make altinstall
```

#### Installing Postgres using docker

```console
sudo apt-get update
sudo apt-get install gdal-bin libgdal-dev python3-gdal binutils libproj-dev
sudo apt-get install python3-psycopg2
sudo apt-get install postgis postgresql-14-postgis-3
sudo docker pull postgis/postgis:12-3.0-alpine
mkdir -p $HOME/docker/volumes/postgres
sudo docker run --restart=always --name etek-docker-db -e POSTGRES_PASSWORD={your password} -d -p 5432:5432 -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data postgis/postgis:12-3.0-alpine
```

#### Installing Redis using docker

```console
sudo docker pull redis:6.0.5
sudo docker run --restart=always --name etek-redis -p 6379:6379 -d redis:6.0.5
```

#### Verify python and pip

```console
python3.10 --version
pip3.10 --version
```

## Install Pipenv

```console
pip3.10 install pipenv
```

#### Verify Postgres and Redis containers

```console
sudo docker ps | grep homzhub-docker-db
```

## Create Database

```console
sudo docker container ps
sudo docker exec -it CONTAINER_ID /bin/sh
psql -h localhost -U postgres
CREATE DATABASE your_database_name;
CREATE USER your_database_user WITH PASSWORD 'your_database_user_password';
GRANT ALL PRIVILEGES ON DATABASE your_database_user to your_database_name;
```

## Project Setup

```console
git clone https://github.com/bagavedip/SITAbackend.git
cd SITAbackend
pipenv install
```

## Configure environment variables

Copy all the environment variables keys from .env.example
into `.env` paste appropriate values.

## Activate Pipenv Shell

```console
pipenv shell
```

## Initial Migration

```console
python manage.py migrate_schemas --shared
```

## Create Tenant

```console
python manage.py create_tenant

schema_name: SCHEMA_NAME Specifies the schema_name for Tenant.
name: NAME Specifies the name of the Tenant
domain: DOMAIN Specifies the tenant domain ex: localhost, insights.com
```
## Run server

```console
python manage.py runserver
```
#### CreateSuper User
'''console
python manage.py tenant_command createsuperuser -s tenant_name
'''
#### Migrations

```console
python manage.py makemigrations
python manage.py migrate_schemas --shared
python manage.py migrate_schemas -s {your tenant schema name}
```
