from json import dumps, loads
import os
import browserid
import beaker.middleware


from bottle import ServerAdapter
import bottle
from bottle import *
from bottle.ext.tornadosocket import TornadoWebSocketServer
import tornado.web
import tornado.websocket

STATIC = os.path.join(os.path.dirname(__file__), 'static')
bottle.TEMPLATE_PATH = [os.path.join(os.path.dirname(__file__),
                                     'views')]

debug(True)



class Dispatcher(object):
    def __init__(self):
        self.clients = []
        self.subscribe = []

    def add_client(self, client):
        evt = {'user': client.get_username(),
               'status': 'online'}
        for sub in self.subscribe:
            sub(evt)
        self.clients.append(client)

    def remove_client(self, client):
        user = client.get_username()
        evt = {'user': user,
               'status': 'offline'}
        for sub in self.subscribe:
            sub(evt)
        if client in self.clients:
            self.clients.remove(client)

    def broadcast(self, message):
        for c in self.clients:
            c.write_message(message)

    def subscribe_events(self, handler):
        self.subscribe.append(handler)

    def unsubscribe_events(self, handler):
        self.subscribe.remove(handler)


dispatcher = Dispatcher()
session_opts = {
    'session.type': 'file',
    'session.data_dir': './session/',
    'session.auto': True,
    }

STATIC = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))

verifier = browserid.LocalVerifier(['*'])


@get('/')
@view('index')
def index():
    return {'title': 'Presence Handler',
            'session': request.environ.get('beaker.session')}


@get('/admin')
@view('admin')
def admin():
    return {'title': 'Presence Handler', 'presence': dispatcher}

@route('/login', method='POST')
def login():
    assertion = request.POST['assertion']
    try:
        data = verifier.verify(assertion, '*')
        email = data['email']
        app_session = request.environ.get('beaker.session')
        app_session['logged_in'] = True
        app_session['email'] = email
        app_session['assertion'] = assertion
        app_session.save()
    except ValueError, UnicodeDecodeError:
        # need to raise a auth
        pass
    return {'email': email}


@route('/logout', method='POST')
def logout():
    app_session = request.environ.get('beaker.session')
    app_session['logged_in'] = False
    app_session['email'] = None
    redirect("/")



class AdminHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        dispatcher.subscribe_events(self._event)

    def on_close(self):
        dispatcher.unsubscribe_events(self._event)

    def _event(self, event):
        print event
        # sends events as they come (status changes in presence)
        self.write_message(dumps(event))


class PresenceHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kw):
        tornado.websocket.WebSocketHandler.__init__(self, *args, **kw)
        self._user = None

    def get_username(self):
        return self._user

    def on_message(self, message):
        message = loads(message)
        self._user = user = message['user']
        status = message['status']

        if status in ('online', 'offline'):
            if status == 'online':
                dispatcher.add_client(self)
            else:
                dispatcher.remove_client(self)

            self.write_message(dumps({"status": status,
                                      "user": user}))
        else:
            self.write_message(dumps({"status": "error",
                                      "user": user}))

    def on_close(self):
        dispatcher.remove_client(self)


class TornadoWebSocketServer(ServerAdapter):
    def run(self, handler): # pragma: no cover
        import tornado.wsgi, tornado.httpserver, tornado.ioloop
        wsgiapp = beaker.middleware.SessionMiddleware(handler[0])
        wsgi_handler = tornado.wsgi.WSGIContainer(wsgiapp)

        default_handlers = [
            (r".*", tornado.web.FallbackHandler, {'fallback': wsgi_handler})
        ]

        if self.options['handlers'] is not None and isinstance(self.options['handlers'], list):
            handlers = list(self.options['handlers']) + list(default_handlers)
        else:
            handlers = default_handlers

        tornado_app = tornado.web.Application(handlers)
        tornado.httpserver.HTTPServer(tornado_app).listen(self.port)
        tornado.ioloop.IOLoop.instance().start()


def main(port=8080, reloader=True):
    tornado_handlers = [
        (r"/presence", PresenceHandler),
        (r"/_admin", AdminHandler),
        (r"/js/(.*)", tornado.web.StaticFileHandler,
         {"path": os.path.join(STATIC, 'js')}),
    ]
    run(port=port, reloader=reloader, app=app,
        server=TornadoWebSocketServer, handlers=tornado_handlers)
