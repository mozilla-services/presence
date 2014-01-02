from bottle import get, view, app, request, redirect, route


def get_user():
    session = request.environ.get('beaker.session')
    return session.get('email')


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
    if 'email' in app_session:
        del app_session['email']
    app_session.save()
    redirect("/")
