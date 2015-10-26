from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Qazi'}
    return '''
<html>
    <head>
        <title>Home Page</title>
    </head>
    <body>
        <h1>Hello, ''' + user['nickname'] + '''</h1>
    </body>
</html>
'''

