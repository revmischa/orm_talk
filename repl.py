#!/usr/bin/env python3
"""REPL"""

import atexit
import os
import readline
import rlcompleter
import logging

historyPath = os.path.expanduser("~/.pyhistory")

# Tab completion
readline.parse_and_bind('tab: complete')


def save_history(historyPath=historyPath):
    import readline
    readline.write_history_file(historyPath)

atexit.register(save_history)
del os, atexit, readline, rlcompleter, save_history, historyPath

def show_sql():
    import logging
    logging.getLogger('sqlalchemy.engine').setLevel(level=logging.INFO)
    print("SQL statements visible")

def hide_sql():
    import logging
    logging.getLogger('sqlalchemy.engine').setLevel(level=logging.NOTSET)

# handler = logging.Handler()
fmt = logging.Formatter(fmt=">")
sqlalchemy_log_handlers = logging.getLogger('sqlalchemy.engine').handlers
for handler in sqlalchemy_log_handlers:
    handler.setFormatter(fmt)
# handler.setFormatter(fmt)
# logging.getLogger('sqlalchemy.engine').addHandler(handler)
# logging.getLogger('sqlalchemy.engine').basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


banner = """
   __   , __  ,__ __       ____                      
  /\_\//|/  \/|  |  |     (|   \                     
 |    | |___/ |  |  |      |    | _   _  _  _    __  
 |    | | \   |  |  |     _|    ||/  / |/ |/ |  /  \_
  \__/  |  \_/|  |  |_/  (/\___/ |__/  |  |  |_/\__/ 
  ==================================================

"""

show_sql()
from model import *
main()

