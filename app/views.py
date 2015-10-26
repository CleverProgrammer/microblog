from flask import render_template
from app import app
from random import choice

@app.route('/')
@app.route('/index')
def index():
    user = choice([{'nickname': 'Qazi'}, {'nickname': 'James'}])
    posts = [
        {
            'author': {'swagname': 'Magnus'},
            'body': 'A beautiful chess game!'
        },
        {
            'author': {'swagname': 'Carlsen'},
            'body': 'An immortal game that one must see...'
        },
        {
            'author': {'swagname': 'Qazi'},
            'body': 'Chess is pretty cool.'
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)

