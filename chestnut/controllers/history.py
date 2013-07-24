from __future__ import division
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import os, sys, time, string

from chestnut.models.history_entry import HistoryEntry
from chestnut.models.chestnut_index_entry import ChestnutIndexEntry

class HistoryController:
    # Singleton Class
    home = os.path.expanduser("~")
    db_path = 'sqlite:///' + home + '/.chestnut/chestnut/models/chestnut.db'

    def __init__(self):
        self.db = create_engine( self.db_path )
        self.db.echo = False
        self.Session = sessionmaker(bind=self.db)
        self.session = self.Session()

        ChestnutIndexEntry.__table__.metadata = MetaData( bind=self.db )
        ChestnutIndexEntry.__table__.create(checkfirst=True)

        HistoryEntry.__table__.metadata = MetaData( bind=self.db )
        HistoryEntry.__table__.create(checkfirst=True)

    def record(self, query):
        q = self.session.query(HistoryEntry).filter_by(query=query).first()

        if q == None:
            self.session.add( HistoryEntry(query) )
        else:
            q.count += 1
#            print "This is the count:", q.count

        self.session.commit()

    def autocomplete(self, query):

        'Get only the string after the /'
        'Example: chestnut/controllers => controllers'
        split_query = query.split("/")
        word_to_complete = split_query.pop()
        prefix_phrase = ""
        if split_query != []:
            prefix_phrase = "/".join( split_query ) + "/"

        'Base autocomplete on the history in the logs'
        q = (self.session.query( HistoryEntry )
                .filter( HistoryEntry.query.like( word_to_complete+"%" ) )
                .all())
        results = []

        for row in q:
            results.append( prefix_phrase + row.query )

        return results
