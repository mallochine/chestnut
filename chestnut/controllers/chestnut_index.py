from __future__ import division
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import os, sys, time, string

from chestnut.models.chestnut_index_entry import ChestnutIndexEntry

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

        'Clear all the entries in chestnut_index'
        ChestnutIndexEntry.__table__.drop(checkfirst=True)
        ChestnutIndexEntry.__table__.create(checkfirst=True)

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

    def answer(self, query):
        if self.session.query(ChestnutIndexEntry).count() == 0:
            self.crawl( self.home )

        actual_query = " ".join(query)
        index = (self.session.query(ChestnutIndexEntry)
                    .filter(ChestnutIndexEntry.path.like("%"+actual_query+"%"))
                    .all())

        "Get the shortest path in index"
        best_path = self.home + "/"
        if index != []:
            best_path = min(index, key=lambda entry: len(entry.path)).path

        """
        Now that we have the path, get the appropriate command.
        We want to use vim for file, and cd for directories
        """
        commands = []
        commands.append("cd " + self.get_dir( best_path ))

        commands.append("echo")
        commands.append("pwd")
        commands.append("echo")

        if best_path[-1] != '/':
            commands.append("vim " + best_path)

        return commands
