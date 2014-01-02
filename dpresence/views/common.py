from bottle import get, view, app, request, redirect, route
from bottle import request, response


def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

        if request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cors


def get_user():
    session = request.environ.get('beaker.session')
    return session.get('email')


@route('/login', method='POST')
@enable_cors
def login(db=None):
    assertion = request.POST['assertion']
    try:
        data = app.verifier.verify(assertion, '*')
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
@enable_cors
def logout(db=None):
    app_session = request.environ.get('beaker.session')
    app_session['logged_in'] = False
    if 'email' in app_session:
        del app_session['email']
    app_session.save()
    redirect("/")
