from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class HistoryEntry(Base):
    __tablename__ = 'history'
    id = Column(Integer, primary_key = True)
    query = Column(String(200), nullable = False)
    count = Column(Integer, nullable=False)

    def __init__(self, query='', count=1):
        self.query = query
        self.count = count

    def __repr__(self):
        id = self.id
        query = self.query
        count = self.count
        return "<HistoryEntry('%s','%s','%s')>" % (id, query, count)
