#!/usr/bin/env python
# encoding=utf8
from __future__ import unicode_literals

import logging
import os.path
import shutil

from inotifyrecursive import INotify, flags, masks

# config
logging.basicConfig(level=logging.INFO)
blocklist = ['@eaDir', '.DS_Store']
cleanup_ms=5000
path = '/volume1'
exclude = []
mask = flags.CREATE #: Subfile was created

EA_DIRS = set()

def dirfilter(name, parent, is_dir):
    if name in blocklist:
        logging.info('Found: %s' % name)
        EA_DIRS.add((name, parent))
    if exclude and parent > 0:
        full_path = os.path.join(i.get_path(parent), name)
        if full_path in exclude:
            logging.info('excluding: %s' % full_path)
            return False
    return True

i = INotify()
logging.info('scanning tree')
i.add_watch_recursive(path, mask, dirfilter)


while True:
    try:
        events = i.read(timeout=cleanup_ms)
        logging.info('loop: %s' % events)
        if not events and EA_DIRS:
            logging.info('cleanup time')
            for name, parent in list(EA_DIRS):
                eaDir = os.path.join(i.get_path(parent), name)
                try:
                    logging.info('Deleting: %s' % eaDir)
                    if os.path.isfile(eaDir):
                        os.remove(eaDir) # Handle .DS_Store
                    else:
                        shutil.rmtree(eaDir)
                except OSError, e:
                    logging.exception('unknown issue')
                finally:
                    EA_DIRS.discard((name, parent))
    except OSError, e:
        print(e)
        logging.exception('inotify issue')
