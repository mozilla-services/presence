from json import dumps, loads

from bottle import get, view, app, request, redirect, route, post, abort
from tornado.websocket import WebSocketHandler

from dpresence.database import Application, get_session
from dpresence.views.common import get_user


# web socket at /myapps/<appid>
class AppHandler(WebSocketHandler):
    """Handles the app presence stream
    """
    def __init__(self, *args, **kw):
        WebSocketHandler.__init__(self, *args, **kw)
        self.application = None

    def on_message(self, message):
        message = loads(message)
        action = message.get('action')

        # authenticatino
        if action == 'auth':
            # XXX let's verify the token
            self.write_message(dumps({'result': 'OK',
                                      'action': action}))
            self.connected = True
            return

        if not self.connected:
            # we're supposed to be connected here
            self.send(dumps({'result': 'ERROR'}))

        return

    def open(self, appid):
        db = get_session()
        apps = db.query(Application).filter_by(uid=appid)
        self.application = apps.first()
        if self.application is None:
            self.close()

        # XXX make sure the app exists
        app.dispatcher.subscribe_events(self._event)

    def on_close(self):
        try:
            app.dispatcher.unsubscribe_events(self._event)
        except ValueError:
            pass

    def _can_see_user(self, email, app_uid):
        # XXX todo: return the user uid
        # given the user email and app id
        # this is located in ApplicationUser
        return 1234

    def _event(self, event):
        # here we will allow the connection to see the presence
        # change if the user has allowed that app to see her
        user_uid = self._can_see_user(event['user'], self.application.uid)

        if user_uid is not None:
            # user_uid is the user uid as the app knows it
            # we replace the email in the event with that id
            del event['user']
            event['uid'] = user_uid

            # sends events as they come (status changes in presence)
            self.write_message(dumps(event))



@get('/myapps')
@view('myapps')
def myapps(db):
    email = get_user()
    if email is None:
        apps = []
    else:
        apps = db.query(Application).filter_by(email=email)

    return {'title': 'Mozilla Presence',
            'session': request.environ.get('beaker.session'),
            'apps': apps}


@post('/myapps')
def post_app(db):
    email = get_user()
    if email is None:
        abort(401, "Authorization required")

    # XXX CRSF protection etc..
    data = dict(request.POST)
    data['email'] = email
    app = Application(**data)
    db.add(app)

    redirect('/myapps')

@post('/validate_app')
def validate_app(db):
    email = get_user()
    if email is None:
        abort(401, "Authorization required")

    # XXX CRSF protection etc..
    name = request.POST['name']
    app = db.query(Application).filter_by(email=email, name=name)
    app = app.first()
    if app is not None:
        app.validate_domain()

    redirect('/myapps')

@post('/activate_app')
def activate_app(db):
    email = get_user()
    if email is None:
        abort(401, "Authorization required")

    # XXX CRSF protection etc..
    name = request.POST['name']
    app = db.query(Application).filter_by(email=email, name=name)
    app = app.first()
    if app is not None:
        app.notified = 'activate' in request.POST

    redirect('/myapps')
