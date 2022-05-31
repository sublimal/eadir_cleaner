Synology @eaDir cleaning daemon

Scans and monitors directories recursively under `path`. Will queue up any files matching `blocklist` on first scan, add new matches on creation (via inotify), and then cleanup/delete whenever there is idle block of `cleanup_ms`.

Supports python2.7 (DSM6)
Depends on Inotify Recursive:

    python -m pip install -r requirements.txt

Run in background shell or setup something more complicated

    $ ./eadir_cleaner.py
    INFO:root:scanning tree
    INFO:root:Found: @eaDir
    INFO:root:cleanup time
    INFO:root:Deleting: /volume1/public/test/@eaDir
