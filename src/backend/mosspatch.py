#!/usr/bin/env python
"""
Mosspatch is a streaming media server that lets you access your music and
videos from web browsers and mobile devices.

mosspatch.py is the backend server that manages your media library and
streaming/transcoding media for presentation on other devices.
"""

from mosspatch.settings import MosspatchConfig
from mosspatch.server import MosspatchServer
from mosspatch.database.base import MosspatchDatabase
from mosspatch.database.setting import Setting


if __name__ == "__main__":
    config = MosspatchConfig()
    server = MosspatchServer(config)
    db = MosspatchDatabase(config)

    db.session.add_all([Setting('audio-extensions', 'flac, m4a, mp3'),
                        Setting('video-extensions', 'avi, mp4, mpg, mkv')])
    db.session.commit()

    s = db.session.query(Setting).all()
    for p in  s:
        print p
