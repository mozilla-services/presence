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
import tornado.wsgi, tornado.httpserver, tornado.ioloop

from dpresence.database import db_plugin
from dpresence.presence import Presence
from dpresence.views.user import PresenceHandler
from dpresence.views.developer import AppHandler



STATIC = os.path.join(os.path.dirname(__file__), 'static')
bottle.TEMPLATE_PATH = [os.path.join(os.path.dirname(__file__),
                                     'templates')]

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


class TornadoWebSocketServer(ServerAdapter):
    def run(self, handler): # pragma: no cover
        wsgiapp = handler[0]
        wsgiapp.install(db_plugin)
        wsgiapp = beaker.middleware.SessionMiddleware(handler[0])

        wsgi_handler = tornado.wsgi.WSGIContainer(wsgiapp)

        default_handlers = [
            (r".*", tornado.web.FallbackHandler, {'fallback': wsgi_handler})
        ]

        handlers = self.options.get('handlers')

        if isinstance(handlers, list):
            handlers = handlers + default_handlers
        else:
            handlers = default_handlers

        tornado_app = tornado.web.Application(handlers)
        tornado.httpserver.HTTPServer(tornado_app).listen(self.port)
        tornado.ioloop.IOLoop.instance().start()


def main(port=8282, reloader=True):
    tornado_handlers = [
        (r"/presence", PresenceHandler),
        (r"/myapps/(.*)", AppHandler),
        (r"/_admin", AdminHandler),
        (r"/js/(.*)", tornado.web.StaticFileHandler,
         {"path": os.path.join(STATIC, 'js')}),
        (r"/img/(.*)", tornado.web.StaticFileHandler,
         {"path": os.path.join(STATIC, 'img')}),
        (r"/css/(.*)", tornado.web.StaticFileHandler,
         {"path": os.path.join(STATIC, 'css')}),

    ]

    app.dispatcher = Presence()
    app.verifier = browserid.LocalVerifier(['*'])

    # importing all views
    from dpresence import views

    run(port=port, reloader=reloader, app=app,
        server=TornadoWebSocketServer, handlers=tornado_handlers)
