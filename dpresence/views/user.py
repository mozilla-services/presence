from json import dumps, loads

from bottle import get, view, app, request, redirect, route, post, abort
from bottle import HTTPResponse

from tornado.websocket import WebSocketHandler

from dpresence.views.common import get_user
from dpresence.database import ApplicationUser


class PresenceHandler(WebSocketHandler):
    """Handles the user presence
    """
    def __init__(self, *args, **kw):
        WebSocketHandler.__init__(self, *args, **kw)
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


@get('/grant/<appid>')
@view('grant')
def grant(appid, db):
    return {'title': 'Mozilla Presence',
            'session': request.environ.get('beaker.session'),
            'redirect': request.GET['redirect']}


@post('/grant/<appid>')
def post_grant(appid, db):
    email = get_user()
    if email is None:
        abort(401, "Authorization required")


    redirect_url = request.POST['redirect']

    if 'allow' in request.POST:
        app_user = ApplicationUser(appid, email)
        db.add(app_user)
        uid = app_user.uid
        redirect_url += '?' + 'Presence-UID=%s' % str(uid)

    code = 303 if request.get('SERVER_PROTOCOL') == "HTTP/1.1" else 302
    response = HTTPResponse("", status=code, Location=redirect_url)
    raise response


@get('/')
@view('index')
def index(db):
    return {'title': 'Mozilla Presence',
            'session': request.environ.get('beaker.session')}


@get('/sidebar')
@view('sidebar')
def sidebar(db):
    return {'title': 'Mozilla Presence',
            'session': request.environ.get('beaker.session')}


@get('/admin')
@view('admin')
def admin(db):
    return {'title': 'Mozilla Presence Admin', 'presence': app.dispatcher}
