#!/usr/bin/python

from __future__ import division
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import os, sys, time, string

from chestnut.models.history_entry import HistoryEntry
from chestnut.models.history_from_fs_entry import HistoryFromFSEntry
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

        HistoryFromFSEntry.__table__.metadata = MetaData( bind=self.db )
        HistoryFromFSEntry.__table__.create(checkfirst=True)

    def record(self, query):
        q = self.session.query(HistoryEntry).filter_by(query=query).first()

        if q == None:
            self.session.add( HistoryEntry(query) )
        else:
            q.count += 1
#            print "This is the count:", q.count

        self.session.commit()

    def build_history_from_fs(self):
        'All the keywords in the filesystem should be in the index'
        index = (self.session.query( ChestnutIndexEntry.path )
                        .all())

        words_count_table = {}
        for entry in index:
            bag_of_words = entry.path.split("/")
            for word in bag_of_words:
                if word in words_count_table:
                    words_count_table[word] += 1
                else:
                    words_count_table[word] = 1

        for word in words_count_table:
            self.session.add( HistoryFromFSEntry(word, words_count_table[word]))

        self.session.commit()
#        print words_count_table

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

        'If autocomplete had no matches, default to matches based on filesystem'
        if len(results) == 0:

            'If HistoryFromFSEntry has no rows, then build the table'
            if self.session.query( HistoryFromFSEntry ).count() == 0:
                self.build_history_from_fs()

            'Proceed to find matches'
            q = (self.session.query( HistoryFromFSEntry )
                    .filter(HistoryFromFSEntry.word.like(word_to_complete+"%"))
                    .all())

            'Store matches into results'
            for row in q:
                results.append( prefix_phrase + row.word )

        return results
