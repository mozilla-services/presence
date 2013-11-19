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
