from json import dumps
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
        self.subscribe = []

    def add_client(self, client):
        evt = {'user': client.get_username(),
               'status': 'online'}
        for sub in self.subscribe:
            sub(evt)
        self.clients.append(client)

    def remove_client(self, client):
        evt = {'user': client.get_username(),
               'status': 'offline'}
        for sub in self.subscribe:
            sub(evt)
        self.clients.remove(client)

    def broadcast(self, message):
        for c in self.clients:
            c.write_message(message)

    def subscribe_events(self, handler):
        self.subscribe.append(handler)

    def unsubscribe_events(self, handler):
        self.subscribe.remove(handler)


dispatcher = Dispatcher()


@get('/')
@view('index')
def index():
    return {'title': 'Presence Handler'}


@get('/admin')
@view('admin')
def admin():
    return {'title': 'Presence Handler', 'presence': dispatcher}


class AdminHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        dispatcher.subscribe_events(self._event)

    def on_close(self):
        dispatcher.unsubscribe_events(self._event)

    def _event(self, event):
        # sends events as they come (status changes in presence)
        self.write_message(dumps(event))


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
        self.write_message(dumps({"status": "online",
                                  "user": self.username}))

    def on_message(self, message):
        user = self.get_username()

        if message == 'online':
            dispatcher.add_client(self)
            self.write_message(dumps({"status": "online",
                                      "user": user}))
        elif message == 'offline':
            dispatcher.remove_client(self)
            self.write_message(dumps({"status": "offline",
                                      "user": user}))
        elif message == 'list':
            data = {'users': dispatcher.clients}
            self.write_message(dumps(data))
        else:
            self.write_message(dumps({"status": "error",
                                      "user": user}))

    def on_close(self):
        dispatcher.remove_client(self)



def main(port=8080, reloader=True):
    tornado_handlers = [
        (r"/presence", PresenceHandler),
        (r"/_admin", AdminHandler),
        (r"/js/(.*)", tornado.web.StaticFileHandler,
         {"path": os.path.join(STATIC, 'js')}),
    ]
    run(port=port, reloader=reloader,
        server=TornadoWebSocketServer, handlers=tornado_handlers)
