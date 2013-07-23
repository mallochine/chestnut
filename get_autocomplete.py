from chestnut.controllers.history import HistoryController
import sys, os

"""
The arguments will look something like:

    ['/path/to/get_autocompletion.py','j','arg_to_complete','prev_arg']
"""

"Don't need the first two args"
completion_args = sys.argv[2:]

"""
completion_args must always consist of two args:
completion_args[0] is the word to complete
completion_args[1] is the word immediately preceding the word to complete
"""
while len(completion_args) < 2:
    completion_args.insert(0, "")

word_to_complete = completion_args[0]
prev_word = completion_args[1]

history = HistoryController()
options = history.autocomplete( word_to_complete )

f = open(history.home + "/.chestnut/tmp_autocomplete.txt", "w")
f.write( " ".join(options) )
f.close()
