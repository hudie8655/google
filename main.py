from flask import Flask
from rmrb import tmp
from google.appengine.api import taskqueue
app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    taskqueue.add(url='/rmrb')#, target='rmrb')
    return "htllo"#urllib.urlopen('http://www.baidu.com').read()


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
	
@app.route('/rmrb',methods=['POST','GET'])
def rmrb():
	tmp()
	return 'sended'
