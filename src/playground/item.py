from storm.locals import *


class MediaItem(object):
    __storm_table__ = "items"

    item_id = Int(primary=True)
    file_path = Unicode()
    file_name = Unicode()
    stat_hash = Int()
    file_type = Int()
    metadata = Pickle()

    def __init__(self, path, name, h, t, metadata):
        self.file_path = path
        self.file_name = name
        self.stat_hash = h
        self.file_type = t
        self.metadata = metadata
