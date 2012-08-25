#!/usr/bin/env python
"""
Mosspatch is a streaming media server that lets you access your music and
videos from web browsers and mobile devices.

mosspatch.py is the backend server that manages your media library and
streaming/transcoding media for presentation on other devices.
"""

from mosspatch.settings import MosspatchConfig
from mosspatch.server import MosspatchServer


if __name__ == "__main__":
    config = MosspatchConfig()
    server = MosspatchServer(config)
    server.run()
