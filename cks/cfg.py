import os

DATADIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
CKSDIR = os.getenv('CKSDIR', os.path.expanduser('~/.cks'))