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
mask = flags.CREATE #: Subfile was created

EA_DIRS = set()

def dirfilter(name, parent, is_dir):
    if name in blocklist:
        logging.info('Found: %s' % name)
        EA_DIRS.add((name, parent))
    return True

i = INotify()
logging.info('scanning tree')
i.add_watch_recursive(path, mask, dirfilter)


while True:
    events = i.read(timeout=cleanup_ms)
    logging.debug('loop: %s' % events)
    if not events and EA_DIRS:
        logging.info('cleanup time')
        for name, parent in list(EA_DIRS):
            eaDir = os.path.join(i.get_path(parent), name)
            try:
                logging.info('Deleting: %s' % eaDir)
                shutil.rmtree(eaDir)
            except OSError, e:
                logging.exception('unknown issue')
            finally:
                EA_DIRS.discard((name, parent))
