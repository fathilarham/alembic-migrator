import sys

# Init Logger
import logging
logging.basicConfig(level=logging.INFO)

# Detect the Config Type
import os
config_type = os.getenv("CONFIG_TYPE")

if config_type is None:
    config_type = "env"

if config_type is not None and config_type not in ["yaml", "env"]:
    logging.error('Invalid config type')
    sys.exit(0)

# Load Migrator config using ENV
if config_type == "env":
    db_host = os.getenv("HOST")
    db_port = os.getenv("PORT")
    db_user = os.getenv("USER")
    db_password = os.getenv("PASSWORD")
    db_name = os.getenv("DB_NAME")
    
# Load Migrator Config using YAML 
if config_type == "yaml":
    import yaml

    yaml_config_file = 'config/config.yaml'
    try:
        with open(yaml_config_file) as fh:
            read_data = yaml.load(fh, Loader=yaml.FullLoader)
            
            try:
                db_host = read_data['Postgres']['Host']
                db_port = read_data['Postgres']['Port']
                db_user = read_data['Postgres']['User']
                db_password = read_data['Postgres']['Password']
                db_name = read_data['Postgres']['DBName']
            except:
                logging.error('Invalid config file')    
                sys.exit(0)
    except OSError:
        logging.error('Config file is not found')    
        sys.exit(0)
        
# Validation
if db_host is None:
    logging.error('Database Host is empty')    
    sys.exit(0)
    
if db_port is None:
    logging.error('Database Port is empty')    
    sys.exit(0)

if db_user is None:
    logging.error('Database User is empty')    
    sys.exit(0)
    
if db_password is None:
    logging.error('Database Password is empty')    
    sys.exit(0)

if db_name is None:
    logging.error('Database Name is empty')    
    sys.exit(0)
    
# Alembic Process
logging.info('Running migration using ' + config_type + ' config')

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Init Alembic Config 
config = context.config

# Setup database url
config.set_main_option("sqlalchemy.url", "postgresql://%s:%s@%s:%s/%s" % (
    db_user,
    db_password,
    db_host,
    db_port,
    db_name,
))

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Schema Metadata
import schema
target_metadata = schema.Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
    