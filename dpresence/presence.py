
class Presence(object):
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



