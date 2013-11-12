import os

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

    def add_client(self, client):
        self.clients.append(client)

    def remove_client(self, client):
        self.clients.remove(client)

    def broadcast(self, message):
        for c in self.clients:
            c.write_message(message)


dispatcher = Dispatcher()


@get('/')
@view('index')
def index():
    return {'title': 'Presence Handler'}


@get('/admin')
@view('admin')
def admin():
    return {'title': 'Presence Handler', 'presence': dispatcher}



class PresenceHandler(tornado.websocket.WebSocketHandler):
    clients = []
    unique_id = 0

    @classmethod
    def get_username(cls):
        cls.unique_id += 1
        return 'User%d' % cls.unique_id

    def open(self):
        self.username = self.get_username()
        dispatcher.add_client(self)
        self.write_message("You are now appearing online.")

    def on_message(self, message):
        if message == '/quit':
            dispatcher.remove_client(self)
            self.close()

    def on_close(self):
        dispatcher.remove_client(self)



def main(port=8080, reloader=True):
    tornado_handlers = [
        (r"/presence", PresenceHandler),
        (r"/js/(.*)", tornado.web.StaticFileHandler,
         {"path": os.path.join(STATIC, 'js')}),
    ]
    run(port=port, reloader=reloader,
        server=TornadoWebSocketServer, handlers=tornado_handlers)
