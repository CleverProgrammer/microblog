#!/Users/Rafeh/anaconda/envs/microblog/bin/python3
import os
import unittest
from config import basedir
from app import app, db
from app.models import User, Post


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

    def test_Users_and_Posts(self):
        import datetime
        # create user 1
        u = User(nickname='john', email='john@email.com')
        db.session.add(u)
        db.session.commit()
        # create user 2
        u = User(nickname='susan', email='susan@email.com')
        db.session.add(u)
        db.session.commit()
        users = User.query.all()
        # Access everything
        self.assertEqual(users.__repr__(), "[<User 'john'>, <User 'susan'>]")

        # -------------- CHECK JOHN ---------------------------
        # Access john's id
        self.assertEqual(users[0].id, 1, "john's id should be 1")
        # Access john's nickname
        self.assertEqual(users[0].nickname, 'john', 'john should be john')
        # Access john's email
        self.assertEqual(users[0].email, 'john@email.com', 'john should be john')

        # -------------- CHECK SUSAN ---------------------------
        # Access susan's id
        self.assertEqual(users[1].id, 2, "susan's id should be 1")
        # Access susan's nickname
        self.assertEqual(users[1].nickname, 'susan', 'susan should be susan')
        # Access susan's email
        self.assertEqual(users[1].email, 'susan@email.com', 'susan should be susan')

        # Get users with id
        u = User.query.get(1)
        self.assertEqual(u.__repr__(), "<User 'john'>")
        susan = User.query.get(2)
        self.assertEqual(susan.__repr__(), "<User 'susan'>")

        # Get all posts from Susan
        post = Post(body='my first post!', timestamp=datetime.datetime.utcnow(), author=susan)
        db.session.add(post)
        db.session.commit()
        posts = susan.posts.all()
        self.assertEqual(posts.__repr__(), "[<Post 'my first post!'>]")

        # obtain author of each post
        for post in posts:
            print(post.id, post.author.nickname)
            self.assertEqual(post.id, 1)
            self.assertEqual(post.author.nickname, 'susan')
            self.assertEqual(post.body, "my first post!")
            pass

        # get all users in reverse alphabetical order
        nicknames_desc = User.query.order_by('nickname desc').all()
        expected = "[<User 'susan'>, <User 'john'>]"
        self.assertEqual(nicknames_desc.__repr__(), expected)
