import pickle
import os

from storm.locals import *
from bottle import route, run, request, static_file

from item import MediaItem


DB_FILE = "media.db"
database = None
store = None


@route('/api/1.0/all_music')
def all_music():
    lim = request.query.lim or '100'
    limit = int(lim)
    result = store.find(MediaItem, MediaItem.file_type == 0)
    music_list = []
    for item in result.order_by(MediaItem.item_id)[:limit]:
        md = pickle.loads(item.metadata)
        music_list.append({'item_id': item.item_id,
                           'title': md['title'] or item.file_name,
                           'artist': md.get('artist', 'Unknown'),
                           'album': md.get('album', 'Unknown'),
                           'year': md.get('year', 'Unknown')})

    return {'all_music': music_list}


@route('/')
def frontend():
    return static_file('frontend.htm', root=os.getcwd())


@route('/js/<filename:path>')
def static_js(filename):
    return static_file(filename, root=os.getcwd() + '/js/')


if __name__ == "__main__":
    database = create_database("sqlite:" + DB_FILE)
    store = Store(database)

    run(host='localhost', port=8990)
