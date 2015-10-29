#!/Users/Rafeh/anaconda/envs/microblog/bin/python3
import os
import unittest
from config import basedir
from app import app, db
from app.models import User


class MyTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_avatar(self):
        u = User(nickname='john', email='john@example.com')
        avatar = u.avatar(128)
        expected = 'http://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6'
        self.assertEqual(avatar[0:len(expected)], expected, 'test avatar')

    def test_make_unique_nickname(self):
        # add john in the database
        u = User(nickname='john', email='john@example.com')
        db.session.add(u)
        db.session.commit()
        # create a unique username for 2nd john since we have already added the first one
        nickname = User.make_unique_nickname('john')
        self.assertEqual(nickname != 'John', True, 'test make unique nickname')
        u = User(nickname=nickname, email='susan@example.com')
        db.session.add(u)
        db.session.commit()
        nickname2 = User.make_unique_nickname('john')
        self.assertEqual(nickname2 != 'john', True, 'test make unique nickname2')
        self.assertEqual(nickname2 != nickname, True, 'test make unique nickname2')
        print(nickname, nickname2)

