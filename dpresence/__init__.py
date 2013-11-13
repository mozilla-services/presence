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
from dpresence.presence import Presence

STATIC = os.path.join(os.path.dirname(__file__), 'static')
bottle.TEMPLATE_PATH = [os.path.join(os.path.dirname(__file__),
                                     'views')]

debug(True)

session_opts = {
    'session.type': 'file',
    'session.data_dir': './session/',
    'session.auto': True,
    }

STATIC = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))


class AdminHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        app.dispatcher.subscribe_events(self._event)

    def on_close(self):
        app.dispatcher.unsubscribe_events(self._event)

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
                app.dispatcher.add_client(self)
            else:
                app.dispatcher.remove_client(self)

            self.write_message(dumps({"status": status,
                                      "user": user}))
        else:
            self.write_message(dumps({"status": "error",
                                      "user": user}))

    def on_close(self):
        app.dispatcher.remove_client(self)


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

    app.dispatcher = Presence()
    app.verifier = browserid.LocalVerifier(['*'])

    from dpresence import views

    run(port=port, reloader=reloader, app=app,
        server=TornadoWebSocketServer, handlers=tornado_handlers)
