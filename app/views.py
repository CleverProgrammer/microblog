from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .forms import LoginForm
from .models import User
from random import choice


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
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
@oid.loginhandler  # tells flask that this is our login view function.
def login():
    # flask.g global is used to share and store data during the life of a session by flask.
    # we will be storing the logged in user in g.
    if g.user is not None and g.user.is_authenticated:
        # letting flask build its own links using url_for
        # I can also simply just remove the url_for.
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # flask.session stores data and keeps it alive for that particular user for all their
        # future requests.
        # store remember me boolean value
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

@app.before_request
def before_request():
    g.user = current_user

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again')
        return redirect(url_for('login'))
    # check our database for the user email.
    user = User.query.filter_by(email=resp.email).first()
    # if not found in our database, then this is a new user.
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    # session is a dictionary.
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    # register this if it is a valid login.
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))
