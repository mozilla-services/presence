import time
from json import dumps, loads

from bottle import get, view, app, request, redirect, route, post, abort
from bottle import HTTPResponse

from tornado.websocket import WebSocketHandler
from tornado.ioloop import IOLoop

from dpresence.views.common import get_user
from dpresence.database import ApplicationUser, pop_notifications, Application


#
# web socket at /presence
#
class PresenceHandler(WebSocketHandler):
    """Handles the user presence
    """
    def __init__(self, *args, **kw):
        print 'Presence handler created'
        WebSocketHandler.__init__(self, *args, **kw)
        self._user = None
        self._closed = False
        IOLoop.instance().add_timeout(time.time() + 5,
                                      self._check_notifications)
    def open(self):
        print 'web socket opened'    
        msg = {'message': 'welcome'}
        self.write_message(dumps({"status": "notification",
                                  "user": "root",
                                  "notifications": [msg]}))

 

    def _check_notifications(self):
        print '_check_notifications'
        if self._user is not None:
            print '_check_notifications %s connected' % self._user
            notifications = pop_notifications(self._user)
            if len(notifications) > 0:
                print '%s got some, sending' % self._user
                self.write_message(dumps({"status": "notification",
                                          "user": self._user,
                                          "notifications": notifications}))
        else:
            # anonymous user, let's drop it
            print '_check_notification anonymous user.. dropping'

        # back in 5'
        if not self._closed:
            IOLoop.instance().add_timeout(time.time() + 5,
                                          self._check_notifications)

    def get_username(self):
        return self._user

    def on_message(self, message):
        print 'received ' + message
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
        self._closed = True


#
# apps permissions APIs
#

@get('/redirect')
def redirect():
    redirect_url = request.GET.get('url', '/')
    code = 303 if request.get('SERVER_PROTOCOL') == "HTTP/1.1" else 302
    response = HTTPResponse("", status=code, Location=redirect_url)
    raise response


    return {'title': 'Mozilla Presence',
            'session': request.environ.get('beaker.session'),
            'redirect': request.GET['redirect']}



@get('/grant/<appid>')
@view('grant')
def grant(appid, db):
    if 'redirect' not in request.GET:
        raise HTTPResponse("", status=400)

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


def _get_apps(db):
    email = get_user()
    if email is not None:
        # XXX will do a join or something

        app_ids = [app.appid for app in
                    db.query(ApplicationUser).filter_by(email=email)]
        if app_ids == []:
            apps = []
        else:
            in_ = Application.__table__.c.uid.in_
            apps = db.query(Application).filter(in_(app_ids))
    else:
        apps = []

    return [{'name': app.name, 'uid': app.uid} for app in apps]


@route('/getApps', method='GET')
def get_apps(db):
    return {'apps': _get_apps(db)}


def _revoke_apps(db, appid):
    email = get_user()
    if email is None:
        return {'result': 'error'}

    apps = db.query(ApplicationUser).filter_by(email=email, appid=appid)
    apps.delete()
    return {'result': 'OK'}


@post('/revoke/<appid>', method='GET')
def revoke(appid, db):
    return _revoke_apps(db, appid)


@get('/sidebar')
@view('sidebar')
def sidebar(db):
    return {'title': 'Mozilla Presence',
            'session': request.environ.get('beaker.session'),
            'apps': _get_apps(db)}


@get('/admin')
@view('admin')
def admin(db):
    return {'title': 'Mozilla Presence Admin', 'presence': app.dispatcher}
