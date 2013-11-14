from bottle import get, view, app, request, redirect, route


@get('/')
@view('index')
def index():
    return {'title': 'Mozilla Presence',
            'session': request.environ.get('beaker.session')}

@get('/sidebar')
@view('sidebar')
def sidebar():
    return {'title': 'Mozilla Presence',
            'session': request.environ.get('beaker.session')}


@get('/admin')
@view('admin')
def admin():
    return {'title': 'Mozilla Presence Admin', 'presence': app.dispatcher}


@route('/login', method='POST')
def login():
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
def logout():
    app_session = request.environ.get('beaker.session')
    app_session['logged_in'] = False
    app_session['email'] = None
    redirect("/")
