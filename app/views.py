from flask import render_template
from app import app
from random import choice


@app.route('/')
@app.route('/index')
def index():
    user = choice([
        { 'nickname': 'Qazi' },
        { 'nickname': 'Adil' }
    ])

    posts = [
        {
            'author': {'nickname': 'Magnus'},
            'body': 'A beautiful chess game!'
        },
        {
            'author': {'nickname': 'Carlsen'},
            'body': 'An immortal game that one must see...'
        },
        {
            'author': {'nickname': 'Qazi'},
            'body': 'Chess is pretty cool.'
        },
        {
            'author': {'nickname': 'Joker'},
            'body': 'Stuff is pretty stuffy. Lorem bitchsum.'
        }
    ]

    images = {
        'cat':'http://bit.ly/1Brje4z',
        'ugly-cat': 'http://bit.ly/1O4b1LS',
        'curtain-cat': 'http://bit.ly/1MfLNDN',
        'claw-cat': 'http://bit.ly/1E3DquM'
    }

    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts,
                           images=images)

