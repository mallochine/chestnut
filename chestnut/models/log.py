from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ChestnutIndex(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key = True)
    query = Column(String(200), nullable = False)
    count = Column(Integer, nullable = False)

    def __init__(self, query='', count=1):
        self.path = path
        self.count = count

    def __repr__(self):
        return "<ChestnutIndex('%s','%s')>" % (self.id, self.path, self.count)
