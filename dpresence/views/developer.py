from bottle import get, view, app, request, redirect, route, post, abort

from dpresence.database import Application
from dpresence.views.common import get_user


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
