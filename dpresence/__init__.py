from bottle import *
from bottle.ext.tornadosocket import TornadoWebSocketServer
import tornado.web
import tornado.websocket

debug(True)


@get('/')
@view('index')
def index():
    return {'title': 'Presence Handler'}



class MessageDispatcher(object):
    clients = []

    @classmethod
    def add_client(cls, client):
        cls.clients.append(client)

    @classmethod
    def remove_client(cls, client):
        cls.clients.remove(client)

    @classmethod
    def broadcast(cls, message):
        for c in cls.clients:
            c.write_message(message)


class PresenceHandler(tornado.websocket.WebSocketHandler):
    clients = []
    unique_id = 0

    @classmethod
    def get_username(cls):
        cls.unique_id += 1
        return 'User%d' % cls.unique_id

    def open(self):
        self.username = self.get_username()
        MessageDispatcher.add_client(self)

    def on_message(self, message):
        if message == '/quit':
            MessageDispatcher.remove_client(self)
            self.close()

    def on_close(self):
        MessageDispatcher.remove_client(self)



def main(port=8080, reloader=True):
    tornado_handlers = [
        (r"/++presence++", PresenceHandler),
        (r"/js/(.*)", tornado.web.StaticFileHandler,
         {"path": "./static/js/"}),
    ]
    run(port=port, reloader=reloader,
        server=TornadoWebSocketServer, handlers=tornado_handlers)
