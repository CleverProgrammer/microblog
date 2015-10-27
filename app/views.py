from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm
from random import choice


@app.route('/')
@app.route('/index')
def index(user=''):
    if not user:
        user = choice([
            { 'nickname': 'Qazi' },
            { 'nickname': 'Adil' }
        ])
    else:
        user = {'nickname': user}

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
            'body': 'Stuff is pretty stuffy. Lorem snitchsum.'
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s",'
              'remember_me=%s'\
              %(form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


