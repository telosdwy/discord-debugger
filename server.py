import flask, datetime, webbrowser
from discordapi import *

# A basic flask server for what we're doing.

app:flask.Flask = flask.Flask(__name__)

@app.route('/') # Index
def index() -> flask.Response:
    if flask.request.args.get('code'):
        try:
            token = fetchBearerToken(flask.request.args['code'])
            resp = flask.make_response('<a href = \'/\'>Return home</a><br>Okay<br>%s' % token)
            resp.set_cookie('access_token', token['access_token'], expires = datetime.datetime.now() + datetime.timedelta(days = 7))
            resp.set_cookie('scope', token['scope'], expires = datetime.datetime.now() + datetime.timedelta(days = 7))
            return resp
        except Exception as e:
            return '<a href = \'/\'>Return home</a><br>Fail -- %s' % e
    else:
        return flask.render_template('index.html', CLIENT_ID = CLIENT_ID, routes = routes)

@app.route('/request')
def request() -> flask.Response:
    try:
        route = next( route for route in routes if route.name == flask.request.args['route'] )
        access_token = flask.request.cookies['access_token']
        t = route.function(API(access_token), **flask.request.args)
        return '<a href = \'/\'>Return home</a><br>Okay<br>%s' % t
    except Exception as e:
        return '<a href = \'/\'>Return home</a><br>Fail -- %s' % e

@app.route('/ipc') # IPC routes
def ipc() -> flask.Response:
    return flask.render_template('ipc.html', CLIENT_ID = CLIENT_ID, routes = routes)

@app.route('/ipc/request')
def ipcRequest() -> flask.Response:
    return 'Not implemented yet'

if __name__ == '__main__':
    webbrowser.open('http://localhost:1234')
    app.run(host = '0.0.0.0', port = 1234)
