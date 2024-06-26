from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import URL
from alembic import command
from alembic.config import Config

url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="1234",
    host="localhost",
    database="testdb",
    port="5432"
)

engine = create_engine(url)

def setup_database():
    engine = create_engine(url)
    metadata = MetaData()
    alembic_cfg = Config("alembic.ini")
    metadata.bind = engine
    command.upgrade(alembic_cfg, "head")
    return engine, metadata

   