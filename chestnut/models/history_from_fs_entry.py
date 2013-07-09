from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

'Try to guess autocomplete based on common words in the filesystem'
class HistoryFromFSEntry(Base):
    __tablename__ = 'history_from_fs'
    id = Column(Integer, primary_key = True)
    word = Column(String(200), nullable = False)
    count = Column(Integer, nullable=False)

    def __init__(self, word='', count=1):
        self.word = word
        self.count = count

    def __repr__(self):
        id = self.id
        word = self.word
        count = self.count
        return "<HistoryFromFSEntry('%s','%s','%s')>" % (id, word, count)
