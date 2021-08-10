import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()
DATABASE_URL = os.getenv('EXT_CHANNEL_DB_URL')

engine = create_engine(DATABASE_URL)

Base = declarative_base()

class Channel(Base):
    __tablename__ = 'channels'
    channel_id = Column(BigInteger, primary_key=True)
    
    def __init__ (self, channel_id):
        self.channel_id = channel_id
        
Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)

def get_channel(session, channel_id):
    return session.query(Channel).filter_by(channel_id=channel_id).one_or_none()

def get_channel_list():
    result = []
    session = Session()
    for channel in session.query(Channel).all():
        result.append(channel.channel_id)
    session.close()
    return result

def is_channel_exist(channel_id):
    result = False
    session = Session()
    if get_channel(session, channel_id):
        result = True
    session.close()
    return result

def add_channel(channel_id):
    if not channel_id:
        return

    result = False
    session = Session()

    channel = get_channel(session, channel_id)
    if not channel:
        channel = Channel(channel_id)
        session.add(channel)
        session.commit()
        result = True

    session.close()
    return result

def del_channel(channel_id):
    if not channel_id:
        return
    
    result = False
    session = Session()

    channel = get_channel(session, channel_id)
    if channel:
        session.delete(channel)
        session.commit()
        result = True

    session.close()
    return result
