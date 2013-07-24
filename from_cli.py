from chestnut.controllers.chestnut_index import ChestnutIndexController
from chestnut.controllers.history import HistoryController
import sys, os

search = ChestnutIndexController()

'Get the results'
sys.argv.pop(0) # remove the first element, which is usually './from_cli.py'
script_cmds = search.answer( sys.argv )

'Write commands that the parent bash script will execute'
f = open(search.home + "/.chestnut/tmp/cmds.txt","w")
f.write( "\n".join(script_cmds) )
f.close()

'Update the history'
history = HistoryController()
query = " ".join( sys.argv )
history.record( query )
