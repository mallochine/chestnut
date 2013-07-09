from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ChestnutIndexEntry(Base):
    __tablename__ = 'chestnut_index'
    id = Column(Integer, primary_key = True)
    path = Column(String(200), nullable = False)

    def __init__(self, path=''):
        self.path = path

    def __repr__(self):
        return "<ChestnutIndexEntry('%s','%s')>" % (self.id, self.path)
