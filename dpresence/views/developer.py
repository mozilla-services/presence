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
