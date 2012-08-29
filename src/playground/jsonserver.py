import pickle

from storm.locals import *
from bottle import route, run, request

from item import MediaItem


DB_FILE = "pipboy-media.db"
database = None
store = None


@route('/api/1.0/all_music')
def all_music():
    lim = request.query.lim or '100'
    limit = int(lim)
    result = store.find(MediaItem, MediaItem.file_type == 0)
    music_list = [pickle.loads(item.metadata) for item in result.order_by(MediaItem.file_path)[:limit]]
    return {'all_music': music_list}


if __name__ == "__main__":
    database = create_database("sqlite:" + DB_FILE)
    store = Store(database)

    run(host='localhost', port=8990)
