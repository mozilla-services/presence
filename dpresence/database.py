import uuid

from sqlalchemy import (create_engine, Column, Integer, Sequence, String,
                        Text, Boolean)
from sqlalchemy.ext.declarative import declarative_base
from bottle.ext import sqlalchemy


Base = declarative_base()
engine = create_engine('sqlite:///:memory:', echo=True)

db_plugin = sqlalchemy.Plugin(engine, Base.metadata, keyword='db',
                              create=True, commit=True, use_kwargs=False)


class Application(Base):
    """Defines an application.
    """
    __tablename__ = 'application'

    id = Column(Integer, Sequence('id_seq'), primary_key=True)

    uid = Column(Integer)
    name = Column(String(200))
    description = Column(Text())
    email = Column(String(200))
    domain = Column(String(200)
    notified = Column(Boolean)
    api_key = Column(String(200))

    def __init__(self, name, domain, email, description=''):
        self.name = name
        self.domain = domain
        self.email = email
        self.uid = str(uuid.uuid4())
        self.notified = False
        self.generate_apikey()

    def generate_apikey(self):
        self.api_key = str(uuid.uuid4())


class ApplicationUser(Base):
    __tablename__ = 'application_user'

    id = Column(Integer, Sequence('id_seq2'), primary_key=True)

    email = Column(String(200))
    application = Column(String(200))
    uid = Column(Integer)

    def __init__(self, application, email):
        self.application = application
        self.email = email
        self.uid = str(uuid.uuid4())
