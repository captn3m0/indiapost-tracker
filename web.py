import json
import sys

from bottle import route, run, static_file, response, abort, request

from encoder import DateTimeEncoder
from tracker import Tracker
from auth import Auth
from international import InternationalTracker

t = Tracker()
auth = Auth()

@route('/')
def index():
    return static_file('index.html', root='./public')


@route('/robots.txt')
def robots():
    return static_file('robots.txt', root='./public')


@route('/track/<id>')
def track(id):
    details = None
    international = 'international' in request.query

    if international:
        details = InternationalTracker().track(id)
    else:
        details = t.track(id)

    if details is not None:
        response.set_header('Content-Type', 'application/json')
        return json.dumps(details, cls=DateTimeEncoder, sort_keys=True, indent=4, separators=(',', ': '))
    else:
        abort(404, 'Consignment details not Found')

@route('/captcha/update')
def update_captcha():
    if (auth.is_admin(request)):
        t.captcha_update(request.body)
    else:
        abort(403)


run(host='0.0.0.0', port=sys.argv[1])
