from bottle import route, run, static_file, response, abort
from tracker import Tracker
from encoder import DateTimeEncoder    
import json
import sys

@route('/')
def index():
  return static_file('index.html', root='./public')

@route('/robots.txt')
def robots():
  return static_file('robots.txt', root='./public')

@route('/track/<id>')
def track(id):
  details = Tracker().track(id)
  if details != None:
    response.set_header('Content-Type', 'application/json')
    return json.dumps(details, cls=DateTimeEncoder, sort_keys=True, indent=4, separators=(',', ': '))
  else:
    abort(404, 'Consignment details not Found')

run(host='0.0.0.0', port=sys.argv[1])