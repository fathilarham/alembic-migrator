# 🕊 Alembic Migrator
A simple tool to migrate a service database schema. 
DB Migrator supports OS Environment or YAML config type.

## How to use
1. Build/Pull the DB Migrator image. ([Installation](#installation))
1. Run the image to the container. ([Setup](#setup-service-template))
1. Run the available DB Migrator operations from the container. ([Operations](#operations))


## Installation
Pull the image from ghcr.io
```bash
docker pull ghcr.io/fathilarham/alembic-migrator
```


## Installation (Manual Build)
If you want to manually build the docker image, make sure you have a Docker & Git installed on your machine.

Clone this repository

```bash
git clone https://github.com/fathilarham/alembic-migrator.git

```

Go to the alembic-migrator directory
```bash
cd alembic-migrator
```

Build the Docker image
```bash
docker build -t fathilarham/alembic-migrator .
```

## Setup (OS Env)
By default, the ```CONFIG_TYPE``` is set to "env". If you want to use the OS Env as the configuration, you have to run the image and set the(```HOST```,```PORT```,```USER```,```PASSWORD```,```DB_NAME```) env.
You also have to mount your ```schema.py``` file & ```versions``` folder to the container using volume. 
```bash
docker run -d -it --name alembic-migrator \
    --network host \
    -e CONFIG_TYPE=env \
    -e HOST=localhost \
    -e PORT=5432 \
    -e USER=secret \
    -e PASSWORD=secret \
    -e DB_NAME=playground \
    -v {{ your database versions directory path }}:/app/alembic/versions \
    -v {{ your database schema.py path }}:/app/schema.py \
    ghcr.io/fathilarham/alembic-migrator:latest 
```


## Setup (YAML)
If you want to use the YAML file as the configuration, you have to run the image and set the (```CONFIG_TYPE```) env to "yaml". You also have to mount your ```schema.py``` file, ```config.yaml```, and ```versions``` folder to the container using volume. 
```bash
docker run -d -it --name alembic-migrator \
    --network host \
    -e CONFIG_TYPE=yaml \
    -v {{ your config.yaml path }}:/app/config/config.yaml \
    -v {{ your database versions directory path }}:/app/alembic/versions \
    -v {{ your database schema.py path }}:/app/schema.py \
    ghcr.io/fathilarham/alembic-migrator:latest 
```


## Operations
- Create a Revision
 
```bash
docker exec alembic-migrator alembic revision --autogenerate -m "{revision message}"
```

- Upgrade the database
 
```bash
docker exec alembic-migrator alembic upgrade head
```

- Downgrade the database
 
```bash
docker exec alembic-migrator alembic downgrade -1
```


## Optimizations
- [ ]  Handle multiple kind of databases (mysql, mongodb, etc).