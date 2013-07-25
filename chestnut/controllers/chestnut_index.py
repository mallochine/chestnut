from __future__ import division
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import os, sys, time, string

from chestnut.models.chestnut_index_entry import ChestnutIndexEntry
from chestnut.controllers.history import HistoryController

class ChestnutIndexController:
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

    'Given the path to the file, return the directory of the file'
    def get_dir(self, path):
        while path[-1] != '/':
            path = path[:-1]
            if path == "": break
        return path

    def crawl(self, start_path):
        start_time = time.time()

        'Walk through all the files and sub-directories'
        for (dirpath, dirnames, filenames) in os.walk(start_path):
            'Add and print the current directory'
            self.session.add( ChestnutIndexEntry( dirpath+'/' ) )
            print dirpath

            'Add and print all the files in the current directory'
            for filename in filenames:
                full_file_path = os.sep.join([dirpath, filename])
                self.session.add( ChestnutIndexEntry(full_file_path) )
                print full_file_path

        self.session.commit()
        finish_time = time.time()

        print "Crawl took", (finish_time - start_time), "seconds"

    def populate_empty_tables(self):
        'If table chestnut_index is empty:'
        if self.session.query(ChestnutIndexEntry).count() == 0:

            'Clear all the entries in chestnut_index'
            ChestnutIndexEntry.__table__.drop(checkfirst=True)
            ChestnutIndexEntry.__table__.create(checkfirst=True)

            self.crawl( self.home )

    def answer(self, query):
        'Answering the query requires non-empty tables'
        self.populate_empty_tables()

        'Start the timer on the query'
        start_time = time.time()

        'Get the shortest path that contains query'
        actual_query = " ".join(query)
#        best_entry = (self.session.query(ChestnutIndexEntry)
#                    .filter(ChestnutIndexEntry.path.like("%"+actual_query+"%"))
#                    .order_by( func.char_length(ChestnutIndexEntry.path) )
#                    .first())
        query = self.session.query(ChestnutIndexEntry)
        query = query.filter(ChestnutIndexEntry.path.like("%"+actual_query+"%"))
        query = query.order_by( func.char_length(ChestnutIndexEntry.path) )
        query = query.limit(5)

        print query.statement

        best_entry = query.first()

        best_path = self.home + "/"
        if best_entry is not None:
            best_path = best_entry.path

        '''
        Now that we have the path, request the appropriate commands.
        We want to use vim for editing, and cd for directories.
        '''
        commands = []
        commands.append('cd ' + self.get_dir( best_path ))
        commands.append('echo')
        commands.append('pwd')
        commands.append('echo')

        if best_path[-1] != '/':
            commands.append('vim ' + best_path)

        'Stop the timer on the query'
        finish_time = time.time()

        'Print how long the query took'
        print "Query took", (finish_time - start_time), "seconds"

        return commands
