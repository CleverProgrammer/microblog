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
        print('I am in setup')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        print('I am in tearDown')

    def test_avatar(self):
        u = User(nickname='john', email='john@example.com')
        avatar = u.avatar(128)
        expected = 'http://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6'
        self.assertEqual(avatar[0:len(expected)], expected, 'test avatar')
        print('I am testing avatar')

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
        print('I am testing make_unique_nickname')

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
            self.assertEqual(post.id, 1)
            self.assertEqual(post.author.nickname, 'susan')
            self.assertEqual(post.body, "my first post!")
            pass

        # get all users in reverse alphabetical order
        nicknames_desc = User.query.order_by('nickname desc').all()
        expected = "[<User 'susan'>, <User 'john'>]"
        self.assertEqual(nicknames_desc.__repr__(), expected)
        print('I am testing User_and_Posts')

    # noinspection PyShadowingNames
    def test_follow(self):
        print('I am testing follow')
        u1 = User(nickname='john', email='john@gmail.com')
        u2 = User(nickname='susan', email='susan@yahoo.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.unfollow(u2) is None, True, "john should not be able to unfollow susan")
        u = u1.follow(u2)
        db.session.add(u)
        db.session.commit()
        self.assertEqual(u1.follow(u2) is None, True, "john should be able to follow susan")
        self.assertEqual(u1.is_following(u2), True, 'john should now be following susan')
        self.assertEqual(u1.followed.count(), 1, 'john should now have 1 person followed')
        self.assertEqual(u1.followed.first().nickname, 'susan', 'susan should be the first one john followed')
        self.assertEqual(u2.followers.count(), 1, 'susan should now have 1 follower')
        self.assertEqual(u2.followers.first().nickname, 'john', 'susans follower should be john')
        u = u1.unfollow(u2)
        self.assertEqual(u is not None, True, 'john does not want to follow susan anymore')
        db.session.add(u)
        db.session.commit()
        self.assertEqual(not u1.is_following(u2), True, 'john should not susans follower anymore')
        self.assertEqual(u1.followed.count(), 0, 'susan should now have 0 followers')
        self.assertEqual(u2.followed.count(), 0, 'john should still be a loner :p')
