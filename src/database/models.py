from database import Base, engine
from sqlalchemy import Column, Integer, String, Float


class MutesModel(Base):
    __tablename__ = "mutes"

    id = Column(Integer, primary_key=True)
    userid = Column(String(128))
    guildid = Column(String(128))
    expires = Column(Float)
    reason = Column(String(128))


class BanModel(Base):
    __tablename__ = "bans"

    id = Column(Integer, primary_key=True)
    userid = Column(String(128))
    guildid = Column(String(128))
    expires = Column(String(128))
    reason = Column(String(128))


def create_all():
    Base.metadata.create_all(bind=engine)