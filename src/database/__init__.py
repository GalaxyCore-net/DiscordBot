from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine(
    f"mariadb+mariadbconnector://root:iusearchbtw@db:3306/root?auto_reconnect=true"
)
