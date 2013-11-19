from bottle import get, view, app, request, redirect, route, post


@get('/myapps')
@view('myapps')
def myapps():

    # here get and display all apps
    # + a form to add a new one
    #
    return {'title': 'Mozilla Presence',
            'session': request.environ.get('beaker.session')}

@post('/myapps')
def post_app():
    # XXX receives a new app to add
    pass


