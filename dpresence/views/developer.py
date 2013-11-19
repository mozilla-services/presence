from bottle import get, view, app, request, redirect, route


@get('/myapps')
@view('myapps')
def myapps():

    # here get and display all apps
    # + a form to add a new one
    #
    return {'title': 'Mozilla Presence',
            'session': request.environ.get('beaker.session')}
