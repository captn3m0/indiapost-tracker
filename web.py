import json
import sys

from bottle import route, run, static_file, response, abort, request

from encoder import DateTimeEncoder
from tracker import Tracker


@route('/')
def index():
    return static_file('index.html', root='./public')


@route('/robots.txt')
def robots():
    return static_file('robots.txt', root='./public')


@route('/track/<id>')
def track(id):
    international = 'international' in request.query
    details = Tracker().track(id, international)
    if details is not None:
        response.set_header('Content-Type', 'application/json')
        return json.dumps(details, cls=DateTimeEncoder, sort_keys=True, indent=4, separators=(',', ': '))
    else:
        abort(404, 'Consignment details not Found')


run(host='0.0.0.0', port=sys.argv[1])
